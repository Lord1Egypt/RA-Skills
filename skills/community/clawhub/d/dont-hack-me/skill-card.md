## Description: <br>
Security self-check for Clawdbot/Moltbot that audits clawdbot.json for exposed gateway bind, missing auth, weak tokens, open DM or group policies, loose permissions, and plaintext secrets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peterokase42](https://clawhub.ai/user/peterokase42) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to review Clawdbot or Moltbot configuration for common security misconfigurations and to receive proposed fixes for unsafe settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases may lead an agent to read sensitive Clawdbot configuration without a clearly targeted opt-in. <br>
Mitigation: Invoke the skill only with an explicit request for this security check and review the report before sharing it. <br>
Risk: The skill can propose changes to authentication, tokens, gateway binding, DM or group policy, and file permissions. <br>
Mitigation: Review each proposed fix before approving edits and update paired clients if a gateway token is replaced. <br>
Risk: Reports may include details about local tokens, secrets, or configuration weaknesses. <br>
Mitigation: Avoid pasting or publishing the full report unless sensitive values and environment details have been removed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/peterokase42/dont-hack-me) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with PASS, WARN, FAIL, or SKIP statuses and optional shell commands or configuration edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to clawdbot.json and permission changes after user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
