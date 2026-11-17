## Description:

Daily monitoring for Indian equity holdings (NSE/BSE) using a documented severity rubric; it stays silent by default and surfaces Sev-1 events, quarterly checks, conglomerate segment views, and guidance tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daveanandraj](https://clawhub.ai/user/daveanandraj)

### License/Terms of Use:

MIT-0

## Use Case:

External investors and agent users tracking Indian cash equity portfolios use the skill to onboard holdings, update portfolios conversationally, run manual or scheduled scans, and receive alerts when critical Sev-1 signals affect their holdings. The skill is informational only and does not execute trades or provide investment advice.

### Deployment Geography for Use:

Global, with monitoring focused on Indian NSE/BSE equities.

## Known Risks and Mitigations:

Risk: Holdings, average prices, preferences, alerts, and comparison history are stored in local skill files.

Mitigation: Treat portfolio files as sensitive, review them periodically, and avoid sharing the skill directory with untrusted parties.

Risk: Broker screenshots may expose sensitive account or portfolio information.

Mitigation: Prefer text entry where practical or redact screenshots before using screenshot-based portfolio updates.

Risk: Optional scheduled monitoring can create recurring local state updates and web searches for user holdings.

Mitigation: Enable scheduled scans only when recurring local updates and holding-specific searches are acceptable.

Risk: Financial signals can be incomplete, stale, or wrong and are not investment advice.

Mitigation: Verify material facts against exchange filings or other primary sources before making investment decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/daveanandraj/skills/ai-stock-watchdog)
- [Publisher Profile](https://clawhub.ai/user/daveanandraj)
- [README](README.md)
- [Severity Rubric](severity-rubric.md)
- [Data Sources](sources.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Conversational text, Markdown alerts, and JSON configuration/state file updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores holdings, preferences, alerts, comparison history, and guidance tracking in local skill files; scheduled scans are optional.]

## Skill Version(s):

2.2.0 (source: server release metadata, SKILL.md frontmatter, manifest.json, CHANGELOG released 2026-05-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
