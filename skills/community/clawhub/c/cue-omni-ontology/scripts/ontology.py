#!/usr/bin/env python3
"""Offline knowledge packaging. Semantic extraction is performed by the host agent.

Only Python's standard library is required. No network requests or telemetry. The one exception is opt-in:
`omni-source` may start the user's own Omni Bridge solely to read an artifact result back from its local cache
(read_result; this script handles no key and starts no parse).
Hashes and range checks establish internal integrity, not source truth or IAM.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import ipaddress
import json
import math
import re
import shutil
import sys
import tempfile
from collections import defaultdict
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit

VERSION = "0.3.18"  # 与 SKILL.md 的 version 成对：升号必须同改这两处（包内产物与自报行都取这一枚）
SCHEMA_VERSION = "0.1.0"
ID = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]{0,119}$")
HASH = re.compile(r"^[0-9a-f]{64}$")
TYPES = {"Organization", "Product", "BusinessSegment", "Topic"}
VALUE_TYPES = {"number", "string", "boolean", "entity", "set"}
OMNI = "omni_native_source_pdf_page"


class Invalid(ValueError):
    pass


def need(condition, message):
    if not condition:
        raise Invalid(message)


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(value if isinstance(value, bytes) else canonical(value).encode()).hexdigest()


def read_json(path):
    return decode_json(Path(path).read_text(encoding="utf-8"))


def decode_json(content):
    def pairs(items):
        out = {}
        for key, value in items:
            need(key not in out, f"duplicate JSON key: {key}")
            out[key] = value
        return out
    return json.loads(content, object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(Invalid(f"nonfinite number: {x}")))


def text(value, label):
    need(isinstance(value, str) and bool(value.strip()), f"{label}: nonempty text required")
    return value


def ident(value, label):
    need(isinstance(value, str) and ID.fullmatch(value), f"{label}: invalid ID")
    return value


def iso_date(value, label, nullable=False):
    if value is None and nullable:
        return
    need(isinstance(value, str), f"{label}: date required")
    try:
        need(date.fromisoformat(value).isoformat() == value, f"{label}: YYYY-MM-DD required")
    except (ValueError, TypeError):
        raise Invalid(f"{label}: YYYY-MM-DD required")


def public_url(value):
    text(value, "source.url")
    need(not any(c.isspace() or c in '<>"`' for c in value), "source.url: unsafe characters")
    try:
        p = urlsplit(value)
        need(p.scheme in {"http", "https"} and bool(p.hostname), "source.url: HTTP(S) required")
        need(not p.username and not p.password, "source.url: userinfo forbidden")
        host = p.hostname.lower().rstrip(".")
        need(host != "localhost" and not host.endswith((".localhost", ".local", ".internal")),
             "source.url: public host required")
        try:
            need(ipaddress.ip_address(host).is_global, "source.url: non-public IP")
        except ValueError as exc:
            if isinstance(exc, Invalid):
                raise
            need("." in host, "source.url: public hostname required")
        sensitive = {"token", "access_token", "api_key", "key", "signature", "sig", "x-amz-signature"}
        need(not any(k.lower() in sensitive for k, _ in parse_qsl(p.query)), "source.url: credential-like query")
    except ValueError as exc:
        raise Invalid(str(exc))


def local_file(root, rel):
    text(rel, "content_file")
    p = Path(rel)
    need(not p.is_absolute() and ".." not in p.parts, "content_file: relative path without traversal required")
    target = (root / p).resolve()
    need(target.is_relative_to(root.resolve()) and target.is_file(), "content_file: unavailable or outside input directory")
    need(target.stat().st_size <= 32 * 1024 * 1024, "content_file: exceeds 32 MiB")
    return target


def indexed(items, label):
    need(isinstance(items, list), f"{label}: list required")
    out = {}
    for item in items:
        need(isinstance(item, dict), f"{label}: object required")
        key = ident(item.get("id"), label)
        need(key not in out, f"{label}: duplicate ID {key}")
        out[key] = copy.deepcopy(item)
    return out


def key_of(a):
    return {k: a[k] for k in ("entity_id", "concept_id", "unit", "period", "basis", "qualifiers", "valid_from", "valid_to")}


def fact_id(a):
    return "fact:" + digest(key_of(a))[:24]


def assertion_id(a):
    # Value and exact supporting ranges belong to the source assertion, not the logical fact key.
    return "assert:" + digest({k: a[k] for k in ("fact_id", "value", "evidence")})[:24]


def value_key(value):
    # Compare numeric spelling without rounding large integers or changing stored identities.
    return ("number", Decimal(str(value))) if type(value) in {int, float} else ("other", canonical(value))


def check_knowledge(k, root, normalized=True):
    need(isinstance(k, dict) and k.get("schema_version") == SCHEMA_VERSION, "unsupported schema_version")
    scope = k.get("scope", {})
    need(isinstance(scope, dict), "scope: object required")
    text(scope.get("title"), "scope.title")
    iso_date(scope.get("as_of"), "scope.as_of")
    entities = indexed(k.get("entities"), "entities")
    for e in entities.values():
        need(e.get("type") in TYPES, "unsupported entity type")
        text(e.get("name"), "entity.name")
    defs = indexed(k.get("definitions"), "definitions")
    for d in defs.values():
        need(d.get("kind") in {"metric", "relation", "attribute"}, "invalid definition kind")
        need(d.get("value_type") in VALUE_TYPES, "invalid definition value_type")
        if d["kind"] == "relation":
            need(d["value_type"] == "entity", "relation must have entity value_type")
        text(d.get("name"), "definition.name")
        text(d.get("description"), "definition.description")
        need(d.get("status", "candidate") == "candidate", "public-beta definitions remain candidates; no schema approval engine")
    sources = indexed(k.get("sources"), "sources")
    source_bytes = {}
    for s in sources.values():
        public_url(s.get("url"))
        text(s.get("title"), "source.title")
        iso_date(s.get("published_at"), "source.published_at", True)
        iso_date(s.get("accessed_at"), "source.accessed_at")
        need(s.get("public_status") in {"user_confirmed", "retrieved_public", "synthetic"}, "source public_status required")
        need(s.get("parse_origin") in {"omni_live", "omni_replay", "synthetic", "other"}, "source parse_origin required")
        raw = local_file(root, s.get("content_file")).read_bytes()
        raw.decode("utf-8")
        need(isinstance(s.get("sha256"), str) and HASH.fullmatch(s["sha256"]) and digest(raw) == s["sha256"],
             f"source hash mismatch: {s['id']}")
        source_bytes[s["id"]] = raw
        spans = s.get("page_spans", [])
        need(isinstance(spans, list), "source.page_spans: list required")
        previous = 0
        pages = set()
        for span in spans:
            need(isinstance(span, dict), "page span must be object")
            page, start, end = span.get("page"), span.get("start_utf8"), span.get("end_utf8")
            need(type(page) is int and page > 0 and page not in pages, "page must be unique positive integer")
            need(type(start) is int and type(end) is int and previous <= start < end <= len(raw), "invalid page span")
            raw[:start].decode("utf-8"); raw[start:end].decode("utf-8")
            need(span.get("basis") in {OMNI, "synthetic_page", "manual_page"}, "invalid page basis")
            need(span["basis"] != OMNI or s["parse_origin"] in {"omni_live", "omni_replay"}, "native page requires Omni provenance")
            previous = end; pages.add(page)
    assertions = k.get("assertions")
    need(isinstance(assertions, list), "assertions: list required")
    seen = set()
    for a in assertions:
        need(isinstance(a, dict), "assertion must be object")
        need(a.get("entity_id") in entities, "unknown assertion entity")
        need(a.get("concept_id") in defs, "unknown assertion concept")
        for field in ("unit", "period", "basis"):
            text(a.get(field), f"assertion.{field}; use explicit not_applicable when appropriate")
        q = a.get("qualifiers")
        need(isinstance(q, dict) and all(isinstance(x, str) and isinstance(v, (str, bool, int, float))
                                       and (not isinstance(v, float) or math.isfinite(v)) for x, v in q.items()),
             "qualifiers: flat object of finite scalars required")
        for field in ("valid_from", "valid_to"):
            iso_date(a.get(field), field, True)
        need(not (a.get("valid_from") and a.get("valid_to")) or a["valid_from"] <= a["valid_to"], "reversed validity interval")
        vt = defs[a["concept_id"]]["value_type"]
        value = a.get("value")
        valid = {"number": type(value) is int or (type(value) is float and math.isfinite(value)),
                 "boolean": type(value) is bool, "string": isinstance(value, str) and bool(value.strip()),
                 "entity": isinstance(value, str) and value in entities,
                 "set": isinstance(value, list) and all(isinstance(x, str) and x for x in value)}[vt]
        need(valid, f"invalid value for {vt}")
        if vt == "set":
            need(value == sorted(set(value)), "set value must be sorted and unique")
        need(a.get("claim_kind") == "reported", "assertion.claim_kind must be 'reported' or omitted; packages store directly reported claims only, keep derived answers separate")
        need(a.get("status") in {"candidate", "accepted", "rejected"}, "invalid assertion status")
        evidence = a.get("evidence")
        need(isinstance(evidence, list) and evidence, "assertion needs evidence")
        for ev in evidence:
            need(isinstance(ev, dict) and ev.get("source_id") in sources, "unknown evidence source")
            raw = source_bytes[ev["source_id"]]
            start, end = ev.get("start_utf8"), ev.get("end_utf8")
            need(type(start) is int and type(end) is int and 0 <= start < end <= len(raw), "invalid evidence range")
            raw[:start].decode("utf-8"); raw[start:end].decode("utf-8")
            need(ev.get("span_sha256") == digest(raw[start:end]), "evidence span hash mismatch")
            text(ev.get("role"), "evidence.role")
            page = ev.get("page")
            if page is not None:
                need(type(page) is int and page > 0, "invalid evidence page")
                matches = [s for s in sources[ev["source_id"]].get("page_spans", []) if
                           s["page"] == page and s["start_utf8"] <= start < end <= s["end_utf8"]
                           and s["basis"] == ev.get("locator_basis")]
                need(bool(matches), "page claim has no matching source span")
            else:
                need(ev.get("locator_basis") == "text_range", "page-less evidence must use text_range")
        if normalized:
            need(a.get("fact_id") == fact_id(a), "fact ID mismatch")
            need(a.get("id") == assertion_id(a), "assertion ID mismatch")
            need(a["id"] not in seen, "duplicate assertion ID")
            seen.add(a["id"])
        reviews = a.get("reviews", [])
        need(isinstance(reviews, list), "reviews must be list")
        for review in reviews:
            need(isinstance(review, dict) and review.get("decision") in {"accepted", "rejected"}, "invalid review")
            text(review.get("reviewer"), "review.reviewer")
            text(review.get("note"), "review.note")
            text(review.get("at"), "review.at")
        need(a["status"] == (reviews[-1]["decision"] if reviews else "candidate"), "status does not match review log")
    return {"sources": len(sources), "entities": len(entities), "definitions": len(defs),
            "assertions": len(assertions), "facts": len({fact_id(a) for a in assertions})}


def prepare_input(path):
    root = Path(path).resolve().parent
    k = read_json(path)
    need(isinstance(k, dict), "input must be object")
    need(isinstance(k.get("assertions"), list), "assertions: list required")
    for a in k.get("assertions", []):
        need(isinstance(a, dict), "assertion must be object")
        need(a.get("status", "candidate") == "candidate" and not a.get("reviews"), "input cannot inject review decisions")
        a["status"] = "candidate"; a["reviews"] = []
        a.setdefault("valid_from", None); a.setdefault("valid_to", None)
        a.setdefault("claim_kind", "reported")
        a["fact_id"] = fact_id(a)
        a["evidence"] = sorted(a["evidence"], key=canonical)
        a["id"] = assertion_id(a)
    # Identical input rows are idempotent; inconsistent declared identities are never guessed.
    k["assertions"] = list({a["id"]: a for a in k.get("assertions", [])}.values())
    check_knowledge(k, root)
    return k, root


def load_package(path):
    root = Path(path).resolve()
    k = read_json(root / "knowledge.json")
    run = read_json(root / "run.json")
    changes = read_json(root / "changes.json")
    need(run.get("knowledge_sha256") == digest(k), "knowledge integrity mismatch")
    need(run.get("changes_sha256") == digest(changes), "changes integrity mismatch")
    need(changes.get("current_sha256") == digest(k), "changes current version mismatch")
    counts = check_knowledge(k, root)
    need(run.get("counts") == counts, "run counts mismatch")
    expected = "".join(canonical(s) + "\n" for s in k["sources"])
    need((root / "sources.jsonl").read_text(encoding="utf-8") == expected, "source manifest mismatch")
    return k, run


def active_groups(k):
    groups = defaultdict(list)
    for a in k["assertions"]:
        if a["status"] != "rejected":
            groups[a["fact_id"]].append(a)
    return groups


def conflict_ids(k):
    return sorted(fid for fid, rows in active_groups(k).items() if len({value_key(a["value"]) for a in rows}) > 1)


QUERY_FIELDS = frozenset({
    "entity", "concept", "period", "basis", "unit", "qualifiers",
    "valid_from", "valid_to", "fact", "with_evidence",
})
# CLI flag form uses hyphens for the two date fields.
QUERY_CLI_FLAGS = frozenset({
    "entity", "concept", "period", "basis", "unit", "qualifiers",
    "valid-from", "valid-to", "fact", "with-evidence", "args-json",
})


def _source_order_key(k, source_id):
    sources = {s["id"]: s for s in k["sources"]}
    s = sources.get(source_id, {})
    return (s.get("published_at") or "", s.get("accessed_at") or "", source_id)


def _assertion_order_key(k, a):
    srcs = sorted(_source_order_key(k, ev["source_id"]) for ev in a["evidence"])
    return (srcs[0] if srcs else ("", "", ""), a.get("period") or "", a["id"])


def conflict_kind(k, rows):
    """cross_period only when DIFFERING values are backed by different sources; else intra_report.

    dev-0.2.5: a fact group that merely has support from two sources (e.g. last year's value repeated in the
    new report) but whose disagreeing values all sit in one report is intra_report, not a restatement.
    Missing/coarse qualifiers that collapse distinct rows inside one report are intra_report.
    """
    by_value = defaultdict(set)
    for a in rows:
        by_value[value_key(a["value"])] |= {ev["source_id"] for ev in a["evidence"]}
    keys = list(by_value)
    for i, x in enumerate(keys):
        for y in keys[i + 1:]:
            if by_value[x] - by_value[y] and by_value[y] - by_value[x]:
                return "cross_period"
    return "intra_report"


def conflict_severity(kind, values):
    if kind == "intra_report":
        return "low"
    nums = [v for v in values if type(v) in {int, float}]
    if len(nums) >= 2:
        lo, hi = min(nums), max(nums)
        base = max(abs(lo), abs(hi), 1.0)
        if abs(hi - lo) / base >= 0.2:
            return "high"
        if abs(hi - lo) / base >= 0.05:
            return "medium"
    return "medium" if kind == "cross_period" else "low"


EXCERPT_CHARS = 160


def evidence_excerpts(k, a, raw_by_source, limit=EXCERPT_CHARS):
    """dev-0.2.6: short VERBATIM excerpts of an assertion's EvidenceSpans (report, page, quote), cut from source bytes."""
    if not raw_by_source:
        return []
    titles = {s["id"]: s.get("title") for s in k["sources"]}
    out = []
    for ev in a["evidence"]:
        raw = raw_by_source.get(ev["source_id"])
        if raw is None:
            continue
        text_ = raw[ev["start_utf8"]:ev["end_utf8"]].decode("utf-8")
        out.append({"source_id": ev["source_id"], "report": titles.get(ev["source_id"]), "page": ev.get("page"),
                    "start_utf8": ev["start_utf8"], "end_utf8": ev["end_utf8"],
                    "quote": text_[:limit], "truncated": len(text_) > limit})
    return out


