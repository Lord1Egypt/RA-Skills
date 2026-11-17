# Inquiry Letter Reply Checklist (监管问询函)

Turns one regulatory inquiry letter into a table where **every question is matched to its reply**.

What the regulator asked, what materials were requested, what the company answered, and which reply documents are still missing — four columns, with every gap named out loud.

**It never drafts the reply, never concludes, never speaks for the company.** Quoted text is the regulator's wording; the package only puts that wording where it belongs.

---

## 1. First, something that decides the design

**The exchange's letter itself is not available through any public filing channel.** This is not an oversight:

- Full-text search in the public disclosure database turns up mostly the **company-side reply announcements**; a small remainder are the company's own notices that a letter was *received* — those carry no question text.
- The Shanghai and Shenzhen exchanges' own "regulatory inquiry" pages exist, but their query endpoints return empty; Beijing's redirects.

So this package **has no "fetch the letter automatically" feature, and will not pretend to have one**. You paste the letter in or point at a local file.

What *can* be listed automatically is the reply side: reply announcements, annual and semi-annual reports, and prospectuses in offering scenarios. The package lays that side out as a skeleton and checks its completeness.

---

## 2. Thirty seconds, no input

With no data file at all you can still see a complete, compliant deliverable and how the checks read:

```bash
python3 scripts/check_inquiry_letter.py --demo
```

Save it and run the checker on it — it passes itself:

```bash
python3 scripts/check_inquiry_letter.py --demo > sample.md
python3 scripts/check_inquiry_letter.py sample.md
# → sample.md 结论：六道全过（零发条）
```

Then point it at your own table:

```bash
python3 scripts/check_inquiry_letter.py your-table.md
```

Exit codes: `0` all clear, `1` findings, `2` usage error, `3` unreadable or empty file.

### Starting from the source letter

1. **Bring the letter in** (paste or local path) and copy each question verbatim.
2. **Match every question to a reply**: answered ones get reply points, unanswered ones say `- 问题N 未取到：<what>` — **never a blank row**.
3. **Run the self-test** and fix what turns red:

```bash
python3 scripts/check_inquiry_letter.py --selftest      # 10 built-in fixtures
```

### Confirm the channel is present (optional)

Only needed with `CUE_API_KEY` set. List the catalog, then take the group's routing address from it and confirm the tools are present:

