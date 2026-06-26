#!/usr/bin/env python3
"""
Verify CAS numbers against PubChem PUG REST API.

Extracts CAS numbers from chemistry/precursor-chains.md and trade/hs-codes.md,
queries PubChem for each, and cross-checks chemical names against our files.

Usage:
    python scripts/verify_cas.py

Output: cas_verification_report.md + cas_verification.json
"""

import time

from _verify_common import (
    CAS_PATTERN,
    ensure_package,
    extract_from_markdown,
    find_skill_dir,
    write_json,
    write_report,
)

ensure_package("requests")
import requests  # noqa: E402

PUBCHEM_BASE = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name"


def query_pubchem(cas: str) -> dict:
    """Query PubChem for a CAS number. Returns property + synonym data."""
    result = {
        "cas": cas,
        "valid": False,
        "iupac_name": None,
        "molecular_formula": None,
        "synonyms": [],
        "cid": None,
        "error": None,
    }

    try:
        # Get properties
        props_url = (
            f"{PUBCHEM_BASE}/{cas}/property/"
            "IUPACName,MolecularFormula/JSON"
        )
        resp = requests.get(props_url, timeout=15)

        if resp.status_code == 404:
            result["error"] = "CAS not found in PubChem"
            return result
        resp.raise_for_status()

        data = resp.json()
        props = data["PropertyTable"]["Properties"][0]
        result["valid"] = True
        result["cid"] = props.get("CID")
        result["iupac_name"] = props.get("IUPACName")
        result["molecular_formula"] = props.get("MolecularFormula")

        # Get synonyms (separate request)
        time.sleep(0.3)  # PubChem rate limiting: 5 req/sec
        syn_url = f"{PUBCHEM_BASE}/{cas}/synonyms/JSON"
        syn_resp = requests.get(syn_url, timeout=15)
        if syn_resp.status_code == 200:
            syn_data = syn_resp.json()
            synonyms = syn_data["InformationList"]["Information"][0].get(
                "Synonym", []
            )
            # Keep first 20 synonyms
            result["synonyms"] = synonyms[:20]

    except requests.RequestException as e:
        result["error"] = f"HTTP error: {str(e)[:80]}"
    except (KeyError, IndexError) as e:
        result["error"] = f"Unexpected response format: {str(e)[:80]}"

    return result


def cross_check_name(file_context: str, synonyms: list[str]) -> dict:
    """Check if the chemical name in our file matches PubChem synonyms."""
    if not synonyms:
        return {"match": False, "reason": "No synonyms to compare"}

    # Extract the chemical name from context (before CAS number or in first column)
    # Common patterns: "Chemical Name | CAS" or "Chemical Name (CAS)"
    context_lower = file_context.lower()
    synonyms_lower = [s.lower() for s in synonyms]

    # Check if any synonym appears in the file context
    for syn in synonyms_lower:
        if len(syn) > 3 and syn in context_lower:
            return {"match": True, "matched_synonym": syn}

    # Check if common abbreviations match
    common_abbrevs = ["HF", "NF3", "PGMEA", "TMAH", "TEOS", "TEMAH", "HMDS", "H2O2"]
    for abbrev in common_abbrevs:
        if abbrev in file_context and abbrev.lower() in " ".join(synonyms_lower):
            return {"match": True, "matched_synonym": abbrev}

    return {"match": False, "reason": "No synonym found in file context"}


