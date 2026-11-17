## Description:

Self-improvement loop that reads learnings, errors, and memory, detects patterns, and updates skills/protocols automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dodge1218](https://clawhub.ai/user/dodge1218)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run a self-improvement loop that scans prior errors, learnings, corrections, and memory, then updates persistent playbooks or proposes changes based on risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to rewrite persistent instructions, memory, or playbooks.

Mitigation: Use it only in controlled workspaces and review proposed changes before they alter skills, AGENTS.md, SOUL.md, or memory files.

Risk: Automatic improvement loops can preserve incorrect lessons or overfit to repeated errors and corrections.

Mitigation: Require review for medium- and high-impact updates, and verify that each proposed change is grounded in observed errors, learnings, or user corrections.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dodge1218/skills/dsb-auto-improve)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with proposed file edits, code snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update persistent skill, protocol, memory, reminder, or ticket files when permitted by the host agent workflow.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
