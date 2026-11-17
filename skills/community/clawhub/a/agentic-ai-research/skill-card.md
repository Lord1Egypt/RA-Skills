## Description:

Searches recent top-conference and top-journal Agentic AI research, filters papers through the H=(E,T,C,S,L,V)+P lens, reads abstracts and introductions to understand contributions, and produces a human-readable literature review with optional local wiki compilation after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neuhanli](https://clawhub.ai/user/neuhanli)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and technical teams use this skill to survey recent Agentic AI work in a chosen area, understand paper contributions, and produce a readable Markdown literature review. When explicitly confirmed by the user, it can compile the review into a local project wiki.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted wiki page metadata may cause generated Markdown files to be written outside the intended wiki folder.

Mitigation: Use the optional wiki workflow only with trusted content, or first validate topic slugs and enforce that generated files stay under wiki/topics.

Risk: Optional dependency installation may introduce supply-chain or environment risk.

Mitigation: Review and pin dependencies before installation, and avoid running installation commands in privileged or credential-rich environments.

Risk: Literature-search outputs can contain incomplete or misleading paper summaries.

Mitigation: Review the generated literature review, search log, and cited paper evidence before relying on conclusions or compiling them into a wiki.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neuhanli/skills/agentic-ai-research)
- [README.md](artifact/README.md)
- [schema-guide.md](artifact/references/schema-guide.md)
- [page-authoring.md](artifact/references/page-authoring.md)
- [cascade-update.md](artifact/references/cascade-update.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown literature review, with optional local wiki Markdown pages and JSON index metadata after user confirmation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses WebSearch for literature discovery and local Python scripts for the optional wiki workflow; wiki writes require explicit user confirmation.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
