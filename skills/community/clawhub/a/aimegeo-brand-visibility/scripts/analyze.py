#!/usr/bin/env python3
"""Validate local answer evidence and aggregate it. No network or report writing."""

import argparse
from collections import Counter, defaultdict
from datetime import datetime
import hashlib
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit, urlunsplit

STATUSES = ("observed", "query_failed", "missing", "not_run", "simulated")
VERDICTS = ("match", "contradiction", "unverified")
TONES = ("positive", "neutral", "negative", "mixed", "unknown")


class InputError(ValueError):
    pass


def require(condition, path, message):
    if not condition:
        raise InputError(f"{path}: {message}")


def obj(value, path):
    require(isinstance(value, dict), path, "expected an object")
    return value


def array(value, path):
    require(isinstance(value, list), path, "expected an array")
    return value


def string(value, path, nullable=False, empty=False):
    if nullable and value is None:
        return None
    require(isinstance(value, str), path, "expected a string")
    require(empty or bool(value.strip()), path, "must not be blank")
    return value


def timestamp(value, path):
    if value is None:
        return None
    string(value, path)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise InputError(f"{path}: expected ISO 8601 timestamp with timezone") from None
    require(parsed.tzinfo is not None, path, "timezone is required")
    return value


def quote(value, answer, path):
    string(value, path)
    require(value in answer, path, "quote is not an exact substring of answer")
    return value


def url(value, path):
    string(value, path)
    try:
        parsed = urlsplit(value)
        port = parsed.port
    except ValueError:
        raise InputError(f"{path}: invalid URL") from None
    require(parsed.scheme in ("http", "https") and bool(parsed.hostname), path,
            "expected absolute http(s) URL")
    require(not parsed.username and not parsed.password, path, "credentials in URL are forbidden")
    require(not any(c.isspace() for c in value), path, "whitespace in URL is forbidden")
    host = parsed.hostname.lower()
    host = f"[{host}]" if ":" in host else host
    netloc = host + (f":{port}" if port is not None else "")
    # A fragment does not create a second cited document. Queries are preserved.
    key = urlunsplit((parsed.scheme.lower(), netloc, parsed.path or "/", parsed.query, ""))
    return value, key


def boolean_review(raw, answer, path):
    if raw is None:
        return {"value": None, "quote": None, "reason": None}
    raw = obj(raw, path)
    value = raw.get("value")
    require(value is None or type(value) is bool, path + ".value", "expected boolean or null")
    reason = string(raw.get("reason"), path + ".reason")
    excerpt = raw.get("quote")
    if value is True or excerpt is not None:
        excerpt = quote(excerpt, answer, path + ".quote")
    return {"value": value, "quote": excerpt, "reason": reason}


