## Description:

Retrieves bibliographic information for articles, book chapters, and books by resolving a supplied DOI or searching Crossref metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carlosdelfino](https://clawhub.ai/user/carlosdelfino)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agents use this skill to look up DOI records, identify likely Crossref matches, and return concise bibliographic metadata with uncertainty noted when matching is weak.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided DOI text can be placed directly into curl commands.

Mitigation: Validate DOI values, percent-encode path components, and avoid constructing shell command strings from raw user input before execution.

## Reference(s):

- [Crossref REST API documentation](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)
- [DOI resolver](https://doi.org/)
- [ClawHub Doi Search release page](https://clawhub.ai/carlosdelfino/skills/doi-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with DOI links, bibliographic fields, and concise uncertainty notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and curl; uses public DOI.org and Crossref REST endpoints without an API key.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
