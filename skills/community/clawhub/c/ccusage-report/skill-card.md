## Description: <br>
Report Claude Code token consumption and costs using ccusage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spideystreet](https://clawhub.ai/user/spideystreet) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Claude Code users use this skill to summarize local Claude Code token usage and costs by day, week, month, or specific date range. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Usage reports may be generated with a Europe/Paris timezone assumption, which can shift date-range interpretation for users in other timezones. <br>
Mitigation: Before relying on the report for billing, budgeting, or operational decisions, verify the timezone used by ccusage and adjust or reinterpret the requested date range. <br>
Risk: The skill invokes ccusage through bunx, so reporting depends on bunx availability and local Claude Code session data. <br>
Mitigation: Confirm bunx is installed and local Claude Code usage data is available before treating missing or empty output as authoritative. <br>


## Reference(s): <br>
- [Claude Code Usage Report README](artifact/README.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/spideystreet/ccusage-report) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown-formatted usage report with optional shell command execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bunx ccusage output; supports daily, weekly, and monthly summaries with optional per-model breakdowns.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