def main():
    skill_dir = find_skill_dir()

    # Extract CAS numbers from relevant files
    source_files = [
        skill_dir / "chemistry" / "precursor-chains.md",
        skill_dir / "trade" / "hs-codes.md",
    ]

    all_cas = []
    for f in source_files:
        extracted = extract_from_markdown(f, CAS_PATTERN)
        all_cas.extend(extracted)
        if extracted:
            print(f"  {f.name}: {len(extracted)} CAS numbers found")

    # Deduplicate by value
    seen = set()
    unique_cas = []
    for item in all_cas:
        if item["value"] not in seen:
            seen.add(item["value"])
            unique_cas.append(item)

    print(f"\nTotal unique CAS numbers to verify: {len(unique_cas)}")
    print("Verifying against PubChem (free API, no key needed)...\n")

    # Verify each CAS number
    results = []
    valid_count = 0
    invalid_count = 0

    for i, item in enumerate(unique_cas):
        cas = item["value"]
        print(f"  [{i+1}/{len(unique_cas)}] {cas}...", end=" ", flush=True)

        verification = query_pubchem(cas)
        verification["source_file"] = item["file"]
        verification["source_line"] = item["line"]
        verification["file_context"] = item["context"]

        # Cross-check name
        name_check = cross_check_name(item["context"], verification["synonyms"])
        verification["name_match"] = name_check

        if verification["valid"]:
            formula = verification["molecular_formula"] or "?"
            print(f"OK -- {formula} ({verification['iupac_name'][:50] if verification['iupac_name'] else 'N/A'})")
            valid_count += 1
        else:
            print(f"FAILED -- {verification['error']}")
            invalid_count += 1

        results.append(verification)
        time.sleep(0.3)  # Rate limiting

    # Generate report
    sections = []

    # Summary
    summary = f"**Source:** PubChem PUG REST API (no API key)\n"
    summary += f"**Total CAS numbers checked:** {len(results)}\n\n"
    summary += "| Status | Count |\n|---|---|\n"
    summary += f"| Valid | {valid_count} |\n"
    summary += f"| Invalid/Not Found | {invalid_count} |\n"
    sections.append({"heading": "Summary", "content": summary})

    # Valid CAS numbers
    valid_rows = "| CAS | Formula | IUPAC Name | Name Match | Source |\n"
    valid_rows += "|---|---|---|---|---|\n"
    for r in sorted(results, key=lambda x: x["cas"]):
        if r["valid"]:
            match_str = "yes" if r["name_match"].get("match") else "NO"
            iupac = (r["iupac_name"] or "N/A")[:50]
            valid_rows += (
                f"| {r['cas']} | {r['molecular_formula']} | {iupac} "
                f"| {match_str} | {r['source_file']} |\n"
            )
    sections.append({"heading": f"Valid CAS Numbers ({valid_count})", "content": valid_rows})

    # Invalid CAS numbers
    if invalid_count > 0:
        invalid_rows = "| CAS | Error | Source File | Line |\n"
        invalid_rows += "|---|---|---|---|\n"
        for r in sorted(results, key=lambda x: x["cas"]):
            if not r["valid"]:
                invalid_rows += (
                    f"| {r['cas']} | {r['error'][:60]} "
                    f"| {r['source_file']} | {r['source_line']} |\n"
                )
        sections.append({
            "heading": f"Invalid CAS Numbers ({invalid_count}) -- NEED ATTENTION",
            "content": invalid_rows,
        })

    # Name cross-check failures
    mismatches = [r for r in results if r["valid"] and not r["name_match"].get("match")]
    if mismatches:
        mismatch_rows = "| CAS | PubChem Top Synonym | In File Context | Source |\n"
        mismatch_rows += "|---|---|---|---|\n"
        for r in mismatches:
            top_syn = r["synonyms"][0] if r["synonyms"] else "N/A"
            ctx = r["file_context"][:60]
            mismatch_rows += f"| {r['cas']} | {top_syn} | {ctx} | {r['source_file']} |\n"
        sections.append({
            "heading": "Name Cross-Check (review manually)",
            "content": mismatch_rows,
        })

    report_path = skill_dir / "cas_verification_report.md"
    write_report(report_path, "CAS Number Verification Report", sections)
    print(f"\nReport: {report_path}")

    json_path = skill_dir / "cas_verification.json"
    write_json(json_path, results)
    print(f"JSON:   {json_path}")

    return invalid_count == 0


if __name__ == "__main__":
    success = main()
    raise SystemExit(0 if success else 1)
