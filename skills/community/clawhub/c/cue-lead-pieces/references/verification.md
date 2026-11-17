# Verification record — cue-lead-pieces (measured with 0.3.x, 2026-10-07)

**Parsing path: the 24-company numbers in this record were measured with local parsing (PyMuPDF / pdftotext for cninfo PDFs, HTML page breaks for EDGAR) — what 0.4.0 calls the `local` fallback. The 0.4.0 primary path, Cue Omni Reader with `ingest`, was measured only on the two filings in "Omni path (0.4.0)" at the end.**

This record lists what was measured, on what, and what it does not show. It is not a general accuracy benchmark. Numbers below are as measured; re-run `python3 scripts/test_skill_regression.py` for the current offline result.

## Setup

- Question (identical for every run, asked in Chinese): "As a credit officer, what are the 5 most important credit-deterioration signals for this company right now? Each must have verbatim source evidence and page."
- Companies: 24 listed companies — 10 A-share in distress, 10 US in distress (some already in Chapter 11), 4 healthy controls (2 A-share, 2 US). Filings from cninfo and SEC EDGAR, last ~12 months; both arms read the same files.
- Arms: A = bare Claude Code; B = the same Claude Code with this skill. One model (thinking off) for every model slot; each run's actual model was checked and runs that could not be checked were voided.
- One run per company per arm for the headline (valid answers: A 19, B 22; 7 voided or missing). 60-minute cap per run; an answer on disk at timeout was scored as is.
- Every quote was scored by the same `cue.py verify`: verbatim (cited page ±1, ignoring whitespace and punctuation), wrong source/page, edited, table restated, not in the source; plus "fabricated numbers" (a number in the quote that appears nowhere in the company's files).

## Results (version before 0.3.0)

| Sample | Arm | Answers | Quotes | Verbatim | Fabricated numbers |
|---|---|---|---|---|---|
| All 24 | A bare | 19 | 421 | 61% | 0 |
| All 24 | B skill | 22 | 443 | 95% | 0 |
| A-share 12 | A / B | 9 / 10 | 194 / 202 | 63% / 94% | 0 / 0 |
| US 12 | A / B | 10 / 12 | 227 / 241 | 59% / 96% | 0 / 0 |
| Healthy 4 | A / B | 2 / 3 | 46 / 45 | 41% / 96% | 0 / 0 |

95% intervals by company bootstrap: A 54%–67% verbatim (so 33%–46% not matching), B 91%–98%. Healthy controls: every claimed signal had source support (A 10/10, B 15/15).

Bare-agent mismatches split as: wrong source/page 7%, edited 16%, table restated 15%, not in the source 2% (shares of all quotes). Five bare-agent quotes (one US company) lost a "$digit" to shell expansion when the agent rewrote its answer file with a shell command; counting those five as matching leaves 38% not matching.

## 0.3.0 speed re-test

The 14 companies whose B runs still timed out after one retry in the run above; same question, filings, host and model; 0.3.0 and the previous version run interleaved at the same time, so endpoint load was shared.

| | 0.3.0 | previous version, same time |
|---|---|---|
| Runs completed / valid answers | 14 / 14 | 14 / 14 |
| 60-minute timeouts | 1 | 4 |
| Median wall time | 42.1 min | 45.4 min |
| Median model turns | 11.5 | 13 |
| Median time to first written answer | 29.1 min | 38.8 min |
| Quotes in final answers | 279 | 265 |
| Final answers verbatim | 100% | 98% |
| Agent draft verbatim before `--fix` | 98% (273/278) | — |
| Fabricated numbers | 0 | 0 |

## Limits

- One host (Claude Code) and one model; no claim for other models or hosts. One run per company per arm.
- The B arm was told to load the skill, which asks for `verify` before answering. The comparison is the same agent with and without this tool and workflow, not model capability.
- Scoring is programmatic: it checks that quotes can be found in the source, not that signals are right. Table checks only test that the numbers are on the same page, not row/column alignment. Fabricated numbers are string matches, so a number that happens to appear elsewhere passes (conservative).
- Sentences swapped in by `--fix` are the nearest original text chosen by the program; no person reviewed whether they still support the original claim.
- The 14-company re-test is the slowest subset, not a sample of all companies.
- Distressed companies were picked from public announcements. Not investment or credit advice.

## Omni path (0.4.0, 2026-10-07)

What was measured: one real grounded parse each of two cninfo PDFs of 600606 (Greenland Holdings), through `@cueai/omni-reader-mcp` 1.8.3, compared page by page with a local PyMuPDF parse of the same PDF. Two files, one company: this shows page alignment and coverage on these files, not a rate.

| | Announcement 2026-10-01 | 2025 annual report |
|---|---|---|
| PDF pages / Omni pages | 3 / 3 | 391 / 391 |
| Charged (Omni billing) | 0.201 credits | 26.197 credits |
| Result storage | inline | artifact (content 989,981 B, grounding 87,371 B) |
| Anchors | `source_pdf_page_1_based`, reliable | same |
| incomplete / truncated pages | none | none |
| Best-matching Omni page = same PDF page | 3/3 | 391/391 |
| Local text found on the same Omni page (median / mean / min) | 1.0 / 0.996 / 0.988 | 0.983 / 0.967 / 0.557 |
| Local numeric tokens on the same Omni page | 30/30 | 16,973/16,984 |
| Omni table rows (GFM, non-separator) | 14 on 2 pages | 5,896 on 277 pages, plus 3 HTML tables on 1 page |

Coverage = share of the local page's character 4-grams (letters, digits, CJK only) found on the Omni page with the same number. The 7 annual-report pages below 0.8 (121, 133, 151, 245, 304, 347, 388) are multi-column tables whose cell order differs between the two parsers; their numbers are present. Before 0.4.0 the local parser stopped at 300 pages, so pages 301–391 existed only in the Omni result.

Mini end-to-end on the Omni-ingested store: 8 quotes copied from the Omni pages, with one wrong page, one edited number and one too-short table fragment planted. `verify`: 5 verbatim, 1 verbatim_elsewhere, 1 not_found, 1 too_short. `verify --fix`: 1 page corrected, 2 dropped, 6/6 verbatim. Checked against the local PDF text, 5 kept quotes sit on the cited page and 1 on the next page (the ±1 rule).

`cue.py omni` against live Omni: one run with `--yes` on the same announcement (Bridge 1.8.3, `result_delivery="artifact"`): completed in about 30 s, 0.201 credits charged (as reported), 3 PDF pages identical to the first run. The small result still came back inline.

Not measured: US EDGAR through Omni (the 8-K attempts failed before parsing and were not billed: `SOURCE_ACCESS_DENIED` for the EDGAR URL, `DETAIL_CAPABILITIES_UNAVAILABLE` for a local file in grounded mode on Bridge 1.8.3, `MIME_MISMATCH` for the inline-XBRL file in text mode), and the 24-company comparison on the Omni path.