def validate(raw):
    raw = obj(raw, "input")
    require(raw.get("schema_version") == "1.0", "schema_version", "expected '1.0'")
    brand = obj(raw.get("brand"), "brand")
    name = string(brand.get("name"), "brand.name")
    aliases = [string(v, f"brand.aliases[{i}]") for i, v in
               enumerate(array(brand.get("aliases", []), "brand.aliases"))]
    facts = []
    fact_ids = set()
    for i, raw_fact in enumerate(array(brand.get("facts", []), "brand.facts")):
        p = f"brand.facts[{i}]"
        f = obj(raw_fact, p)
        fid = string(f.get("id"), p + ".id")
        require(fid not in fact_ids, p + ".id", "duplicate fact id")
        fact_ids.add(fid)
        facts.append({"id": fid, "statement": string(f.get("statement"), p + ".statement"),
                      "source": string(f.get("source"), p + ".source"),
                      "as_of": timestamp(f.get("as_of"), p + ".as_of")})
    records = []
    ids, runs, question_defs = set(), set(), {}
    for i, raw_record in enumerate(array(raw.get("records"), "records")):
        p = f"records[{i}]"
        r = obj(raw_record, p)
        clean = {key: string(r.get(key), p + "." + key) for key in
                 ("id", "question_id", "question", "intent", "platform", "run_id", "source", "status")}
        require(clean["status"] in STATUSES, p + ".status", "unsupported status")
        require(clean["id"] not in ids, p + ".id", "duplicate record id")
        ids.add(clean["id"])
        clean["model"] = string(r.get("model"), p + ".model", nullable=True)
        clean["search_mode"] = r.get("search_mode", "unknown")
        require(clean["search_mode"] in ("on", "off", "unknown"), p + ".search_mode", "unsupported mode")
        clean["context_note"] = string(r.get("context_note"), p + ".context_note", nullable=True)
        run_key = (clean["question_id"], clean["platform"], clean["model"], clean["run_id"])
        require(run_key not in runs, p, "duplicate question/platform/model/run_id; do not double count")
        runs.add(run_key)
        definition = (clean["question"], clean["intent"])
        require(clean["question_id"] not in question_defs or question_defs[clean["question_id"]] == definition,
                p + ".question_id", "same question_id has different question or intent")
        question_defs[clean["question_id"]] = definition
        clean["captured_at"] = timestamp(r.get("captured_at"), p + ".captured_at")
        status = clean["status"]
        clean["answer"] = string(r.get("answer"), p + ".answer", nullable=status not in ("observed", "simulated"))
        clean["reason"] = string(r.get("reason"), p + ".reason", nullable=status in ("observed", "simulated"))
        capture = r.get("citations_capture", "not_captured")
        require(capture in ("complete", "partial", "not_captured"), p + ".citations_capture", "unsupported capture state")
        clean["citations_capture"] = capture
        links = array(r.get("citations", []), p + ".citations")
        clean["citations"] = []
        seen_links = {}
        for j, raw_link in enumerate(links):
            cp = f"{p}.citations[{j}]"
            c = obj(raw_link, cp)
            href, key = url(c.get("url"), cp + ".url")
            kind = c.get("kind")
            relation = c.get("relation", "unreviewed")
            require(kind in ("native", "inline"), cp + ".kind", "expected native or inline")
            require(kind != "native" or capture != "not_captured", cp,
                    "native links require partial or complete source capture")
            require(relation in ("brand", "other", "unreviewed"), cp + ".relation", "unsupported relation")
            evidence = string(c.get("evidence"), cp + ".evidence")
            relation_evidence = string(c.get("relation_evidence"), cp + ".relation_evidence",
                                       nullable=relation == "unreviewed")
            identity = (kind, key)
            require(identity not in seen_links or seen_links[identity] == relation,
                    cp, "duplicate URL has conflicting relation labels")
            if identity not in seen_links:
                clean["citations"].append({"url": href, "kind": kind, "relation": relation,
                                           "evidence": evidence, "relation_evidence": relation_evidence})
                seen_links[identity] = relation
        review = obj(r.get("review", {}), p + ".review")
        if status not in ("observed", "simulated"):
            require(not review and not links, p, "failed/missing/not_run records cannot carry assessed evidence")
        answer = clean["answer"] or ""
        mention = boolean_review(review.get("mention"), answer, p + ".review.mention")
        recommendation = boolean_review(review.get("recommendation"), answer, p + ".review.recommendation")
        require(recommendation["value"] is not True or mention["value"] is True,
                p + ".review.recommendation", "recommendation requires a reviewed brand mention")
        tone_raw = obj(review.get("tone", {"value": "unknown"}), p + ".review.tone")
        tone = {"value": tone_raw.get("value"), "quote": None, "reason": None}
        require(tone["value"] in TONES, p + ".review.tone.value", "unsupported tone")
        if tone["value"] != "unknown":
            require(mention["value"] is True, p + ".review.tone", "brand tone requires a reviewed mention")
            tone["quote"] = quote(tone_raw.get("quote"), answer, p + ".review.tone.quote")
            tone["reason"] = string(tone_raw.get("reason"), p + ".review.tone.reason")
        checks, used_facts = [], set()
        for j, raw_check in enumerate(array(review.get("fact_checks", []), p + ".review.fact_checks")):
            fp = f"{p}.review.fact_checks[{j}]"
            f = obj(raw_check, fp)
            verdict, fid = f.get("verdict"), f.get("fact_id")
            require(verdict in VERDICTS, fp + ".verdict", "unsupported verdict")
            require(fid is None and verdict == "unverified" or isinstance(fid, str) and fid in fact_ids,
                    fp + ".fact_id", "a determinate verdict requires a known brand fact")
            require(fid is None or fid not in used_facts, fp + ".fact_id", "duplicate fact check in answer")
            used_facts.add(fid)
            require(mention["value"] is True, fp, "brand fact checks require a reviewed mention")
            checks.append({"fact_id": fid, "verdict": verdict,
                           "quote": quote(f.get("quote"), answer, fp + ".quote"),
                           "reason": string(f.get("reason"), fp + ".reason")})
        clean["review"] = {"mention": mention, "recommendation": recommendation,
                           "tone": tone, "fact_checks": checks}
        # These are search hints, never inferred entity/recommendation judgments.
        clean["literal_candidates"] = [a for a in dict.fromkeys([name] + aliases) if a.casefold() in answer.casefold()]
        clean["answer_sha256"] = hashlib.sha256(answer.encode("utf-8")).hexdigest() if answer else None
        native = [c for c in clean["citations"] if c["kind"] == "native"]
        native_known = capture == "complete" and all(c["relation"] != "unreviewed" for c in native)
        brand_links = [c["url"] for c in native if c["relation"] == "brand"]
        assessed = status in ("observed", "simulated")
        clean["native_brand_urls"] = brand_links
        clean["native_brand_citation_count"] = len(brand_links) if assessed and native_known else None
        clean["brand_native_cited"] = bool(brand_links) if assessed and native_known else None
        clean["included_in_measured_metrics"] = status == "observed"
        records.append(clean)
    scope = obj(raw.get("scope", {}), "scope")
    return {"schema_version": "1.0", "brand": {"name": name, "aliases": aliases, "facts": facts},
            "scope": {k: string(scope.get(k), "scope." + k, nullable=True) for k in ("locale", "market")},
            "records": records}


