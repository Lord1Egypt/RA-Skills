## Description:

Auto-generates comparison tables for concepts, drugs, or study results in Markdown format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts can use this tool to scaffold Markdown comparison tables for concepts, drugs, treatments, or study results from comma-separated items and attributes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional output path can overwrite any writable file path without containment or warning.

Mitigation: Use stdout or a dedicated output directory, avoid absolute or parent-directory paths, and do not let untrusted text choose the output path until overwrite protection and path containment are added.

## Reference(s):

- [Comparison Table Gen References](references/guidelines.md)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/comparison-table-gen)
- [Publisher Profile](https://clawhub.ai/user/aipoch-ai)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files]

**Output Format:** [JSON object containing a Markdown table string and comparison metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The optional output flag writes the JSON result to a caller-provided file path.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
