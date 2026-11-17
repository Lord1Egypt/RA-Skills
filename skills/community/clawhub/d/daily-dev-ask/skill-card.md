## Description:

Answer technical questions using daily.dev's knowledge base by searching developer community articles and synthesizing answers with source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nimrodkra](https://clawhub.ai/user/nimrodkra)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to search daily.dev's article knowledge base for technical questions, compare relevant results, and receive a source-linked answer grounded in the returned articles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a daily.dev API token that can grant access to personalized content.

Mitigation: Store the token in an environment secret or operating system credential store, never commit it, and send it only to api.daily.dev.

Risk: Technical search queries are sent to daily.dev when the skill performs keyword or semantic searches.

Mitigation: Install and use the skill only when sending those queries to daily.dev is acceptable; avoid sensitive or confidential query text.

Risk: Optional shell-profile auto-load examples can affect future terminal sessions if copied into startup files.

Mitigation: Review profile changes before adding them and prefer scoped environment secrets when available.

## Reference(s):

- [daily.dev Ask on ClawHub](https://clawhub.ai/nimrodkra/skills/daily-dev-ask)
- [daily.dev Plus](https://app.daily.dev/plus)
- [daily.dev API Token Settings](https://app.daily.dev/settings/api)
- [daily.dev Keyword Recommend API](https://api.daily.dev/public/v1/recommend/keyword?q={keywords}&limit=20)
- [daily.dev Semantic Recommend API](https://api.daily.dev/public/v1/recommend/semantic?q={query}&limit=20)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown answer with source links and optional inline shell or PowerShell commands for setup and API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers should be grounded in daily.dev article results, include relevant source links, and state gaps when returned articles only partially answer the question.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
