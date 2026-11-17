# Evidence-Synthesis Evaluation Benchmarks (TrialMind / TrialReviewBench / MedReview)

> Sources: ① TrialMind + TrialReviewBench — *npj Digital Medicine* (2025), doi:10.1038/s41746-025-01840-7 (100 systematic reviews / 2,220 clinical studies); ② MedReview — *npj Digital Medicine* (2024), doi:10.1038/s41746-024-01239-w (8,161 Cochrane result–conclusion pairs); ③ TrialPanorama — *npj Digital Medicine* (2026), doi:10.1038/s41746-026-02933-7 (8 tasks, registry + literature corpus).
> Intel source: WeChat article "Those who explore AI in clinical trials" (Lin Shaonan GCP, 2026-10-08).
> Maps to ct-literature improvement: v1.4.0 (2026-10-08; landed from WeChat intel weekly report wechat_intel_2026-10-08.md).
> Scope: **evaluation design blueprint** for regression-testing and recall assessment of this skill's retrieval → screening → extraction chain; no change to engine behavior.

## 1. Why these benchmarks matter for ct-literature

TrialMind/TrialReviewBench is the first large-scale, human-verified benchmark covering the
**full evidence-synthesis chain** this skill automates: literature search → screening →
study-data extraction. Its task decomposition gives ct-literature a ready-made, citable
evaluation framework instead of ad-hoc spot checks:

| Stage | Benchmark task | ct-literature analogue |
|-------|----------------|------------------------|
| Search / retrieval | Given a review topic, retrieve the included-study set | `ct_literature.py --topic` multi-source search recall |
| Screening | Include/exclude decisions on candidate records | Safety / review-type filters (`--safety`, `--review-type`) |
| Extraction | PICO + study-characteristics extraction from full text | Record normalization (`source/id/title/authors/year/doi/mesh/…`) + Docling PDF parsing |

## 2. Key benchmark facts (for citation and metric design)

- **TrialReviewBench**: 100 systematic reviews, 2,220 clinical studies with human-verified
  screening labels and extraction targets — usable as a held-out recall test set for
  multi-source search (OpenAlex + Europe PMC + preprints).
- **MedReview**: 8,161 Cochrane outcome–conclusion pairs — evaluates whether generated
  narrative conclusions are faithful to the reported results (faithfulness metric design).
- **TrialPanorama** (2026): 8 tasks across evidence synthesis and trial design, integrating
  registry and literature records — registry + literature **dual-source** coverage matches
  the `ct-registry → ct-literature` pipeline pairing in this library.

## 3. Suggested evaluation protocol for ct-literature regression

1. **Recall gate**: sample topics from TrialReviewBench reviews; run the multi-source
   pipeline; measure included-study recall@k against human-verified gold sets. Gate:
   regression run must not drop recall vs. previous engine version.
2. **Dedup precision**: compare DOI/id de-duplication output against gold duplicates
   (merge correctness, no lost records).
3. **Faithfulness spot-check**: for any generated summary text, verify each claim traces
   to a retrieved record field (no fabrication) — aligns with the library's
   "no unverifiable assertions" hard rule (SKILL.md §Traceability).
4. **Report format**: record recall/precision/faithfulness per run in `out/` with engine
   version + date, so cross-version comparisons are auditable.

## 4. Boundaries

- The benchmark datasets are external research artifacts (not shipped with this skill);
  using them requires downloading from the publishers' linked sources under their licenses.
- Blueprint only — v1.4.0 changes no engine behavior, adds no dependency, performs no network
  call beyond the skill's existing optional search paths.