def new_fact_details(k, changes, raw_by_source):
    """dev-0.2.6: every new fact carries its own excerpt and, when the baseline holds the same scope for an earlier
    period (same entity/concept/basis/unit/qualifiers), the prior-period counterpart with its excerpt."""
    new_ids = set(changes.get("new_assertions", []))
    rows = [a for a in k["assertions"] if a["status"] != "rejected"]
    base_rows = [a for a in rows if a["id"] not in new_ids]
    want = set(changes.get("new_facts", []))
    out = []
    seen = set()
    for a in rows:
        if a["fact_id"] not in want or a["fact_id"] in seen or a["id"] not in new_ids:
            continue
        seen.add(a["fact_id"])
        same_scope = [b for b in base_rows if b["entity_id"] == a["entity_id"] and b["concept_id"] == a["concept_id"]
                      and b["basis"] == a["basis"] and b["unit"] == a["unit"]
                      and canonical(b["qualifiers"]) == canonical(a["qualifiers"]) and b["period"] != a["period"]
                      and str(b["period"]) < str(a["period"])]
        prior = max(same_scope, key=lambda b: (str(b["period"]), b["id"])) if same_scope else None
        out.append({"fact_id": a["fact_id"], "entity_id": a["entity_id"], "concept_id": a["concept_id"],
                    "period": a["period"], "basis": a["basis"], "unit": a["unit"], "qualifiers": a["qualifiers"] or {},
                    "value": a["value"], "evidence": evidence_excerpts(k, a, raw_by_source),
                    "prior_period": prior["period"] if prior else None, "prior_value": prior["value"] if prior else None,
                    "prior_evidence": evidence_excerpts(k, prior, raw_by_source) if prior else [],
                    "note": None if prior else "baseline has no same-scope fact for an earlier period / 上年包内无同口径事实"})
    return out