def rate(hits, n, unknown):
    return {"numerator": hits if n else None, "denominator": n,
            "percent": round(hits * 100 / n, 1) if n else None, "unknown": unknown}


def aggregate(records):
    n = len(records)
    mentions = [r["review"]["mention"]["value"] for r in records]
    recommendations = [r["review"]["recommendation"]["value"] for r in records]
    citations = [r["brand_native_cited"] for r in records]
    metrics = {}
    for key, values in (("mention_rate", mentions), ("recommendation_rate", recommendations),
                        ("native_brand_citation_rate", citations)):
        known = [v for v in values if v is not None]
        metrics[key] = rate(sum(known), len(known), n - len(known))
    checks = [f for r in records for f in r["review"]["fact_checks"]]
    decided = [f for f in checks if f["verdict"] != "unverified"]
    metrics["fact_match_rate"] = rate(sum(f["verdict"] == "match" for f in decided), len(decided),
                                       len(checks) - len(decided))
    intents = defaultdict(list)
    for r in records:
        intents[r["intent"]].append(r["review"]["mention"]["value"])
    full_intents = [values for values in intents.values() if all(v is not None for v in values)]
    metrics["intent_coverage"] = rate(sum(any(v) for v in full_intents), len(full_intents),
                                      len(intents) - len(full_intents))
    tone_counts = Counter(r["review"]["tone"]["value"] for r in records)
    tone_n = n - tone_counts["unknown"]
    tone = {"reviewed_answers": tone_n, "unknown_answers": tone_counts["unknown"],
            "counts": {k: tone_counts[k] if tone_n else None for k in TONES if k != "unknown"}}
    by_fact = defaultdict(lambda: defaultdict(list))
    for r in records:
        for check in r["review"]["fact_checks"]:
            if check["fact_id"] is not None:
                by_fact[check["fact_id"]][check["verdict"]].append(r["id"])
    disagreements = [{"fact_id": fid, "match_record_ids": groups["match"],
                      "contradiction_record_ids": groups["contradiction"]}
                     for fid, groups in sorted(by_fact.items()) if groups["match"] and groups["contradiction"]]
    times = sorted((r["captured_at"] for r in records if r["captured_at"]),
                   key=lambda s: datetime.fromisoformat(s.replace("Z", "+00:00")))
    return {"valid_answers": n, "metrics": metrics, "tone": tone,
            "fact_review_disagreements": disagreements,
            "captured_at_range": {"first": times[0] if times else None, "last": times[-1] if times else None},
            "missing_capture_time_ids": [r["id"] for r in records if r["captured_at"] is None],
            "answers_without_fact_checks": sum(not r["review"]["fact_checks"] for r in records)}


