## Description:

Provides fork-safe context cloning, message history compaction, and fast session restoration for multi-agent OpenClaw workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suda6632](https://clawhub.ai/user/suda6632)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to preserve parent context when spawning child agents, compact long message histories, and restore local sessions efficiently.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cached context may contain secrets, credentials, private customer data, or sensitive system prompts.

Mitigation: Avoid using the skill with sensitive data until it limits what it stores and adds restrictive cache permissions or encryption.

Risk: Restoring cached snapshots uses unsafe pickle deserialization.

Mitigation: Replace pickle with safe serialization before using the skill outside a controlled local environment.

Risk: Weak session-id and path controls may allow cache confusion or unintended file access patterns.

Mitigation: Validate session identifiers and keep cache files isolated from other users and processes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/suda6632/skills/context-cache-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe local cache behavior and context-management workflows.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
