## Description:

Convert a book, paper, document, documentation site, or code repository into a structured, on-demand agent skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and engineers use this skill to turn source material such as documents, documentation sites, URLs, and repositories into reusable agent skills while preserving extraction limits and source coverage notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on installing and running an external anything-to-skill CLI.

Mitigation: Review and verify the CLI before running it.

Risk: Generated skills can affect future agent behavior.

Mitigation: Inspect each generated skill before loading or deploying it.

Risk: Web crawls may gather more content than intended.

Mitigation: Keep crawls limited to the documentation scope the user actually wants.

## Reference(s):

- [anything-to-skill releases](https://github.com/asale-ai/anything-to-skill/releases)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the anything-to-skill CLI on PATH; web and repository sources may require network access, and repositories require git.]

## Skill Version(s):

0.2.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