def conflict_details(k, raw_by_source=None):
    """Enriched conflict records for changes.json (old/new/period/severity/kind)."""
    out = []
    for fid, rows in active_groups(k).items():
        vals = {value_key(a["value"]) for a in rows}
        if len(vals) <= 1:
            continue
        ordered = sorted(rows, key=lambda a: _assertion_order_key(k, a))
        kind = conflict_kind(k, ordered)
        values = [a["value"] for a in ordered]
        distinct = []
        seen = set()
        for a in ordered:
            vk = value_key(a["value"])
            if vk in seen:
                continue
            seen.add(vk)
            distinct.append(a)
        old_a, new_a = distinct[0], distinct[-1]
        if kind == "cross_period":
            # dev-0.2.5: old = earliest source's value, new = latest source's differing value (not two rows of one report)
            src_key = lambda a: max(_source_order_key(k, ev["source_id"]) for ev in a["evidence"])
            by_src = sorted(ordered, key=src_key)
            old_a = by_src[0]
            later = [a for a in by_src if value_key(a["value"]) != value_key(old_a["value"])
                     and src_key(a) > src_key(old_a)]
            new_a = later[-1] if later else distinct[-1]
        source_ids = sorted({ev["source_id"] for a in ordered for ev in a["evidence"]})
        out.append({
            "fact_id": fid,
            "entity_id": ordered[0]["entity_id"],
            "concept_id": ordered[0]["concept_id"],
            "period": ordered[0].get("period"),
            "basis": ordered[0].get("basis"),
            "unit": ordered[0].get("unit"),
            "qualifiers": ordered[0].get("qualifiers") or {},
            "old_value": old_a["value"],
            "new_value": new_a["value"],
            "values": values,
            "assertion_ids": [a["id"] for a in ordered],
            "source_ids": source_ids,
            "kind": kind,
            "severity": conflict_severity(kind, [a["value"] for a in distinct]),
            "old_evidence": evidence_excerpts(k, old_a, raw_by_source),
            "new_evidence": evidence_excerpts(k, new_a, raw_by_source),
            "note": ("同一报告内多值并列（常见于 qualifiers 缺失）；不是跨期更正。"
                     if kind == "intra_report" else
                     "跨来源/跨期同事实范围数值不一致；请人工核对是否为追溯调整。"),
        })
    rank = {"high": 0, "medium": 1, "low": 2}
    out.sort(key=lambda c: (0 if c["kind"] == "cross_period" else 1, rank.get(c["severity"], 9), c["fact_id"]))
    return out


