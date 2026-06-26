# Severity Rubric — AI stock watchdog v2

The skill MUST stay silent unless a Sev-1 trigger is hit. Sev-2 only lands in the optional dashboard. Sev-1 = "the user should see this within hours."

**Core philosophy**: The rubric gives high weight to promoter/pledge and insider changes, governance and regulatory action, cash flow quality vs reported profit, and sector-wide shocks. Ordering and thresholds are a design choice, not a guarantee of outcomes.

---

## Sev-1 — CRITICAL (Notify the user immediately)

### A. Promoter & insider signals (high weight in this rubric)

**Promoter holding decline:**
- Promoter holding dropped >2 percentage points in latest quarterly shareholding pattern (QoQ)
- Promoter holding dropped below 50% (control threshold) for the first time
- Promoter sold via open market (not OFS/block) — ANY amount is a red flag
- Promoter entity reclassified out of promoter group

**Promoter pledge escalation:**
- Pledge increased >5 percentage points QoQ
- Total pledge crossed 50% of promoter holding (liquidation risk territory)
- Pledge crossed 75% (imminent margin call risk)
- Pledge + encumbrance (non-disposal undertaking) crossed 40% combined
- Lender invoked pledged shares (even partial)

**Insider trading red flags:**
- KMP (CEO/CFO/CS) sold shares within 30 days before results (check SAST/PIT disclosures)
- Multiple independent directors sold in the same quarter
- Designated persons sold >25% of their holding in a single quarter

### B. Governance / trust collapse

