## Description:

Unlimited organized memory for your AI agent. Store, search, and organize projects, contacts, decisions, and knowledge across categories. Never lose context again.

This skill is ready for commercial/non-commercial use.

## Publisher:

[certainlogicai](https://clawhub.ai/user/certainlogicai)

### License/Terms of Use:

Business Source License 1.1

## Use Case:

External users and developers use this skill to give an agent a local, file-based memory system for long-term notes about projects, people, decisions, knowledge, and collections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist sensitive personal, client, business, or preference information in local plaintext files.

Mitigation: Store only information the user is comfortable keeping as local plaintext, avoid secrets and regulated data, and periodically review or remove sensitive entries.

Risk: Built-in memory sync can duplicate private context into the local memory folder.

Mitigation: Confirm exactly what will be copied before syncing, keep sync read-only from built-in memory, and avoid syncing confidential or regulated data.

Risk: Manual indexes and keyword search can become stale or miss relevant context.

Mitigation: Maintain category INDEX.md files, add searchable keywords to entries, and archive or split large categories when search becomes slow or unreliable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/certainlogicai/skills/ai-agent-memory)
- [AI Agent Memory skill instructions](artifact/SKILL.md)
- [Setup guide](artifact/setup.md)
- [Memory templates](artifact/memory-template.md)
- [Organization patterns](artifact/patterns.md)
- [Troubleshooting guide](artifact/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and local file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and updates local plaintext Markdown files under the user's memory directory.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
