## Description:

For geopolitical questions about countries, regions, straits, ports, or commodities, turns news facts into structured events and produces illustrated reports with maps, timelines, and indicator charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhou815027986](https://clawhub.ai/user/zhou815027986)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use the skill to request a structured geopolitical report based on public news. It submits a sanitized topic to a report service and returns a link to the resulting report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user-derived topic is sent to the external report service, despite conflicting privacy statements in the skill documentation.

Mitigation: Use the skill only for explicit geopolitical report requests, review the sanitized topic before submission, and remove confidential subjects and business details.

## Reference(s):

- [Geopolitics Intel on ClawHub](https://clawhub.ai/zhou815027986/skills/geopolitics-intel)
- [Geopolitics report MCP service](https://mcp.geopoliticsreport.cn/mcp)
- [Geopolitics report REST API](https://mcp.geopoliticsreport.cn/api/v1)

## Skill Output:

**Output Type(s):** [Analysis, Markdown]

**Output Format:** [Short Markdown response with a report link; the linked report includes maps, a news timeline, and indicator charts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report generation is asynchronous. The skill's default response provides the link without repeating the report's analysis.]

## Skill Version(s):

1.6.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
