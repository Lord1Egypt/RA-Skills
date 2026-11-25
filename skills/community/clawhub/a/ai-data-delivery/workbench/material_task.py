"""Bounded workspace identity selection and source-to-source discovery for authoring."""
import re
from pathlib import Path
import unicodedata

from workbench.scenario_contract import closure
from workbench.semantic_package import discover_candidates


def identity(asset, source_index):
    row = {key: asset.get(key) for key in ("id", "name", "kind", "definition", "domain", "scope", "status")}
    row["definition"] = (row["definition"] or "")[:240]
    row["role"] = asset.get("properties", {}).get("role") or asset.get("predicate")
    evidence = asset.get("evidence", [])
    row["evidence_count"] = len(evidence)
    row["evidence"] = [
        {**{key: ev[key] for key in ("type", "actor", "source_id", "revision", "extraction_id", "fragment_id") if key in ev},
         "source_name": source_index.get(ev.get("source_id"), {}).get("name"), "quote": ev.get("quote", "")[:160]}
        for ev in evidence[:2]]
    return row


def select_assets(sem, sources, req, scenario):
    assets = sem["assets"]
    index = {a["id"]: a for a in assets}
    roots, question, full = req.get("asset_ids"), req.get("question"), req.get("all_assets", False)
    if type(full) is not bool or sum((roots is not None, question is not None, full, scenario is not None)) > 1:
        raise ValueError("Select one of --id, --question, --all-assets or --scenario / 仅选一种范围方式")
    if roots is not None and (not isinstance(roots, list) or not roots or
                              not all(isinstance(aid, str) and aid.strip() for aid in roots)):
        raise ValueError("Select nonempty asset IDs / 请选择有效资产身份")
    limit, offset = req.get("limit", 12), req.get("offset", 0)
    if type(limit) is not int or not 1 <= limit <= 100 or type(offset) is not int or offset < 0:
        raise ValueError("Use limit 1–100 and a nonnegative offset / 分页数量为 1–100，起点须为非负整数")
    if scenario:
        roots, question = scenario["asset_ids"], scenario.get("question") or scenario.get("title")
    base = {"total_count": len(assets), "omitted_count": len(assets),
            "browse_options": ["--question", "--id", "--all-assets"]}
    if full:
        return assets, {**base, "selection": "current_graph", "status": "selected", "omitted_count": 0}
    if roots:
        paths = closure(sem, roots)
        selected = [a for a in assets if a["id"] in paths]
        missing = sorted(paths.keys() - index.keys())
        return selected, {**base, "selection": ("scenario_roots_and_required_dependencies" if scenario
                                                  else "roots_and_required_dependencies"),
                          "status": "needs_selection" if missing else "selected", "requested_ids": roots,
                          "missing_ids": missing, "omitted_count": len(assets) - len(selected),
                          "next_step": "Search other identities with --question; select with --id."}
    active = [a for a in assets if a["status"] != "retired"]
    if question is not None:
        found = discover_candidates(active, question, limit=limit, offset=offset)
        page, total = found["candidates"], found["total"]
    else:
        active.sort(key=lambda a: (a["name"].casefold(), a["id"]))
        page, total = active[offset:offset + limit], len(active)
    source_index = {s["id"]: s for s in sources}
    candidates = [{**identity(index[a["id"]], source_index),
                   **{key: a[key] for key in ("match_reason", "match_fields") if key in a}} for a in page]
    return [], {**base, "selection": "question_candidates" if question else "browse_candidates",
                "status": "needs_selection" if total else "no_match", "question": question,
                "candidates": candidates, "candidate_count": total, "offset": offset, "limit": limit,
                "next_offset": offset + limit if offset + limit < total else None,
                "next_step": "Select the relevant identity with --id; use --offset for the next candidate page or --question to refine."}


def _normalize(text):
    return unicodedata.normalize("NFKC", text).casefold()


