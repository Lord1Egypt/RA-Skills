# Changelog

All notable changes to this skill are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this skill adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] — 2026-05-04

### Changed
- Display name updated to **AI stock watchdog** on ClawHub listing (slug remains `indian-stock-monitor`)
- All user-facing references (README, SKILL.md heading, severity-rubric, sources, LICENSE, data file comments) updated to "AI stock watchdog"
- Removed mistakenly created separate `ai-stock-watchdog` skill from ClawHub

## [2.1.1] — 2026-05-03

### Changed
- Toned down marketing language in SKILL.md, README.md, manifest.json, and severity-rubric.md (removed unverifiable claims; descriptions now state what the skill does and its limits)
- Rubric philosophy and section headers no longer imply guaranteed predictive power
- `sources.md`: removed named-company callouts in section titles (kept topic-based headings)

## [2.1.0] — 2026-05-03

### Changed
- Removed all agent-specific references — skill is now fully agent-agnostic (works with OpenClaw, Claude Code, Codex, Copilot)
- Removed hardcoded stock names from methodology — SKILL.md uses generic placeholders; specific stocks are reference data in competitors.json only
- Updated install instructions to follow ClawHub conventions (`openclaw skills install`)
- Compatibility section now lists platforms generically instead of version-pinning to a specific LLM
- Examples use "Agent" instead of model-specific names
- Emptied ticker_to_sector for clean first-run state

## [2.0.0] — 2026-05-03

### Added — Methodology overhaul based on 20-year Indian market advisor perspective

**Promoter & insider monitoring (new — highest-impact addition):**
- Full QoQ promoter holding tracking against quarterly shareholding patterns
- Promoter pledge escalation detection with tiered thresholds (5pp jump, 50% crossed, 75% margin-call territory)
- Encumbrance (pledge + non-disposal undertaking) combined tracking
- Insider trading (SAST/PIT) disclosure monitoring for KMP pre-results selling
- Lender pledge invocation detection

**Cash flow quality analysis (new — catches manipulation):**
- CFO vs PAT ratio tracking over quarters (below 0.5x for 2+ quarters = Sev-1)
- CFO trend divergence from PAT trend (growing profits with flat/declining cash flow)
- Trade receivable / inventory growth vs revenue divergence
- Working capital cycle deterioration detection
- Tax rate anomaly detection

**Conglomerate segment analysis (new — critical for Reliance, L&T, ITC):**
- Segment-level revenue and EBIT tracking per quarter
- Cross-subsidization pattern detection (profitable segment funding loss-making)
- Full segment mapping for Reliance (O2C, Jio, Retail, E&P, New Energy), HDFC Bank (Retail, Wholesale, Treasury), L&T, and ITC
- Segment-specific peer comparison and regulatory watch
- Sum-of-parts awareness

**Management credibility tracking (new):**
- Guidance extraction from concalls — store specific numbers
- Forward comparison: did management deliver what they promised?
- Credibility score (HIGH/MEDIUM/LOW) based on guidance delivery over quarters
- Two consecutive misses = automatic credibility downgrade

**Portfolio health check (new):**
- Concentration risk detection (>30% single stock, >40% single sector)
- Sector correlation warnings (3+ stocks in same sector)
- Promoter group concentration check
- Liquidity risk flagging (low-volume stocks)
- STCG vs LTCG holding period tracking (365-day boundary)
- Unrealized P&L awareness (anchor bias detection)

**India market calendar awareness (new):**
- RBI MPC week detection
- Union Budget window
- GST Council meeting
- F&O monthly/quarterly expiry volatility context
- Result season windows
- Market holiday detection

**Positive signal tracking (new — opt-in):**
- Promoter open market buying (strong conviction signal)
- Buyback announcements
- Credit rating upgrades
- GSM/ASM exit
- Major contract wins
- Institutional (PE/sovereign fund) stake pickup

**Banking-specific quarterly analysis (new — for HDFC Bank, ICICI, etc.):**
- NIM tracking (QoQ bps change)
- CASA ratio trend
- GNPA/NNPA and slippage ratio
- Credit cost
- CD ratio (Credit-Deposit) with risk thresholds
- Provision coverage ratio (PCR) trend
- Post-merger integration metrics for HDFC Bank

### Changed
- Severity rubric expanded from 4 sections to 10, with context modifiers (peer-relative, horizon-adjusted, position-size-weighted, market-regime-aware)
- Quarterly deep-dive now covers cash flow statement, balance sheet quality, segment analysis, related party transactions, contingent liabilities, auditor emphasis of matter — not just P&L headline numbers
- Sources expanded with SEBI adjudication, shareholding pattern filings, sector-specific data sources, India market calendar links, and copy-paste search query templates
- Competitors.json restructured with conglomerate segment mapping, sector regulator mapping, and expanded peer lists
- All examples rewritten with realistic Reliance + HDFC Bank scenarios
- Notification format now includes management credibility score, portfolio concentration context, and holding-period-specific impact

### Security
- Removed `mcp__workspace__bash` from all tool references (v1.0.1 change carried forward)
- `mcp__scheduled-tasks__create_scheduled_task` remains optional-only

## [1.0.1] — 2026-05-03

### Security
- Removed `mcp__workspace__bash` (unused, flagged in OpenClaw review)
- Moved scheduled-tasks to optional with graceful fallback

## [1.0.0] — 2026-05-01

### Added
- Initial release
- Daily monitoring workflow for NSE/BSE
- Conversational portfolio management (text + screenshot)
- First-run onboarding
- Severity rubric (Sev-1/2/3)
- Quarterly workflow with QoQ/YoY comparison
- Sector peer monitoring
- Auto-backup of portfolio.json
- Alert suppression (14-day window)
- Support for 7+ broker screenshot formats
- 30+ sector peer mappings

### Out of scope (deliberately)
- F&O / derivatives
- Mutual funds / ETFs
- US/global stocks
- Trade execution

## Roadmap (planned)

### [2.1.0] — possible additions
- Beneish M-Score (earnings manipulation probability scoring)
- Piotroski F-Score tracking over quarters
- Trendlyne / Screener API integration (if APIs become available)
- Telegram / WhatsApp notification adapters
- Interactive HTML dashboard artifact
- Concall transcript caching for faster repeat comparisons

### [2.2.0] — under consideration
- Multi-portfolio support (separate "core" and "tactical" books)
- Tax-optimized trim suggestions (STCG vs LTCG aware rebalancing)
- Indexed peer-relative valuation (P/E, P/B, EV/EBITDA vs sector median)
- Custom severity rubric weights per user
