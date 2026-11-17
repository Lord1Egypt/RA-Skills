# Task playbooks

Short recipes. Adapt names and numbers to the task. Every recipe ends with the Done criteria in SKILL.md.
Start every new task with `agentbox now`, and `agentbox note clear --apply` if `agentbox note list` shows notes from an older task.

## Stock briefing (price, move, context)

```bash
agentbox now
agentbox quote get NVDA ^GSPC
agentbox quote history NVDA --range 1mo
agentbox search "Nvidia stock news" --news --time week --max-results 5 --save 2
agentbox read doc:1 --grep Nvidia
agentbox calc "(237.47 - 180.2) / 180.2 * 100"
```

Report price, change %, quote time, 1-month change from `summary`, 52-week range, and 1-3 cited news drivers. Add the delay note.

## Event lookup (what happened, when, where)

```bash
agentbox search "Computex 2026 dates venue" --max-results 5 --save 2
agentbox read doc:1 --grep 2026
agentbox extract doc:1 doc:2 --kind dates --grep June
```

Confirm the date in two sources if you can. Use `agentbox now` to tell past from upcoming.

## Executive lookup

```bash
agentbox search "Nvidia CEO" --max-results 5 --save 3
agentbox extract doc:1 doc:2 doc:3 --kind people --grep CEO
agentbox search "Jensen Huang biography" --site nvidia.com --save 1
agentbox report build "Nvidia CEO profile" --template exec-lookup --out exec.md --apply
```

Prefer the company's own leadership page and recent press. Give the full name, exact title, since when, and one or two cited facts.

## Pricing research / comparison

```bash
agentbox search "Asana pricing per user per month" --max-results 4 --save 2
agentbox search "ClickUp pricing per user per month" --max-results 4 --save 2
agentbox extract doc:1 doc:2 doc:3 doc:4 --kind prices --save-table
agentbox table query tbl:1 --where "per = user" --where "period = month" --sort value --select value,raw,url
agentbox report build "Project tool pricing" --template compare --columns "Tool,Entry price (USD/user/mo),Free tier,Source" --out pricing.md --apply
```

Fetch the vendor's own pricing page when a search result is a third-party blog. State the billing period (monthly or yearly) for each price.

## Polymarket briefing (top N markets)

```bash
agentbox now
agentbox market trending --tag politics --limit 10
agentbox market get balance-of-power-2026-midterms
agentbox note add 'Democrats Sweep trades at 63.5%, +2 pts in a day' --source https://polymarket.com/event/balance-of-power-2026-midterms --tag item1
agentbox report build "Polymarket politics brief" --template market-brief --n 3 --out brief.md --apply
agentbox report check brief.md --template market-brief --n 3
```

Pick N distinct events. For each: question, current %, move in points, 24h volume, end date, event URL. Note the snapshot time.

## EU regulation research

```bash
agentbox search "AI Act general-purpose AI obligations timeline" --site europa.eu --max-results 5 --save 3
agentbox read doc:1 --grep obligation
agentbox extract doc:1 doc:2 --kind dates --grep 2025
agentbox report build "EU AI Act GPAI obligations" --template brief --out eu.md --apply
```

Cite official sources first (`eur-lex.europa.eu`, `digital-strategy.ec.europa.eu`). Give the regulation number, who it applies to, key dates, and penalties if asked.

## Open-source alternatives

```bash
agentbox search "open source alternative to Notion self-hosted" --max-results 8 --save 3
agentbox extract doc:1 doc:2 doc:3 --kind links --site github.com
agentbox fetch https://github.com/AppFlowy-IO/AppFlowy
agentbox read doc:4 --grep license
agentbox report build "Open-source Notion alternatives" --template top-n --n 3 --out oss.md --apply
```

For each project: name, license, what it replaces, and the repo URL. Check the license on the repo page.

## Competitive research

```bash
agentbox search "Figma competitors 2026" --max-results 6 --save 3
agentbox search "Penpot pricing" --max-results 3 --save 1
agentbox extract doc:1 doc:2 doc:3 --kind prices --save-table
agentbox report build "Figma competitive landscape" --template compare --columns "Competitor,Price,Strengths,Weaknesses" --out comp.md --apply
```

One row per competitor. Use the same facts for each (price, target user, key feature).

## IT procurement (shortlist vendors)

```bash
agentbox search "business laptop 16GB RAM price Lenovo ThinkPad T14" --max-results 5 --save 2
agentbox extract doc:1 doc:2 --kind tables
agentbox table query tbl:2 --where "Memory >= 16" --sort Price
agentbox report build "Laptop shortlist" --template compare --columns "Option,Price,Specs,Warranty,Source" --out shortlist.md --apply
```

Check the requirement list (budget, specs, support) and show which option meets each. Sum totals with `agentbox calc`.

## Deep research (open question, many sources)

```bash
agentbox search "small modular reactors cost per MWh 2025" --max-results 8 --save 4
agentbox search "SMR cost estimate criticism" --max-results 5 --save 2
agentbox read doc:1 --grep MWh
agentbox note list
agentbox report build "Cost of small modular reactors" --template brief --out research.md --apply
```

Use 3+ independent sources. Note where sources disagree and give both numbers with citations.

## BYOK (bring your own key) best practices

```bash
agentbox search "BYOK API key best practices environment variables secret manager" --max-results 6 --save 3
agentbox read doc:1 --grep rotate
agentbox report build "BYOK best practices" --template brief --out byok.md --apply
```

Cover: keep keys in environment variables or a secret manager, never in code or chat; least privilege; rotation; per-environment keys; revocation. Never print a real key. Do not run `agentbox config set`.
