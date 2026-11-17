## Description:

Researches codebases and crafts professional RFC proposals for GitHub publication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zz0116](https://clawhub.ai/user/zz0116)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to analyze codebases, research prior art, design evidence-based improvements, and draft RFCs for open-source projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish GitHub issues using the user's credentials without a clear final confirmation step.

Mitigation: Before publication, require the agent to show the target repository, files to be written, issue title and body, labels, and credential source, and proceed only after explicit user approval.

Risk: Research documents and RFCs may include private code details, sensitive repository context, or unsupported claims.

Mitigation: Review generated documents for sensitive information and verify that claims are backed by cited code locations, issues, discussions, or research references before sharing externally.

## Reference(s):

- [Code Research Crafter GitHub Homepage](https://github.com/zz0116/code-research-crafter)
- [Academic Research Guide](references/academic-research-guide.md)
- [Architecture Patterns](references/architecture-patterns.md)
- [RFC Template](references/rfc-template.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown documents with code blocks, shell commands, and optional GitHub issue publication]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce research-context.md, proposal.md, proposal.docx, rfc-[slug].md, and a GitHub issue link when publication is approved.]

## Skill Version(s):

1.1.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
