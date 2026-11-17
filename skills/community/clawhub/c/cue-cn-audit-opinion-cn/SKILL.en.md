---
name: cn-audit-opinion-cn
slug: cue-cn-audit-opinion-cn
displayName: "Audit Opinion · Every Claim Sourced"
summary: "Sourced register of one audit report: opinion, basis, KAMs, going concern."
description: "One audit report into a sourced register: opinion type, basis, key audit matters, going concern. Five offline checks. Not for earnings commentary, ratings or target prices. Triggers: audit opinion / key audit matters / qualified opinion / going concern"
version: "0.1.0"
license: MIT
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    envVars:
      - name: CUE_API_KEY
        required: false
        desc: "Optional credential: without it the skill only lays out a skeleton from user-supplied files; with it, disclosure search and original-text parsing become available."
tags: [audit-opinion, key-audit-matters, going-concern, annual-report, disclosure]
---

# Audit Opinion · Every Claim Sourced

## 0. What this is, and what it is not

| Is | Is not |
|---|---|
| A register of one audit report's opinion and matter paragraphs | An assessment of the company's business quality, or a run through its figures |
| Opinion type copied in a registered wording | An invented umbrella label such as "modified opinion" or "problematic" |
| Key audit matters copied one by one, with the auditor's response | A judgement about which matter "matters more" |
| Missing material named item by item | Squashed with "not applicable" |
| Everything copied verbatim — no conversion, no rewriting | Fraud findings, distress warnings, ratings, target prices, trading advice |

**Three boundaries (how users tell this apart from its neighbours):**

- `cn-earnings-note` works from the **income statement**, figure by figure. This piece **does not touch income-statement figures** — it registers what the audit report said.
- `event-risk-scan` scans **penalties, regulatory measures and external guarantees**. This piece reads **the audit report itself** and scans no regulatory surface.
- `dd-checklist` is a **public-information due-diligence list** reconciled across nine categories. This piece registers **one audit report**, with no coverage reconciliation.

**"Never generalise" means two things here:**

1. **The opinion type is one of six registered wordings** — unmodified, unmodified with emphasis of matter, unmodified with a material-uncertainty-on-going-concern paragraph, qualified, adverse, disclaimer. A wording not on that list means you rewrote the report: put the original back.
2. **"Modified opinion" is never a conclusion.** It is an umbrella label the note invents. If the report says unmodified, the note cannot call it modified. To mention the phrase at all, quote it and name who said it.

## 1. When to use it

- "What opinion did this company get?" / "Is it a modified opinion?"
- "Which key audit matters were named?" / "What is the auditor most concerned about?"
- "Is there an emphasis-of-matter or going-concern paragraph?"
- "What does the basis-for-opinion section say?"

**Do not use** for: earnings commentary on a published report (`cn-earnings-note`); penalty and guarantee scanning (`event-risk-scan`); a nine-category public-information list (`dd-checklist`); fraud findings, ratings, target prices, share-price views (this skill does not produce them, and no skill should).

## 2. Sourcing discipline

1. **Only the licensed firm's formal audit report.** Every item must resolve to a report link and a retrieval date. Broker notes, news and forum posts are not sources.
2. **Quote every item.** Write `- item：「verbatim sentence」〔anchor: page/section〕[S#]`. An empty quote is not a citation.
3. **Copy the opinion type.** See section 0.
4. **Key audit matters one at a time.** One matter per line, with its title sentence and the auditor's response; no merging, no reordering, no picking favourites.
5. **No conversion, no rewriting.** If the report gives an amount, give that amount — not "about" or "roughly".
6. **A gap is written as a gap, checked both ways.** If the body says "not obtained: X", section five must name X; if section five names X, the body must say it. Zero gaps: write `- 未取到：无`.
7. **No next-year inference.** An opinion covers the audited period; this piece never writes "next year it may".

## 3. Output contract (six sections, in order)

```
AI 整理初稿｜请回原文核对｜不构成投资建议｜判断位 [待人工]

主体：<company>
报告期：<YYYY fiscal year>
数据口径：审计报告（审计意见与非标事项逐项登记）

## 一、审计意见
## 二、形成意见的基础
## 三、关键审计事项
## 四、其他信息与持续经营
## 五、未取到与口径
## 六、来源
```

