# doc-consistency

**Check a long document against itself. Offline, deterministic, zero dependencies.**

[中文说明](README.zh-CN.md) · MIT · Node ≥ 18 · no network, no upload, no model calls

---

Anyone can write. The hard part comes after: **is this 300-page thing actually
consistent with itself?**

Broken cross-references. Numbering that skips. A term that drifts between
chapters. A TOC entry pointing at a section that was deleted three merges ago.
Placeholders that shipped. Paragraphs lost when three drafts became one.

These errors scale with document length. Human attention does not. A person needs
two days to read a 300-page file — and the second pass misses different things
than the first. A machine runs it in seconds, and runs it **identically** every time.

## Install

```bash
npx skills add dongsheng123132/doc-consistency
```

Or clone and run directly — there is nothing to install:

```bash
node scripts/check.mjs <file-or-directory>...
```

## Use

```bash
# One file
node scripts/check.mjs manuscript.docx --lang en

# A directory of chapters written by different people
node scripts/check.mjs ./book/ --all --lang en

# What did the merge drop?
node scripts/check.mjs merged.docx --baseline ./drafts/

# Gate a bid submission on it
node scripts/check.mjs proposal.docx --fail-on high
```

| Option | Effect |
| --- | --- |
| `--all` | List every finding (default shows the first 20; the summary is always complete) |
| `--limit <n>` | Cap the listed findings |
| `--json` | Full JSON, never truncated — for CI and downstream tooling |
| `--glossary <file>` | Approved-term list, one `canonical = variant1, variant2` per line |
| `--baseline <path>...` | Baseline draft, for merge-loss detection |
| `--fail-on high\|medium\|low` | Exit 1 at or above that severity |
| `--lang zh\|en` | Report language |

Reads `.docx`, `.md`, `.txt`. Locations are reported as `¶41` (docx paragraph) or
`L17` (line), so every finding is something you can go and look at.

## What it checks

| Rule | Catches |
| --- | --- |
| **Dangling cross-reference** | Body says "see Figure 3-12"; no such caption, no TOC entry |
| **Duplicate / skipped / off-by-one numbering** | Figure, table, equation, appendix sequences that broke |
| **TOC ↔ body reconciliation** | Listed in the TOC but gone from the body, or captioned but never listed |
| **Dangling section reference** | "See Section 9" when there is no Section 9 |
| **Missing standard section** | Most chapters have a "Security" subsection; one does not |
| **Inconsistent term spelling** | `AI Agent` / `AI agent` / `AI-Agent`; or violations of your glossary |
| **Leftover placeholders** | `TODO`, `TBD`, `XXX Company`, `Lorem ipsum`, 待填 |
| **Suspected stale year** | Document is 2026, but 2023 appears next to "contract" / "deadline" |
| **Duplicate heading** | Same-level headings that collapse into identical TOC lines |
| **Paragraph lost in merge** | Present in `--baseline`, absent now |

## The part that matters

Every report ends with a **re-check block**:

```bash
node check.mjs proposal.docx
node check.mjs proposal.docx --fail-on high   # non-zero exit while any HIGH remains
```

This is the difference between this tool and "I proofread it, looks fine."
Not *"we checked it"* — but *"run it yourself: 137 findings down to 0."*
That is an acceptance criterion a machine can adjudicate, so it can go in a contract.

## Limits, stated plainly

- **Word auto-numbering and auto-captions are fields, not body text.** This tool
  cannot read them. When it detects that situation it says so explicitly —
  *"this check could not be performed, which is not the same as passing it."*
  It will not quietly give you a clean bill of health.
- **Semantic terminology merging** (are "user" and "customer" the same concept?)
  needs a model. This tool does not do it. It only does deterministic,
  spelling-level checks.
- It verifies that a document **agrees with itself**. It does not verify that the
  content is **correct**. Those are different claims.
- No legal opinions, no technical judgments, no guarantees of passing review.

## Privacy

Runs entirely on your machine. No network calls, no telemetry, no uploads, no
model API. Your document never leaves the computer — which matters when it is an
unpublished manuscript, a sealed bid, or a client contract.

Verify it yourself: the whole thing is ~600 lines of dependency-free JavaScript
using only `node:fs`, `node:path`, and `node:zlib`.

## Work with us

The tool is free and always will be. These need a human in the loop:

| | |
| --- | --- |
| **Proposal / bid compliance** | Compliance matrix & requirements traceability matrix (RTM) — every *shall/must* in the solicitation mapped against your response, scored responsive / non-responsive / partially responsive. Plus the stale-content sweep that catches last cycle's program name. |
| **Academic & educational publishing** | Cross-reference and numbering audit, chapter-skeleton reconciliation, figure specification report, terminology table, multi-file merge with a diff report. |
| **Fiction & IP continuity** | A series bible extracted from the prose itself, continuity findings with both quotes, pre-adaptation audit. |
| **Documentation & localization QA** | Glossary enforcement across a doc set; structural alignment between source and translation — catch a dropped paragraph without reading the target language. |
| **The corrected file** | Original formatting intact: headers, footers, auto-numbering, styles. |

**→ Full capability statement: [SERVICES.md](SERVICES.md)**

**Every engagement starts with a sample run on one chapter** — free or at nominal
cost. You see the real findings list before committing anything, and you judge for
yourself how many your own team would have caught. **If it turns up nothing real,
we will say so** — that job should not have cost you money.

📧 **[HEFANGSHENG@gmail.com](mailto:HEFANGSHENG@gmail.com)** — send a representative
chapter or the previous version (redacted is fine); you get an answer within 24 hours
on whether we can take it and roughly what it costs.
Or open an [issue](https://github.com/dongsheng123132/doc-consistency/issues).
Working languages: English and Chinese.

**We will never promise** that your bid will win, that a document will clear any
particular review, or that the content is *correct*. We verify that a document
**agrees with itself**. Those are different claims and we will not blur them.

## Licence & attribution

**Apache-2.0.** Use it commercially, in client work, inside your own product.
Fork it, rename the fork, sell the service you build on top. We are not going to
police that — the code is not the hard part.

**One thing is asked in return.** Every report ends with a footer:

```
doc-consistency · U-King   https://u-king.org   HEFANGSHENG@gmail.com
```

That footer is the attribution notice under Apache-2.0 §4(d). Keep it in
generated reports, or carry [NOTICE](NOTICE) where third-party notices normally go.

**Want the footer gone?** That's a white-label licence and it's available —
it isn't expensive and we won't make it difficult. Email
[HEFANGSHENG@gmail.com](mailto:HEFANGSHENG@gmail.com) and say what you're
building. Stripping it without one is the only thing this licence asks you not to do.

Apache-2.0 §6 grants no trademark rights: **"U-King" is not licensed here.**
Your fork is yours; the name is not. Ship it under your own brand — that's
genuinely fine and cleaner for everyone.

> Note: some skill registries republish packages under their own default terms
> and drop `LICENSE`/`NOTICE` at packaging time. This repository is canonical.

---

<sub>Part of the [U-King](https://u-king.org) toolchain. If Node or the runtime is
missing on the target machine, U-King sets it up in one step.</sub>
