## Description:

Search research papers and retrieve publication details from Clarity Protocol, including PubMed identifiers, abstracts, citation metrics, and full-text availability when available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarityprotocol](https://clawhub.ai/user/clarityprotocol)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to search Clarity Protocol's literature database, retrieve paper details by PMID, and gather abstracts, citation metrics, and PubMed/Semantic Scholar-derived metadata for literature review and bibliography workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts clarityprotocol.io and may send CLARITY_API_KEY when that environment variable is set.

Mitigation: Review network use before installation and provide the API key only in trusted environments.

Risk: The current search behavior should be treated as a database listing unless the provider adds documented keyword or filtered search.

Mitigation: Use retrieved results as candidate literature records and apply independent filtering for precise search workflows.

Risk: Paper metadata, abstracts, and citation counts may be incomplete or stale.

Mitigation: Verify important citations and publication details against primary publication sources before relying on them.

## Reference(s):

- [Clarity Protocol](https://clarityprotocol.io)
- [Clarity Protocol API](https://clarityprotocol.io/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with JSON or text command output from the bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires internet access to clarityprotocol.io; optional CLARITY_API_KEY increases rate limits.]

## Skill Version(s):

1.0.0 (source: skill metadata and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
