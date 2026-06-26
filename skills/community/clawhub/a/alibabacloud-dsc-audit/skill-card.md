## Description: <br>
Query and handle security risk events from Alibaba Cloud Data Security Center. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud security operators and engineers use this skill to inspect unprocessed Alibaba Cloud Data Security Center risk events and manually mark confirmed events with an audit note. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Alibaba Cloud credentials and profiles are sensitive, and over-permissive credentials could expose more cloud access than this workflow needs. <br>
Mitigation: Use a dedicated RAM user or role with only yundun-sddp:DescribeRiskRules and, when handling is required, yundun-sddp:PreHandleAuditRisk; do not paste access keys into chat, shell history, or logs. <br>
Risk: Handling a RiskId performs a manual action on a Data Security Center risk event. <br>
Mitigation: Confirm the active profile, exact RiskId, and handling note before running the handling script; use the read-only RAM policy when the agent should only query events. <br>


## Reference(s): <br>
- [Data Security Center API Reference](references/related-apis.md) <br>
- [Data Security Center RAM Permission Configuration](references/ram-policies.md) <br>
- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Alibaba Cloud Python SDK Generic Invocation Documentation](https://help.aliyun.com/zh/sdk/developer-reference/generalized-call-python) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The query script prints risk event summaries; the handling script prints validation, operation status, and request identifiers.] <br>

## Skill Version(s): <br>
0.0.2 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
