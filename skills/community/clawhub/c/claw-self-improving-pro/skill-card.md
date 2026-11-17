## Description:

Self-reflection + Self-criticism + Self-learning + Self-organizing memory. Agent evaluates its own work, catches mistakes, and improves permanently. Use before starting work and after responding to the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[williamwang-wh](https://clawhub.ai/user/williamwang-wh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to maintain a local self-improvement memory that records explicit corrections, reusable preferences, and self-reflection lessons across sessions. It supports scoped memory, correction tracking, promotion and demotion rules, and user-visible deletion or export flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory can influence future agent behavior across sessions.

Mitigation: Enable the skill only when persistent behavioral memory is desired, review setup changes before adding them to agent steering files, and audit memory contents regularly.

Risk: Memory exports, archives, and retained correction history may preserve information longer than expected.

Mitigation: Avoid storing sensitive personal, credential, financial, medical, or third-party information, and use the documented forget and export workflows to review or remove retained data.

Risk: Unclear deletion and consent boundaries can cause unwanted preference retention.

Mitigation: Require confirmation for inferred preferences, keep learned rules visible with source tracking, and verify deletion by showing the updated memory state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/williamwang-wh/skills/claw-self-improving-pro)
- [Clawic self-improving skill homepage](https://clawic.com/skills/self-improving)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local markdown memory files under ~/self-improving/ when the user enables the workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter version: 1.2.10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