- Auditor resignation mid-cycle (any reason — always material in India; rotation doesn't count)
- Auditor qualification or adverse opinion in latest annual report
- Emphasis of matter paragraph mentioning going concern, fraud investigation, or regulatory non-compliance
- SEBI order (adjudication, interim, show-cause) naming the company, promoter, or KMP
- ED / CBI / IT raid or investigation naming the company or promoter
- Forensic audit ordered by board or regulator
- CEO/MD or CFO resignation without named successor within 7 days
- CEO + CFO exit within 90 days of each other (classic pre-fraud-discovery pattern)
- Independent director resignation citing governance concerns or "personal reasons" within 6 months of joining
- Whistleblower complaint reported by reputable media
- Restatement or revision of past financials (any period)
- Related party transactions jumped >50% YoY without proportionate revenue growth
- Auditor changed mid-tenure to a smaller/less reputable firm

### C. Surveillance / regulatory red flags

- Stock entered GSM Stage 2 or higher (Stage 1 alone = Sev-2)
- Stock entered ASM Long-term additional surveillance framework
- Stock moved to Trade-to-Trade (T2T) segment
- Trading suspended or halt imposed by exchange
- Circuit limit reduced (from 20% to 10%, or 10% to 5%)
- SEBI debarment order against promoter/KMP
- NSE/BSE issued clarification letter and company response was evasive or delayed

### D. Capital structure / solvency stress

- Credit rating downgrade by ≥2 notches OR downgrade to below investment grade (below BBB-)
- Credit rating placed on "watch with negative implications" (not just "negative outlook")
- Debt-to-equity jumped >30% QoQ in latest results
- Interest coverage ratio fell below 1.5x (debt servicing at risk)
- Default or delay on debt servicing (even technical default)
- Company drew down emergency credit lines or raised expensive short-term debt
- Debt maturity wall: >30% of total debt maturing within 12 months with inadequate cash/facilities
- Convertible instrument (FCCB/OCD/CCD) conversion triggered at adverse terms

### E. Earnings shock (when quarterly results are out)

**Revenue & profit:**
- Revenue miss >20% vs consensus OR >15% below same quarter last year without one-off explanation
- PAT miss >25% vs consensus
- Operating loss reported for first time in 8+ quarters
- Revenue degrowth for 2nd consecutive quarter (trend confirmation)

**Margin deterioration:**
- EBITDA margin compression >300 bps QoQ without one-off explanation
- Gross margin compression >500 bps QoQ (input cost pass-through failure)
- FY guidance cut >15% on revenue OR >200 bps on margin

**Cash flow quality (THE most underrated check — catches window dressing):**
- Cash flow from operations (CFO) negative while PAT is positive (classic red flag)
- CFO/PAT ratio below 0.5x for 2+ consecutive quarters (accrual-heavy, cash-light earnings)
- CFO/PAT ratio diverging: PAT growing while CFO is flat or declining over 3+ quarters
- Significant increase in "other income" as % of PBT (>25%) without clear treasury/investment explanation
- Trade receivables growing >2x revenue growth rate for 2 consecutive quarters
- Inventory buildup >1.5x revenue growth for 2 consecutive quarters
- Exceptional/extraordinary items used to inflate PAT for 2+ of last 4 quarters

**Working capital deterioration:**
- Working capital cycle (inventory days + receivable days - payable days) increased >15 days QoQ
- Net working capital turned negative to positive (company now funding WC from debt, not operations)
- Receivable days crossed 90 (collection risk in Indian context)

**Tax rate anomalies:**
- Effective tax rate below 15% without SEZ/tax holiday explanation (aggressive planning signal)
- Sharp ETR swing (>10pp) QoQ without disclosed reason (reserves/write-backs manipulation)

### F. Concall delta signals

Sev-1 if 2+ of these hit simultaneously. Any single one = Sev-2.

- Management explicitly mentions demand weakness / slowdown in core segment
- Capex plan cut >20% vs prior guidance
- Order book / pipeline declining QoQ for 2nd consecutive quarter
- Tone shift on guidance: "confident/strong" language replaced with "cautious/watchful/challenging"
- Pricing pressure or competitive intensity called out as NEW development
- Customer concentration risk disclosed (top client >15% of revenue)
- Management unable to provide forward guidance (previously used to guide)
- Concall significantly shorter than usual with fewer analyst questions taken

**Management credibility check (track over time in state):**
- Management guided X in previous quarter, delivered <70% of guided number → low credibility flag
- 2+ consecutive quarters of missing own guidance → credibility score drops, weight all management statements lower

### G. Litigation / business disruption

- Adverse Supreme Court or High Court ruling with quantifiable financial impact >5% of market cap
- Loss of a top-3 customer (by revenue share) or key licence/contract
- Plant/facility shutdown lasting >7 days with >10% revenue impact
- Cyber/data breach disclosed to exchanges
- Major product recall or quality failure
- Anti-trust (CCI) order with penalty >2% of revenue
- Environmental clearance revoked or NOC denied for expansion project
- Key raw material supply disrupted (>30 day impact)

### H. Sector-wide regulatory shocks (map to held stocks)

- Government ban, export restriction, or sharp duty change on company's primary product
- RBI action: PCA framework, lending restrictions, digital lending curbs (for banks/NBFCs)
- USFDA Warning Letter or Import Alert (for pharma — held stock or 2+ peers)
- TRAI tariff order change (telecom)
- IRDAI product/pricing regulation change (insurance)
- MoEFCC clearance policy shift affecting mining/metals/power
- GST rate change with direct revenue line impact on held stock

### I. Short-term triggers (elevated weight when user horizon = short-term)

- Block/bulk deal: promoter or >5% shareholder sold ≥1% of equity
- Single-day fall ≥7% on volumes >3x 20-day average
- 52-week low breached on >2x average volume
- FII holding cut >2 percentage points in quarterly disclosure
- Stock entered F&O ban period (derivative settlement pressure)
- Open interest buildup >30% with price decline >3% (short buildup)

### J. Conglomerate-specific triggers (for multi-segment companies like Reliance, Tata, Adani)

- Segment EBIT turned negative for any major segment (>10% of revenue)
- Cross-subsidization: profitable segment margin declining while loss-making segment scales
- Holding company discount widened >30% vs sum-of-parts NAV
- Key subsidiary IPO/demerger cancelled or delayed
- Intercompany loans or guarantees crossed >20% of standalone net worth

---

## Sev-1 POSITIVE — Actionable good news (notify if user preference allows)

These don't trigger alerts by default (silence-first design) but are logged and shown on request or in daily_brief mode:

- Promoter increased holding via open market purchase (strong conviction signal in India)
- Company announced buyback (especially if at premium to CMP)
- Credit rating upgrade by ≥1 notch
- Stock exited GSM/ASM surveillance framework
- Major new contract win >10% of annual revenue
- Received regulatory approval pending for >6 months (USFDA ANDA, SEBI, RBI licence)
- Debt repaid ahead of schedule / became debt-free
- Institutional investor (marquee PE/sovereign fund) picked up >1% stake

---

## Sev-2 — Dashboard only (do NOT push notification)

- GSM Stage 1 entry (no immediate action, but watch)
- Single brokerage downgrade (note target price change)
- Single concall warning sign (doesn't meet 2+ threshold for Sev-1)
- Peer earnings miss or guidance cut (industry signal, not direct)
- Mutual fund net selling >0.5% of equity in latest month-end data
- Single block deal 0.5–1% of equity by non-promoter institutional investor
- 200-DMA breakdown on normal volume
- Sector derating (PE compression) without company-specific trigger
- Promoter pledge increased 1–5 percentage points (below Sev-1 threshold but worth noting)
- Management missed guidance by 10–30% (below credibility-collapse threshold)
- Trade receivables growing faster than revenue for 1 quarter (not yet 2-quarter trend)
- CFO/PAT ratio between 0.5x–0.7x for 1 quarter
- Company in MSCI/Nifty rebalancing exclusion list (passive flow risk)
- FII holding cut 1–2 percentage points
- ADR/GDR discount widened significantly (for dual-listed stocks)

---

## Sev-3 — Log only (never surface)

- Routine corporate actions (dividend declaration, AGM notice, routine board meeting)
- Minor management changes below KMP level
- Regular brokerage initiating coverage or reiterating rating
- Macro news without direct sector mapping to held stocks
- Index rebalancing inclusion (generally positive but not actionable)
- Routine SEBI circular not specific to company/sector
- Stock split / bonus announcement (mechanical, not fundamental)
- ESG rating change by third-party agency

---

## Context modifiers (adjust severity based on these)

### Peer-relative adjustment
If the entire sector (3+ peers) fell >5% on the same day, a single stock falling 7% is less alarming — reduce from Sev-1 to Sev-2. Conversely, if the stock fell 7% while peers are flat/up, elevate urgency.

### Horizon adjustment
- **Short-term holder**: Elevate all Section I triggers by one level. Block deals, volume spikes, and F&O ban are immediately actionable.
- **Long-term holder**: Demote single-day price triggers by one level UNLESS accompanied by a fundamental trigger (governance, earnings, capital structure). A 7% drop alone is noise for a long-term holder.

### Position size adjustment
If the stock is >25% of portfolio value (concentration risk), elevate any Sev-2 trigger to Sev-1. The user has outsized exposure and deserves earlier warning.

### Market regime
During broad market corrections (Nifty down >10% from recent high), individual stock price drops need a higher threshold to qualify as Sev-1 (raise single-day fall threshold from 7% to 12%). During bull markets, lower the threshold (5%).

---

## Decision rule

Notify the user IF AND ONLY IF:
1. At least one Sev-1 trigger fires for a held stock NOT flagged in last 14 days, OR
2. At least 2 Sev-1 triggers fire across peers in same sector within 7 days (industry stress), OR
3. Quarterly workflow concluded EXIT BIAS or WATCH on a held stock, OR
4. Portfolio health check found concentration risk >30% in a single stock with any Sev-2+ signal on that stock.

When in doubt, default to silence. False positives erode trust faster than missed Sev-2 signals.
