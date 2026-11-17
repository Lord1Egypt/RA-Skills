## Description:

Self-reflection + Self-criticism + Self-learning + Self-organizing memory. Agent evaluates its own work, catches mistakes, and improves permanently.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to help an agent reflect on completed work, learn from explicit corrections, and maintain local execution-improvement memory across sessions. It supports local memory setup, correction logging, tiered memory organization, and transparent review or deletion of learned entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently change agent behavior by storing learned instructions across sessions.

Mitigation: Require explicit confirmation for first-use setup and every new persistent memory entry; treat memory entries as advisory notes subordinate to current user instructions and safety rules.

Risk: Setup guidance may modify agent steering files such as AGENTS.md, SOUL.md, or HEARTBEAT.md.

Mitigation: Review proposed setup edits before applying them and keep changes scoped to the self-improving memory workflow.

Risk: Local memory could capture sensitive or third-party information if used carelessly.

Mitigation: Follow the documented boundaries against storing credentials, financial, medical, biometric, third-party, location-pattern, or access-pattern data.

Risk: Old or incorrect lessons could continue influencing future agent behavior.

Mitigation: Use audit, source tracking, deletion, export, decay, and confirmation workflows to keep learned entries visible and removable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smallkeyboy/skills/16-self-improving-agent-proactive-self-reflection)
- [Skill homepage](https://clawic.com/skills/self-improving)
- [Security Boundaries](artifact/boundaries.md)
- [Learning Mechanics](artifact/learning.md)
- [Memory Operations](artifact/operations.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local memory files under ~/self-improving/ and proposed agent steering-file edits when enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata; source skill frontmatter reports 1.2.10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
