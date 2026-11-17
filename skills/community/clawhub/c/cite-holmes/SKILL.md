---
name: cite-holmes
version: 6.6.0
author: DoctorQ Lab
license: MIT
description: >-
  Deep research that interrogates its own sources (Verified Deep Research):
  literature discovery (topic in, verified reference list out), then calibrates scope first (3-5 sharp questions), then searches iteratively and
  machine-verifies every citation. Also a standalone citation checker: paste
  any reference list and it runs full citation verification (it will verify
  citations before you cite) against official registries —
  hallucinated references, fabricated DOIs, fake PMIDs, arXiv IDs, stitched
  fakes, retracted papers; a fact check for your bibliography. Five verdicts;
  unverified references never masquerade as real (AI hallucination detection).
  Medical mode (Cochrane/BMJ/ChiCTR/NMPA/CDC/NICE presets, PMID check) and
  bibliography export (BibTeX/GB·T 7714-2025/RIS/CSV + JSON workpaper) built
  in. Skip when: translation, polishing, rewriting, de-AI-flavoring — anything
  not about citation authenticity (mis-triggers are harmless; state your real
  intent). Trigger matching is semantic, not exact.
when_to_use: >-
  Use when the user says "deep research", "look into", "investigate",
  "compare A vs B", "fact check", "verify this claim", "is it true that...",
  "check these references", "are these citations real", wants a research
  report with sources, a literature review, a medical evidence lookup, or
  wants references verified before submission — even if they never say the
  word "research".
---

# cite-holmes (Cite Holmes): deep research with citation verification

One line: **a question goes in — a verified report comes out.**

Three differences from a plain "search and summarize":

1. **Calibrate before working** — sharp questions first; the costliest waste is researching the wrong question.
2. **Conclusions carry evidence grades** — 🟢 two independent sources agree / 🟡 single authority / 🔴 contested.
3. **Every citation is checked** — mechanical layer (reachability, authority, completeness, dedup) + semantic layer (does the source support the claim?); unverified references never masquerade as real.

---
## ⛔ Iron rules (zero exceptions)

1. **Never fabricate**: citations must come from pages actually fetched this
   session. Re-search rather than write URLs from memory.
2. **Never pretend**: unchecked references are marked `unverified`; fetch
   failures are `unreachable` (≠ nonexistent — flagged for human review).
3. **Don't hide conflicts**: when sources disagree, present the disagreement,
   mark 🔴, show each side's evidence.
4. **Budgeted search**: QUICK ≤6 searches, FULL ≤15. Out of budget → state the
   gaps honestly instead of forcing conclusions.
5. **Calibrate before searching** (FULL mode): scope / timeframe / audience /
   output format must be locked first.

---
## 30-second quickstart

```bash
# 1. references as JSON (title/url/source/year) — or a Zotero .bib
# 2. verify:
python scripts/verify_refs.py --refs refs.json --out report.md
# 3. read report.md — CiteScore + pre-submission conclusion at the top.
# Paper? add --export bibtex.  Medical? add --profile medical.
# Literature hunt? --discover "topic" --review-kit (verified at birth, kit out).
# Already verified once? add --grill report.json for the review checklist.
```

---
## Step 0: mode selection

| Mode | Fits | Calibration | Budget | Output |
|---|---|---|---|---|
| **QUICK** | Single fact-check: "is this claim true", "when was X released" | skipped | ≤6 | short report |
| **FULL** | Open research: "state of X", "A vs B", "do a survey" | mandatory | ≤15 | full report |

One verifiable fact → QUICK. Synthesis or trade-offs → FULL. Unsure → FULL.
Pre-submission final check skips this: `--preset submission` (one flag =
strict + GB·T/BibTeX/CSV exports).

## Five-phase workflow

### 1. CALIBRATE (FULL only)

Ask 3–5 high-leverage questions at once: scope, timeframe, audience/depth,
output format, decision context. Never re-ask what the user provided; if they
decline, proceed with stated defaults. Three rules: order questions by dependency; **each carries a recommended answer phrased so "yes" accepts it**;
facts you can look up yourself never become questions — decisions stay with
the user.

### 2. PLAN

Show a short plan: 3–7 sub-questions, source priority (primary/official >
major media > community/blog as leads only), budget.

### 3. SEARCH (iterative)

Read `references/search-strategies.md` first. Each round targets one
sub-question; evolve queries with discovered terms; search both English and
Chinese when the topic spans both; fetch full text of the 2–5 most valuable
sources (never conclude from snippets); verify key numbers on the original
page before quoting.

### 4. VERIFY (the heart of this skill)

Register every reference in `research_refs.json` (schema in
`references/report-template.md`), then run:

```bash
python scripts/verify_refs.py --refs research_refs.json --out verify_report.md
# Zotero/EndNote .bib feeds in directly:
python scripts/verify_refs.py --refs bibliography.bib --out report.md
# Big batch? Self-check first (zero outbound by default):
python scripts/verify_refs.py --doctor --net
```

