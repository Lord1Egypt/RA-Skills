# Example 1 — First-run onboarding with Reliance + HDFC Bank

A new user installs the skill and sets up monitoring for two holdings.

## User
> set up stock monitor

## Agent (using the skill)
> Welcome. Here's what this skill does in a nutshell:
>
> 1. It watches your Indian stocks every weekday morning.
> 2. It ONLY pings you when something genuinely critical happens — promoter selling shares, governance failures, cash flow deterioration, surveillance moves, big earnings misses.
> 3. When results come out, it does a deep-dive: not just headline PAT, but cash flow quality, segment trends, and whether management delivered what they promised.
> 4. Most days you'll hear nothing. That's the design.
>
> Want to set it up now? How would you like to share your portfolio?
>
> 1. **Drop a screenshot** of your broker app (Zerodha, Groww, Upstox, Angel One, etc.)
> 2. **Describe in text** (e.g., "10 Reliance at 2900, 50 HDFC Bank at 1620")
> 3. **Skip for now**

## User
> 10 Reliance at avg 1265, 50 HDFC Bank at avg 1620

## Agent
> ```
> Proposed portfolio update:
>
>   ✱ ADD   RELIANCE   qty: 10    avg: ₹1,265   sector: Conglomerate (O2C + Digital + Retail + E&P + New Energy)
>   ✱ ADD   HDFCBANK   qty: 50    avg: ₹1,620   sector: Private Banks (post-merger entity)
>
>   Invested value: ₹12,650 + ₹81,000 = ₹93,650
>   Concentration: HDFCBANK 86.5% / RELIANCE 13.5%
>   ⚠ Note: HDFCBANK is 86.5% of portfolio — that's highly concentrated in a single stock.
>
> Net result: 2 holdings across 2 sectors.
> ```
>
> Apply? (yes / no / edit)

## User
> yes

## Agent
> ✓ Portfolio updated. Backup saved.
>
> A few setup questions:
>
> 1. **Investment horizon**: short-term (<3 months) / medium-term (3–12 months) / long-term (1+ year)?
> 2. **Alert sensitivity**: critical only (recommended) / critical + high / daily digest?
> 3. **Include positive signals** (promoter buying, credit upgrades, contract wins)? yes / no
> 4. **Set up daily 8:30 AM IST scan?** (recommended)

## User
> long-term, critical only, yes for positive signals, yes for daily

## Agent
> ✓ Preferences saved: long-term horizon, critical-only alerts, positive signals enabled.
> ✓ Daily scan scheduled — Mon–Fri at 8:30 AM IST.
>
> Two things to know about your holdings:
> - **RELIANCE** is a conglomerate — I'll track 5 segments separately: O2C (refining + petchem), Jio (Digital Services), Retail, E&P, and New Energy. Consolidated numbers alone don't tell the real story.
> - **HDFCBANK** is post-merger with HDFC Ltd — I'll track merger integration metrics (LDR normalization, branch conversion, PSL compliance) alongside standard banking KPIs.
>
> Want a first-look scan now to flag anything from the last 7 days?