The four self-labels are fixed in the Chinese face — they are part of the deliverable, not a translation surface. The three header lines and the six section headings are likewise fixed; the checker matches them literally.

- **一、审计意见**: exactly one `- 意见类型：<registered type>｜「quote」〔anchor〕[S#]` line.
- **二、形成意见的基础**: copy each sub-item if the report has the section; if it does not (common for an unmodified opinion), write `- 意见基础：本报告未单列形成意见的基础一节 [待人工]`.
- **三、关键审计事项**: one matter per line. "No key audit matters" is itself a sentence to copy — never leave it blank.
- **四、其他信息与持续经营**: emphasis of matter, going-concern uncertainty, other information — each copied. A section the report omits is named as a gap and appears in section five.
- **五、未取到与口径**: gaps named one by one, plus a line stating what was copied and what was not obtained.
- **六、来源**: one line per source — `- [S#] title｜URL｜检索日 YYYY-MM-DD`.

## 4. Channel

The skill takes disclosures through Cue's MCP channel. List the catalog first, then call `tools/list` at the routing address it returns, so you are working from tools that are actually present:

```bash
CATALOG="https://cuecue.cn/api/mcp-catalog"
curl -s "$CATALOG" | head -c 2000
# take the group's routing address from the catalog, then confirm the tools are present
curl -s -X POST "$ROUTING_URL" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

Once you have the report text, `scripts/make_outline.py` turns a listing into the skeleton.

## 5. Red lines

- **No fraud finding, no misconduct finding.** "Risk of material misstatement due to fraud" is the auditor's wording — quote-only; the note's own words must never carry it.
- **No distress or going-concern-collapse calls.**
- **No ratings, target prices, investment advice, buy/sell or increase/decrease advice.**
- **No next-year forecast** — no "will rise", "will fall", "likely to strengthen".
- **No hedging in place of the report's own words.** "About" and "roughly" never replace a stated term.
- **No second-hand sourcing.** A fact without a report link and retrieval date does not enter this piece.

Red lines judge **the note's own words** only. Text inside `「」` and source lines are exempt — the register must be able to copy the auditor verbatim.

## 6. Quick flow

1. Get the audit report, fix the company and the fiscal year.
2. Copy the opinion-type sentence (usually in the annual report's "Important Notice" section).
3. Copy the basis for opinion, the key audit matters, the emphasis and going-concern paragraphs.
4. Write the gaps and the basis line, aligned both ways.
5. Run `python3 scripts/check_audit_opinion.py your-note.md` and fix what turns red.

Not sure where to start? Run the built-in sample first:

```bash
python3 scripts/check_audit_opinion.py --demo
```

## 7. The checks

```bash
python3 scripts/check_audit_opinion.py your-note.md   # five checks; rc 0 clear / 1 findings / 3 unreadable or empty
python3 scripts/check_audit_opinion.py --selftest     # built-in fixtures
python3 scripts/check_audit_opinion.py --demo         # a complete compliant sample, zero input
bash scripts/fixtures/run_fixtures.sh                 # three offline tiers, zero network, zero billing
```

`AU-STRUCT` form / `AU-QUOTE` quote and anchor / `AU-OPINION` opinion type / `AU-GAP` gaps both ways / `AU-LINE` red lines.

The checker judges **form and registered wording**. It cannot tell whether the classification is right — a note that says unmodified when the report is actually qualified looks fine to it. That step has to go back to the report by hand.

## 8. Zero channel

Without `CUE_API_KEY` the skill **produces no content**; it lays out a skeleton from the listing you supply, leaving content as `[待人工]`. The skeleton fails the checks by design — that is a reminder to finish it, not a shell pretending to be a deliverable.

The cost, stated plainly: **no channel means no report text, no report text means no quoted sentence, and without a quoted sentence the opinion type cannot be anchored** — what remains is a single sentence the user typed in. Use `--demo` to see the finished shape; it costs nothing and touches no channel.
