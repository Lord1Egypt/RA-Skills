## Description:

Agent Hand helps users monitor and manage multiple AI agent sessions from a unified terminal dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weykon](https://clawhub.ai/user/weykon)

### License/Terms of Use:

MIT-0

## Use Case:

Solo developers, founders, and other users running multiple AI coding agents use this skill to understand, install, and operate Agent Hand as a terminal command center for session monitoring, switching, and hook-based detection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The one-line installer downloads and runs mutable remote code.

Mitigation: Prefer a pinned release or installer, inspect it before execution, and verify a checksum when available.

Risk: Hook installation may make broad persistent changes across multiple agent configurations.

Mitigation: Review what `agent-hand hooks install` changes before enabling it and confirm there is a clear uninstall path.

## Reference(s):

- [ClawHub Agent Hand Skill Page](https://clawhub.ai/weykon/skills/agent-hand)
- [Agent Hand Website](https://agent-hand.dev)
- [Agent Hand GitHub Repository](https://github.com/weykon/agent-hand)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include installation commands, key bindings, pricing notes, and operational guidance for a terminal dashboard.]

## Skill Version(s):

0.3.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