def conflict_fact_ids(conflicts):
    if not conflicts:
        return []
    if isinstance(conflicts[0], dict):
        return [c["fact_id"] for c in conflicts]
    return list(conflicts)


def merge(base, incoming):
    need(base["scope"]["title"] == incoming["scope"]["title"], "scope.title differs; create separate knowledge package")
    need(incoming["scope"]["as_of"] >= base["scope"]["as_of"], "scope.as_of moves backwards")
    merged = copy.deepcopy(base)
    merged["scope"] = copy.deepcopy(incoming["scope"])
    additions = {}
    for name in ("entities", "definitions", "sources"):
        old = indexed(base[name], name)
        additions[name] = []
        for item in incoming[name]:
            previous = old.get(item["id"])
            if previous is not None:
                # Packaging may relocate the same source snapshot.
                omit = {"content_file"} if name == "sources" else set()
                need({k: v for k, v in previous.items() if k not in omit} ==
                     {k: v for k, v in item.items() if k not in omit},
                     f"{name} ID reused with changed definition/content: {item['id']}; preserve old ID and add a candidate")
            else:
                merged[name].append(copy.deepcopy(item)); additions[name].append(item["id"])
    prior = {a["id"] for a in base["assertions"]}
    prior_facts = {a["fact_id"] for a in base["assertions"]}
    new = [a for a in incoming["assertions"] if a["id"] not in prior]
    merged["assertions"].extend(copy.deepcopy(new))
    changes = {"new_definitions": additions["definitions"], "new_entities": additions["entities"],
               "new_sources": additions["sources"], "new_facts": sorted({a["fact_id"] for a in new} - prior_facts),
               "additional_support": [a["id"] for a in new if a["fact_id"] in prior_facts and any(
                   b["fact_id"] == a["fact_id"] and value_key(b["value"]) == value_key(a["value"]) for b in base["assertions"])],
               "new_assertions": [a["id"] for a in new], "duplicate_assertions": len(incoming["assertions"]) - len(new),
               "not_in_incoming": sorted(prior - {a["id"] for a in incoming["assertions"]}),
               "note": "Missing from this batch does not mean deleted, discontinued or withdrawn. New means new to this package."}
    return merged, changes


