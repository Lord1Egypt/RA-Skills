## Description: <br>
Monitor competitor websites for changes, analyze updates, and generate competitive intelligence reports tracking pricing, content, features, and significant changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawdio-afk](https://clawhub.ai/user/clawdio-afk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales teams, product managers, and competitive strategists use this skill to monitor public competitor websites, detect pricing, product, content, and messaging changes, and produce competitive intelligence reports and recommended actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monitoring may collect content from target sites whose terms restrict automated access. <br>
Mitigation: Confirm each target site is public and that the monitoring frequency and collection method comply with the site's terms before enabling scheduled snapshots. <br>
Risk: Reports may contain sensitive, non-public, or retained competitive intelligence beyond the intended review window. <br>
Mitigation: Avoid collecting non-public content and set a local retention policy for snapshot and report files before operational use. <br>
Risk: Optional delivery to email, Slack, databases, or webhooks can broaden access to generated reports. <br>
Mitigation: Review and approve every outbound destination before forwarding reports outside the local workspace. <br>


## Reference(s): <br>
- [Competitor Change Monitor on ClawHub](https://clawhub.ai/clawdio-afk/competitor-change-monitor) <br>
- [API & Configuration Guide](references/api-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, and generated JSON snapshot and report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local snapshots and reports under snapshots/ and reports/ when the monitoring script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
