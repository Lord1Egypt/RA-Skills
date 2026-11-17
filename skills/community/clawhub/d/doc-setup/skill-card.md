## Description:

Organizes, summarizes, and indexes technical documentation from repositories, websites, and manuals into numbered, source-linked Markdown notes and setup guides.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brauliodiasribeiro](https://clawhub.ai/user/brauliodiasribeiro)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and documentation maintainers use this skill to turn raw documentation into navigable knowledge bases with indexes, topic files, source attribution, and setup steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read or fetch source documentation and summarize it into local notes, which may expose private or authenticated documentation if those sources are provided.

Mitigation: Provide only source URLs or folders intended for documentation output, and avoid private or authenticated sources unless summarizing them into local notes is intended.

Risk: Generated documentation may become stale or may summarize source material incorrectly.

Mitigation: Keep original source links in each file, mark outputs as living documents, and review generated summaries before relying on them.

## Reference(s):

- [Doc Setup ClawHub release](https://clawhub.ai/brauliodiasribeiro/skills/doc-setup)
- [Workflow Patterns](references/workflow-patterns.md)
- [Output Examples](references/output-examples.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files with source links, tables, checklists, and optional code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates numbered files such as 00-index.md and NN-topic.md, with living document markers when applicable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
