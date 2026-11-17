## Description:

Guides agents in setting up or maintaining a wiki with a shared schema, consistent pages, and agent-facing instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dexio](https://clawhub.ai/user/dexio)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams using agents to maintain a knowledge base can establish a wiki schema, organize existing notes, and give agents consistent writing and review rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changes to the wiki schema or agent instructions can influence future agent behavior.

Mitigation: Review the generated schema and any AGENTS.md or CLAUDE.md changes before adopting them.

Risk: Sensitive information could be copied into a durable wiki.

Mitigation: Keep secrets and credentials out of wiki pages.

## Reference(s):

- [Wiki schema template](assets/SCHEMA.template.md)
- [ClawHub skill release](https://clawhub.ai/dexio/skills/dexio-wiki-setup)

## Skill Output:

**Output Type(s):** [Markdown, Configuration instructions]

**Output Format:** [Wiki schema and README Markdown, with agent instruction snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Adapts page structure, metadata, and review rules to the wiki.]

## Skill Version(s):

1.2.0 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