```bash
CATALOG="https://cuecue.cn/api/mcp-catalog"
curl -s "$CATALOG" | head -c 2000
curl -s -X POST "$ROUTING_URL" \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

Without credentials it still works: put the materials in your workspace and use the user-supplied path.

---

## 3. What the six checks cover

| Code | Name | Judges | Most common catch |
|---|---|---|---|
| `IL-STRUCT` | Shape | header self-labels, subject and letter lines, six sections in order, a finding row in each of the first three | a missing section; a section with only a heading; an invented seventh column |
| `IL-QUOTE` | Quote and anchor | every finding row ends with quote + anchor + `[S#]`; source rows carry a URL and retrieval date; every cited number is registered | a point with no quoted sentence; a source row with no link |
| `IL-PAIR` | Questions vs replies | every indexed question has a matching row in reply points, and vice versa | question 3 is indexed but reply points jumps to question 4 |
| `IL-GAP` | Gap naming | a gap in the body must appear in the gaps section and vice versa; a clean run must say `未取到：无` | excusing it with "not applicable" |
| `IL-MEDIA` | Filing-party completeness | one inquiry usually yields 3–5 filings from company, auditor and sponsor; company-only with no intermediary gap named fires | searching only the company name and missing the auditor and sponsor filings |
| `IL-LINE` | Red lines | with quotes stripped, no speaking for the company and no conclusions | "the company will rectify" / "no material impact" |

---

## 4. Four red lines

1. **Never draft the reply.** `本公司将` / `现回复如下` / `特此答复` fire once quoted text is stripped. What sits inside a quote is verbatim source and is not this package's voice.
2. **Never conclude.** `不构成重大影响` / `不存在问题` / `风险可控` / `回复充分` / `预计通过` are all banned. The deliverable is a register, not a verdict.
3. **Never leave an unanswered question blank.** Every indexed question needs a matching row in reply points: an answer, or an explicit gap.
4. **Never excuse a gap.** `不适用` / `无此项` / `无需披露` treat "not checked" as "nothing there", which is not the same as a gap.

---

## 5. What a finding looks like

```markdown
- 问题1 募投项目产能消化「请说明本次募投项目新增产能的消化措施及合理性」〔锚：问询函·第 1 页·问题 1〕[S1]
```

An unanswered question looks like this — no quote is available, which is by design, not an escape hatch:

```markdown
- 问题2 未取到：前次募集资金使用明细
```

The reply-documents column looks like this:

```markdown
## 4. 回复文件

- 主体:公司本体｜[S2]
- 主体:会计师事务所｜[S3]
```

**Why this column exists:** one inquiry typically produces 3–5 filings, filed separately by the company, the accounting firm, and the sponsor or counsel. Searching only the company name misses the intermediary filings — so when only the company itself is registered and the gaps section does not name the intermediaries, `IL-MEDIA` fires.

---

## 6. How this differs from neighbouring packages

| You have | Use |
|---|---|
| one inquiry letter, want it torn down question by question | **this package** |
| "draft the reply for me" | out of scope — drafting is not what this does |
| "will it pass review, will there be a penalty" | out of scope — those stay `[待人工]` |
| a five-part announcement brief | `event-brief-cn` |
| regulatory letters as diligence-checklist rows | `dd-checklist` |
| placement terms, convertible-bond terms | `placement-terms-cn` / `convertible-bond-terms-cn` |

**Versus `dd-checklist`:** that package maps an inquiry letter into a `合规与处罚` category and records **one anchored event row** — when, what kind of letter, involving whom. This package does not record "there is a letter"; it records **which questions were asked, which were answered, which were not**. One is an event, the other is a clause-by-clause cross-check.

---

## 7. Zero-channel path

With no channel output at all, the script reads only the listing you give it:

```bash
python3 scripts/make_outline.py listing.jsonl skeleton.md
```

Each line needs `title`, `url` and `asof` (`YYYY-MM-DD`); `id` may be omitted and is assigned `S1`/`S2`… by row order.

- Bad lines (invalid JSON, missing keys, malformed date, non-http url) are **named one by one and not used**; good lines are kept.
- **An empty listing exits 1 and emits no empty shell.**
- The skeleton **fails the checks on purpose** — by design, not a to-do.

```bash
python3 scripts/make_outline.py --selftest       # 15 built-in fixtures
```

---

## 8. Fixtures and tests

```bash
bash scripts/fixtures/run_fixtures.sh
python3 tests/test_inquiry.py
```

Three tiers: checker self-test / good and bad fixtures run one at a time / line-by-line substitution on the good sample to prove that what should fire does and what should not doesn't. Zero network, zero billing, artifacts land only in a temp directory and are deleted when done.

The last line self-reports `档数=3｜不合=N｜不可判=N`; exit `0` all clear, `1` findings, `3` value-domain failure.

`tests/` covers the shell properties the fixtures cannot: `--help` exits 0, no args exits 2, missing or empty file exits 3, `--demo` passes its own checker and is byte-reproducible and identical to the good fixture, an empty listing emits nothing, and the first-run marker lands once per day and fails silently.

---

## 9. First-run marker

After argument parsing succeeds and before doing real work, each entry script drops an **empty file** at `~/.cue-usage/<slug>-<date>`.

**Why:** both platform download counters are unreliable — a new listing gets 50–60 seeded into its count in the first 48 hours, and that is not downloads. This local file is the only evidence that someone actually installed and ran the package.

**It never gets in the way:** any failure (read-only home, quota, no HOME) is swallowed silently — no error, no change to the exit code, no noise. Running it several times a day leaves exactly one file.

To clear it: `rm -rf ~/.cue-usage`.

---

## 10. Where materials come from

- **The letter itself:** no public filing channel exists; bring it yourself (paste or local path).
- **The reply side:** reply announcements, annual and semi-annual reports, prospectuses in offering scenarios — parse them, then build the skeleton from a listing.
- **Channel retrieval:** with `CUE_API_KEY` set, announcement search and document parsing are available. Installed ≠ credentialed ≠ connected; keep the three separate.
- **Zero channel:** `make_outline.py` builds the skeleton, see section 7.

This package sends no requests on its own and does not pay on your behalf; consumption is whatever the server returns.

---

## 11. Files

| File | Purpose |
|---|---|
| `SKILL.md` / `SKILL.en.md` | Chinese and English faces, including the check contract |
| `scripts/check_inquiry_letter.py` | six checks; `--selftest` runs built-in fixtures, `--demo` prints a sample |
| `scripts/make_outline.py` | reply-document listing → skeleton; `--selftest` runs built-in fixtures |
| `scripts/fixtures/` | 1 good sample + 6 bad samples + three-tier runner |
| `tests/test_inquiry.py` | package-level tests (entry contract, zero input, marker) |