def _terms(text, ignored):
    # Lexical overlap retrieves passages for people to compare. A shared location
    # or generic obligation verb supplies no evidence of a shared requirement.
    text = _normalize(text)
    for value in ignored:
        text = text.replace(value, " ")
    words = {w for w in re.findall(r"[a-z][a-z0-9_-]{2,}", text) if w not in
             {"the", "and", "for", "are", "that", "with", "from", "must", "shall", "this", "should", "under"}}
    for section in re.findall(r"[\u3400-\u9fff]{2,}", text):
        words.update(section[i:i + size] for size in (2, 4) for i in range(len(section) - size + 1))
    return words


def _citation_pattern(source):
    title = _normalize(Path(source["name"]).stem).strip()
    if not title:
        return None
    # A document name mentioned in prose may just be the topic. Require an
    # actual reference marker or a literal filename for the stronger signal.
    label = re.escape(title)
    return re.compile(r"《\s*" + label + r"\s*》|(?:参照|依据|根据|引用|见|按照|参见|依照|pursuant to|refers? to|see|cites?)\s*[\"'“《]?\s*" +
                      label + (r"(?![a-z0-9_-])" if title.isascii() else "") +
                      r"|(?<![a-z0-9_-])" + re.escape(_normalize(source["name"])) + r"(?![a-z0-9_-])")


def _anchor(source, version, fragment, term=None):
    row = {"source_id": source["id"], "revision": version["revision"], "extraction_id": version.get("current_extraction")}
    if fragment:
        text = fragment["text"]
        position = text[:CHARACTER_LIMIT].casefold().find(term.casefold()) if term else 0
        start = max(0, position - 64)
        row.update(fragment_id=fragment["id"], location=fragment["location"], quote=text[start:start + 240])
    return row


DISCOVERY_FORMATS = {"text", "markdown", "docx", "pdf"}
FRAGMENT_LIMIT = 256
CHARACTER_LIMIT = 65536


def _profile(source):
    version = source["revisions"][-1]
    fragments = version["parsed"]["fragments"]
    scanned, remaining = [], CHARACTER_LIMIT
    ignored = {_normalize(v) for v in (source.get("scope"), source.get("domain")) if isinstance(v, str) and v}
    ignored.update(("应当", "必须", "要求", "相关", "可以", "规定", "地区", "企业应", "根据", "材料"))
    ignored = sorted(ignored, key=lambda value: (-len(value), value))
    truncated = False
    if source["format"] in DISCOVERY_FORMATS:
        for fragment in fragments[:FRAGMENT_LIMIT]:
            excerpt = fragment["text"][:remaining]
            normalized = _normalize(excerpt)
            scanned.append((fragment, normalized, _terms(normalized, ignored)))
            remaining -= len(excerpt)
            if remaining == 0:
                truncated = len(excerpt) < len(fragment["text"])
                break
        truncated |= len(scanned) < len(fragments)
    return {"source": source, "version": version, "rows": scanned, "citation": _citation_pattern(source),
            "truncated": truncated}


def _related_pair(left_profile, right_profile, left_terms):
    left, right = left_profile["source"], right_profile["source"]
    lv, rv = left_profile["version"], right_profile["version"]
    best = None
    for fragment, _, fragment_terms in right_profile["rows"]:
        by_fragment = {}
        for term in sorted((t for t in fragment_terms if t in left_terms), key=lambda t: (-len(t), t)):
            primary = left_terms[term]
            terms = by_fragment.setdefault(primary["id"], [])
            if len(terms) < 4 and all(term not in previous and previous not in term for previous in terms):
                terms.append(term)
        for terms in by_fragment.values():
            if len(terms) < 2 and not re.fullmatch(r"[\u3400-\u9fff]{4}", terms[0]):
                continue
            score = sum(map(len, terms))
            if best is None or score > best[0]:
                best = (score, terms, left_terms[terms[0]], fragment)
    left_pattern, right_pattern = left_profile["citation"], right_profile["citation"]
    left_cite = next((f for f, body, _ in left_profile["rows"] if right_pattern and right_pattern.search(body)), None)
    right_cite = next((f for f, body, _ in right_profile["rows"] if left_pattern and left_pattern.search(body)), None)
    if not best and not left_cite and not right_cite:
        return None
    reasons = []
    if left_cite or right_cite:
        reasons.append({"kind": "explicit_reference",
                        "citing_source_id": left["id"] if left_cite else right["id"],
                        "primary": _anchor(left, lv, left_cite or (best[2] if best else next(iter(lv["parsed"]["fragments"]), None)), Path(right["name"]).stem),
                        "counterpart": _anchor(right, rv, right_cite or (best[3] if best else next(iter(rv["parsed"]["fragments"]), None)), Path(left["name"]).stem)})
    if best:
        score, terms, primary, counterpart = best
        reasons.append({"kind": "shared_passage_terms", "terms": terms,
                        "primary": _anchor(left, lv, primary, terms[0]),
                        "counterpart": _anchor(right, rv, counterpart, terms[0])})
    return (bool(left_cite or right_cite), best[0] if best else 0), reasons


