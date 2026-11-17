# Audit Opinion · Every Claim Sourced

Read **one audit report** into a register where every conclusion goes back to a quoted sentence: the opinion type, the basis for opinion, key audit matters, emphasis-of-matter and going-concern paragraphs, and other information.

**No fraud calls, no misconduct findings, no distress warnings, no next-year forecasts, no ratings or target prices.** The opinion type is recognised only in its six registered wordings; umbrella labels like "modified opinion" are not allowed to stand in as a conclusion.

---

## 1. Thirty seconds (zero input)

With no data file at all, produce a complete, compliant sample to see what the deliverable looks like and how the checks behave:

```bash
python3 scripts/check_audit_opinion.py --demo
```

Save that sample and run the checker on it — it passes itself:

```bash
python3 scripts/check_audit_opinion.py --demo > sample.md
python3 scripts/check_audit_opinion.py sample.md
# → sample.md 发条=0｜AU-STRUCT=0｜AU-QUOTE=0｜AU-OPINION=0｜AU-GAP=0｜AU-LINE=0
```

Then point it at your own draft:

```bash
python3 scripts/check_audit_opinion.py your-note.md
```

Exit codes: `0` all clear, `1` findings raised, `2` usage error, `3` file unreadable or empty.

---

## 2. What the five checks enforce

| Code | Name | What it checks | What it most often catches |
|---|---|---|---|
| `AU-STRUCT` | Form | Four self-labels before the first `## `; subject, period and data-basis lines present, with the basis starting `审计报告`; six sections present and ordered; each of the first four has a finding line; exactly one opinion-type line | A missing section; a heading with nothing under it; the data basis written as "earnings commentary" |
| `AU-QUOTE` | Quote and anchor | Every finding line ends in quote + anchor + `[S#]`; source lines carry a clickable URL and a retrieval date; every cited number is registered | A figure with no quoted sentence; an empty `「」`; a source line with no link |
| `AU-OPINION` | Opinion type | Only the six registered wordings count; a type named outside quotes must match the declared one; "modified" used as a conclusion outside quotes raises | Writing `无保留意见` when the registered name is `标准无保留意见`; declaring unmodified then writing "this report is qualified" |
| `AU-GAP` | Gaps named both ways | A gap in the body must appear in section five, and vice versa; zero gaps must be stated explicitly | Brushing a gap aside with "not applicable" |
| `AU-LINE` | Red lines | Fraud, misconduct, distress, delisting, ratings and target prices, buy/sell advice, next-year forecasts — zero tolerance | "This piece finds the company committed fraud" |

**Red lines judge only the note's own words.** Text inside `「」` and source lines are exempt — a register has to be able to copy the auditor's own wording, and audit reports do say things like "risk of material misstatement due to fraud".

---

## 3. What this piece exists to prevent

1. **The opinion type is copied, never generalised.** Six registered wordings only. If yours isn't on the list, you rewrote the report — put the original back.
2. **"Modified opinion" is never a conclusion.** It is an umbrella label the note invents. If the report says unmodified, the note cannot call it modified.
3. **Key audit matters are copied one by one.** One matter per line, with its title sentence and the auditor's response; no merging, no reordering, no picking favourites.

---

## 4. What one finding looks like

```markdown
- 意见类型：标准无保留意见｜「我们认为，后附的财务报表在所有重大方面按照企业会计准则的规定编制，公允反映了……的合并及母公司财务状况以及 2025 年度的合并及母公司经营成果和现金流量。」〔锚：2025 年年度报告·第 112 页·审计报告·审计意见段〕[S1]
```

```markdown
- 关键审计事项（一）：「收入确认」〔锚：2025 年年度报告·第 114 页·关键审计事项段〕[S1]
- 应对程序（一）：「我们了解、评估了管理层对收入确认相关的内部控制的设计，并测试了关键控制运行的有效性。」〔锚：2025 年年度报告·第 114 页·关键审计事项段〕[S1]
```

