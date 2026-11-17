## Description:

A 股投研指挥官 orchestrates A-share stock analysis skills into workflows for sector scanning, sector analysis, single-stock deep dives, and portfolio checks, then produces structured investment briefs and Feishu archives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jioup777](https://clawhub.ai/user/jioup777)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to coordinate multiple A-share market analysis skills for opportunity scans, sector research, individual stock reports, and portfolio health checks. It is intended to assemble concise investment briefs, deeper research reports, debate summaries, and operational suggestions from configured market-data sources and companion skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically save investment reports, charts, analyzed symbols, and portfolio details to a fixed Feishu workspace.

Mitigation: Run it only with a controlled Feishu destination, restricted workspace tokens, and explicit approval before each Feishu upload or portfolio-analysis workflow.

Risk: Portfolio health checks may expose sensitive holdings and trading intent to configured external services.

Mitigation: Use local-only or confirmation-first workflows for portfolio inputs, redact holdings when possible, and avoid sharing reports outside approved workspaces.

Risk: Generated market analysis may be incomplete, delayed, or misleading and should not be treated as financial advice.

Mitigation: Require human review of data sources, assumptions, and recommendations before acting on any trading or portfolio suggestion.

Risk: Optional third-party API integrations and dependency installs can broaden credential and supply-chain exposure.

Mitigation: Pin dependencies, scope API tokens narrowly, keep optional tokens unset when not needed, and review all companion skill calls before execution.

## Reference(s):

- [Sub-skill Quick Reference](references/sub-skills.md)
- [ClawHub Skill Page](https://clawhub.ai/jioup777/skills/a-stock-orchestrator)
- [Configured Feishu Archive Space](https://vicyrpffceo.feishu.cn/wiki/EhQ6w2F5yiC0DKkxlzlcEMvIn2f)
- [TradingAgents API](https://api.510168.xyz/v1/analyze)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration instructions, API Calls]

**Output Format:** [Markdown reports with tables, links, optional inline shell commands, and Feishu document output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a three-document report structure: summary brief, deep research report, and bull-bear debate report.]

## Skill Version(s):

2.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