Five verdicts: `verified` / `partial` / `unreachable` (needs_human_check) /
`invalid` / `unverified`. Every identifier (`url`/`doi`/`pmid`/`arxiv`) is
cross-checked against its official registry, so fabricated IDs are judged
`invalid` — never silently `unreachable`. Every report opens with a **BLUF
dual-reader header** + **CiteScore** (0-100 + A-D grade) + a one-line
**pre-submission conclusion**.

#### Mechanical layer (the script)

| Capability | Boundary |
|---|---|
| Registry consistency (title/year/journal/author) | 12 machine-readable error codes; thresholds 0.50/0.82 |
| Clone-pair detection | same title under different DOIs / one DOI with different titles — paired leads, never verdicts |
| Cross-lingual title bridging | six writing-system families (Latin/Cyrillic/Greek/Han/Kana/Hangul); hit→`verified`, miss→`partial`; language difference is never fabrication evidence; families outside the six (Arabic/Hebrew/Thai…) do NOT trigger the guard yet — attach an English/romanized title |
| Bibliography profiling | list-level batch-fabrication fingerprints — review leads, never verdicts |
| Preprint upgrade hints | arXiv-only refs since published get the formal DOI annotated |
| Retraction checks | Crossref online, or offline via `--retraction-cache`; notice granularity: retraction / partial retraction / withdrawal → human hand-off, Expression of Concern → caps `verified` at `partial`, correction → note only; a failed check is flagged, never reported as clean |
| Identifier-less references (Vancouver) | PubMed title reverse-lookup → `verified` with PMID anchor back-filled; works from 2 content words; a transport failure is marked `network_error` and never counted as a miss |
| GB/T 7714 Chinese medical references | `[1]`-style bracket numbering and title-first entries parse; inline `PMID:`/`DOI:` anchors are extracted and verified; when no ID exists, journal+year+volume(issue):page uniquely located in PubMed upgrades to `verified` (Single-Citation-Matcher semantics, language-independent — a Chinese claimed title against an English registered title never counts as fabrication) |
| Chinese scholarly registries | wanfangdata / CNKI / yiigle classified at journal tier |
| Non-MEDLINE journals (identifier-less) | OpenAlex anchor search → DOI resolution: the aggregator is only an index, the verdict evidence comes entirely from the DOI registry (retraction checks still run on the anchored DOI) |
| Retraction checks at scale | `tools/build_retraction_cache.py` builds a local Retraction Watch index from the official daily-updated dump — `--retraction-cache` then verifies offline with notice granularity |
| Literature discovery | `--discover "topic"` searches PubMed + OpenAlex and verifies every hit at birth - a verified reference list out, GB/T 7714 / BibTeX export ready; `--discover-since 2020` filters by year; `--discover-sort cited|newest` orders by citations or date; `--demo` runs the bundled 8-reference sample (3 planted fakes) for a zero-setup tour |
| Review kit (literature review) | `--review-kit` turns any verified batch into a review-ready file: comparison table (verified first, citations-per-paper shown) + annotated bibliography + paste-ready GB/T 7714 list — with `--discover` it is a one-command literature workflow; verdicts stay verdicts (partial is never "verified") |
| Scholarly usage & open access | Semantic Scholar citing contexts show usage distribution (methodology/background/result) + one sample quote; a heuristic divergence signal flags batches where sampled contexts contain contrastive/critical phrasing (advisory banner, never a verdict); `--mailto` also queries Unpaywall for open-access status (X/N free-to-read summary, per-entry license) — enhancement signals only, never a verdict; absent data renders nothing |
| Deep-research controls | `--plan plan.json --plan-out plan.md` validates & renders an editable research-plan artifact (collaborative planning); `--preset deep` raises the discovery ceiling (25) and timeout floor (20s); `--source-policy journal_only,deny-domain=x.com` curates discovery hits and annotates policy hits at verify (annotation only, never a verdict); `--trace trace.md` appends a per-round audit log; `--research-profile p.json` injects persistent preference defaults (explicit flags win); `--require-version` strict tier: multi-revision arXiv citations without a pinned version degrade to partial for human confirmation (default off) |
| EB/OL references (guidelines, labels) | URLs in [EB/OL]-style entries are extracted (when no stronger identifier exists) and routed through reachability + source-tier checks; when such a reference lands partial, the page <title> is cross-checked against the claim and a match is recorded as existence evidence in the workpaper |
| Reference-list completeness | `--check-document` audits orphans (listed but never cited — a writing-integrity advisory, never a verdict) and coverage; one-file mode: pass the document alone and the reference section is auto-extracted; `--audit-mode` renders an editor-facing audit report (P0 fabrication suspects / P1 high-risk leads / P2 review items + action checklist); `--refs-dir` batch-loads a local library folder into one batch; `--next-round report.json` regenerates a retry skeleton from unresolved entries (invalid never recycled); `--check-paper doc.md` runs the whole pre-submission audit package in one command (verify + audit tiers + GB/T/BibTeX export + INDEX with a mechanical READY/NOT-READY verdict and explicit human-review boundary) |
| Wayback archive links | attached to dead links automatically |
| Completeness scoring | how many export fields the registry CSL can back-fill |
| Speed | 20-ref mixed list ≈18s at `--workers 4` (default), ≈7s cache-warm, ≈47s serial — measured table: `references/verification-details.md` |
| Weak network | `--proxy` / `--cn` / `--preflight`; auto degraded-network mode after 3+ registry transport failures |

