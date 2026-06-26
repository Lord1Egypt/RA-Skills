"""Deep Research v2 — Analyst (local, deterministic).

Implements lightweight synthesis utilities for a list of extracted findings.

Core entrypoint:
    analyze_findings(findings: list[dict], dimensions: list[str]) -> AnalysisResult

Expected finding fields (best-effort, all optional):
    - claim / content / text: str
    - source_url / url: str
    - dimension: str
    - confidence: float (0..1) from extractor (treated as claim-level certainty)
    - source_score: float (0..1) or source.score: float (0..1)
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
import re
from collections import Counter, defaultdict



@dataclass(frozen=True)
class AnalysisResult:
    themes: list[dict]
    contradictions: list[dict]
    gaps: list[dict]
    confidence_map: dict[str, float]
    coverage_score: float


_WORD_RE = re.compile(r"[a-z0-9][a-z0-9\-']{1,}")
_NEGATIONS = {"no", "not", "never", "none", "without", "cannot", "can't", "won't"}
_DIRECTION_UP = {"increase", "increas", "increases", "increased", "higher", "more", "up", "rise", "ris", "rises", "rising", "grow", "grows", "growth"}
_DIRECTION_DOWN = {"decrease", "decreas", "decreases", "decreased", "lower", "less", "down", "fall", "falls", "falling", "decline", "declines", "declined", "drop", "drops", "dropped"}

# A tiny, intentionally conservative stopword list (stdlib-only).
_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "have",
    "in",
    "into",
    "is",
    "it",
    "its",
    "of",
    "on",
    "or",
    "that",
    "the",
    "their",
    "this",
    "to",
    "was",
    "were",
    "will",
    "with",
}


def analyze_findings(findings: list[dict], dimensions: list[str]) -> AnalysisResult:
    """Analyze a list of extracted findings across given research dimensions.

    Steps:
      1) Deduplicate by simple hash + Jaccard similarity on token sets
      2) Theme extraction via keyword co-occurrence clusters (3-7 clusters)
      3) Contradiction detection via keyword overlap + polarity heuristics
      4) Confidence scoring from source quality + corroboration count
      5) Gap analysis across provided dimensions + overall coverage score
    """
    normalized_dimensions = [d.strip() for d in dimensions if str(d).strip()]

    prepared = [_prepare_finding(f) for f in findings if _get_text(f)]
    deduped = _deduplicate(prepared)

    themes = _extract_themes(deduped)
    contradictions = _detect_contradictions(deduped)
    confidence_map = _score_confidence(deduped)
    gaps, coverage_score = _gap_analysis(deduped, normalized_dimensions)

    return AnalysisResult(
        themes=themes,
        contradictions=contradictions,
        gaps=gaps,
        confidence_map=confidence_map,
        coverage_score=coverage_score,
    )


def _get_text(finding: dict) -> str:
    for key in ("claim", "content", "text"):
        v = finding.get(key)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def _get_url(finding: dict) -> str:
    for key in ("source_url", "url"):
        v = finding.get(key)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def _prepare_finding(finding: dict) -> dict:
    text = _get_text(finding)
    tokens = _tokens(text)
    finding_id = _stable_id(text)

    prepared = dict(finding)
    prepared["_id"] = finding_id
    prepared["_text"] = text
    prepared["_tokens"] = tokens
    prepared["_url"] = _get_url(finding)
    prepared["_dimension"] = (finding.get("dimension") or "").strip().lower()
    prepared["_extractor_confidence"] = _clamp01(_as_float(finding.get("confidence"), default=0.5))
    prepared["_source_quality"] = _clamp01(_infer_source_quality(finding))
    prepared["_polarity"] = _polarity(text, tokens)
    return prepared


def _stable_id(text: str) -> str:
    norm = _normalize_text(text)
    return hashlib.sha1(norm.encode("utf-8")).hexdigest()[:16]


def _normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def _tokens(text: str) -> set[str]:
    words = {_stem(m.group(0)) for m in _WORD_RE.finditer(text.lower())}
    return {w for w in words if w not in _STOPWORDS and len(w) >= 3}


def _stem(word: str) -> str:
    """Tiny stemmer to improve similarity/polarity heuristics (no third-party deps)."""
    if len(word) <= 4:
        return word
    for suffix in ("ing", "ed"):
        if word.endswith(suffix) and len(word) - len(suffix) >= 4:
            return word[: -len(suffix)]
    if word.endswith("s") and len(word) >= 5:
        return word[:-1]
    return word


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    denom = len(a | b)
    if denom == 0:
        return 0.0
    return len(a & b) / denom


def _deduplicate(prepared: list[dict]) -> list[dict]:
    """Deduplicate by exact hash first, then Jaccard similarity."""
    if not prepared:
        return []

    by_hash: dict[str, list[dict]] = defaultdict(list)
    for f in prepared:
        by_hash[f["_id"]].append(f)

    collapsed: list[dict] = []
    for group in by_hash.values():
        collapsed.append(_merge_duplicates(group))

    # Second pass: near-duplicate merge via Jaccard on tokens.
    # Skip merging when polarities differ — opposing claims should survive for
    # contradiction detection.
    merged: list[dict] = []
    for f in collapsed:
        placed = False
        for i, existing in enumerate(merged):
            if _jaccard(f["_tokens"], existing["_tokens"]) >= 0.6:
                # Don't merge opposing claims
                if _is_opposing(f["_polarity"], existing["_polarity"]):
                    continue
                merged[i] = _merge_duplicates([existing, f])
                placed = True
                break
        if not placed:
            merged.append(f)

    return merged


def _merge_duplicates(group: list[dict]) -> dict:
    """Merge duplicates, preserving best confidences and collecting source URLs."""
    if len(group) == 1:
        f = dict(group[0])
        f["_sources"] = [f["_url"]] if f["_url"] else []
        return f

    # Choose representative: highest extractor_confidence then longest text.
    rep = max(group, key=lambda x: (x.get("_extractor_confidence", 0.0), len(x.get("_text", ""))))
    merged = dict(rep)
    sources: list[str] = []
    for f in group:
        u = f.get("_url", "")
        if u and u not in sources:
            sources.append(u)
    merged["_sources"] = sources
    merged["_extractor_confidence"] = max((f.get("_extractor_confidence", 0.0) for f in group), default=merged.get("_extractor_confidence", 0.5))
    merged["_source_quality"] = max((f.get("_source_quality", 0.0) for f in group), default=merged.get("_source_quality", 0.5))
    # Preserve dimension — prefer any non-empty dimension from the group.
    dims = [f.get("_dimension", "") for f in group if f.get("_dimension")]
    merged["_dimension"] = merged.get("_dimension", "") or (dims[0] if dims else "")
    return merged


def _extract_themes(deduped: list[dict]) -> list[dict]:
    """Group findings into 3-7 themes via keyword co-occurrence."""
    if not deduped:
        return []

    keyword_counts: Counter[str] = Counter()
    for f in deduped:
        keyword_counts.update(list(f["_tokens"]))

    # Candidate keywords: reasonably frequent, capped for determinism.
    candidate_keywords = [kw for kw, c in keyword_counts.most_common(40) if c >= 2]
    if not candidate_keywords:
        # Fall back: still produce 1-3 clusters with best tokens per finding.
        candidate_keywords = [kw for kw, _ in keyword_counts.most_common(12)]

    # Co-occurrence graph among candidate keywords.
    adjacency: dict[str, Counter[str]] = {kw: Counter() for kw in candidate_keywords}
    for f in deduped:
        present = [kw for kw in candidate_keywords if kw in f["_tokens"]]
        for i in range(len(present)):
            for j in range(i + 1, len(present)):
                a, b = present[i], present[j]
                adjacency[a][b] += 1
                adjacency[b][a] += 1

    # Build clusters as connected components using a minimal edge threshold.
    seen: set[str] = set()
    clusters: list[set[str]] = []
    for kw in candidate_keywords:
        if kw in seen:
            continue
        stack = [kw]
        component: set[str] = set()
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            component.add(cur)
            for nbr, w in adjacency.get(cur, {}).items():
                if w >= 2 and nbr not in seen:
                    stack.append(nbr)
        clusters.append(component)

    # Assign findings to best cluster by keyword overlap.
    theme_items: list[dict] = []
    for idx, kwset in enumerate(clusters):
        if not kwset:
            continue
        finding_ids = []
        for f in deduped:
            if f["_tokens"] & kwset:
                finding_ids.append(f["_id"])
        if not finding_ids:
            continue

        keywords_sorted = sorted(list(kwset), key=lambda k: (-keyword_counts.get(k, 0), k))
        name = _theme_name(keywords_sorted[:4])
        theme_items.append(
            {
                "name": name,
                "keywords": keywords_sorted[:12],
                "finding_ids": finding_ids,
                "size": len(finding_ids),
            }
        )

    # Ensure 3-7 themes: split/merge heuristically.
    theme_items.sort(key=lambda t: (-t["size"], t["name"]))
    if len(theme_items) > 7:
        theme_items = theme_items[:7]
    if len(theme_items) < 3 and len(deduped) >= 3:
        # Create additional singleton-ish themes from top findings tokens.
        used_ids = {fid for t in theme_items for fid in t["finding_ids"]}
        for f in deduped:
            if f["_id"] in used_ids:
                continue
            kws = sorted(list(f["_tokens"]), key=lambda k: (-keyword_counts.get(k, 0), k))[:6]
            if not kws:
                continue
            theme_items.append(
                {
                    "name": _theme_name(kws[:3]),
                    "keywords": kws,
                    "finding_ids": [f["_id"]],
                    "size": 1,
                }
            )
            used_ids.add(f["_id"])
            if len(theme_items) >= 3:
                break

    return theme_items


def _theme_name(keywords: list[str]) -> str:
    if not keywords:
        return "General"
    top = keywords[0].replace("-", " ").strip()
    if len(keywords) >= 2:
        second = keywords[1].replace("-", " ").strip()
        return f"{top} / {second}"
    return top


def _polarity(text: str, tokens: set[str]) -> str:
    """Return a coarse polarity label: 'affirm', 'negate', 'up', 'down'.

    When both directional words (up/down) appear, the *last* directional
    word in the sentence is taken as the claim's actual direction — this
    handles cases like "increasing rates *decrease* affordability".
    """
    lowered = text.lower()
    has_neg = any(re.search(rf"\b{re.escape(n)}\b", lowered) for n in _NEGATIONS)
    has_up = bool(tokens & _DIRECTION_UP)
    has_down = bool(tokens & _DIRECTION_DOWN)

    if has_up and not has_down:
        return "up"
    if has_down and not has_up:
        return "down"
    # Both up and down present — use the last directional word as the claim direction.
    if has_up and has_down:
        last_dir = "affirm"
        for m in re.finditer(r"[a-z]+", lowered):
            w = _stem(m.group(0))
            if w in _DIRECTION_UP:
                last_dir = "up"
            elif w in _DIRECTION_DOWN:
                last_dir = "down"
        if last_dir != "affirm":
            return last_dir
    if has_neg:
        return "negate"
    return "affirm"


def _detect_contradictions(deduped: list[dict]) -> list[dict]:
    """Find likely opposing claims across sources (heuristic)."""
    contradictions: list[dict] = []
    if len(deduped) < 2:
        return contradictions

    # Only compare pairs with meaningful overlap to keep it cheap and reduce false positives.
    for i in range(len(deduped)):
        a = deduped[i]
        for j in range(i + 1, len(deduped)):
            b = deduped[j]
            overlap = _jaccard(a["_tokens"], b["_tokens"])
            if overlap < 0.35:
                continue

            if _is_opposing(a["_polarity"], b["_polarity"]):
                contradictions.append(
                    {
                        "finding_id_a": a["_id"],
                        "finding_id_b": b["_id"],
                        "claim_a": a["_text"],
                        "claim_b": b["_text"],
                        "source_a": a.get("_url") or (a.get("_sources") or [""])[0],
                        "source_b": b.get("_url") or (b.get("_sources") or [""])[0],
                        "overlap": round(overlap, 3),
                        "reason": f"Opposing polarity: {a['_polarity']} vs {b['_polarity']}",
                    }
                )

    # Dedup contradictions by unordered pair.
    seen_pairs: set[tuple[str, str]] = set()
    unique: list[dict] = []
    for c in contradictions:
        pair = tuple(sorted([c["finding_id_a"], c["finding_id_b"]]))
        if pair in seen_pairs:
            continue
        seen_pairs.add(pair)
        unique.append(c)
    unique.sort(key=lambda x: (-x["overlap"], x["finding_id_a"], x["finding_id_b"]))
    return unique


def _is_opposing(p1: str, p2: str) -> bool:
    opposing_pairs = {("up", "down"), ("down", "up"), ("affirm", "negate"), ("negate", "affirm")}
    return (p1, p2) in opposing_pairs


def _score_confidence(deduped: list[dict]) -> dict[str, float]:
    """Compute reliability score combining source quality + corroboration."""
    confidence_map: dict[str, float] = {}
    if not deduped:
        return confidence_map

    # Corroboration: count of other findings with high similarity.
    corroboration_count: dict[str, int] = {f["_id"]: 0 for f in deduped}
    for i in range(len(deduped)):
        for j in range(i + 1, len(deduped)):
            sim = _jaccard(deduped[i]["_tokens"], deduped[j]["_tokens"])
            if sim >= 0.6:
                corroboration_count[deduped[i]["_id"]] += 1
                corroboration_count[deduped[j]["_id"]] += 1

    for f in deduped:
        base = 0.55 * f["_source_quality"] + 0.45 * f["_extractor_confidence"]
        # Diminishing returns: +0.07 per corroboration up to +0.21.
        corr = min(3, corroboration_count.get(f["_id"], 0))
        score = base + 0.07 * corr
        confidence_map[f["_id"]] = round(_clamp01(score), 4)

    return confidence_map


def _gap_analysis(deduped: list[dict], dimensions: list[str]) -> tuple[list[dict], float]:
    """Identify dimensions with insufficient coverage; compute coverage score."""
    if not dimensions:
        return ([], 1.0 if deduped else 0.0)

    counts: dict[str, int] = {d.lower(): 0 for d in dimensions}
    for f in deduped:
        dim = (f.get("_dimension") or "").strip().lower()
        if dim in counts:
            counts[dim] += 1

    gaps: list[dict] = []
    for dim in dimensions:
        key = dim.lower()
        c = counts.get(key, 0)
        if c == 0:
            gaps.append({"dimension": dim, "coverage": c, "severity": "high"})
        elif c == 1 and len(deduped) > 3:
            # Only flag single-coverage as medium when there are enough
            # findings that more could reasonably be expected.
            gaps.append({"dimension": dim, "coverage": c, "severity": "medium"})

    covered = sum(1 for d in dimensions if counts.get(d.lower(), 0) > 0)
    coverage_score = covered / max(1, len(dimensions))
    return (gaps, round(coverage_score, 4))


def _infer_source_quality(finding: dict) -> float:
    """Infer source quality in 0..1 from common fields (best-effort)."""
    # Explicit numeric hint.
    direct = finding.get("source_score")
    if direct is not None:
        return _as_float(direct, default=0.6)

    source = finding.get("source")
    if isinstance(source, dict):
        if "score" in source:
            return _as_float(source.get("score"), default=0.6)

    url = _get_url(finding).lower()
    if not url:
        return 0.55

    # Very coarse domain heuristics.
    if ".gov/" in url or url.endswith(".gov") or ".gov." in url:
        return 0.9
    if ".edu/" in url or url.endswith(".edu") or ".edu." in url:
        return 0.85
    if "arxiv.org" in url:
        return 0.75
    if "wikipedia.org" in url:
        return 0.65
    if "medium.com" in url or "substack.com" in url:
        return 0.55
    if "reddit.com" in url or "twitter.com" in url or "x.com" in url:
        return 0.45
    return 0.6


def _as_float(value: object, default: float) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default


def _clamp01(x: float) -> float:
    if math.isnan(x) or math.isinf(x):
        return 0.0
    return max(0.0, min(1.0, x))

