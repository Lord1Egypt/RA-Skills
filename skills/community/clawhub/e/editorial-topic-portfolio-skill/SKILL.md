---
name: editorial-topic-portfolio
slug: editorial-topic-portfolio-skill
displayName: Editorial Topic Portfolio
version: "1.0.11"
description: >
  This skill should be used when evaluating a portfolio of technology, AI, data,
  cloud, or enterprise-software content topics. It normalizes Notion or
  Markdown/JSON/CSV inputs, applies factual, timeliness, originality,
  argument-capacity, positioning, and privacy gates, scores eligible topics,
  selects one primary and two backups, produces merge/watch/covered/abandon
  decisions, and prepares a confirmed Notion writeback preview. By default, it
  never writes to Notion without two explicit confirmations; a workspace with a
  documented standing instruction to sync every routine review may use that
  instruction as the authorization, but must still generate a change preview and
  perform readback verification.
  中文触发词: 选题评估, 选题组合, 竞争密度, 原创空间, Notion选题库, 内容排期
description_zh: 选题组合评估与写作排期
description_en: Editorial topic portfolio
not_for:
  - Writing, editing, or laying out a single article (use the writing or publishing pipeline skills)
  - Publishing or distributing content to platforms
  - Developing Notion databases or API integrations
  - Performance review of already-published content
agent_created: true
read_when:
  - editorial topic portfolio
  - topic prioritization
  - 选题组合
  - 选题评估
  - 本周写什么
  - 选题优先级
  - Notion 选题库复核
  - 内容排期
allowed-tools:
  - env
  - Read
  - Write
metadata:
  openclaw:
    permissions:
      - env
      - file_read
      - file_write
---

# Editorial Topic Portfolio

Evaluate a batch of technology / AI / data / cloud / enterprise-software topics and output the current cycle's 1 primary-write + 2 backups, plus merge / watch / short-note / covered-track / abandon decisions. Uses Routing + Prompt Chaining: pass hard gates first, then score and solve the portfolio.

## When to use

- You need to determine this / next week's writing portfolio from a Notion topic database or local files.
- You need to decide whether a topic is an independent long-form, merges into another article, shrinks to a short note, stays on watch, or closes.
- You need to check competition density, originality space, fact readiness, timeliness window, and positioning fit.
- You need to generate a Notion field-change preview before writeback.

## Do not use

- Writing the body directly; hand the primary topic to `industry-deep-dive-pipeline`.
- Generating WeChat layout, summaries, covers, social assets, or publish content directly.
- Writing to Notion without confirmation (unless the current workspace has an explicit, persistent standing instruction authorizing routine-review auto-sync).
- Ranking purely by buzz, a single number, or headline spreadability.

## Inputs

### Supported sources

- Markdown, JSON, CSV: convert directly to a standard topic record.
- Notion: read via a private adapter; credentials, database ID, and field mapping come only from secure environment variables or private config.

### Required fields

- topic title
- source date and captured date
- lifecycle status
- topic type
- source/evidence
- hypothesis or value judgment
- related published content

Read `references/evaluation-gates.md`, `references/scoring-model.md`, and `references/portfolio-rules.md` for fields and rules.

## Workflow

### Step 1: [Deterministic] Normalize input

1. Route Notion or file input.
2. Run:

```bash
python scripts/normalize_topics.py --input <input.md|input.json|input.csv> --output <run-dir>/01-normalized-topics.json
```

3. Deduplicate by title, URL, event subject, and synonymous topic.
4. Preserve stable topic ID or Notion page ID; title is for display only.

### Step 2: [Deterministic + LLM] Pre-screen

1. Execute G0 input completeness check.
2. Classify event, trend, framework, case, policy, research.
3. Check lifecycle status, identify published, adopted, watch, and closed items.
4. Output `02-gate-precheck.json`.

### Step 3: [LLM + Search] Research evidence and competition

