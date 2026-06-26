## Description: <br>
Daily monitoring for Indian equity holdings (NSE/BSE) using a documented severity rubric, silent by default and surfacing only Sev-1 events such as governance, cash flow, promoter or pledge, surveillance, earnings, and flow signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daveanandraj](https://clawhub.ai/user/daveanandraj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External investors and agents use this skill to monitor NSE/BSE portfolios, update holdings, and surface critical stock alerts based on a documented severity rubric. It is informational only and not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portfolio details, alert history, and derived monitoring state are stored in local skill files. <br>
Mitigation: Keep local files private, redact account numbers and personal identifiers from broker screenshots, and delete local state files when you stop using the skill. <br>
Risk: Financial alerts can be incomplete, stale, or wrong because they depend on available sources and search quality. <br>
Mitigation: Verify material alerts from primary exchange, regulatory, and company sources before acting; treat all output as informational rather than investment advice. <br>
Risk: Portfolio update workflows can change local holdings, peer mappings, backups, and alert state. <br>
Mitigation: Review the proposed portfolio diff and only approve writes after confirming quantities, prices, sectors, and removals. <br>
Risk: Optional scheduled scans can continue to process local portfolio state on weekdays. <br>
Mitigation: Disable the optional schedule or remove local state files if monitoring is no longer desired. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/daveanandraj/ai-stock-watchdog) <br>
- [README](README.md) <br>
- [Severity rubric](severity-rubric.md) <br>
- [Data sources](sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown alerts and conversational guidance, with JSON state and configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local portfolio, state, backup, and alert files after user confirmation; optional scheduled monitoring can run on weekdays.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release, SKILL.md frontmatter, and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