def question_summary(all_records, assessed):
    grouped = defaultdict(list)
    for r in all_records:
        grouped[r["question_id"]].append(r)
    selected = {r["id"] for r in assessed}
    rows = []
    for qid, records in grouped.items():
        valid = [r for r in records if r["id"] in selected]
        mentions = [r["review"]["mention"]["value"] for r in valid]
        reviewed = [v for v in mentions if v is not None]
        absent = not any(reviewed) if valid and len(reviewed) == len(valid) else None
        rows.append({"question_id": qid, "question": records[0]["question"], "intent": records[0]["intent"],
                     "record_ids": [r["id"] for r in records], "status_counts": dict(Counter(r["status"] for r in records)),
                     "valid_answers": len(valid), "mention_reviewed": len(reviewed),
                     "mention_hits": sum(reviewed) if reviewed else None, "unmentioned_in_all_valid_answers": absent})
    return rows


def analyze(raw):
    data = validate(raw)
    records = data["records"]
    measured = [r for r in records if r["status"] == "observed"]
    simulated = [r for r in records if r["status"] == "simulated"]
    observed_summary = aggregate(measured)
    observed_summary["questions"] = question_summary(records, measured)
    groups = defaultdict(list)
    for r in measured:
        groups[(r["platform"], r["model"], r["search_mode"])].append(r)
    observed_summary["by_platform_model_search"] = [
        {"platform": k[0], "model": k[1], "search_mode": k[2], "summary": aggregate(v)}
        for k, v in groups.items()]
    return {"schema_version": "1.0", "brand": data["brand"], "scope": data["scope"],
            "metric_system": "local-answer-evidence-v1 (not ABI)",
            "measurement_basis": "Imported observed answers only; source authenticity and semantic labels require Agent review.",
            "status_counts": {k: sum(r["status"] == k for r in records) for k in STATUSES},
            "measured": observed_summary,
            "simulation_preview": ({"label": "SYNTHETIC ONLY — excluded from measured results",
                                    "summary": aggregate(simulated),
                                    "questions": question_summary(simulated, simulated)} if simulated else None),
            "records": records}


def reject_constant(value):
    raise InputError(f"JSON: non-finite constant {value} is not allowed")


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "JSON", f"duplicate key {key}")
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="UTF-8 JSON evidence file")
    parser.add_argument("--output", type=Path, help="new JSON file; existing files are never overwritten")
    args = parser.parse_args()
    try:
        with args.input.open(encoding="utf-8") as stream:
            data = json.load(stream, parse_constant=reject_constant, object_pairs_hook=unique_keys)
        result = analyze(data)
        payload = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        if args.output:
            with args.output.open("x", encoding="utf-8") as stream:
                stream.write(payload)
        else:
            sys.stdout.write(payload)
        return 0
    except (InputError, OSError, UnicodeError, json.JSONDecodeError, RecursionError) as error:
        sys.stderr.write(json.dumps({"status": "error", "error": str(error)}, ensure_ascii=False) + "\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
