## Description:

Long-term memory system for OpenClaw agents. Store, retrieve, and query conversation history and learned information across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigas](https://clawhub.ai/user/indigas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to give OpenClaw agents durable local memory for preferences, decisions, learnings, and session context across conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and reuses long-term conversation context, which may retain sensitive or stale information and influence future prompts.

Mitigation: Do not store secrets or sensitive personal data, review injected memories before relying on them, and prune or expire memories that are no longer appropriate.

Risk: Local memory import, deletion, and test behavior can cause data loss or introduce untrusted memory records if run against a real home directory.

Mitigation: Back up the memory store before deletion or import, import only trusted files, and test with an isolated storage path.

Risk: Unpinned installation examples can make it harder to verify the exact code being installed.

Mitigation: Prefer pinned, verified ClawHub release sources before deployment.

## Reference(s):

- [Memory Types Reference](references/memory-types.md)
- [ClawHub Skill Page](https://clawhub.ai/indigas/skills/claw-memory-augment)
- [Publisher Profile](https://clawhub.ai/user/indigas)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, YAML configuration, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read, write, import, export, summarize, and inject local memory records according to the configured storage and retention settings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
