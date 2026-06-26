## Description: <br>
Analyze application logs to produce actionable error digests with pattern detection, severity classification, trend analysis, and remediation recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and incident responders use this skill to parse application or server logs, group recurring errors, classify severity, detect trends, and produce remediation-focused reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Logs and generated reports may contain tokens, user data, IP addresses, internal errors, or other sensitive operational details. <br>
Mitigation: Only provide intended log files or folders, avoid supplying credentials, and review or redact reports before sharing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/cm-log-analyzer) <br>
- [Error Pattern Reference](references/error-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Text, JSON, or Markdown log-analysis reports with remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return CI-friendly exit codes based on whether warnings, errors, or fatal log entries are found.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
