## Description:

Apollo Immu helps an agent intercept risky actions before execution and uses trust accumulation to reduce repeated confirmation prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nic-yuan](https://clawhub.ai/user/nic-yuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to gate sensitive actions such as file deletion, outbound messaging, command execution, and permission changes before an agent proceeds. It is intended to reduce repeated confirmations for familiar recipient-operation pairs while keeping higher-risk actions confirmation-gated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The trust-learning logic can reduce confirmations for sensitive actions based on casual conversation cues.

Mitigation: Review before installing and keep sensitive sends, permission changes, command execution, and deletion operations confirmation-gated until trust updates require explicit approval.

## Reference(s):

- [Apollo Immu ClawHub Skill Page](https://clawhub.ai/nic-yuan/skills/apollo-immu)
- [Automatic Trust Learning Guide](references/auto_learn.md)
- [Risk Level Reference](references/risk_levels.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance, configuration]

**Output Format:** [Markdown guidance with bash commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local trust state in assets/trust_db.json]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
