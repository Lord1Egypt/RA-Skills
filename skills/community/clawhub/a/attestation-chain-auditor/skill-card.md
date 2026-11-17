## Description:

Helps validate the completeness and integrity of trust attestation chains in AI agent ecosystems by identifying broken links, expired credentials, and missing vouching relationships that make verified trust claims unverifiable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud)

### License/Terms of Use:


## Use Case:

Developers, trust reviewers, and marketplace operators use this skill to audit whether a skill or agent has a complete, current, and independently verifiable attestation chain from the subject to a root of trust.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may use curl or python3 to fetch or process attestation metadata during an audit.

Mitigation: Provide only the attestation documents, URLs, or identifiers intended for review, and review any proposed fetches before allowing access to private systems.

Risk: Opaque or unpublished chain metadata can limit the audit to identifying missing information rather than reconstructing the chain.

Mitigation: Treat unknown, opaque, or undocumented links as verification gaps until supporting attestation metadata is supplied.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/skills/attestation-chain-auditor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown attestation chain audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a user-provided skill or agent identifier, attestation chain document, or list of vouching relationships; no credential inputs are required.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
