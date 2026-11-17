## Description:

Extracts structured text and Markdown from web pages, PDFs, office documents, and images using the Docling CLI, with optional GPU-accelerated OCR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[er3mit4](https://clawhub.ai/user/er3mit4)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to extract clean, structured content from known URLs, PDFs, office documents, images, and scanned material before analysis or summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs, including destinations reachable from the local network.

Mitigation: Use only trusted URLs and run extraction in a sandbox or environment with restricted network egress, especially on shared agents, servers, CI runners, or machines with private-network access.

Risk: Remote services and external plugins can send content to remote endpoints or load third-party code.

Mitigation: Avoid enabling remote services or external plugins unless they have been reviewed and approved for the documents being processed.

Risk: Unpinned Docling installations can change parsing behavior or dependency exposure over time.

Mitigation: Pin the Docling package version for deployed agents and re-review security guidance when upgrading.

## Reference(s):

- [Docling CLI Reference](references/cli-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/er3mit4/skills/docling)
- [Publisher Profile](https://clawhub.ai/user/er3mit4)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and file-output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for running the docling CLI and reading generated extraction files from controlled output directories.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
