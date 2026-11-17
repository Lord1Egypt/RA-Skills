## Description:

Defines a multi-agent collaboration protocol for OpenClaw that governs file handovers, acknowledgment loops, cross-channel routing, identity mapping, and context retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[libaie](https://clawhub.ai/user/libaie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to coordinate OpenClaw multi-agent pipelines with explicit file handovers, route-aware acknowledgments, channel-safe mentions, and termination signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The protocol asks agents to access private session history and system configuration broadly.

Mitigation: Review before installation in environments with private histories or broad configuration files; prefer task-scoped summaries and narrow identity lookup data.

Risk: Outbound group messaging and routing fields could send acknowledgments or errors to an unintended channel or user.

Mitigation: Validate routing fields against trusted task metadata before using messaging tools in real channels.

Risk: File handovers depend on agents respecting a shared-directory boundary.

Mitigation: Keep handoff files in the designated shared directory and reject task paths outside that boundary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/libaie/skills/advanced-collab-protocol)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with structured routing and acknowledgment examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes file handoff rules, routing envelope format, mention syntax examples, and safety constraints.]

## Skill Version(s):

1.4.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
