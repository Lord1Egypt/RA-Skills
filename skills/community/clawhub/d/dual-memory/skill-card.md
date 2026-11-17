## Description:

Combines OpenClaw's local memory-core with SuperMemory cloud memory in one memory plugin so agents can search local and cloud memories, keep MEMORY.md and dreaming support, and persist context across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dobrinalexandru](https://clawhub.ai/user/dobrinalexandru)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to run local memory-core and SuperMemory-backed cloud memory through one OpenClaw memory slot. It is intended for agents that need local MEMORY.md and dreaming support while also retaining cross-session or cross-device memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables cloud-backed memory capture and search through SuperMemory, which can send memory queries and captured conversation-derived content to an external service.

Mitigation: Install only when that data flow is acceptable, configure the SuperMemory API key deliberately, and disable autoCapture or narrow capture scope for sensitive work.

Risk: The skill depends on a separately installed sibling SuperMemory extension with broad OpenClaw plugin privileges.

Mitigation: Verify and pin the exact sibling extension version before deployment, and treat that extension as part of the trusted runtime.

## Reference(s):

- [Dual memory on ClawHub](https://clawhub.ai/dobrinalexandru/skills/dual-memory)
- [dobrinalexandru publisher profile](https://clawhub.ai/user/dobrinalexandru)
- [SuperMemory](https://supermemory.com)
- [SuperMemory skill on ClawHub](https://clawhub.ai/skills/supermemory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with configuration snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OpenClaw plugin configuration and operational guidance for local and cloud memory behavior.]

## Skill Version(s):

1.0.11 (source: server release evidence; artifact frontmatter reports 1.0.7 and package.json reports 1.0.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