#### Semantic layer (the model)

Decompose each cited claim into atomic
claim-triplets (subject–relation–object) and verify each against the source;
register the verdict structurally (`"semantic": {"claim", "support", "quote",
"note"}`) — it becomes auditable workpaper; `not_in_source`/`contradicted` cap
the mechanical verdict at `partial` — a source that exists is not a source
that agrees.

#### Task → flag

| Task | Flags |
|---|---|
| Medical topics | `--easy` · `--profile medical` |
| Literature review build-out | `--discover "topic" --review-kit` (table + annotated bibliography + GB/T) |
| Share / archive | `--format html` |
| Export | `--export bibtex,gbt7714,ris,csv,auditjson` |
| CI | `--strict` · `--offline` |
| Polite pacing | `--mailto you@lab.edu` |
| API keys | `--openalex-key` / `--s2-key` / `--ncbi-key` |
| Weak network | `--proxy` · `--cn` · `--preflight` · `--timeout` |
| Cache | `--no-cache` / `--refresh-cache` / `--cache-ttl` |
| Self-check | `--doctor` (add `--net`) |
| Pre-submission check | `--preset submission` |
| Explain one verdict | `--explain N` |
| Pre-submission grill | `--grill report.json` / `--reviewer` (same checklist embedded into the report) |
| External judging | `--judge-url` / `--nli-url` / `--fast-judge-url` (notes only) |
| MCP server | `mcp/server.py` — `verify_references` / `discover_references` / `check_document` / `build_review_kit` / `explain_verdict` |

### 5. SYNTHESIZE

Follow `references/report-template.md`: executive summary first; every key
conclusion carries a confidence grade + citation ids; the reference table
carries verdicts; `unverified/unreachable` live only in the "human review"
section; finish with a **finding ledger** — revisit the plan's question
list and mark each as answered / partially answered / unresolved (with the
budget ledger: rounds used, remaining), then gaps, disagreements, follow-up
questions.

---

## Files

| File | When |
|---|---|
| `scripts/verify_refs.py` · `tools/` | engine (pure stdlib); `run_eval.py` held-out eval runner & gate · `build_holdout.py` holdout build pipeline · `selfcheck.py` offline install check (incl. shipped test subset) · `netcheck.py` live-net stability check · `run_tests.sh` suite entry (time budget + `--shipped`/`--held-out`) |
| `references/GLOSSARY.md` | canonical terms (five verdicts / signals / error codes) with Avoid lists |
| `references/out-of-scope.md` | explicit non-goals + honest limits, each with a reason |
| `references/security.md` | full security & behavior declaration |
| `docs/adr/` · `docs/benchmark.md` · `docs/onboarding.md` | decisions; eval methodology; 5-minute onboarding path |
| `mcp/server.py` | optional MCP server (same engine) |
| `references/verification-details.md` | full option semantics, thresholds |
| `references/anti-patterns.md` | misuse catalog, each with an alternative |
| `references/faq.md` | common questions |
| `references/medical-mode.md` | read before medical/clinical work |
| `examples/demo_refs.json` | 8 refs, 3 planted fabrications |
| `examples/review-kit-sample.md` | real-data review-kit output (discover → verify → kit) |

## ⚠️ Common mistakes

See `references/anti-patterns.md` (16 entries, each with the right way
instead). The two that matter most: never treat `verified` as "the content is
correct" — that is the semantic layer's job; never treat `unreachable` as
"fake" — retry via `--cn`/`--proxy` first.

## Security, honest limits, FAQ

- Security & behavior declaration: single-run; HTTPS-only to official academic
  registries (doi.org / api.crossref.org / eutils.ncbi.nlm.nih.gov /
  export.arxiv.org / api.openalex.org / api.semanticscholar.org / archive.org /
  pubmed.ncbi.nlm.nih.gov) **and the source URLs you submit**; zero telemetry.
  Full text: `references/security.md`
- Honest limits & explicit non-goals: `references/out-of-scope.md`
- Common questions: `references/faq.md`
- No web tools? Say honestly that only "user-supplied material + mechanical
  verification" is possible — never pretend to search.
