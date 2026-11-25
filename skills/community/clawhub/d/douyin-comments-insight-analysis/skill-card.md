## Description:

Search public Douyin videos and accounts, retrieve post details and comments, and check trending topics to support content research, competitor analysis, and sentiment monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Content, product, customer support, and marketing teams can use the skill to research public Douyin posts, comments, creators, and trending topics for content planning, competitor review, and sentiment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence notes that supplied links, IDs, and search terms may be sent to a third-party API at guaikei.com.

Mitigation: Use the skill only for public-data queries when that disclosure is acceptable; avoid sending sensitive or private identifiers.

Risk: Security evidence flags uncertainty about keyword-based account discovery, and notes that analysis of some files was partial.

Mitigation: Confirm current account-search support and review the relevant provider documentation before relying on that capability.

## Reference(s):

- [Usage and output contract](artifact/references/contract.md)
- [Comment demand analysis guide](artifact/references/demand-mining.md)
- [Comment-based customer acquisition guide](artifact/references/customer-acquisition.md)
- [Error handling reference](artifact/references/errors.md)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON results for Douyin searches, account and post data, comments, and trends; concise agent guidance for analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may be saved locally for follow-up analysis.]

## Skill Version(s):

1.5.0 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
