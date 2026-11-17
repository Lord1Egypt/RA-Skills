## Description:

Add or remove emoji reactions on Feishu (Lark) messages, and respond to user reactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[magicaldd](https://clawhub.ai/user/magicaldd)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to let an agent add, remove, and respond to Feishu message reactions when a Feishu channel is configured with the required reaction permission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe input handling in the reaction script can turn message or emoji arguments into local Python code execution.

Mitigation: Require input validation and safe JSON/config parsing fixes before use in shared or production workspaces.

Risk: The skill can send Feishu reactions using local app credentials.

Mitigation: Install only from a trusted publisher and restrict who can trigger the skill.

Risk: Proactive reactions may be sent when they are not wanted.

Mitigation: Avoid proactive mode unless the workspace explicitly wants that behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/magicaldd/skills/feishu-reaction)

## Skill Output:

**Output Type(s):** [shell commands, guidance, configuration]

**Output Format:** [Markdown guidance with bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Feishu message ID, emoji type, and optional remove action.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