def cell(value):
    s = str(value) if isinstance(value, str) else canonical(value)
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", " ").replace("\r", " ")
    return re.sub(r"([\\`*_{}\[\]()|!])", r"\\\1", s)


def render(k, changes):
    entities = {e["id"]: e for e in k["entities"]}
    definitions = {d["id"]: d for d in k["definitions"]}
    sources = {s["id"]: s for s in k["sources"]}
    conflicts = set(conflict_ids(k))
    lines = [f"# {cell(k['scope']['title'])}", "", f"As of: {k['scope']['as_of']} | Schema {SCHEMA_VERSION}", "",
             "Machine-organized source claims. Candidate definitions; no automatic business decision. / 机器整理的来源断言，定义待审。", "",
             "## Changes / 变化", "", f"- New facts / 新事实: {len(changes.get('new_facts', []))}",
             f"- Additional support / 新增支持: {len(changes.get('additional_support', []))}",
             f"- Conflicting fact groups / 冲突组: {len(changes.get('conflicts', []))}",
             f"- Cross-period conflicts / 跨期冲突: {sum(1 for c in changes.get('conflicts', []) if isinstance(c, dict) and c.get('kind')=='cross_period')}",
             f"- Intra-report conflicts / 报告内并列: {sum(1 for c in changes.get('conflicts', []) if isinstance(c, dict) and c.get('kind')=='intra_report')}",
             "- Absence is not deletion. / 未发现不代表废止。", "",
             "## Claims / 事实审阅", "", "| Fact ID | Subject | Concept | Value | Unit | Period | Basis / qualifiers | Validity | Status | Evidence |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for a in k["assertions"]:
        refs = []
        for ev in a["evidence"]:
            src = sources[ev["source_id"]]
            page = f" p.{ev['page']}" if ev.get("page") else ""
            refs.append(f"[{cell(src['id'])}{page}](<{src['url']}>) bytes {ev['start_utf8']}:{ev['end_utf8']}")
        status = a["status"] + (" / conflict" if a["status"] != "rejected" and a["fact_id"] in conflicts else "")
        validity = f"{a.get('valid_from') or 'unspecified'} → {a.get('valid_to') or 'unspecified'}"
        vals = [a["fact_id"], entities[a["entity_id"]]["name"], definitions[a["concept_id"]]["name"], a["value"],
                a["unit"], a["period"], a["basis"] + " " + canonical(a["qualifiers"]), validity, status]
        lines.append("| " + " | ".join(cell(x) for x in vals) + " | " + "; ".join(refs) + " |")
    lines += ["", "## Boundaries / 边界", "", "Hash/range validation checks integrity and declared alignment, not semantic entailment or source authenticity.",
              "See knowledge.json for full IDs and review history. This is not an approval or access-control service.", "",
              "## Optional feedback / 自愿反馈", "", "Found an error, want this for routine work, or need internal deployment? Generate a local feedback draft and review it before sharing.",
              "Public issues: https://github.com/huhoo/cue-awesome/issues/new . Do not post internal documents or contact details there.", ""]
    return "\n".join(lines)


def write_package(k, roots, out, changes, parent=None, operation="build"):
    dest = Path(out).resolve()
    need(not dest.exists(), "output already exists; choose a new version directory")
    dest.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".ontology-", dir=dest.parent))
    try:
        result = copy.deepcopy(k)
        (stage / "evidence").mkdir()
        for s in result["sources"]:
            src = roots[s["id"]]
            raw = src.read_bytes()
            need(digest(raw) == s["sha256"], "source changed during packaging")
            rel = "evidence/" + digest(s["id"])[:24] + ".txt"
            (stage / rel).write_bytes(raw)
            s["content_file"] = rel
        counts = check_knowledge(result, stage)
        h = digest(result)
        raw_by_source = {s["id"]: (stage / s["content_file"]).read_bytes() for s in result["sources"]}
        changes = dict(changes, baseline_sha256=parent, current_sha256=h, conflicts=conflict_details(result, raw_by_source))
        if "new_facts" in changes:
            changes["new_fact_details"] = new_fact_details(result, changes, raw_by_source)
        run = {"skill_version": VERSION, "schema_version": SCHEMA_VERSION, "operation": operation,
               "created_at": datetime.now(timezone.utc).isoformat(), "knowledge_sha256": h,
               "changes_sha256": digest(changes), "parent_sha256": parent, "counts": counts,
               "semantic_verification": "not_established_by_scripts", "billing": "not_observed_by_offline_packager"}
        for name, data in (("knowledge.json", result), ("changes.json", changes), ("run.json", run)):
            (stage / name).write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
        (stage / "sources.jsonl").write_text("".join(canonical(s) + "\n" for s in result["sources"]), encoding="utf-8")
        (stage / "report.md").write_text(render(result, changes), encoding="utf-8")
        load_package(stage)
        stage.rename(dest)
        return run
    finally:
        if stage.exists():
            shutil.rmtree(stage)


