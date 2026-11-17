---
name: cn-inquiry-letter-reply
slug: cue-cn-inquiry-letter-reply
displayName: "Inquiry Letter Reply Checklist (监管问询函)"
summary: "拆一份监管问询函：问题、要求材料、回复要点、回复文件四栏，逐问对答复，没答的点名。"
description: "A-share inquiry letter teardown: split a letter into questions, requested materials, reply points and reply documents, each with a quote and anchor; every question matched to its reply, gaps named. Checking only, never drafting. Triggers: inquiry letter / regulatory inquiry / reply checklist"
version: "0.1.0"
license: MIT
tags: [inquiry-letter, regulatory-inquiry, reply-checklist, disclosure]
---

# Inquiry Letter Reply Checklist (监管问询函)

**What it does**: turns one regulatory inquiry letter into a checklist where **every question is matched to its reply** — what the regulator asked, what materials were requested, what the company answered, and which reply documents are missing.

**It is not** a reply drafter, not a compliance opinion, not a prediction of whether the review will pass.

## 1. Where the letter itself comes from

The exchange's letter is **not available through any public filing channel**. What the public databases hold is the other side: the company's reply announcements, and notices saying a letter was received (which carry no question text).

So this package **does not fetch the letter and does not pretend to**. You paste it in or point at a local file; the package splits and checks.

The reply side *can* be listed automatically: reply announcements, annual and semi-annual reports, and prospectuses in offering scenarios.

## 2. Six sections

| # | Section | Records |
|---|---|---|
| 1 | Question index | one row per question: `- 问题N <topic> 「quote」〔anchor〕[S#]` |
| 2 | Requested materials | what each question asks to be provided, sourced |
| 3 | Reply points | the answer to each question; unanswered ones say `未取到: <what>` |
| 4 | Reply documents | who filed what: company, auditor, sponsor, counsel — `- 主体: <name>｜[S#]` |
| 5 | Gaps | every missing item named; a clean run says `未取到: 无` |
| 6 | Sources | one source line each, with clickable URL and retrieval date |

## 3. Six checks

1. **IL-STRUCT** — header self-labels present; subject and letter lines present; six sections in order; the first three sections each carry at least one finding row; no extra section.
2. **IL-QUOTE** — every product row ends with quote + anchor + `[S#]`; source rows carry a clickable URL and retrieval date; every cited number is registered.
3. **IL-PAIR** (the load-bearing check) — every question in the index has a matching row in reply points, and vice versa. Both directions are judged.
4. **IL-GAP** — a gap written in the body must appear in the gaps section and vice versa; `不适用` / `无此项` / `无需披露` always fire.
5. **IL-MEDIA** — one inquiry usually produces 3–5 filings from the company, the auditor and the sponsor/counsel. If only the company itself is registered and the gaps section does not name the intermediary replies, it fires.
6. **IL-LINE** — no speaking for the company, no conclusions. Quoted text is stripped before judging: a quote is the regulator's wording, not this package's position.

## 4. Four red lines

1. **Never draft the reply.** `本公司将` / `现回复如下` / `特此答复` fire once quotes are stripped.
2. **Never conclude.** `不构成重大影响` / `不存在问题` / `风险可控` / `回复充分` / `预计通过` are all banned — the deliverable is a register, not a verdict.
3. **Never leave an unanswered question blank.** Every indexed question needs a row in reply points: an answer, or an explicit gap.
4. **Never excuse a gap.** `不适用` / `无此项` / `无需披露` treat "not checked" as "nothing there".

## 5. Zero-channel path

With no data file at all you can still see what the deliverable looks like:

```bash
python3 scripts/check_inquiry_letter.py --demo
```

`scripts/make_outline.py` builds a skeleton from your reply-document listing — it never needs a parsed doc:

```bash
python3 scripts/make_outline.py listing.jsonl skeleton.md
```

Each line needs `title`, `url` and `asof` (`YYYY-MM-DD`). Bad lines are named one by one and not used; an empty listing exits 1 rather than emitting an empty shell. A skeleton failing the checks is by design.

## 6. Files

`SKILL.md` / `SKILL.en.md` / `README.md` / `README.en.md` / `CHANGELOG.md` / `scripts/check_inquiry_letter.py` / `scripts/make_outline.py` / `scripts/fixtures/` / `tests/test_inquiry.py`.
