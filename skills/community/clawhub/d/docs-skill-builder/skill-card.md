## Description:

Use when creating a Hindsight-docs-style local documentation skill for another tool, SDK, API, or docs repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theangrypit](https://clawhub.ai/user/theangrypit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to build and refresh local documentation skills for tools, SDKs, APIs, and documentation repositories. It helps map source documentation paths and generate a local skill with mirrored references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Refreshing a generated documentation skill replaces its generated directory and can overwrite local edits.

Mitigation: Keep local edits separately and use pinned mode when reproducible source content is needed.

## Reference(s):

- [Docs Skill Model](artifact/references/docs-skill-model.md)
- [ClawHub release](https://clawhub.ai/theangrypit/skills/docs-skill-builder)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Files, Guidance]

**Output Format:** [Local documentation skill files, mirrored references, and a generator shell script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mirrored documentation is copied verbatim; generated references may be large.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
