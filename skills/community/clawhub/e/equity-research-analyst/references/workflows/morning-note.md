# Morning Note

description: Draft concise morning meeting notes summarizing overnight developments, trade ideas, and key events for coverage stocks. Designed for the 7am morning meeting format — tight, opinionated, actionable. Triggers on "morning note", "morning meeting", "what happened overnight", "trade idea", "morning call prep", or "daily note".

## Structured Data Source

Use `tradingviewapi` for the overnight numeric and event scan:

- `GET /api/news/stock?lang=en&market_country=US` — US single-name headlines
- `GET /api/news/economic?lang=en` — macro headlines
- `GET /api/news?symbol={symbol}` — company-specific follow-up headlines
- `GET /api/quote/{symbol}?session=regular&fields=all` or `POST /api/quote/batch` — pre/post-market move, volume, session status
- `GET /api/calendar/economic?from=&to=&market=america` — today's macro calendar
- `GET /api/calendar/earnings?from=&to=&market=america` — today's earnings slate

Web Search remains necessary for rumors, full article context, and event types not covered by the structured feed.

## Execution Notes

- If you start from company names, resolve symbols first via `/api/search/market/{query}?filter=stock` and keep the resolved `EXCHANGE:TICKER` as canonical.
- Prefer `GET /api/quote/{symbol}?session=regular&fields=all` or the batch equivalent for overnight / pre-market context. The payload shape is nested, with key quote fields under `data.data`.
- Treat venue-like exchange fields from quote-style payloads as market-data context, not definitive primary-listing metadata.

## Workflow

### Step 1: Overnight Developments

Scan for relevant events across coverage universe:

**Earnings & Guidance**
- Any coverage companies reporting overnight or pre-market? Start with `/api/calendar/earnings`
- Earnings surprises (beat/miss on revenue, EPS, key metrics) from `tradingviewapi` + latest release
- Guidance changes (raised, lowered, maintained) from latest release / transcript

**News & Events**
- M&A announcements or rumors
- Management changes
- Product launches or regulatory decisions
- Analyst upgrades/downgrades from competitors
- Macro data or policy changes affecting the sector from `/api/news/economic` and `/api/calendar/economic`

**Market Context**
- Overnight futures / pre-market moves from `/api/quote/{symbol}?session=regular&fields=all` or `POST /api/quote/batch`
- Sector ETF performance
- Relevant commodity or currency moves
- Key economic data releases today

### Step 2: Morning Note Format

Keep it tight — a morning note should be readable in 2 minutes:

---

**[Date] Morning Note — [Analyst Name]**
**[Sector Coverage]**

**Top Call: [Headline — the one thing PMs need to hear]**
- 2-3 sentences on the key development and why it matters
- Stock impact: price target, rating reiteration/change

**Overnight/Pre-Market Developments**
- [Company A]: One-line summary of earnings/news + our take
- [Company B]: One-line summary + our take
- [Sector/Macro]: Relevant sector-wide development

**Key Events Today**
- [Time]: [Company] earnings call
- [Time]: Economic data release (expectations vs. our view)
- [Time]: Conference or investor day

**Trade Ideas** (if any)
- [Long/Short] [Company]: 1-2 sentence thesis + catalyst
- Risk: What would make this wrong

---

### Step 3: Quick Takes on Earnings

If a coverage company reported, provide a quick reaction:

| Metric | Consensus | Actual | Beat/Miss |
|--------|-----------|--------|-----------|
| Revenue | | | |
| EPS | | | |
| [Key metric] | | | |
| Guidance | | | |

**Our Take**: 2-3 sentences — is this good or bad for the stock? Does it change our thesis?

**Action**: Maintain / Upgrade / Downgrade rating? Adjust price target?

Use `tradingviewapi` for the actuals, quote reaction, and calendar timestamps; use the release / transcript for exact guidance wording.

### Step 4: Output

- Markdown text for email/Slack distribution
- Word document if formal distribution is needed
- Keep to 1 page max — PMs and traders won't read more

## Important Notes

- Be opinionated — morning notes that just summarize news without a view are useless
- Lead with the most important thing — don't bury the headline
- "No news" is a valid morning note — say "nothing material overnight, maintaining positioning"
- Distinguish between actionable events (earnings, M&A) and noise (minor analyst notes, non-events)
- Time-stamp your takes — if you're writing at 6am, note that pre-market may change by open
- If you're wrong, own it in the next morning note — credibility matters more than being right every time
