## Description:

Maintain an agent's long-term memory files: deduplicate, expire stale facts, and keep a clean index. Use on a schedule or whenever memory starts contradicting itself.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manteclaw](https://clawhub.ai/user/manteclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this workflow monthly, after major projects, or when memory appears inconsistent to consolidate duplicate entries, verify or expire stale facts, handle secrets carefully, and refresh the index.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential rotation can interrupt applications or integrations that depend on the credential.

Mitigation: Review the rotation step and plan the change for affected applications or integrations before applying it.

## Reference(s):

- [Agent Memory Hygiene on ClawHub](https://clawhub.ai/manteclaw/skills/agent-memory-hygiene)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Structured memory hygiene report in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports merged, expired, and corrected entries, a secret count only, and the updated index state.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
