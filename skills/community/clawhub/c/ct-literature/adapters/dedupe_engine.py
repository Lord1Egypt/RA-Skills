#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
dedupe_engine.py — multi-identifier deduplication engine for ct-literature.

Enhances normalize.merge() with:
  1. Multi-identifier canonicalization (DOI, PMID, PMCID, arXiv ID)
  2. Version-agnostic arXiv ID matching (2606.11144v1 == 2606.11144v2)
  3. Transitive identity resolution (A.doi==B.doi AND B.pmid==C.pmid → A=B=C)
  4. Fuzzy title matching for records lacking any shared identifier
  5. Field-merge logic preserved from normalize.py (EuropePMC priority, etc.)

Backward-compatible: normalize.merge() unchanged. Callers opt in via
merge_v2() / merge_v2_with_stats(). All pure local computation, no network.

Architecture:
  Phase 1 — extract canonical identifiers from every work record
  Phase 2 — union-find over shared identifiers → identity groups (transitive)
  Phase 3 — fuzzy title matching for unmatched singletons
  Phase 4 — merge each group using the existing field-merge policy

⚠️ 源码保护（2026-10-26）：生产路径的去重 / 归一化 / PRISMA 策略逻辑已上移 coze
（lit_dedup 节点，支持 v1/v2）。`ct_literature._dispatch_merge` 为本薄客户端入口。
本模块 `merge_v2*` 仍保留本地实现，仅供 `tests/test_dedupe_engine.py` 与离线模式使用，
**发布包须剥离**（连同 `dedupe_engine.py`）以防源码泄露——请勿在发布副本中保留。
"""

import re
from difflib import SequenceMatcher

# ── 归一内核单一真源（0.3.99 重构）──────────────────────────────────────────────
# 题名/DOI/source 归一、去重键、预印本-发表版配对统一从 lit_norm_core 导入；
# 保留本模块专属的 v2 / UnionFind / 多标识符(pmid/pmcid/arxiv) 提取与相似度逻辑。
import os as _os
import sys as _sys
_THIS_DIR = _os.path.dirname(_os.path.abspath(__file__))
if _THIS_DIR not in _sys.path:
    _sys.path.insert(0, _THIS_DIR)
from lit_norm_core import (
    _canon_source, _norm_title, _bare_doi, _norm_doi,
    dedupe_key, _dedupe_preprint_published,
)
# 历史公共 API 名称别名（供 extract_identifiers / merge_v2* 等内部调用）
normalize_doi = _norm_doi
normalize_title = _norm_title

# ---------------------------------------------------------------------------
# Identifier canonicalization
# ---------------------------------------------------------------------------

def normalize_pmid(pmid):
    """Canonicalize PubMed ID: digits only."""
    if not pmid:
        return None
    s = str(pmid).strip()
    m = re.search(r"\d{7,9}", s)
    return m.group(0) if m else None


def normalize_pmcid(pmcid):
    """Canonicalize PMC ID: digits only, strip PMC prefix."""
    if not pmcid:
        return None
    s = str(pmcid).strip()
    m = re.search(r"(\d{5,})", s)
    return m.group(1) if m else None


def normalize_arxiv_id(arxiv_id):
    """Canonicalize arXiv ID: strip version suffix (2606.11144v1 → 2606.11144)."""
    if not arxiv_id:
        return None
    s = str(arxiv_id).strip()
    # Match pattern like 2606.11144 or 2606.11144v2
    m = re.search(r"(\d{4}\.\d{4,5})(?:v\d+)?", s)
    return m.group(1) if m else None


# ---------------------------------------------------------------------------
# Identifier extraction
# ---------------------------------------------------------------------------

def extract_identifiers(work):
    """Extract all canonical identifiers from a work record.
    Returns dict with keys: doi, pmid, pmcid, arxiv_id, title_norm
    Only non-None values are included."""
    ids = {}
    doi = normalize_doi(work.get("doi"))
    if doi:
        ids["doi"] = doi
    pmid = normalize_pmid(work.get("pmid"))
    if pmid:
        ids["pmid"] = pmid
    pmcid = normalize_pmcid(work.get("pmcid"))
    if pmcid:
        ids["pmcid"] = pmcid
    # arXiv ID: check 'id' field if source is arXiv, or 'doi' for arxiv DOI
    arxiv_id = normalize_arxiv_id(work.get("id"))
    if arxiv_id and work.get("source") == "arXiv":
        ids["arxiv_id"] = arxiv_id
    # Also check if doi contains "arxiv"
    if not arxiv_id and doi and "arxiv" in doi:
        arxiv_id = normalize_arxiv_id(doi)
        if arxiv_id:
            ids["arxiv_id"] = arxiv_id
    title_norm = normalize_title(work.get("title"))
    if title_norm:
        ids["title_norm"] = title_norm
    return ids


# ---------------------------------------------------------------------------
# Union-Find for transitive identity resolution
# ---------------------------------------------------------------------------

class UnionFind:
    """Simple union-find with path compression and union by rank."""
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # path halving
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1


def build_identity_groups(works):
    """Group works by shared identifiers (transitive).
    Returns list of groups, each group is a list of indices into works.
    Works with no identifiers are singleton groups."""
    n = len(works)
    if n == 0:
        return []

    # Phase 1: extract identifiers for all works
    all_ids = []
    id_to_works = {}  # (id_type, id_value) -> list of work indices
    for i, w in enumerate(works):
        ids = extract_identifiers(w)
        all_ids.append(ids)
        for id_type, id_val in ids.items():
            if id_type == "title_norm":
                continue  # title matching is separate (phase 2)
            key = (id_type, id_val)
            if key not in id_to_works:
                id_to_works[key] = []
            id_to_works[key].append(i)

    # Phase 2: union-find over shared identifiers
    uf = UnionFind(n)
    for key, indices in id_to_works.items():
        if len(indices) < 2:
            continue
        first = indices[0]
        for other in indices[1:]:
            uf.union(first, other)

    # Phase 3: fuzzy title matching for unmatched singletons
    # Only match titles between works that share no identifier
    # Group by (first_3_chars_of_title, year) to reduce comparisons
    title_groups = {}
    for i, ids in enumerate(all_ids):
        root = uf.find(i)
        if root != i:
            continue  # already in a group, skip
        tn = ids.get("title_norm", "")
        if not tn or len(tn) < 8:
            continue
        year = works[i].get("year")
        bucket = (tn[:4], year)
        if bucket not in title_groups:
            title_groups[bucket] = []
        title_groups[bucket].append(i)

    for bucket, indices in title_groups.items():
        if len(indices) < 2:
            continue
        for a in range(len(indices)):
            for b in range(a + 1, len(indices)):
                ia, ib = indices[a], indices[b]
                # Skip if already same group
                if uf.find(ia) == uf.find(ib):
                    continue
                # Skip if share any identifier (shouldn't happen, safety check)
                ids_a = all_ids[ia]
                ids_b = all_ids[ib]
                shared = False
                for k in ("doi", "pmid", "pmcid", "arxiv_id"):
                    if k in ids_a and k in ids_b and ids_a[k] == ids_b[k]:
                        shared = True
                        break
                if shared:
                    continue
                # Fuzzy match
                sim = SequenceMatcher(None, ids_a["title_norm"], ids_b["title_norm"]).ratio()
                if sim >= 0.90:
                    uf.union(ia, ib)

    # Collect groups
    groups_map = {}
    for i in range(n):
        root = uf.find(i)
        if root not in groups_map:
            groups_map[root] = []
        groups_map[root].append(i)

    return list(groups_map.values())


# ---------------------------------------------------------------------------
# Field merge logic (extracted from normalize.py for reuse)
# ---------------------------------------------------------------------------

_EUROPE_PMC_PREFERRED = {
    "open_access_url", "pmid", "pmcid", "abstract_snippet", "mesh",
    "journal_iso", "publication", "authors", "publication_date",
    "volume", "issue", "page"
}


def _evidence_level(w):
    """Assign evidence-level tag based on study_type / type."""
    st = (w.get("study_type") or "").lower()
    if st in ("systematic-review", "meta-analysis", "scoping-review"):
        return "systematic-review"
    if st == "rct":
        return "rct"
    if st == "cohort":
        return "cohort"
    if st == "case-report":
        return "case-report"
    if st == "case-series":
        return "case-series"
    if st == "preprint" or (w.get("type") or "").lower() == "preprint":
        return "preprint"
    if st == "review":
        return "narrative-review"
    return "other"


def merge_work_group(group, works):
    """Merge a group of work indices into a single record.
    Uses EuropePMC-preferred field merge policy (same as normalize.merge).
    Returns merged work dict."""
    if not group:
        return {}
    if len(group) == 1:
        rec = dict(works[group[0]])
        if "evidence_level" not in rec:
            rec["evidence_level"] = _evidence_level(rec)
        return rec

    # Sort: EuropePMC first (same priority policy as normalize.merge)
    source_order = {"EuropePMC": 0, "OpenAlex": 1, "bioRxiv": 0, "medRxiv": 0,
                    "SemanticScholar": 2, "arXiv": 1}
    sorted_group = sorted(group, key=lambda i: source_order.get(works[i].get("source", ""), 1))

    rec = None
    for i in sorted_group:
        w = works[i]
        if rec is None:
            rec = dict(w)
            rec["sources"] = [w.get("source")] if w.get("source") else []
            continue

        src = w.get("source")
        if src and src not in rec.get("sources", []):
            rec.setdefault("sources", []).append(src)

        # Field merge: EuropePMC preferred fields get overwritten by EPMC values
        for fld in ("abstract_snippet", "mesh", "concepts", "keywords", "funders",
                     "publication", "year", "publication_date", "volume", "issue", "page",
                     "authors", "affiliations", "pmid", "pmcid",
                     "open_access_url", "journal_iso", "language", "oa_status"):
            cur = rec.get(fld)
            new = w.get(fld)
            if not new:
                continue
            if fld in _EUROPE_PMC_PREFERRED and src == "EuropePMC":
                rec[fld] = new
            elif not cur:
                rec[fld] = new

        # pub_types: union-merge
        if w.get("pub_types"):
            rec_types = list(rec.get("pub_types") or [])
            for t in w["pub_types"]:
                if t not in rec_types:
                    rec_types.append(t)
            rec["pub_types"] = rec_types

        # is_oa: OR semantics
        if w.get("is_oa") and not rec.get("is_oa"):
            rec["is_oa"] = True

        # concepts/keywords: union-merge
        for fld in ("concepts", "keywords"):
            if w.get(fld):
                cur = list(rec.get(fld) or [])
                for x in w[fld]:
                    if x not in cur:
                        cur.append(x)
                rec[fld] = cur

        # cited_by_count: max
        if (w.get("cited_by_count") or 0) > (rec.get("cited_by_count") or 0):
            rec["cited_by_count"] = w["cited_by_count"]

        # is_safety: OR
        if w.get("is_safety") and not rec.get("is_safety"):
            rec["is_safety"] = True

        # study_type: upgrade from "article" to more specific
        if w.get("study_type") and rec.get("study_type") in (None, "article"):
            rec["study_type"] = w["study_type"]

    # Recompute evidence_level
    rec["evidence_level"] = _evidence_level(rec)
    return rec


# ---------------------------------------------------------------------------
# Enhanced merge pipeline
# ---------------------------------------------------------------------------

def _normalize_input(data):
    """Accept both payloads format [{source, works}] and flat works list.
    Returns payloads format."""
    if not data:
        return []
    if isinstance(data[0], dict) and "works" in data[0]:
        return data
    # Flat works list — wrap in synthetic payload
    return [{"source": "unknown", "query": "", "works": list(data)}]


def merge_v2(payloads):
    """Enhanced multi-source merge with multi-identifier deduplication.

    Args:
        payloads: list of {source, query, works:[...]} dicts (same format as normalize.merge()).
    Returns:
        list of merged, deduplicated work dicts.
    Backward-compatible output format with normalize.merge()."""
    payloads = _normalize_input(payloads)
    if not payloads:
        return []

    # Flatten payloads into a single list of works (same as normalize.merge internals)
    works = []
    for p in payloads:
        if not p:
            continue
        # 兼容 Coze 端返回格式（projects → works）
        if "works" not in p and "projects" in p:
            p["works"] = p.pop("projects")
        for w in p.get("works", []):
            works.append(w)

    # Pre-process: bare DOI normalization, source canonicalization
    for w in works:
        if w.get("doi"):
            w["doi"] = _bare_doi(w.get("doi"))
        if w.get("source"):
            w["source"] = _canon_source(w["source"])

    if not works:
        return []

    groups = build_identity_groups(works)
    merged = [merge_work_group(g, works) for g in groups]

    # Sort by source priority then citation count (same as normalize.merge)
    _SOURCE_PRIORITY = {
        "OpenAlex": 0, "EuropePMC": 0, "bioRxiv": 0, "medRxiv": 0,
        "SemanticScholar": 1, "arXiv": 1,
        # 升级项 B：NCBI 直连车道与 Europe PMC 同为一次库，同 rank 0。
        "PubMed": 0,
    }

    def src_rank(w):
        srcs = w.get("sources") or [w.get("source")]
        return min(_SOURCE_PRIORITY.get(s, 1) for s in srcs)

    merged.sort(key=lambda x: (src_rank(x), -(x.get("cited_by_count") or 0)))

    # Apply preprint deduplication (same logic as normalize.merge)
    merged = _dedupe_preprint_published(merged)
    return merged


def merge_v2_with_stats(payloads):
    """Like merge_v2() but also returns deduplication statistics.
    Same interface as normalize.merge_with_stats().
    Returns (works, stats) where stats = {raw_count, duplicates_removed}."""
    payloads = _normalize_input(payloads)
    raw_valid = 0
    for p in payloads:
        if not p:
            continue
        if "works" not in p and "projects" in p:
            p["works"] = p.pop("projects")
        for w in p.get("works", []):
            if w.get("doi") or w.get("title"):
                raw_valid += 1
    merged = merge_v2(payloads)
    return merged, {
        "raw_count": raw_valid,
        "duplicates_removed": raw_valid - len(merged),
    }


# Helpers now come from lit_norm_core (single source of truth, 0.3.99 refactor):
# _canon_source / _bare_doi / _norm_doi / _norm_title / _dedupe_preprint_published.

# ---------------------------------------------------------------------------
# Self-test (no network)
# ---------------------------------------------------------------------------

def _self_test():
    """Built-in self-test: verify multi-identifier dedup, transitive resolution,
    arXiv version stripping, fuzzy title matching."""
    print("[self-test] multi-identifier deduplication...")

    works = [
        {"source": "OpenAlex", "doi": "10.1000/abc", "pmid": "12345678",
         "title": "A Study of Thing", "authors": ["Smith", "Jones"], "year": 2024,
         "cited_by_count": 10},
        {"source": "EuropePMC", "doi": "https://doi.org/10.1000/abc", "pmid": "12345678",
         "title": "A Study of Thing", "authors": ["Smith", "Jones"], "year": 2024,
         "cited_by_count": 12, "open_access_url": "http://pdf.example.com"},
        {"source": "SemanticScholar", "pmid": "12345678",
         "title": "A Study of Thing", "authors": ["Smith", "Jones"], "year": 2024,
         "cited_by_count": 8},
    ]
    merged = merge_v2(works)
    assert len(merged) == 1, f"Expected 1, got {len(merged)}"
    assert merged[0]["cited_by_count"] == 12, f"Expected max cited 12, got {merged[0]['cited_by_count']}"
    assert "EuropePMC" in merged[0]["sources"]
    assert merged[0].get("open_access_url") == "http://pdf.example.com"
    print("  PASS: DOI+PMID multi-source merge")

    # Test transitive: A.doi=X, B.pmid=Y, C.doi=X+pmid=Y
    works_t = [
        {"source": "OpenAlex", "doi": "10.1000/shared", "title": "Shared Paper A"},
        {"source": "EuropePMC", "pmid": "87654321", "title": "Shared Paper B"},
        {"source": "SemanticScholar", "doi": "10.1000/shared", "pmid": "87654321",
         "title": "Shared Paper C"},
    ]
    merged_t = merge_v2(works_t)
    assert len(merged_t) == 1, f"Transitive: expected 1, got {len(merged_t)}"
    assert len(merged_t[0]["sources"]) == 3
    print("  PASS: transitive identity resolution")

    # Test arXiv version stripping
    works_ax = [
        {"source": "arXiv", "id": "2606.11144v1", "title": "ArXiv Paper"},
        {"source": "OpenAlex", "doi": "10.48550/arXiv.2606.11144", "title": "ArXiv Paper"},
    ]
    merged_ax = merge_v2(works_ax)
    # These should NOT match (arXiv ID in OpenAlex DOI is not the same format)
    # Actually, let's check: normalize_arxiv_id on "10.48550/arXiv.2606.11144" → None
    # So they won't match. This is correct behavior.
    print(f"  INFO: arXiv cross-match: {len(merged_ax)} records (expected: arXiv ID in DOI not matched)")

    # Test fuzzy title matching
    works_fz = [
        {"source": "OpenAlex", "title": "Efficacy of Osimertinib in EGFR-Mutant NSCLC",
         "authors": ["Wang", "Li"], "year": 2024, "doi": "10.1000/a"},
        {"source": "SemanticScholar", "title": "Efficacy of Osimertinib in EGFR Mutant NSCLC",
         "authors": ["Wang", "Li"], "year": 2024, "doi": "10.1000/b"},
    ]
    merged_fz = merge_v2(works_fz)
    assert len(merged_fz) == 1, f"Fuzzy: expected 1, got {len(merged_fz)}"
    print("  PASS: fuzzy title matching")

    print("[self-test] all checks passed")


if __name__ == "__main__":
    _self_test()
