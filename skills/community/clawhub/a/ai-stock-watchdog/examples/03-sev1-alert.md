# Example 3 — Multi-signal alert: HDFC Bank governance + Reliance segment check

The daily scan fires at 8:30 AM IST. Most days, nothing. This day, two signals.

## Trigger
Scheduled daily scan fires.

## What the skill does (silently)
1. Reads portfolio.json — 2 holdings: RELIANCE (5 shares), HDFCBANK (75 shares)
2. Portfolio health: HDFCBANK at 95% concentration — flag noted
3. Market calendar: Not an MPC week, no budget, no expiry week
4. Global cues: Brent crude up 3.2% overnight → note for Reliance O2C (mild positive for GRM, but not Sev-1 level)
5. Per-stock scan begins

### HDFCBANK findings:
- Exchange filing: Chairman resigned, board commissioned external law firm review
- News: Q4 NIM compressed 15 bps QoQ to 3.44%, NII grew only 3.2% YoY
- Cash flow: CFO healthy at 1.1x PAT — no manipulation flag
- Promoter holding: stable (no HDFC entity sold post-merger)
- Severity classification: Chairman exit + legal review = Sev-1 governance trigger
- Context modifier: 95% portfolio concentration → ELEVATE urgency

### RELIANCE findings:
- News: Jio added 8.2M subscribers in Q4, ARPU up ₹3 QoQ to ₹206
- O2C: Singapore GRM at $6.2/bbl (stable), petchem spreads tightening slightly
- Retail: 680 new stores in Q4, revenue/sqft up 4%
- No Sev-1 triggers. Jio/Retail numbers are Sev-1 POSITIVE (logged, included since user opted in).

## What the user sees

> 🔴 STOCK ALERT — 2026-05-01
>
> **HDFCBANK — Governance red flag at the top + NIM pressure**
> Severity: Sev-1 | Category: Governance / Trust Collapse | Sector: Private Banks
>
> **What happened:**
> Atanu Chakraborty, part-time Chairman and Independent Director, resigned effective 18 March 2026. Keki Mistry appointed interim Chairman for 3 months. The board has commissioned external law firms (domestic and international) to review the contents of his resignation letter — an unusual step that signals the board believes the resignation may contain material concerns requiring independent investigation.
>
> Separately, Q4 FY26 results show NIM compressed 15 bps QoQ to 3.44%. NII grew only 3.2% YoY — the weakest growth since the HDFC Ltd merger. Post-merger LDR remains elevated at 104%, pressuring deposit mobilization costs.
>
> **Why it matters for YOU (long-term holder, avg ₹1,607, 75 shares — 95% of portfolio):**
> - Chairman exit + board-level legal review is an early-warning governance signal. In Indian banking history, board-level upheavals preceded regulatory interventions at Yes Bank, ICICI Bank (2018), and DHFL.
> - NIM compression in a rising/stable rate environment suggests the merged book's cost of funds is structurally higher than standalone HDFC Bank.
> - **Critical**: This stock is 95% of your portfolio. Any further deterioration disproportionately impacts your entire capital.
>
> **Suggested action:** WATCH CLOSELY. Do not add to position.
> Escalation triggers to EXIT BIAS:
> - Adverse findings from law firm review
> - No permanent chairman announced by mid-June 2026
> - NIM compression continues in Q1 FY27 (below 3.35%)
> - Any RBI observation in the annual inspection report
>
> **Confidence:** Medium-High
> **Management credibility:** MEDIUM (guided "NIM normalization by H2 FY26" — did not deliver)
>
> **Sources:**
> - [HDFC Bank Q4 FY26 Results — Business Standard](https://www.business-standard.com/companies/quarterly-results/)
> - [HDFC Bank Chairman resignation filing — BSE](https://www.bseindia.com/corporates/ann.html)
>
> **Counter-view:** Resignations can happen for personal/policy reasons. Franchise quality, asset quality (GNPA 1.33%), and deposit franchise remain strong. Legal review could be precautionary governance best practice.
>
> **Portfolio impact:** This is 95% of your invested capital. Given extreme concentration, even Sev-2 signals on this stock warrant your attention.

---

> 🟢 POSITIVE NOTE — 2026-05-01
>
> **RELIANCE — Jio + Retail momentum continues**
>
> Jio added 8.2M net subscribers in Q4 FY26, ARPU up ₹3 QoQ to ₹206 (street expected ₹204). Reliance Retail opened 680 stores, revenue per sqft improved 4% YoY. O2C segment stable with Singapore GRM at $6.2/bbl.
>
> No action needed. Logged for context. This holding is only 5% of your portfolio.

## What happens next
- HDFCBANK alert archived to `alerts/2026-05-01-alert.md`
- `state/last-run.json` updated with signal IDs, management credibility scores, and guidance tracker
- Same HDFCBANK governance signal suppressed for 14 days
- Promoter holding/pledge data stored for QoQ comparison next quarter