1. Re-verify key facts, dates, policy status, product status, and amount caliber.
2. Search Chinese and English for the topic, synonymous judgments, analytical frameworks, signature phrasings, counter-arguments, and historical counter-examples. **⚠️ Before sending: topic details may be confidential/unpublished editorial ideas. Confirm with the user that sending them to an external search service is authorized; if not, minimize/redact the query or skip external research and mark the item "locally unverified". Never transmit private positioning or sensitive topic data.**
3. Check overlap with published, in-progress, and same-batch topics.
4. For watch items, determine trigger conditions, required evidence, and review date.
5. Output `03-evidence-review.md`.

### Step 4: [LLM] Apply hard gates

For each topic, output G0—G5:

- G0 input completeness.
- G1 fact and status.
- G2 timeliness and trigger.
- G3 originality space.
- G4 long-form carrying capacity.
- G5 positioning and privacy boundary.

Output `04-gate-results.json`. BLOCK cannot be offset by score.

### Step 5: [Deterministic] Calculate scores

For topics passing hard gates or recoverable HOLD, fill 0—5 raw scores:

- Originality space and information gain: 20.
- Reader judgment value: 20.
- Fact and evidence readiness: 15.
- Timeliness and window: 15.
- Content positioning match: 15.
- Portfolio contribution: 10.
- Execution feasibility: 5.

Deduct for fact uncertainty, competition heating, angle too broad, recent repetition, and public risk, to get net score. Run:

```bash
python scripts/calculate_scores.py --input <run-dir>/04-gate-results.json --output <run-dir>/05-scores.json
```

### Step 6: [LLM + Deterministic] Build portfolio

1. Select exactly 1 `WRITE_NOW` and 2 `BACKUP`.
2. Constrain: primary and backups cannot all belong to the same company, event, or argument framework.
3. Mark the rest as `MERGE`, `WATCH`, `SHORT_NOTE`, `COVERED_TRACK`, or `ABANDON`.
4. Write the fact, originality, timeliness, and portfolio reason for each decision.
5. Output `06-portfolio-decision.md`.

### Gate A: [Human] Confirm portfolio

Pause, confirm:

- 1 primary and 2 backups.
- P0—P3 adjustments.
- Merge, watch, covered, and abandon handling.
- Manual override reasons and validity period.
- Planned writeback fields.

No change-set generation before confirmation.

### Step 7: [Deterministic] Generate change preview

Generate `07-change-preview.md` and `07-change-set.json`, listing per item:

- page ID or stable topic ID.
- Old/new values for status, priority, competition density, originality, value, positioning match, and evaluation date.
- Changes to recommended reason, suggested angle, and risk reminder.
- Idempotent evaluation block.

Run:

```bash
python scripts/validate_change_set.py --input <run-dir>/07-change-set.json --output <run-dir>/07-change-set-validation.json --enforce
```

### Gate B: [Human] Confirm writeback

Explicitly list target database, page count, fields, and actions. Batch writeback only after the second confirmation.

### Step 8: [Deterministic] Writeback

Notion writeback must follow:

- `NOTION_TOKEN`, `NOTION_TOPIC_DATABASE_ID`, and mapping come from secure config.
- Use page ID; fuzzy title matching for writes is forbidden.
- Preview and dry-run must not send PATCH.
- On failure, pause the batch; record succeeded/failed/skipped.
- Evaluation blocks are idempotently replaced by run ID and date; no repeated appends.

Default read-only adapter:

```bash
NODE_PATH=<managed-node-workspace> node scripts/notion_topic_adapter.js read > <run-dir>/08-notion-read.json
```

Write capability must be driven by a separate, reviewed change set; real-time writeback must not be an unconditional auto-action.

### Step 9: [Deterministic] Readback

- Re-query updated page IDs.
- Compare preview vs actual fields.
- On mismatch, retry once and cross-validate via a different request path.
- Do not mark complete if readback mismatches.

Output `09-readback-verification.md`.

### Step 10: [Deterministic] Handoff primary

Convert the primary to an `industry-deep-dive-pipeline` case brief, preserving facts, competition, core hypothesis, suggested angle, risks, counter-arguments, and series relationship. Do not write the body directly.

## Hard Rules

