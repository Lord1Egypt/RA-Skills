#!/usr/bin/env python3
"""
Discovery Engine — Paper discovery, validation, and saving utility.

The agent running this skill IS the extractor. This script handles
the non-LLM parts: discovering papers, deduplication, normalization,
validation, and saving results.

Usage:
    python extract.py discover --count 10                    # find papers
    python extract.py discover --source arxiv --count 5      # from specific source
    python extract.py save result.json --paper-id arxiv:2401.00001 --source arxiv
    python extract.py validate results/                      # check saved results
"""

import argparse
import json
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

# ── Configuration ────────────────────────────────────────────────────

TRACKING_URL = "https://raw.githubusercontent.com/pcdeni/discovery-engine/master/processed_papers.jsonl"
OUTPUT_DIR = Path.home() / ".discovery" / "data" / "batch"

# SSL context that works on most systems
try:
    SSL_CTX = ssl.create_default_context()
except Exception:
    SSL_CTX = ssl._create_unverified_context()


# ── HTTP helpers ─────────────────────────────────────────────────────

def http_get(url, headers=None, timeout=30):
    """GET request using urllib. Returns (status, body_text)."""
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")
    except Exception as e:
        return 0, str(e)


# ── Paper Discovery ──────────────────────────────────────────────────

def discover_arxiv(count=10, lookback_days=30):
    """Discover recent papers from arXiv via the Atom API."""
    papers = []
    query = "cat:cond-mat+OR+cat:physics+OR+cat:cs+OR+cat:q-bio+OR+cat:math"
    url = f"http://export.arxiv.org/api/query?search_query={query}&sortBy=submittedDate&sortOrder=descending&max_results={count}"
    status, body = http_get(url, timeout=30)
    if status != 200:
        print(f"  [warn] arXiv API returned {status}", file=sys.stderr)
        return papers

    try:
        root = ET.fromstring(body)
        ns = {"a": "http://www.w3.org/2005/Atom"}
        for entry in root.findall("a:entry", ns):
            arxiv_id = (entry.findtext("a:id", "", ns) or "").split("/abs/")[-1].strip()
            if not arxiv_id:
                continue
            title = (entry.findtext("a:title", "", ns) or "").strip().replace("\n", " ")
            abstract = (entry.findtext("a:summary", "", ns) or "").strip()
            papers.append({
                "id": f"arxiv:{arxiv_id}",
                "source": "arxiv",
                "title": title,
                "abstract": abstract,
            })
    except ET.ParseError:
        print("  [warn] Failed to parse arXiv XML", file=sys.stderr)
    return papers[:count]


def discover_pmc(count=10, lookback_days=30):
    """Discover recent open-access papers from PubMed Central."""
    papers = []
    url = (
        f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        f"?db=pmc&retmax={count}&sort=relevance&retmode=json"
        f"&term=open+access[filter]+AND+hasabstract[text]"
    )
    status, body = http_get(url)
    if status != 200:
        return papers

    try:
        data = json.loads(body)
        ids = data.get("esearchresult", {}).get("idlist", [])
    except (json.JSONDecodeError, KeyError):
        return papers

    if not ids:
        return papers

    # Fetch summaries
    id_str = ",".join(ids[:count])
    sum_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pmc&id={id_str}&retmode=json"
    status, body = http_get(sum_url)
    if status != 200:
        return papers

    try:
        data = json.loads(body)
        results = data.get("result", {})
        for pmc_id in ids[:count]:
            info = results.get(str(pmc_id), {})
            title = info.get("title", "")
            abstract = _fetch_pmc_abstract(pmc_id, info)
            if title:
                papers.append({
                    "id": f"pmc:{pmc_id}",
                    "source": "pmc",
                    "title": title,
                    "abstract": abstract,
                })
    except (json.JSONDecodeError, KeyError):
        pass
    return papers


