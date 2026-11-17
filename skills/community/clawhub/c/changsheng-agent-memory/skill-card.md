## Description:

Cross-session memory recovery helps AI agents resume work by loading core memory and checking for changes before re-reading secondary files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccy123abcd](https://clawhub.ai/user/ccy123abcd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use ChangSheng to configure local session-start memory recovery, handovers, and decision recall across their files. It helps agents resume ongoing work without repeatedly re-reading unchanged secondary material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic recovery may load unintended or outdated memory when discovered paths and proposed cleanup are not reviewed.

Mitigation: Review discovered memory paths before enabling automatic recovery, keep essential rules on the always-read list, and review proposed cleanup.

Risk: The keyword gate and editable memory budget are helpers, not security boundaries.

Mitigation: Retain the agent's normal permission controls and do not rely on these helpers as a substitute.

## Reference(s):

- [Memory System Design](references/memory-system.md)
- [ChangSheng on ClawHub](https://clawhub.ai/ccy123abcd/skills/changsheng-agent-memory)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown and JSON memory files, shell commands, and recovery guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local file-based outputs; Python standard library only, with optional host automation.]

## Skill Version(s):

0.99.0 (source: frontmatter, CHANGELOG, released 2026-10-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
