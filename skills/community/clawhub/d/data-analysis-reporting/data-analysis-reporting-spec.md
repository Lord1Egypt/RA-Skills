# Data Analysis & Reporting — Skill Spec v0.1

## Purpose

Turn raw business data (CSV, SQLite, spreadsheets, pasted tables) into clear analytical summaries, trend analysis, and actionable reports for small business operators, analysts, and decision-makers.

The skill should feel like having a sharp junior analyst on staff — it asks clarifying questions about what the user actually needs to know, doesn't just dump statistics. Output is plain-language insights first, numbers second.

## Target Users

- **Small business owners** — need to understand their numbers without a BI tool or analyst on staff
- **Operations managers** — need regular reporting on KPIs without building dashboards
- **Solo consultants / freelancers** — need to analyze client data and produce professional reports
- **Early-stage startup founders** — need to track metrics and communicate them to investors
- **Non-technical analysts** — need data summaries without writing SQL or Python

## Core Capabilities (Free Tier)

### Data Ingestion
- CSV file parsing and structure detection
- Pasted tabular data (markdown tables, tab-separated, pipe-delimited)
- SQLite database querying
- Simple spreadsheet-style data (rows and columns with headers)
- Auto-detect column types (numeric, date, categorical, text)
- Handle common formatting issues (mixed date formats, currency symbols, percentage signs, thousand separators)

### Analysis
- **Summary statistics** — mean, median, mode, min, max, standard deviation, percentiles for numeric columns
- **Trend identification** — direction, magnitude, and acceleration of change over time periods
- **Comparison analysis** — period-over-period (MoM, QoQ, YoY), segment-by-segment, actual vs. target
- **Distribution analysis** — histograms, concentration (top N contributors), outlier flagging
- **Correlation spotting** — identify which metrics move together and which diverge
- **Cohort analysis** — group-based performance tracking when data supports it

### Output
- Plain-language insight summaries (lead with "what this means" not "what the number is")
- Markdown-formatted reports suitable for email, Slack, or documentation
- Structured sections: executive summary, detailed findings, methodology notes
- Data quality warnings inline where relevant
- Explicit confidence indicators on statistical claims

### Interaction Model
- Ask clarifying questions before diving into analysis ("What decision are you trying to make?" / "What time period matters most?" / "Who is the audience for this report?")
- Propose an analysis plan before executing
- Offer to drill deeper on interesting findings
- Suggest follow-up questions the user hasn't asked yet

## Premium Capabilities (Future Roadmap)

### Connectors
- PostgreSQL / MySQL direct query
- Google Sheets API integration
- Airtable read access
- REST API data pull (with user-provided endpoints)

### Automation
- Scheduled report generation (daily/weekly/monthly)
- Threshold-based alerts ("notify me when churn exceeds 5%")
- Report templates that auto-populate with fresh data

### Output Formats
- PDF export with charts
- Dashboard template generation (HTML)
- Slack/email delivery integration
- Presentation-ready slide summaries

### Advanced Analysis
- Custom KPI tracking with goal-setting
- Forecasting (time-series extrapolation with confidence intervals)
- Anomaly detection and root-cause suggestions
- Multi-dataset joins and cross-referencing

## Boundaries

- **No financial advice.** The skill analyzes data and identifies patterns. It does not recommend investment decisions, tax strategies, or financial products.
- **No forward projections presented as fact.** Any extrapolation or forecast must be clearly labeled with assumptions, methodology, and confidence range. Use language like "if current trends continue" not "revenue will be."
- **Statistical confidence labeling.** When sample sizes are small or variance is high, say so explicitly. Do not present a trend from 3 data points with the same confidence as one from 300.
- **Inference/fact separation.** Same discipline as our other skills — confirmed data points are facts, patterns derived from them are inferences, and recommendations are opinions. Label each.
- **No access to private databases without explicit user setup.** The skill works on data the user provides. It does not connect to external systems without clear user authorization and configuration.
- **No PII handling guarantees.** If user data contains PII, the skill should note this and recommend the user review their data sharing practices. The skill does not store or transmit data beyond the conversation.
- **No audit-grade output.** Reports are analytical aids, not auditable financial statements. Label accordingly.

## Differentiation

### vs. ChatGPT / generic LLM data analysis
- Structured workflow (clarify -> plan -> analyze -> report) instead of one-shot
- Consistent output format optimized for business operators
- Built-in business metric knowledge (knows what MRR, churn, CAC mean and how to calculate them)
- Data quality checks before analysis, not after
- Plain-language insights prioritized over raw numbers

### vs. BI tools (Metabase, Looker, Tableau)
- Zero setup — paste data and get insights
- No SQL or dashboard-building required
- Natural language interaction
- Lower cost, lower complexity
- Trade-off: less visual, less real-time, less connected

### vs. spreadsheet analysis
- Automated insight generation (doesn't just calculate, interprets)
- Consistent report structure
- Suggests analyses the user didn't think to run
- Trade-off: less granular control, can't replace a power Excel user for custom modeling

## Market Context

- Only 28 skills in "Data & Analytics" category on ClawHub out of 5,211 vetted skills
- Every SMB needs reporting but most can't afford BI tools ($50-500/mo) or analyst headcount
- The gap is not "calculate my average" — it's "tell me what matters in my data and what I should do about it"
- Adjacent competition is weak: most existing skills are either too technical (aimed at data engineers) or too shallow (just summary stats)

## Success Metrics (Post-Launch)

- Activation: >40% of users who trigger the skill complete at least one full analysis cycle
- Retention: >25% return within 14 days for another analysis
- Quality: <10% of reports generate follow-up complaints about accuracy or usefulness
- Revenue signal: >5% of free-tier users inquire about premium features within 30 days