def _fetch_pmc_abstract(pmc_id, info=None):
    """Fetch abstract for a PMC paper via multiple fallback methods."""
    pmid = ""
    if info:
        for aid in info.get("articleids", []):
            if aid.get("idtype") == "pmid":
                pmid = aid.get("value", "")
                break

    if pmid:
        url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&rettype=abstract&retmode=xml"
        status, body = http_get(url)
        if status == 200 and "<AbstractText" in body:
            try:
                root = ET.fromstring(body)
                parts = []
                for at in root.iter("AbstractText"):
                    label = at.get("Label", "")
                    text = "".join(at.itertext()).strip()
                    if label:
                        parts.append(f"{label}: {text}")
                    elif text:
                        parts.append(text)
                if parts:
                    return " ".join(parts)
            except ET.ParseError:
                pass

    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id={pmc_id}&rettype=abstract&retmode=xml"
    status, body = http_get(url)
    if status == 200 and "<abstract" in body.lower():
        try:
            root = ET.fromstring(body)
            for ab in root.iter():
                if ab.tag.endswith("abstract") or ab.tag == "abstract":
                    text = "".join(ab.itertext()).strip()
                    text = re.sub(r"<[^>]+>", "", text)
                    if len(text) > 100:
                        return text
        except ET.ParseError:
            pass
    return ""


def discover_openalex(count=10, lookback_days=30):
    """Discover recent papers from OpenAlex."""
    papers = []
    url = (
        f"https://api.openalex.org/works"
        f"?filter=is_oa:true,type:article,has_abstract:true"
        f"&sort=publication_date:desc&per_page={count}"
        f"&mailto=discovery-engine@proton.me"
    )
    status, body = http_get(url)
    if status != 200:
        return papers

    try:
        data = json.loads(body)
        for work in data.get("results", [])[:count]:
            oa_id = work.get("id", "").split("/")[-1]
            title = work.get("title", "")
            abstract = _reconstruct_abstract(work.get("abstract_inverted_index"))
            if title and oa_id:
                papers.append({
                    "id": f"openalex:{oa_id}",
                    "source": "openalex",
                    "title": title,
                    "abstract": abstract or "",
                })
    except (json.JSONDecodeError, KeyError):
        pass
    return papers


def _reconstruct_abstract(inverted_index):
    """Reconstruct abstract text from OpenAlex inverted index format."""
    if not inverted_index or not isinstance(inverted_index, dict):
        return ""
    positions = []
    for word, indices in inverted_index.items():
        for idx in indices:
            positions.append((idx, word))
    positions.sort()
    return " ".join(word for _, word in positions)


def discover_osti(count=10, lookback_days=30):
    """Discover recent papers from OSTI (DOE research)."""
    papers = []
    url = (
        f"https://www.osti.gov/api/v1/records"
        f"?sort=publication_date+desc&rows={count}"
    )
    status, body = http_get(url, headers={"Accept": "application/json"})
    if status != 200:
        return papers

    try:
        records = json.loads(body)
        if isinstance(records, dict):
            records = records.get("records", records.get("results", []))
        for rec in records[:count]:
            osti_id = str(rec.get("osti_id", ""))
            title = rec.get("title", "")
            abstract = rec.get("description", "") or rec.get("abstract", "")
            if title and osti_id:
                papers.append({
                    "id": f"osti:{osti_id}",
                    "source": "osti",
                    "title": title,
                    "abstract": abstract or "",
                })
    except (json.JSONDecodeError, KeyError):
        pass
    return papers