def _model_links(sources, assets, primary_ids):
    """Compare passages already cited by the same confirmed asset at these revisions."""
    source_index = {s["id"]: s for s in sources}
    fragments, linked = {}, {}

    def pointer(ev):
        sid = ev["source_id"]
        version = source_index[sid]["revisions"][-1]
        if sid not in fragments:
            fragments[sid] = {f["id"]: f for f in version["parsed"]["fragments"]}
        fragment = fragments[sid].get(ev.get("fragment_id"))
        if fragment:
            return {**_anchor(source_index[sid], version, fragment), "quote": ev["quote"][:240]}
        return None

    for asset in assets:
        if asset["status"] != "confirmed":
            continue
        evidence = {}
        for ev in asset.get("evidence", []):
            source = source_index.get(ev.get("source_id"))
            if source and ev.get("revision") == source["current_revision"]:
                extraction = source["revisions"][-1].get("current_extraction")
                if ev.get("extraction_id", extraction) == extraction:
                    evidence.setdefault(source["id"], ev)
        anchors = sorted(evidence.keys() & primary_ids)
        if not anchors:
            continue
        for sid in sorted(evidence.keys() - primary_ids - linked.keys()):
            left, right = pointer(evidence[anchors[0]]), pointer(evidence[sid])
            if left and right:
                linked[sid] = {"kind": "shared_confirmed_asset", "asset_id": asset["id"], "name": asset["name"],
                               "primary": left, "counterpart": right}
    return linked


def related_sources(sources, primary_ids, assets):
    primary = []
    truncated = 0
    skipped = sum(s["format"] not in DISCOVERY_FORMATS for s in sources)
    for source in sources:
        if source["id"] in primary_ids:
            profile = _profile(source)
            truncated += profile["truncated"]
            postings = {}
            for fragment, _, terms in profile["rows"]:
                for term in terms:
                    postings.setdefault(term, fragment)
            primary.append((profile, postings))
    ranked = []
    model_links = _model_links(sources, assets, primary_ids)
    for other in sources:
        if other["id"] in primary_ids:
            continue
        profile = _profile(other)
        truncated += profile["truncated"]
        matches = [match for source, postings in primary if (match := _related_pair(source, profile, postings))]
        if matches or other["id"] in model_links:
            score, reasons = max(matches, key=lambda match: match[0]) if matches else ((False, 0), [])
            model_link = model_links.get(other["id"])
            if model_link:
                reasons = [model_link, *reasons]
            rank = (int(score[0]), int(bool(model_link)), score[1])
            ranked.append((rank, {"id": other["id"], "name": other["name"], "revision": other["current_revision"],
                                   "domain": other["domain"], "scope": other["scope"],
                                   "effective_from": other["revisions"][-1].get("effective_from"),
                                   "effective_to": other["revisions"][-1].get("effective_to"),
                                   "status": "candidate", "reasons": reasons}))
    ranked.sort(key=lambda pair: (-pair[0][0], -pair[0][1], -pair[0][2], pair[1]["id"]))
    return [row for _, row in ranked], {"formats_for_text_search": sorted(DISCOVERY_FORMATS),
        "fragment_limit_per_source": FRAGMENT_LIMIT, "character_limit_per_source": CHARACTER_LIMIT,
        "truncated_source_count": truncated, "sources_outside_text_search": skipped,
        "full_text_option": "--compare-source"}
