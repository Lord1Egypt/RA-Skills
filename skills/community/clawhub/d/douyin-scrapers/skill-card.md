## Description:

Searches public Douyin videos and accounts, retrieves trending lists, creator posts, video details, and comments, and supports analysis of engagement and audience themes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Content, marketing, and research teams use the skill to discover trending public Douyin content, review creator and post metrics, and analyze comments for content planning or internal audience insights. It returns structured results for follow-up analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports a benign verdict with medium confidence and partial inspection (31 of 53 components fully inspected); its summary flags keyword-based account search as a possible scope mismatch.

Mitigation: Review account-search behavior before use in sensitive workflows and limit queries to public data for authorized internal analysis.

Risk: The skill sends search terms and supplied Douyin links or IDs to the Guaikei third-party API, and some results may be saved locally.

Mitigation: Do not include sensitive information in queries, protect the API token, and review or redact saved results before sharing.

## Reference(s):

- [Usage guide](readme.md)
- [Output contract](references/contract.md)
- [Comment demand analysis guide](references/demand-mining.md)
- [Public data and service FAQ](references/faq.md)
- [Guaikei service](https://www.guaikei.com)
- [Douyin](https://www.douyin.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON results with concise natural-language summaries or comment analysis when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by query; the skill can save result files locally. Queries may include public user-generated content.]

## Skill Version(s):

1.5.0 (source: SKILL.md frontmatter, package.json, changelog released 2026-11-10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