def roots_for(k, root):
    return {s["id"]: local_file(root, s["content_file"]) for s in k["sources"]}


def coerce_query_args(args):
    """Accept Namespace or dict; reject unknown field names (no silent ignore)."""
    if isinstance(args, dict):
        unknown = sorted(set(args) - QUERY_FIELDS)
        need(not unknown, f"unknown query fields: {', '.join(unknown)}")
        payload = {f: args.get(f) for f in QUERY_FIELDS}
        return _NS(payload)
    # Namespace from argparse / tests
    return args


class _NS:
    def __init__(self, d):
        for k, v in d.items():
            setattr(self, k, v)
        # defaults for optional attrs tests may omit
        for k in QUERY_FIELDS:
            if not hasattr(self, k):
                setattr(self, k, None)


def query(k, args):
    args = coerce_query_args(args)
    for field in ("valid_from", "valid_to"):
        if getattr(args, field, None) is not None:
            iso_date(getattr(args, field), field)
    matches = [a for a in k["assertions"] if a["status"] != "rejected" and all(
        getattr(args, arg, None) is None or a[field] == getattr(args, arg)
        for arg, field in (("entity", "entity_id"), ("concept", "concept_id"), ("period", "period"), ("basis", "basis"),
                           ("unit", "unit"), ("valid_from", "valid_from"), ("valid_to", "valid_to"), ("fact", "fact_id")))]
    if getattr(args, "qualifiers", None) is not None:
        q = args.qualifiers if isinstance(args.qualifiers, dict) else decode_json(args.qualifiers)
        need(isinstance(q, dict), "query qualifiers must be JSON object")
        matches = [a for a in matches if canonical(a["qualifiers"]) == canonical(q)]
    ids = {a["fact_id"] for a in matches}
    state = "not_found" if not matches else "needs_scope" if len(ids) > 1 else (
        "conflict" if len({value_key(a["value"]) for a in matches}) > 1 else "found")
    source_ids = {ev["source_id"] for a in matches for ev in a["evidence"]}
    scopes = {a["fact_id"]: dict(fact_id=a["fact_id"], **key_of(a)) for a in matches}
    return {"status": state, "scopes": [scopes[fid] for fid in sorted(scopes)],
            "assertions": matches, "sources": [s for s in k["sources"] if s["id"] in source_ids],
            "note": "found means a structurally matching source claim, not independently verified truth"}


def catalog(k, changes=None, kind="all"):
    """List entities, definitions, and/or change summaries for agent discovery."""
    need(kind in {"all", "entities", "definitions", "changes"}, "catalog kind must be all|entities|definitions|changes")
    ents = k["entities"]
    defs = k["definitions"]
    ac = defaultdict(int)
    ec = defaultdict(int)
    for a in k["assertions"]:
        if a["status"] == "rejected":
            continue
        ac[a["concept_id"]] += 1
        ec[a["entity_id"]] += 1
    result = {"status": "ok", "kind": kind, "counts": {
        "entities": len(ents), "definitions": len(defs),
        "assertions": sum(1 for a in k["assertions"] if a["status"] != "rejected"),
        "facts": len({a["fact_id"] for a in k["assertions"] if a["status"] != "rejected"}),
    }}
    if kind in {"all", "entities"}:
        result["entities"] = [{"id": e["id"], "name": e["name"], "type": e["type"],
                               "assertions": ec.get(e["id"], 0)} for e in ents]
    if kind in {"all", "definitions"}:
        result["definitions"] = [{"id": d["id"], "name": d["name"], "kind": d["kind"],
                                  "value_type": d["value_type"], "assertions": ac.get(d["id"], 0)}
                                 for d in defs]
    if kind in {"all", "changes"}:
        ch = changes if changes is not None else {}
        raw_conflicts = ch.get("conflicts")
        if not raw_conflicts or (isinstance(raw_conflicts, list) and raw_conflicts and isinstance(raw_conflicts[0], str)):
            conflicts = conflict_details(k)  # enrich legacy id-only lists
        else:
            conflicts = raw_conflicts
        result["changes"] = {
            "new_facts": ch.get("new_facts", []),
            "new_fact_details": ch.get("new_fact_details", []),
            "new_entities": ch.get("new_entities", []),
            "new_definitions": ch.get("new_definitions", []),
            "new_sources": ch.get("new_sources", []),
            "additional_support": ch.get("additional_support", []),
            "conflicts": conflicts,
            "cross_period_conflicts": [c for c in conflicts if isinstance(c, dict) and c.get("kind") == "cross_period"],
            "intra_report_conflicts": [c for c in conflicts if isinstance(c, dict) and c.get("kind") == "intra_report"],
            "note": ch.get("note", "Missing from this batch does not mean deleted."),
        }
    return result


