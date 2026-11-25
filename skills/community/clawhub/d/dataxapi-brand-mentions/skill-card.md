## Description:

Search selected social platforms for brand or keyword mentions and prepare a cross-platform engagement and sentiment brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor how a brand, product, or keyword is discussed across selected social platforms. It returns a post table and a brief covering platform activity, engagement, themes, and tone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security guidance notes that the CLI package is unpinned.

Mitigation: Review the package source and consider pinning a trusted CLI version before running it.

Risk: Search terms may disclose sensitive information to DataXAPI.

Mitigation: Avoid sending sensitive terms, or confirm they are appropriate to share with DataXAPI before searching.

## Reference(s):

- [DataXAPI](https://dataxapi.com)
- [ClawHub skill page](https://clawhub.ai/data-x-api/skills/dataxapi-brand-mentions)

## Skill Output:

**Output Type(s):** [CSV data, Markdown report]

**Output Format:** [A mentions.csv post table and a Markdown brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One row per returned post; fields may be empty when a platform does not provide them.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
