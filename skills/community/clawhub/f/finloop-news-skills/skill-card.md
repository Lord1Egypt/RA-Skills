## Description:

Provides Finloop-based financial news retrieval, categorized news search, AI trending news lookup, and real-time stock quote guidance through direct HTTP API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[czzlegend](https://clawhub.ai/user/czzlegend)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer finance information requests with Finloop market-period news, categorized financial news, AI hot news details, and stock or index quote data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Finance and news queries are sent to external Finloop UAT API domains.

Mitigation: Use the skill only in environments where sending those queries to the documented UAT domains is acceptable.

Risk: The AI hot-news endpoint may require an sl-session cookie.

Mitigation: Do not paste or log session cookies; confirm endpoint ownership and credential scope before use.

Risk: The package is installed through npx and includes an installer that copies skill files into the current project.

Mitigation: Review the skill before installing, prefer a pinned package version, and avoid running npx with elevated privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/czzlegend/skills/finloop-news-skills)
- [Finloop API reference](artifact/.agents/skills/finloop-news-skill/references/REFERENCE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline HTTP, curl, JavaScript, or JSON examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include direct HTTP request instructions and finance or news response fields.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact manifest reports 1.1.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