def export_okf(k, out):
    dest = Path(out)
    need(not dest.exists(), "OKF destination exists; choose a new directory")
    dest.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".okf-", dir=dest.parent))
    try:
        links = []
        for d in k["definitions"]:
            name = "concept-" + digest(d["id"])[:20] + ".md"
            # JSON-quoted scalars are valid YAML; no YAML dependency or arbitrary frontmatter injection.
            body = ["---", "type: " + json.dumps(d["kind"]), "title: " + json.dumps(d["name"], ensure_ascii=False),
                    "status: draft", "---", "", "# " + cell(d["name"]), "", cell(d["description"]), "",
                    "Definition is a candidate. No human verification is asserted.", "",
                    "Structured identity: `" + d["id"] + "`", ""]
            selected = dict(k, assertions=[a for a in k["assertions"] if a["concept_id"] == d["id"]])
            body.append(render(selected, {"conflicts": conflict_ids(selected)}))
            (stage / name).write_text("\n".join(body), encoding="utf-8")
            links.append(f"- [{cell(d['name'])}]({name})")
        (stage / "index.md").write_text("# Knowledge concepts\n\n" + "\n".join(links) + "\n", encoding="utf-8")
        stage.rename(dest)
    finally:
        if stage.exists(): shutil.rmtree(stage)
    return {"status": "exported", "concept_files": len(links), "okf_target": "0.2 core Markdown/YAML subset",
            "consumer_import_verified": False, "note": "No runtime actions, permissions or private evidence files exported."}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    for name in ("build", "update"):
        q = sub.add_parser(name, help="Package host-extracted input into a new immutable directory")
        q.add_argument("input")
        if name == "update": q.add_argument("--base", required=True)
        q.add_argument("--out", required=True)
    for name in ("validate", "query", "catalog", "export-okf", "feedback", "review"):
        q = sub.add_parser(name)
        q.add_argument("package")
        if name == "query":
            for field in ("entity", "concept", "period", "basis", "qualifiers", "unit", "valid-from", "valid-to", "fact"):
                q.add_argument("--" + field)
            q.add_argument("--with-evidence", action="store_true", help="Include bounded exact source excerpts")
            q.add_argument("--args-json", help="JSON object of query fields; unknown keys are rejected")
        if name == "catalog":
            q.add_argument("--kind", default="all", choices=["all", "entities", "definitions", "changes"],
                           help="What to list (default all)")
        if name in {"export-okf", "feedback", "review"}: q.add_argument("--out", required=True)
        if name == "review":
            q.add_argument("--assertion", required=True)
            q.add_argument("--decision", required=True, choices=["accepted", "rejected"])
            q.add_argument("--reviewer", required=True)
            q.add_argument("--note", required=True)
    q = sub.add_parser("numeric-import", help="Validate a host-computed numeric pack (deltas/checks/flags) + narrative items against packaged source pages")
    q.add_argument("numeric"); q.add_argument("--narrative"); q.add_argument("--sources", required=True); q.add_argument("--out", required=True)
    q = sub.add_parser("numeric", help="Serve a numeric pack: overview|drivers|consequences|normal|deltas|restatements|checks|narrative (credit-causal order)")
    q.add_argument("package"); q.add_argument("--view", default="overview", choices=["overview", "summary", "drivers", "consequences", "normal", "deltas", "restatements", "checks", "narrative"])
    q.add_argument("--role", choices=["driver", "consequence", "context"]); q.add_argument("--category")
    q.add_argument("--period", default="all", choices=["all", "latest", "earlier"]); q.add_argument("--item"); q.add_argument("--type")
    q.add_argument("--offset", type=int, default=0); q.add_argument("--limit", type=int, default=15); q.add_argument("--failed-only", action="store_true")
    q = sub.add_parser("omni-source", help="Saved Omni parse result (structuredContent / finished JSON) -> exact content file + source record with page_spans; never parses")
    q.add_argument("result"); q.add_argument("--out", required=True)
    q.add_argument("--id", required=True); q.add_argument("--url", required=True); q.add_argument("--title", required=True)
    q.add_argument("--accessed-at", required=True); q.add_argument("--published-at")
    q.add_argument("--public-status", default="retrieved_public", choices=["retrieved_public", "user_confirmed"])
    q.add_argument("--parse-origin", default="omni_live", choices=["omni_live", "omni_replay"])
    q.add_argument("--fy", type=int, help="Also write FY<fy>.pages.jsonl for numeric-import --sources")
    q.add_argument("--stem", help="Output file stem (default: the source id)")
    q.add_argument("--text-only", action="store_true", help="Allow a result without source-PDF page anchors (no page_spans; text_range evidence)")
    q = sub.add_parser("prepare", help="Resolve exact quotes into validated byte evidence; no model or parser call")
    q.add_argument("draft"); q.add_argument("--out", required=True)
    q = sub.add_parser("brief", help="Create a local searchable HTML/Markdown brief with evidence previews")
    q.add_argument("package"); q.add_argument("--base"); q.add_argument("--out", required=True)
    q = sub.add_parser("demo", help="Run the complete synthetic build/update/brief example without an API key")
    q.add_argument("--out", required=True)
    args = p.parse_args(argv)
    try:
        if args.command in {"numeric-import", "numeric"}:
            import numeric
            try:
                if args.command == "numeric-import": result = numeric.import_pack(args.numeric, args.narrative, args.sources, args.out)
                else: result = numeric.view(args.package, args.view, args.period, args.item, args.offset, args.limit, args.failed_only, args.type, True, args.role, args.category)
            except numeric.Invalid as exc:
                raise Invalid(str(exc))
        elif args.command == "omni-source":
            import omni_source
            meta = {"id": args.id, "url": args.url, "title": args.title, "published_at": args.published_at,
                    "accessed_at": args.accessed_at, "public_status": args.public_status}

            def check(m):
                need(isinstance(m["id"], str) and ID.fullmatch(m["id"]), "source id: letters, digits and _.:- only, starting with a letter")
                public_url(m["url"]); text(m["title"], "source.title")
                iso_date(m["published_at"], "source.published_at", True); iso_date(m["accessed_at"], "source.accessed_at")
            result = omni_source.build_source(args.result, args.out, meta, args.parse_origin, args.fy, args.stem,
                                              args.text_only, version=VERSION, validators=check)
        elif args.command in {"prepare", "brief", "demo"}:
            import experience
            if args.command == "prepare": result = experience.prepare(args.draft, args.out)
            elif args.command == "brief": result = experience.brief(args.package, args.out, args.base)
            else: result = experience.demo(args.out)
        elif args.command in {"build", "update"}:
            k, root = prepare_input(args.input)
            roots = roots_for(k, root)
            if args.command == "build":
                changes = {"new_facts": sorted({a["fact_id"] for a in k["assertions"]}),
                           "new_assertions": [a["id"] for a in k["assertions"]], "new_definitions": [d["id"] for d in k["definitions"]]}
                result = write_package(k, roots, args.out, changes)
            else:
                base, run = load_package(args.base)
                combined, changes = merge(base, k)
                roots = dict(roots_for(base, Path(args.base)), **roots)
                result = write_package(combined, roots, args.out, changes, run["knowledge_sha256"], "update")
        else:
            k, run = load_package(args.package)
            if args.command == "validate":
                result = {"status": "valid", "counts": run["counts"], "semantic_verification": "not_established_by_scripts"}
            elif args.command == "catalog":
                changes = read_json(Path(args.package) / "changes.json")
                result = catalog(k, changes, args.kind)
            elif args.command == "query":
                if getattr(args, "args_json", None):
                    payload = decode_json(args.args_json)
                    need(isinstance(payload, dict), "args-json must be a JSON object")
                    # Map CLI-style hyphen keys if present
                    mapped = {}
                    for key, val in payload.items():
                        k2 = {"valid-from": "valid_from", "valid-to": "valid_to",
                              "with-evidence": "with_evidence"}.get(key, key)
                        mapped[k2] = val
                    result = query(k, mapped)
                    with_ev = bool(mapped.get("with_evidence")) or args.with_evidence
                else:
                    result = query(k, args)
                    with_ev = args.with_evidence
                if with_ev:
                    import experience
                    result["evidence_previews"] = experience.previews(k, Path(args.package), result["assertions"])
            elif args.command == "export-okf": result = export_okf(k, args.out)
            elif args.command == "feedback":
                out = Path(args.out); need(not out.exists(), "feedback output exists")
                data = {"skill_version": VERSION, "counts": run["counts"], "intent": "",
                        "task_description_without_private_details": "", "failure_stage": "", "repeat_use": None,
                        "repeat_update_completed": None, "review_minutes_self_reported": None, "next_workflow": "",
                        "notice": "Local draft only. Review and explicitly choose whether to share. No source URLs, raw claims, contacts or telemetry included."}
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                result = {"status": "local_draft_created", "sent": False}
            elif args.command == "review":
                rows = [a for a in k["assertions"] if a["id"] == args.assertion]
                need(len(rows) == 1, "unknown assertion ID")
                a = rows[0]
                a["reviews"].append({"decision": args.decision, "reviewer": text(args.reviewer, "reviewer"),
                                     "note": text(args.note, "note"), "at": datetime.now(timezone.utc).isoformat()})
                a["status"] = args.decision
                result = write_package(k, roots_for(k, Path(args.package)), args.out, {"reviewed_assertions": [a["id"]]},
                                       run["knowledge_sha256"], "review")
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return 0
    except (Invalid, OSError, ValueError, TypeError, KeyError, UnicodeError) as exc:
        print(json.dumps({"status": "invalid", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
