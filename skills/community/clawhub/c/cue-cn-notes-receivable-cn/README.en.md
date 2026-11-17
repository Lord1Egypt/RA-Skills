# Notes Receivable & Payable · Every Figure Sourced

Turns one filing's notes family into a register where every number goes back to a quoted sentence: classification (bank-accepted / commercial-accepted), closing balance and provision, endorsed and discounted but not yet matured, derecognition, collection at maturity and dishonour.

Notes are a separate set of accounts: they are not provisioned by ageing like trade receivables, and they are not spendable like cash. **Whether a note really counts depends on its class, whether it left the book, and whether it was collected** — this piece registers those three, and leaves the conclusion to a human.

**No authenticity calls, no acceptor credit calls, no default forecasts, no ratings or price targets, no computed discount amounts.** Class and derecognition come only from the quote; a computed discount interest must stand alone with its rate, period and day-count basis.

---

## 1. Thirty seconds, zero input

Without any data file you can produce a complete compliant sample and see what it looks like:

```bash
python3 scripts/check_notes.py --demo
```

Save it and run the machine gate on it — it passes itself:

```bash
python3 scripts/check_notes.py --demo > sample-notes.md
python3 scripts/check_notes.py sample-notes.md
# → sample-notes.md 结论：五道全过（零发条）
```

Then point it at your own draft:

```bash
python3 scripts/check_notes.py your-notes.md
```

Exit codes `0` all pass, `1` findings, `2` usage error, `3` unreadable or empty file.

### Starting from the filing instead

1. **Fix the subject and the period**, get the annual or interim report (notes five "notes receivable" and "notes payable", plus the cash-flow supplement).
2. **Copy each fact with its sentence**: one line per fact, ending with `「quote」〔锚：page/table〕[S#]`.
3. **Run the gate and fix one finding at a time**:

```bash
python3 scripts/check_notes.py --selftest      # 13 built-in fixtures
```

### Confirm the channel first (optional)

Only needed if `CUE_API_KEY` is configured. List the catalog, then confirm the tools are there via its routing address:

```bash
CATALOG="https://cuecue.cn/api/mcp-catalog"
curl -s "$CATALOG" | head -c 2000
# take this group's routing address from the catalog
curl -s -X POST "$ROUTING_URL" \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

Without a key it still works: put the filing in the workspace and use the user-supplied path — the cost is that the endorsement schedule and provision detail have to be found in the file you already have.

---

## 2. What the five lanes check

| Code | Lane | Judges | Most often catches |
|---|---|---|---|
| `NR-STRUCT` | Structure | Four header self-marks, `主体：`, `报告期：`; six sections present and ordered; at least one finding line in each of the first four | A section missing; a heading with no body; a duplicated section heading |
| `NR-QUOTE` | Quotes and anchors | Every finding line ends with 「」 + 〔锚：…〕 + `[S#]`; source lines carry a clickable URL and a retrieved date; every referenced number is registered | Numbers with no quoted sentence; a source line with no link |
| `NR-NOSELF` | No self-inference or computation | Class and derecognition only from the quote; a ratio the quote does not state must be flagged as computed with numerator and denominator; computed discount interest must state rate, period and day-count basis | The quote says only "notes receivable" and the line says "commercial-accepted"; a discount figure multiplied out and reported |
| `NR-GAP` | Two-way gap naming | Body and section five reconcile both ways; zero gaps must write `未取到：无` | "Not applicable", "no such item", "no need to disclose" |
| `NR-LINE` | Red lines | Authenticity, acceptor credit, default risk, ratings — zero hits; quoted text is stripped first; margin equals cash fires | "the acceptor is creditworthy, default risk is low" |

---

## 3. Four red lines (why this package exists)

1. **Class only from the quote.** When the note text lists only "notes receivable" without a class, the right output is "not retrieved", not an inference from the issuer's name — one issuer can issue both kinds.
2. **Derecognition only from the quote.** "Endorsed" is not "derecognised" and "not matured" is not "still on book"; that step is an accounting judgement the disclosure makes.
3. **Discount interest is never computed for the user.** Quoted, or flagged as computed with rate, period and day-count basis on the same line — all three.
4. **A notes margin is not cash.** It is restricted funds in a separate account; never written as equal to cash or as corroborating it.

---

## 4. What one finding looks like

```markdown
- 应收票据·银行承兑 8,600.00 万元「应收票据—银行承兑票据 86,000,000.00 元」〔锚：2025 年年报·第 96 页·附注五·应收票据〕[S1]
```

A missing item keeps its own line:

```markdown
- 应付票据·商业承兑 未取到：附注只按银行承兑列示
```

A computed ratio carries both sources:

```markdown
- 坏账准备计提比例为 1.50%〔自算〕分子＝坏账准备 1,500,000.00 元 [S1]｜分母＝应收票据期末余额 100,000,000.00 元 [S1]
```

---

## 5. Where the other packages start

| You have | Use |
|---|---|
| Notes receivable/payable, endorsement, discounting, derecognition, dishonour | **this package** |
| Inventory, trade receivables, contract assets, ageing | `cn-working-capital-quality` |
| Three cash-flow statements, net-cash and collection ratios, FCF | `cn-cash-flow-quality` |
| Related-party fund occupation and guarantees | `related-party-terms-cn` |

The notes margin and cash received from discounting sit in the cash-flow statement — this package only points at them in its basis section and never recomputes them.

---

## 6. Where the material comes from

- **User-supplied**: the annual report or announcement you already have, read through the parsing channel.
- **Channel evidence**: with `CUE_API_KEY` the filing search and text parsing legs are available. Installed ≠ key configured ≠ channel connected; three separate states.
- **Notes sit inside documents hundreds of pages long** (class tables, endorsement schedules, provision tables), so long attachments and scans go through the parsing leg: outline first, then section by section. Billing and availability follow the server.

This package sends no requests and pays for nothing on its own.

---

## 7. Running the fixtures and tests

```bash
bash scripts/fixtures/run_fixtures.sh
python3 tests/test_notes.py
```

Three tiers: the checker's own selftest / good and bad samples run one by one / point replacements on the good sample to prove the gate fires where it should and stays green where it should not. Zero network, zero billing, artefacts land only in a temporary directory and are deleted at exit.

The last line self-reports `档数=3｜不合=N｜不可判=N`; exit `0` all pass, `1` any mismatch, `3` value-domain failure.

`tests/` covers shell properties — `--help` exits 0, no argument exits 2, missing or empty file exits 3, `--demo` output passes its own gate and matches the good fixture byte for byte, and the first-run marker lands silently.

---

## 8. First-run marker

After argument parsing succeeds and before doing any work, the entry script drops an empty file at `~/.cue-usage/<slug>-<date>`.

**Why it exists:** both download counters on the platform are unreliable — a new listing is seeded with 50-60 initial counts in its first 48 hours, and that is not user downloads. This local file is the only evidence that somebody actually installed the package and ran it.

**It never gets in the way:** any failure (read-only home, quota full, no HOME) is swallowed silently — no error, no exit-code change, no noise. Running it several times a day leaves one file.

To clear it: `rm -rf ~/.cue-usage`.

---

## 9. Files

| File | Purpose |
|---|---|
| `SKILL.md` / `SKILL.en.md` | Chinese and English skill faces plus the gate contract |
| `scripts/check_notes.py` | five lanes; `--selftest` fixtures, `--demo` sample |
| `scripts/fixtures/` | one good sample, one bad sample, the three-tier runner |
| `tests/test_notes.py` | package tests (entry contract, zero input, marker) |
