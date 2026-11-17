## Description:

Enriches prospect and company profiles by scraping their website and searching for additional context to build comprehensive profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariokarras](https://clawhub.ai/user/mariokarras)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and marketing teams use this skill to build a single-company prospect profile for outreach, partnership research, competitive analysis, or deal preparation by combining the prospect's website content with external search context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prospect company names, URLs, and research goals may be sent to external Firecrawl or Exa services during enrichment.

Mitigation: Use only authorized public prospect data, disclose external service use where required, and avoid confidential or non-public prospect lists unless approved.

Risk: The skill examples place user-provided company names and URLs directly into shell commands.

Mitigation: Validate URLs and company names, quote or sanitize command arguments, and review commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mariokarras/skills/abm-prospect-enrichment)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown profile with tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sections ask the agent to label confirmed versus inferred information and include confidence ratings.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
