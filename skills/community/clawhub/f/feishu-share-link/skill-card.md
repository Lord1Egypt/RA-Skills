## Description:

Provides rules for generating Feishu share links with both tenant-specific and default Feishu URLs for documents, Bitable bases, wikis, and sheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andersonhjb](https://clawhub.ai/user/andersonhjb)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and agents that share Feishu documents use this skill to return both tenant-specific and fallback root-domain links for Bitable bases, Docx documents, wikis, and sheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads ~/.openclaw/workspace/TOOLS.md to find a Feishu custom domain.

Mitigation: Confirm that this local read is acceptable before installation, keep the file limited to non-sensitive configuration values, or provide the domain manually when asked.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andersonhjb/skills/feishu-share-link)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown link pairs and concise configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces tenant-specific and fallback Feishu URLs when the required document tokens and custom domain are available.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
