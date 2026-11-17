## Description:

Complete memory architecture for AI agents with tiered local storage, correction-based learning, self-reflection, multi-agent memory sharing, intelligent decay, and bootstrap setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ironmanc2014](https://clawhub.ai/user/ironmanc2014)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to set up persistent local memory for AI agents, including preference storage, correction tracking, compaction, and shared memory patterns for multi-agent teams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can retain sensitive preferences, work context, or personal data longer than intended.

Mitigation: Keep the memory directory private with owner-only permissions, audit stored memory regularly, and avoid storing secrets or sensitive personal data.

Risk: Bootstrap setup has review-worthy path containment concerns when using custom roots, untrusted agent names, or forced overwrites.

Mitigation: Review the target path and agent names before running the bootstrap script, avoid --force unless the target files are known, and test setup in a disposable directory first.

Risk: Broad file permission guidance can expose local memory files to other users on the same system.

Mitigation: Use owner-only permissions for the memory directory and files instead of broad read or execute permissions.

## Reference(s):

- [Memory Architecture](references/architecture.md)
- [Multi-Agent Memory](references/multi-agent.md)
- [Security Boundaries](references/security.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with inline bash commands and local file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local files under an agent-memory directory when the bootstrap script is run.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
