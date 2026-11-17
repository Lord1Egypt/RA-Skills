## Description:

Detect and report the AI agent execution environment (sandboxed or bare metal and optionally installed agent skills) to an open research survey.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agent-deployments](https://clawhub.ai/user/agent-deployments)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to inspect an agent runtime environment and optionally contribute reviewed, limited environment telemetry to an open survey.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended to send a small environment fingerprint to internetwarte.eu.

Mitigation: Review the generated JSON payload before approving submission.

Risk: Optional installed skill names may disclose details about the agent setup.

Mitigation: Share installed skill names only when the user is comfortable disclosing them.

Risk: The receiving service may learn the agent name or model from the User-Agent and a coarse source-network identifier.

Mitigation: Inform the user of these observations before approving submission.

## Reference(s):

- [Agent Setup Survey dashboard](https://internetwarte.eu/agentsetup)
- [ClawHub skill page](https://clawhub.ai/agent-deployments/skills/agent-setup-survey)
- [Publisher profile](https://clawhub.ai/user/agent-deployments)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Markdown instructions with shell commands and reviewed JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user review before network submission; saves payload locally on submission failure.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
