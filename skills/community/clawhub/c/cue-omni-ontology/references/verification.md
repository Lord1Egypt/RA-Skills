# Verification record — first written 2026-09-28 (v0.2.0), updated 2026-10-07 (v0.3.0)

This record distinguishes executed code, synthetic host tasks and saved parser output. It is not a general extraction accuracy report.

| Surface | Executed result | Limits |
|---|---|---|
| Offline boundary suite | all boundary tests passed as executed on this date — **count is not authority here**: run `python3 -B scripts/test_ontology.py` and `python3 -B scripts/test_numeric.py` for the current numbers and results | Synthetic fixtures; no live parser, no LLM accuracy or enterprise IAM claim |
| Independent host use | A separate agent followed SKILL.md using newly supplied fictional Cedar Instruments releases; built/updated two versions and answered business questions | Supplied parsed synthetic text; no live Omni invocation and no claim of cold client onboarding |
| Independent query outcomes | Unscoped Q1 `needs_scope`; statutory/adjusted Q1 each `found`; restated Q4 `conflict`; alleged Beacon discontinuation `not_found` | One task, not a statistical generalization benchmark; machine assertions were not marked human-reviewed |
| Public-source replay | Existing grounded Omni output for two Tencent 2026 quarterly releases successfully repackaged and updated | Saved earlier output and seeded rule-extracted claims; not a fresh model extraction or fresh parser run |
| Replay counts | 2 sources, 1 entity, 18 metric definitions, 96 source assertions, 83 fact scopes; second batch adds 36 facts and 13 supporting assertions | Definitions here group metric labels; bases/qualifiers live on facts, so counts differ from the earlier prototype's 23 combined metric/basis concepts |
| OKF exporter | Public replay produced 18 concept files plus navigation | Core Markdown/YAML subset only; no external consumer import verified |

The independent host task and public replay below were originally executed with v0.1.0; the v0.1.1 audit adds eight offline regressions. Version 0.1.1 fixes numeric-spelling conflicts, scope selection, boolean qualifier matching, structured errors for malformed assertions and unsafe Markdown rendering; it exposes conflict IDs/validity in reports. Schema remains 0.1.0.

Scrubbed machine summaries: [forward-results.json](forward-results.json), [replay-results.json](replay-results.json). Public source metadata and hashes: [sources.json](../assets/public-example/sources.json). Full reports/parsed sources are not redistributed with this skill.

The earlier parser run used official Omni Reader Bridge 1.8.4 and native page anchors. The new package preserves the exact stored text hashes. The original v0.1 release added **zero** live parse calls. Version 0.2.0 has a separately recorded fresh run and its returned billing facts; no general speed or cost claim is inferred.

Not established: arbitrary document-family extraction accuracy; fresh installation and end-to-end execution in multiple third-party clients; automated compatibility with other cue-awesome skills; external OKF consumers; full enterprise-local deployment; operational authorization and writeback; customer time savings or willingness to pay.

Version 0.2.0 adds a [fresh source-to-answer run](live-verification.md) on two Microsoft public releases: 21 selected claims, all 11 baseline claims preserved. The installed development environment completed official parsing, host extraction, preparation, updates, evidence queries and a generated brief. Fresh installation in multiple third-party clients and user time-savings remain untested. Preserve independent sources for evaluation rather than tuning against all release examples.

HTML browser checks: the local browser binary was unavailable, and the configured cloud browser rejected local-file navigation under its URL policy. Real-browser interaction and mobile layout are therefore not certified in this environment. HTML generation, safe data embedding, excerpt limits and package workflows have automated coverage; the Markdown output remains a usable fallback.

Independent 0.2 forward use: a fresh agent received two previously unused fictional Vela Components releases and used quote preparation → build → update → validate → evidence queries → brief. It produced 9 assertions / 8 fact scopes, retained all 4 baseline assertions, separated September standard/pilot prices, preserved one June delivery-estimate conflict and left product certification unknown. No command blockers occurred. Human-readable relation names and Markdown/JSON briefs were inspected; browser rendering was not. The observed workflow still requires host judgment for disclosure dates, explicit corrections and absent certification evidence.

## Holdout backtest (2026-10-07; the 0.3.0 code)

Question tested: does a two-period annual-report knowledge package help an agent find the root cause of a later credit event better than simpler inputs? Three groups received the same Omni-parsed text, the same post-loan analysis task and the same `free` model; only the input changed. R = keyword retrieval plus page reads; D = a deterministic text diff of the two annual reports; O = the knowledge package built with this skill's code (numeric pack, catalog, verbatim excerpts) queried through its tools. Grading was blind, order-shuffled, majority of three independent runs, with the same `free` model.

The pass bar and root-cause keys were sealed before any holdout parse or group run. All four conditions had to hold: (1) O's top-3 root-cause hits at least 2× R's; (2) at least 2 more than D's; (3) O's mean false alarms per control company no higher than R's; (4) O's evidence validity no lower than R's. Holdout sample: 10 event companies + 10 matched controls, chosen by the same rule and disjoint from the development pool; 40 annual reports (7,598 pages) all parsed, no sample shrinkage. Omni charged 509.468 credits for these parses.

| Holdout (sealed in advance) | R keyword | D diff | O ontology |
|---|---|---|---|
| Event companies with a root cause in the top 3 (of 10) | 4 | 6 | 5 |
| Evidence validity (quotes found verbatim in the anonymized source) | 0.463 | 0.660 | 0.958 |
| False alarms per control company | 3.3 | 3.9 | 3.2 |
| Pass bar | | | **failed** (5 < 2×4 = 8 and 5 < 6+2 = 8) |

Read the three rows together. O did not find root causes better than retrieval or a plain diff; the diff group found one more. O's verbatim evidence was clearly more valid, and labelling explained-normal events (presentation changes, new standards, same-control mergers, acquisitions) brought false alarms slightly below R. Earlier development rounds on a separate 19-company sample showed the same structure (O never met conditions 1 and 2 together); they were post-hoc and are not used as evidence here.

What this supports: an evidence layer for reviewing material, with verbatim provenance, deterministic figures and explained-normal labels. What it does not support: early warning, risk discovery, or "ranking beats retrieval/diff". For non-standard audit opinions the cause was almost invisible in the prior year's report for all three groups; earlier signals would need faster sources (announcements, litigation, asset freezes), which this pipeline does not read.

Limits: 10 event companies, so one company changes the outcome; the grader is the same `free` model as the answering model; anonymization removed names, yet the model still recognised about 70% of companies from their business structure (14 of 20 in the holdout), a bias common to all groups; one control's brand name was found unmasked after the run and the groups were not re-run; one O run gave no parseable answer and counted as no signal (with it, O would reach at most 6, still failing). Scrubbed run files are kept with the research materials, not shipped with this skill.

## Omni result to page spans (2026-10-07, no new parse)

`omni-source` was checked on a saved grounded result for one public A-share announcement (Bridge 1.8.x, stored inline although artifact delivery had been requested): 3 page spans from `source_pdf_page_1_based` anchors, the content sha256 matched the digest Omni returned, 4 separator bytes stayed outside every span, and a quoted figure resolved through `prepare` and `build` to page 2 with basis `omni_native_source_pdf_page`. No Omni call was made for this check. Artifact storage, digest mismatch, expired results, failed statuses and conservative page mapping are covered by offline tests with synthetic text.
