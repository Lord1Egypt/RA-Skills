## Description:

The one-command magic button for AI-SEO: point it at a site to get a whole-site AEO/GEO audit plus a ready-to-run plan an agent can execute.

This skill is ready for commercial/non-commercial use.

## Publisher:

[automatelab](https://clawhub.ai/user/automatelab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and SEO teams use this skill to audit websites for AI-search visibility and generate a prioritized improvement plan. It produces planning artifacts for review and execution rather than directly editing the site.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on unaudited npm and MCP components with unclear provenance.

Mitigation: Review the CLI source, package manifest, lockfile, and MCP engine provenance before installation.

Risk: The crawler may access private or sensitive site content.

Mitigation: Run in a sandbox or container, avoid elevated privileges, and confirm crawler scope and data handling before using it on private sites.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON plan file and Markdown checklist, with setup shell commands and agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces plan.json and plan.md; execution should be prioritized by severity.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
