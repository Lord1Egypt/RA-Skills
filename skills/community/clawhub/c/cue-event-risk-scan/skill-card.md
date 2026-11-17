## Description:

This skill creates a traceable company scan card covering penalties and regulatory measures, external guarantees as a proxy surface, and sanctions enforcement when relevant, while identifying unreached areas and avoiding overall risk scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

External users, compliance teams, and due diligence analysts can use this skill to prepare a sourced company scan card from a company name or six-digit code. The card records retrieved items and unreached surfaces for human review; it does not provide an overall risk rating or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated external lookups can disclose company identifiers and research interests to Cue, and the security review calls for end-to-end validation of HTTPS destinations and redirects.

Mitigation: Avoid the current authenticated shell example. For offline connectivity inspection, use --catalog-file without --post; use a reviewed, pinned release and confirm destination and redirect validation before authenticated use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huhoo/skills/cue-event-risk-scan)
- [Cue MCP catalog](https://cuecue.cn/api/mcp-catalog)
- [Cue MCP configuration](https://cuecue.cn/hub/mcp)
- [Cue API key setup](https://cuecue.cn/hub/api-key)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown company scan card with sourced rows, status declarations, and pending human checks]

**Output Parameters:** [1D (one company per card)]

**Other Properties Related to Output:** [Lists retrieved information and explicitly names unreached surfaces; does not score overall risk or infer that zero results mean no risk.]

## Skill Version(s):

0.2.25 (source: SKILL.md frontmatter; server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
