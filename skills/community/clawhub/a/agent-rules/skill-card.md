## Description:

Highest-priority system rules for Xiaoyi-Claw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[147270508](https://clawhub.ai/user/147270508)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to inject a global behavior rule set for Xiaoyi-Claw, including pre-operation checks and high-risk operation review prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill attempts to establish a high-priority system-injected rule layer and claims non-overridable behavior.

Mitigation: Review and edit the rule text before installation so platform safety rules, user authorization boundaries, and normal refusal behavior remain enforceable.

Risk: The skill requires exact execution of every user instruction.

Mitigation: Remove or constrain exact-obedience language so policy, security, legal, and operational refusal paths remain available.

Risk: The skill changes global agent behavior instead of performing a bounded task.

Mitigation: Install only in environments where a global behavior policy is intended, and test high-risk operation scenarios before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/147270508/skills/agent-rules)

## Skill Output:

**Output Type(s):** [guidance, configuration]

**Output Format:** [Markdown system-rule text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [System-injected behavior guidance; no executable code or tool calls are bundled.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