1. Hard gates before scoring; BLOCK cannot be offset by high score.
2. Facts, status, and dates must trace to reliable sources; search snippets are leads only.
3. lifecycle status and recommendation priority must be separate.
4. Each round must be 1 primary + 2 backups, unless manually overridden with recorded reason.
5. Published topics default to `COVERED_TRACK`, unless there is a clear new fact or new judgment.
6. Watch items must have trigger conditions, required evidence, and review date.
7. Dedupe before entry: check a candidate topic against the current portfolio for near-duplicates. The same thesis with a different news trigger is not a new topic — extend or replace the existing entry instead.
8. Use page ID for writes; title must not be the sole write key.
9. Any Notion writeback requires portfolio confirmation and writeback confirmation.
10. Credentials, database IDs, personal topics, and private positioning must not enter the generic Skill or public templates.
11. First tool failure must retry and cross-validate; after a fix, rerun.
12. Do not auto-revert adopted, published, or closed status.
13. Before task completion, record output, verification, residual risk, and next task.

## Failure Handling

| Scenario | Action |
|---|---|
| Input field missing | Mark `NEEDS_INPUT`, stop scoring that item |
| Fact or policy unverifiable | `BLOCK_FACT` or `HOLD_EVIDENCE`, no primary/backup |
| Timeliness expired, no increment | `BLOCK_STALE` or `COVERED_TRACK` |
| Insufficient originality space | `MERGE` or `BLOCK_SATURATED` |
| Single event insufficient carrying capacity | `SHORT_NOTE` or `BLOCK_THIN` |
| Positioning/privacy conflict | `BLOCK_BOUNDARY` or `PRIVATE_ONLY` |
| Portfolio not exactly 1+2 | Block change-set, re-solve or await manual override |
| Notion token/mapping missing | Stop, do not read, do not write |
| Notion writeback partial failure | Pause batch, record success/fail/skip, do not blindly retry all |
| Readback mismatch | Retry once and cross-validate; if still mismatch, keep incomplete |
| First tool failure | Retry same action 1—2 times, then switch tool stack |

## Output Format

```text
<run-dir>/
├── 01-normalized-topics.json
├── 02-gate-precheck.json
├── 03-evidence-review.md
├── 04-gate-results.json
├── 05-scores.json
├── 06-portfolio-decision.md
├── 07-change-preview.md
├── 07-change-set.json
├── 07-change-set-validation.json
├── 08-writeback-result.json
└── 09-readback-verification.md
```

Each round's report must include: primary, two backups, other dispositions, hard-gate blockers, net scores, writeback status, and next-step handoff.

## References

- `references/evaluation-gates.md`: G0—G5 hard gates.
- `references/scoring-model.md`: 100-point model and deductions.
- `references/portfolio-rules.md`: portfolio, lifecycle, and idempotency rules.
- `references/notion-adapter-interface.md`: private Notion adapter boundary.
- `references/replay-evaluation.md`: two sets of historical replays.

## Pitfalls

- Conflating status and recommendation priority.
- Using title fuzzy-matching for Notion pages and writing to the wrong target.
- Causing repeated accumulation per run by appending notes.
- Deriving global market share or pricing power from a single aggregation platform's traffic.
- Re-listing a published topic as primary.
- High score but unstable fact, policy, or amount caliber.
- Sorting only by news热度, ignoring reader judgment value and originality space.
- Writing back to Notion before user confirms the portfolio; exception is when the workspace has an explicit standing instruction authorizing routine-review auto-sync, in which case still complete the portfolio judgment, generate a change record, and perform readback first.

## Verification

- [ ] Notion/file inputs both convertible to standard topic record.
- [ ] Each topic has G0—G5 result, base score, deduction, net score, and disposition action.
- [ ] Each round exactly 1 primary + 2 backups, or explicit manual override.
- [ ] No internal competition between primary and backups on same event/framework.
- [ ] Fact blockers (G1/G5 BLOCK) did not enter WRITE_NOW or BACKUP.
- [ ] Change-set uses only page ID or stable topic ID.
- [ ] Preview, portfolio confirmation, and writeback confirmation all recorded.
- [ ] Repeated runs do not repeatedly append evaluation blocks.
- [ ] Readback field consistency 100% after writeback.
- [ ] Real tokens, database IDs, and private topic data not in Skill directory.
