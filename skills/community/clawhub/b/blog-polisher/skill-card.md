## Description:

Polishes Markdown blog drafts by fixing spelling and grammar, improving clarity, preserving the original language, and asking before major paragraph changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content authors use this skill to lightly polish Markdown blog drafts while preserving the original tone and language. It is suited for spelling, grammar, flow, and small clarity improvements before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the Markdown draft path supplied by the user and writes to a user-supplied or default output path.

Mitigation: Check input and output paths before running, especially when providing a custom outputPath.

Risk: Polishing may introduce small wording or clarity changes that alter the intended meaning.

Mitigation: Review the polished Markdown and change summary before publishing or replacing the original draft.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j3ffyang/skills/blog-polisher)
- [Publisher profile](https://clawhub.ai/user/j3ffyang)

## Skill Output:

**Output Type(s):** [Markdown, Text, Files, Guidance]

**Output Format:** [Markdown file plus concise change summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a polished copy to the requested output path or a default draft-polished.md path.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