---

## 5. How this differs from the other packages

| You have | Use |
|---|---|
| The audit report, opinion type, key audit matters | **this skill** |
| Income-statement commentary: period differences, account reconciliation | `cn-earnings-note` |
| Cash-flow statement, net-cash and collection ratios | `cn-cash-flow-quality` |
| Inventory, receivables, contract assets | `cn-working-capital-quality` |
| Penalties, regulatory measures, external guarantees | `event-risk-scan` |
| Nine-category public-information due-diligence list | `dd-checklist` |

---

## 6. Zero channel: build the skeleton first

It runs without any channel artifact — the script only reads the listing you give it:

```bash
python3 scripts/make_outline.py listing.jsonl skeleton.md
```

Each JSONL line needs `title`, `url` and `asof` (`YYYY-MM-DD`); `id` and `page` are optional.

- Bad lines (invalid JSON, missing key, malformed date, non-http url) are **named one by one and not used**; good lines are still taken.
- **An empty listing exits 1** rather than emitting an empty shell.
- The skeleton **fails the checks on purpose** — that is the design, not a defect to fix.

```bash
python3 scripts/make_outline.py --selftest       # 8 built-in fixtures
```

---

## 7. Fixtures and tests

```bash
bash scripts/fixtures/run_fixtures.sh            # three offline tiers, zero network, zero billing
python3 tests/test_audit_opinion.py              # package tests: entry contract / zero input / beacon
```

The runner has three tiers: checker self-test / good and bad samples one by one / line-by-line substitution on the good sample as a positive-and-negative control. The last line reports `档数=3｜不合=N｜不可判=N`.

The tests cover the shell contract — `--help` exits 0, no argument exits 2, missing file exits 3, `--demo` output passes its own checker and is byte-reproducible, an empty listing emits no shell, and the beacon lands while failing silently.

---

## 8. First-run beacon

After argument parsing succeeds and before any real work, the entry scripts drop an **empty file** at `~/.cue-usage/<slug>-<date>`.

**Why:** both platform download counters are unreliable — a new listing is seeded with 50–60 initial counts in its first 48 hours, and that is not people downloading. This local file is the only evidence this piece has that someone actually installed it and ran it.

**It never gets in the way:** any failure (read-only home, full quota, no `HOME`) is skipped silently — no error, no exit-code change, not a single line of noise. Running it several times in one day still leaves one file.

To clear it: `rm -rf ~/.cue-usage`.

---

## 9. Where material comes from

- **User-supplied**: annual reports and audit reports you already have, via `+parse`.
- **Channel retrieval**: with `CUE_API_KEY` set, disclosure search and original-text parsing become available. Skill installed ≠ credential configured ≠ channel connected — three separate things.
- **Zero channel**: `--demo` for the shape, `make_outline.py` for the skeleton.

This skill issues no requests and pays for nothing; consumption is reported as the server returns it.

---

## 10. Confirming the channel is present (optional)

Only needed once `CUE_API_KEY` is configured. List the catalog first, then confirm the tools are present at the routing address it gives:

```bash
CATALOG="https://cuecue.cn/api/mcp-catalog"
curl -s "$CATALOG" | head -c 2000
# take the group's routing address from the catalog, then confirm the tools are present
curl -s -X POST "$ROUTING_URL" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

Without a credential it still runs: `--demo` and `make_outline.py` are both pure-local paths.

---

## 11. Files

| File | Purpose |
|---|---|
| `SKILL.md` / `SKILL.en.md` | Chinese and English faces with the check contract |
| `scripts/check_audit_opinion.py` | The five checks; `--selftest` runs the fixtures, `--demo` prints the sample |
| `scripts/make_outline.py` | Listing → skeleton; `--selftest` runs the built-in fixtures |
| `scripts/fixtures/` | 1 good sample + 6 bad samples + the three-tier runner |
| `tests/test_audit_opinion.py` | Package tests (entry contract, zero input, beacon) |
