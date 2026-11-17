## Description:

Query AV new releases, rankings, and actress info from FANZA GraphQL API. No authentication required. Supports direct curl queries and optional Discord/Telegram bot deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxcnny930](https://clawhub.ai/user/zxcnny930)

### License/Terms of Use:

PolyForm Noncommercial 1.0.0; commercial use requires a separate license from the author

## Use Case:

External users and developers use this skill to ask an agent for FANZA adult-content release, ranking, performer, and keyword queries, usually expressed as curl-based GraphQL requests or summarized result guidance. Users must be adults and are responsible for complying with local laws and service terms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill queries an unofficial adult-content FANZA endpoint that may change, become unavailable, or return content unsuitable for some users or jurisdictions.

Mitigation: Use the on-demand curl examples only when adult-content access is appropriate, comply with local laws and service terms, and handle API errors or empty results gracefully.

Risk: The optional Discord/Telegram bot path asks users to run mutable external code persistently and handle messaging tokens.

Mitigation: Review and pin the cloned code and dependencies, avoid committing or passing tokens in command URLs, and run any service under a dedicated locked-down user rather than root.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zxcnny930/skills/avbuzz)
- [ClawHub publisher profile](https://clawhub.ai/user/zxcnny930)
- [FANZA GraphQL endpoint](https://api.video.dmm.co.jp/graphql)
- [FANZA product page pattern](https://www.dmm.co.jp/digital/videoa/-/detail/=/cid={id}/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with curl examples, JSON response shape guidance, and optional deployment snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [On-demand FANZA GraphQL query guidance; optional Discord and Telegram bot configuration guidance]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
