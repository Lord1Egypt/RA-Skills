# Goodwill Impairment Risk Ledger

Extract the **goodwill line items** from an annual report, semi-annual report, or acquisition
announcement into an eight-section ledger. Every amount and percentage on every row must trace
back, verbatim, to the disclosure sentence it came from.

> Offline self-test: `bash scripts/fixtures/run_fixtures.sh` — good sample stays clean, six bad
> samples each fire their own check code, all three tiers pass, zero network.

## What it solves

Goodwill is the largest "hard to pin down" asset left over from A-share M&A. From one annual report
you may want to know:

- How much goodwill does this company carry? Which acquired target dominates?
- Were the earn-out commitments met? What was the completion rate?
- What discount rate and growth rate did the impairment test use?
- How much was impaired this year, cumulatively, and what balance remains?

All of these numbers exist in the annual report, but they are scattered across the notes, the
board report, and the audit report, written in different styles with different bases. This skill
extracts them into one ledger, **each cell carrying its source sentence and an anchor**, so you can
walk back to that page yourself.

## What it does NOT do (this section matters more than the one above)

| Not done | Why |
|---|---|
| Judge **whether impairment will occur** | That is an investment call, not an extraction. The ledger reports what was disclosed |
| Judge **whether the provision is adequate** | Same. The audit opinion and regulatory inquiry are the referees |
| Give ratings or price targets, predict share prices | Hard red line |
| **Compute the impairment amount or ratio itself** | The denominator could be goodwill at cost, carrying value, or the asset-group basis — get it wrong and every reading on the sheet is wrong. If the disclosure gives no ratio, write "not found"; that is an answer, not a failure |
| Do the accounting treatment or draft an inquiry reply | No agency work |

## Usage

```bash
# 1. Obtain the annual report / announcement (PDF or web page)
# 2. Extract into a markdown ledger following the eight-section contract in SKILL.md §3
# 3. Self-check
python3 -B scripts/check_goodwill.py my-ledger.md
```

Exit `0` = all clean; `1` = findings (tells you which row and which cell); `3` = file missing or not
this kind of ledger.

## The five checks

| Code | Check | Catches |
|---|---|---|
| `GW-STRUCT` | Structure | All eight sections present; three header items present; each of the four row types has its required fields |
| `GW-QUOTE` | Quote & anchor | Non-empty 「」 quote per row, non-empty `锚：`, `[S#]` resolving to a source line with URL and retrieval date |
| `GW-LINE` | Red lines | Will it impair / is the provision adequate / ratings & targets / price prediction / return promises / agency work |
| `GW-GAP` | Missing items & no self-calculation | Declared counts reconcile both ways; "no impairment / not applicable" substituting for disclosure; **an amount or percentage not present verbatim in that row's own quote = self-calculated** |
| `GW-BOUND` | Boundary | A basis line written as restructuring or earnings commentary gets pointed at the right skill |

### The most important cell: judge "verbatim presence", not "numeric equality"

`1,200.00 万元` and `1200 万元` are numerically equal, but the latter is a writing the ledger
processed. A unit change (万元 ↔ 亿元), a padded decimal, a stripped thousands separator — **all
count as not in the quote**.

The reason: this skill sells exactly "this number traces back to that sentence". Once conversion is
allowed, "traces back" becomes "can be computed", and those are two different things.

## Boundaries against existing skills

| Skill | It covers | This one does not touch |
|---|---|---|
| `cn-restructuring-tracker` | Restructuring **events** and consideration timeline (halt, plan, approval, completion) | The goodwill line items |
| `cn-earnings-note` | **Commentary on published results** (revenue, profit, margin — what moved and why) | No performance commentary; only goodwill items onto source sentences |
| `ma-restructuring-terms-cn` | **Term extraction** from a single restructuring document | Goodwill balance and impairment testing |

## Channel

Two optional supporting legs: `cue-data-mcp` (locating annual reports and acquisition announcements)
and `cue-omni-reader` (PDF / web to extractable text). Live connection uses the `tools/list`
handshake with domain id and routing url resolved at run time, never hard-coded.

Three layers are not equivalent: **skill installed ≠ credentials configured ≠ channel connected**.
An anonymous GET only proves the catalog is reachable; a keyed connection returning `tools/list`
proves that key is accepted. A connection error does not mean the domain has no data — report it
as-is.

## Artifacts

- `consumes: []` (explicitly empty — this skill reads user-supplied files, consuming no upstream artifact)
- `inputs: announcement-doc / disclosure-file`
- `produces: structured-note` (registered canonical; no new artifact name introduced)

## Files

- `SKILL.md` — full contract (eight sections, four row shapes, five checks)
- `SKILL.en.md` — this English counterpart
- `README.md` / `README.en.md`
- `CHANGELOG.md`
- `scripts/check_goodwill.py` — the five checks (zero network, standard library only)
- `scripts/fixtures/` — 1 good sample + 6 bad samples + `run_fixtures.sh`

## License

MIT
