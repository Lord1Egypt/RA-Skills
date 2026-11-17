## Description:

Use when the user asks for institutional-style equity research on a public company, ETF, or TradingView-resolvable ticker, including initiation reports, earnings updates or previews, catalyst calendars, morning notes, sector or peer overviews, thesis reviews, model refreshes, and stock screening or idea generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hypier](https://clawhub.ai/user/hypier)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to produce institutional-style equity research deliverables for public companies, ETFs, and TradingView-resolvable tickers. It routes requests into focused workflows for initiation reports, earnings work, market notes, sector overviews, thesis tracking, model refreshes, catalyst calendars, and idea generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may require persistent plaintext RapidAPI credential setup for live market-data access.

Mitigation: Use a project-scoped environment variable or secret manager and avoid storing credentials in shell startup files when possible.

Risk: Live third-party market-data calls can be unavailable, stale, or inconsistent with primary company disclosures.

Mitigation: Validate current dates, cite fetched endpoints, and confirm material financial facts against company filings, investor-relations releases, or SEC sources.

Risk: Unpinned charting dependencies and generated code can behave differently across environments.

Mitigation: Run generated code in a virtual environment with pinned dependencies before relying on charts or analysis outputs.

Risk: Workbook or model edits can overwrite user financial models.

Mitigation: Back up Excel workbooks before allowing edits and review all model changes before use.

## Reference(s):

- [TradingView API Endpoint Map](references/tradingviewapi.md)
- [TradingView API OpenAPI Specification](references/tradingviewapi-docs/openapi.json)
- [TradingView API Docs README](references/tradingviewapi-docs/README.md)
- [Initiating Coverage Workflow](references/workflows/initiating-coverage.md)
- [Earnings Analysis Workflow](references/workflows/earnings-analysis.md)
- [Earnings Preview Workflow](references/workflows/earnings-preview.md)
- [Catalyst Calendar Workflow](references/workflows/catalyst-calendar.md)
- [Morning Note Workflow](references/workflows/morning-note.md)
- [Sector Overview Workflow](references/workflows/sector-overview.md)
- [Thesis Tracker Workflow](references/workflows/thesis-tracker.md)
- [Model Update Workflow](references/workflows/model-update.md)
- [Idea Generation Workflow](references/workflows/idea-generation.md)
- [Initiation Report Template](assets/initiating-coverage/report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, cited analysis, generated code or shell commands, and report-oriented document instructions depending on the active workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require user-provided RapidAPI credentials, live market-data calls, web research, SEC or investor-relations source checks, chart generation, and workbook or document handling.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
