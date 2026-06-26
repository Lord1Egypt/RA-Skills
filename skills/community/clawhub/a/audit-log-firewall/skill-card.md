## Description: <br>
Policy-based monitoring and command-line enforcement for high-risk agent operations that intercepts sensitive commands and logs them for human auditing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[balkanblbn](https://clawhub.ai/user/balkanblbn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to enforce command-line review checkpoints for high-risk operations and retain a local audit trail of terminal activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local audit log can contain sensitive commands, paths, usernames, or operational context. <br>
Mitigation: Define who can read .logs/SECURITY.json and establish redaction, retention, and cleanup practices before using the skill in sensitive environments. <br>
Risk: An incomplete allowlist can either block expected work or miss risky command patterns. <br>
Mitigation: Review and maintain config/allowlist.json for the deployment environment, and require human approval for commands outside the expected policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/balkanblbn/audit-log-firewall) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and local JSON audit records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May pause high-risk command execution for human review and may write command audit records to .logs/SECURITY.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
