## Description: <br>
Use when the user asks for institutional-style equity research on a public company, ETF, or TradingView-resolvable ticker, including initiation reports, earnings updates or previews, catalyst calendars, morning notes, sector or peer overviews, thesis reviews, model refreshes, and stock screening or idea generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hypier](https://clawhub.ai/user/hypier) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to guide agent-generated equity research workflows, including initiation reports, earnings analysis, previews, catalyst calendars, morning notes, sector reviews, thesis tracking, model updates, and idea generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated ratings, price targets, and trading ideas may influence investment decisions. <br>
Mitigation: Treat outputs as research drafts, require qualified human review before use, and preserve source citations for numeric claims. <br>
Risk: The skill requires a RapidAPI key and makes third-party market-data calls. <br>
Mitigation: Use a dedicated key with appropriate limits, avoid embedding secrets in skill files, and review external data-sharing implications before installation. <br>
Risk: The skill may create or update local research files and financial models. <br>
Mitigation: Run it in a dedicated workspace, keep backups, and require confirmation before overwrites or archive extraction. <br>
Risk: Trading-community content and market-data feeds may be incomplete, stale, or untrusted. <br>
Mitigation: Cross-check important claims against primary company filings, investor-relations materials, and current market data before relying on them. <br>


## Reference(s): <br>
- [Skill Dispatcher](SKILL.md) <br>
- [TradingView API Structured Data Reference](references/tradingviewapi.md) <br>
- [TradingView API Docs](references/tradingviewapi-docs/README.md) <br>
- [Initiating Coverage Workflow](references/workflows/initiating-coverage.md) <br>
- [Earnings Analysis Workflow](references/workflows/earnings-analysis.md) <br>
- [Idea Generation Workflow](references/workflows/idea-generation.md) <br>
- [Initiation Report Template](assets/initiating-coverage/report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, cited research prose, API request examples, and file-oriented report instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation or updates of local research files, charts, financial models, and DOCX-style report deliverables.] <br>

## Skill Version(s): <br>
1.0.0 (source: target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
