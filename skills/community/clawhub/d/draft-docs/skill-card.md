## Description:

Generate first-draft technical documentation from code analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation maintainers use this skill to turn code analysis and a topic prompt into draft Tutorial, How-To, Reference, or Explanation docs for review before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publish mode can move drafts or update navigation in an unintended destination if the target path is chosen incorrectly.

Mitigation: Review the destination path and navigation changes before publishing, especially when using a custom path.

Risk: Generated documentation can be incomplete or misleading if code analysis misses relevant symbols, examples, or project conventions.

Mitigation: Review generated drafts for accuracy, frontmatter, examples, and referenced symbols before publication.

## Reference(s):

- [Diataxis documentation framework](https://diataxis.fr/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown documentation drafts and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes drafts under docs/drafts/ and may update documentation navigation during publish mode.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
