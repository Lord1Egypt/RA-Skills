## Description:

Guides agents in retrieving and interpreting Chinese A-share market data through ashareapi's REST API and SDKs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashareapi](https://clawhub.ai/user/ashareapi)

### License/Terms of Use:

MIT

## Use Case:

Developers and analysts use this skill to select A-share data endpoints, interpret market and financial fields, and write REST or SDK queries for analysis and backtesting. It provides data-access guidance, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unreviewed skill archive could contain unexpected instructions or files.

Mitigation: Prefer the reviewed package; inspect any downloaded ZIP before installing it.

Risk: Paid API access requires a secret key that could be exposed.

Mitigation: Use a key only for paid endpoints and keep it in environment variables or client secret storage.

Risk: IP whitelist updates change account access settings.

Mitigation: Require explicit approval before any account-changing action.

Risk: Stale trading dates or misread field units could lead to misleading market analysis.

Mitigation: Check response dates and units before calculations; do not treat the results as investment advice.

## Reference(s):

- [ashareapi website](https://ashareapi.com)
- [ashareapi documentation](https://ashareapi.com/docs)
- [ashareapi endpoint list](https://ashareapi.com/endpoints)
- [ashareapi changelog](https://ashareapi.com/changelog)
- [Endpoint parameters and responses](artifact/references/endpoints.md)
- [Field definitions and units](artifact/references/fields.md)
- [Errors and rate limits](artifact/references/errors.md)
- [Python and Node.js SDK guidance](artifact/references/sdk.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with API examples and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include endpoint selections, field interpretations, and error-handling guidance.]

## Skill Version(s):

0.2.8 (source: skill frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