def discover_papers(source=None, count=10, lookback_days=30):
    """Discover papers from one or all sources."""
    discoverers = {
        "arxiv": discover_arxiv,
        "pmc": discover_pmc,
        "openalex": discover_openalex,
        "osti": discover_osti,
    }

    if source:
        fn = discoverers.get(source)
        if not fn:
            print(f"Unknown source: {source}. Options: {list(discoverers.keys())}", file=sys.stderr)
            return []
        return fn(count=count, lookback_days=lookback_days)

    per_source = max(count // len(discoverers), 3)
    papers = []
    for name, fn in discoverers.items():
        print(f"  Querying {name}...", file=sys.stderr)
        try:
            found = fn(count=per_source, lookback_days=lookback_days)
            papers.extend(found)
            print(f"    Found {len(found)} papers", file=sys.stderr)
        except Exception as e:
            print(f"    [warn] {name} failed: {e}", file=sys.stderr)
        time.sleep(1)
    return papers


# ── Deduplication ────────────────────────────────────────────────────

def fetch_processed_ids():
    """Fetch already-processed paper IDs from GitHub tracking file."""
    status, body = http_get(TRACKING_URL, timeout=15)
    if status != 200:
        return set()

    ids = set()
    for line in body.strip().split("\n"):
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
            pid = entry.get("paper_id", "")
            if pid:
                ids.add(pid)
        except json.JSONDecodeError:
            continue
    return ids


# ── Normalization ────────────────────────────────────────────────────

def _to_snake_case(text):
    """Convert human-readable text to snake_case operation name."""
    if re.match(r"^[a-z][a-z0-9_]*$", text):
        return text[:80]
    cleaned = re.sub(r"[^a-zA-Z0-9\s_]", "", text)
    words = re.split(r"[\s_]+", cleaned.strip())
    result = "_".join(w.lower() for w in words if w)
    return result[:80].rsplit("_", 1)[0] if len(result) > 80 else result


def _infer_constraint_class(text):
    """Infer constraint_class from tension text using simple heuristics."""
    text = text.lower()
    patterns = [
        (r"speed.*accuracy|accuracy.*speed|fast.*precise", "speed_vs_accuracy"),
        (r"throughput.*selectiv|selectiv.*throughput", "throughput_vs_selectivity"),
        (r"cost.*quality|quality.*cost|expensive", "cost_vs_quality"),
        (r"scalab|scale", "scalability"),
        (r"generali[sz]|specific.*general|general.*specific", "generality_vs_specificity"),
        (r"sensitiv.*specific|specific.*sensitiv", "sensitivity_vs_specificity"),
        (r"resolut|precision.*recall|recall.*precision", "resolution_tradeoff"),
        (r"energy.*efficien|power.*consum", "energy_efficiency"),
        (r"stabil.*reactiv|reactiv.*stabil", "stability_vs_reactivity"),
        (r"robustness|robust.*fragil", "robustness"),
        (r"reproduc|replicab", "reproducibility"),
    ]
    for pattern, cls in patterns:
        if re.search(pattern, text):
            return cls
    return "general_tradeoff"


def normalize_result(data):
    """
    Auto-fix common LLM output issues before validation.

    Handles:
    - 'analysis' -> 'paper_analysis' key rename
    - String tensions -> structured dicts
    - String provides/requires -> structured dicts
    - String interface -> dict with provides/requires lists
    - String mechanism -> dict
    - Human-readable operation names -> snake_case
    """
    if not isinstance(data, dict):
        return data
    data = json.loads(json.dumps(data))  # deep copy

    # Fix 1: 'analysis' -> 'paper_analysis'
    if "analysis" in data and "paper_analysis" not in data:
        data["paper_analysis"] = data.pop("analysis")

    # Fix 2: Ensure cross_domain exists
    pa = data.get("paper_analysis", {})
    if "cross_domain" not in data:
        cd_fields = ["core_friction", "mechanism", "unsolved_tensions",
                     "bridge_tags", "interface", "mechanism_components"]
        if any(f in pa for f in cd_fields):
            data["cross_domain"] = {}
            for f in cd_fields:
                if f in pa:
                    data["cross_domain"][f] = pa.pop(f)

    cd = data.get("cross_domain", {})

    # Fix 3: String tensions -> structured dicts
    tensions = cd.get("unsolved_tensions", [])
    if isinstance(tensions, list):
        fixed = []
        for t in tensions:
            if isinstance(t, str):
                fixed.append({
                    "tension": t,
                    "constraint_class": _infer_constraint_class(t),
                    "why_it_matters": "unspecified",
                    "source_quote": "",
                })
            elif isinstance(t, dict):
                if "tension" not in t and "description" in t:
                    t["tension"] = t.pop("description")
                if "constraint_class" not in t:
                    t["constraint_class"] = _infer_constraint_class(t.get("tension", ""))
                fixed.append(t)
            else:
                fixed.append(t)
        cd["unsolved_tensions"] = fixed

    # Fix 4: String interface -> structured dict
    iface = cd.get("interface", {})
    if isinstance(iface, str):
        cd["interface"] = {"provides": [], "requires": []}
        iface = cd["interface"]

    if isinstance(iface, dict):
        for direction in ("provides", "requires"):
            ops = iface.get(direction, [])
            if isinstance(ops, list):
                fixed_ops = []
                for op in ops:
                    if isinstance(op, str):
                        fixed_ops.append({
                            "operation": _to_snake_case(op),
                            "description": op,
                        })
                    elif isinstance(op, dict):
                        operation = op.get("operation", "")
                        if operation and not re.match(r"^[a-z][a-z0-9_]*$", operation):
                            op["operation"] = _to_snake_case(operation)
                        if not op.get("operation") and op.get("description"):
                            op["operation"] = _to_snake_case(op["description"][:60])
                        fixed_ops.append(op)
                    else:
                        fixed_ops.append(op)
                iface[direction] = fixed_ops

    # Fix 5: String mechanism -> dict
    mech = cd.get("mechanism")
    if isinstance(mech, str):
        cd["mechanism"] = {"description": mech, "structural_pattern": ""}

    # Fix 6: Ensure _meta exists
    if "_meta" not in data:
        data["_meta"] = {}

    data["cross_domain"] = cd
    return data


# ── Validation ───────────────────────────────────────────────────────

def validate_result(data):
    """Validate extraction result. Returns list of issues (empty = valid)."""
    issues = []

    if "paper_analysis" not in data:
        if "analysis" in data:
            issues.append("Wrong key: 'analysis' should be 'paper_analysis'")
        else:
            issues.append("Missing required key: paper_analysis")

    if "entities" not in data:
        issues.append("Missing required key: entities")
    elif not isinstance(data["entities"], list) or len(data["entities"]) == 0:
        issues.append("entities must be a non-empty array")

    if "cross_domain" not in data:
        issues.append("Missing required key: cross_domain")
    else:
        cd = data["cross_domain"]
        if "bridge_tags" not in cd or not cd["bridge_tags"]:
            issues.append("Missing or empty: cross_domain.bridge_tags")
        if "unsolved_tensions" not in cd or not cd["unsolved_tensions"]:
            issues.append("Missing or empty: cross_domain.unsolved_tensions")
        if "interface" not in cd:
            issues.append("Missing: cross_domain.interface")
        elif isinstance(cd["interface"], dict):
            if not cd["interface"].get("provides"):
                issues.append("Missing or empty: interface.provides")
            if not cd["interface"].get("requires"):
                issues.append("Missing or empty: interface.requires")
            for p in cd["interface"].get("provides", []):
                if isinstance(p, str):
                    issues.append("provides entries must be objects, not strings")
                    break
            for r in cd["interface"].get("requires", []):
                if isinstance(r, str):
                    issues.append("requires entries must be objects, not strings")
                    break
        else:
            issues.append("cross_domain.interface must be an object")

        for t in cd.get("unsolved_tensions", []):
            if isinstance(t, str):
                issues.append("unsolved_tensions entries must be objects, not strings")
                break

    return issues


# ── CLI Commands ─────────────────────────────────────────────────────

def run_discover(args):
    """Discover papers and output as JSON."""
    count = args.count or 10
    print("Discovering papers...", file=sys.stderr)
    papers = discover_papers(source=args.source, count=count * 2)

    print("Checking for already-processed papers...", file=sys.stderr)
    processed = fetch_processed_ids()

    # Also check local output directory
    output_dir = Path(args.output) if args.output else OUTPUT_DIR
    if output_dir.exists():
        for f in output_dir.glob("*.json"):
            try:
                d = json.loads(f.read_text(encoding="utf-8"))
                pid = d.get("_meta", {}).get("paper_id", "")
                if pid:
                    processed.add(pid)
            except Exception:
                pass

    new_papers = [p for p in papers if p["id"] not in processed][:count]

    print(f"Found {len(papers)} papers, {len(new_papers)} new after dedup", file=sys.stderr)

    # Output as JSON to stdout (agent reads this)
    print(json.dumps(new_papers, indent=2, ensure_ascii=False))


def run_save(args):
    """Normalize, validate, and save a result file."""
    result_path = Path(args.result_file)
    if not result_path.exists():
        print(f"Error: {result_path} not found", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(result_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # Normalize
    data = normalize_result(data)

    # Add/update metadata
    data["_meta"] = data.get("_meta", {})
    if args.paper_id:
        data["_meta"]["paper_id"] = args.paper_id
    if args.source:
        data["_meta"]["source"] = args.source
    if args.title:
        data["_meta"]["title"] = args.title
    data["_meta"]["text_source"] = "abstract"
    data["_meta"]["prompt_version"] = "v_combined"
    data["_meta"]["extracted_at"] = datetime.now(timezone.utc).isoformat()

    # Validate
    issues = validate_result(data)
    if issues:
        print(f"Validation issues ({len(issues)}):", file=sys.stderr)
        for issue in issues:
            print(f"  - {issue}", file=sys.stderr)
        print("Saving anyway (issues may be minor).", file=sys.stderr)

    # Save
    output_dir = Path(args.output) if args.output else OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    paper_id = data.get("_meta", {}).get("paper_id", "unknown")
    safe_id = paper_id.replace(":", "__").replace("/", "_")
    outfile = output_dir / f"{safe_id}.json"
    outfile.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    status = "PASS" if not issues else f"WARN ({len(issues)} issues)"
    print(f"{status}: saved {outfile}")


def run_validate(args):
    """Validate one or more result files."""
    target = Path(args.path)
    files = list(target.glob("*.json")) if target.is_dir() else [target]

    total, valid, invalid = 0, 0, 0
    for f in files:
        total += 1
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            data = normalize_result(data)  # normalize before validating
            issues = validate_result(data)
            if issues:
                invalid += 1
                print(f"FAIL: {f.name}: {issues[0]}")
            else:
                valid += 1
                print(f"PASS: {f.name}")
        except Exception as e:
            invalid += 1
            print(f"ERROR: {f.name}: {e}")

    print(f"\nValidated {total}: {valid} pass, {invalid} fail")
    sys.exit(0 if invalid == 0 else 1)


# ── CLI ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Discovery Engine — paper discovery, validation, and saving",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python extract.py discover --count 10\n"
               "  python extract.py discover --source arxiv --count 5\n"
               "  python extract.py save result.json --paper-id arxiv:2401.00001 --source arxiv\n"
               "  python extract.py validate ~/.discovery/data/batch/\n",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # discover
    disc = sub.add_parser("discover", help="Find new papers (outputs JSON to stdout)")
    disc.add_argument("--source", help="Paper source (arxiv, pmc, openalex, osti)")
    disc.add_argument("--count", type=int, default=10, help="Number of papers (default: 10)")
    disc.add_argument("--output", help="Output dir to check for local dedup")

    # save
    save = sub.add_parser("save", help="Normalize, validate, and save a result file")
    save.add_argument("result_file", help="Path to the JSON extraction result")
    save.add_argument("--paper-id", help="Paper ID (e.g., arxiv:2401.00001)")
    save.add_argument("--source", help="Paper source (arxiv, pmc, openalex, osti)")
    save.add_argument("--title", help="Paper title")
    save.add_argument("--output", help="Output directory (default: ~/.discovery/data/batch/)")

    # validate
    val = sub.add_parser("validate", help="Validate result files")
    val.add_argument("path", help="JSON file or directory")

    args = parser.parse_args()

    if args.command == "discover":
        run_discover(args)
    elif args.command == "save":
        run_save(args)
    elif args.command == "validate":
        run_validate(args)


if __name__ == "__main__":
    main()
