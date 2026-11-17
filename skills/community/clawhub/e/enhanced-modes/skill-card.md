## Description:

Provides three agent working modes: Explore for read-only analysis, Plan for thinking before acting, and Verify for checking results, with feature flags for toggling additional capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayiv-ai](https://clawhub.ai/user/mayiv-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to switch an agent between exploration, planning, and verification behaviors, and to manage optional feature flags for memory, coordination, and background work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory and logging behavior may retain information without enough scoping or retention detail.

Mitigation: Keep auto_memory disabled unless persistent memory processing is required, and inspect any memory or state files the skill creates.

Risk: Background automation can initiate agent work on a timer when enabled.

Mitigation: Keep autonomous_crons disabled unless explicitly needed, and review scheduled behavior before enabling it.

Risk: Installing through an unpinned installer can make the installed behavior harder to reproduce.

Mitigation: Use a pinned and trusted ClawHub installer version when installing the skill.

## Reference(s):

- [Enhanced Agent Modes on ClawHub](https://clawhub.ai/mayiv-ai/skills/enhanced-modes)
- [Mayiv-Ai Publisher Profile](https://clawhub.ai/user/mayiv-ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with slash commands and feature-flag settings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes mode commands and feature defaults; optional persistent memory and background automation features are disabled by default.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
