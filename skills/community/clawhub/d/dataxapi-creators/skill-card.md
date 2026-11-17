## Description:

Searches selected social platforms for creator accounts and returns a table of names, bios, follower counts, and post counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can search selected social platforms by category or keyword to find creator accounts. The results help compare one page of accounts per platform using names, bios, follower counts, and post counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are disclosed to DataXAPI, and each selected platform search can incur a charge.

Mitigation: Review the free cost plan before running searches, set a spend cap, and use a dedicated API key with a small budget.

Risk: The skill depends on an external command-line client installed through npm or npx.

Mitigation: Use a reviewed, pinned CLI version.

## Reference(s):

- [DataXAPI Skills](https://dataxapi.com/skills/)
- [DataXAPI Creators on ClawHub](https://clawhub.ai/data-x-api/skills/dataxapi-creators)
- [Publisher profile](https://clawhub.ai/user/data-x-api)

## Skill Output:

**Output Type(s):** [CSV data, Text]

**Output Format:** [CSV table of creator accounts, with an optional textual summary from the agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One page per selected platform, up to five platforms. Each platform search is separately charged; rates and audience profiles are not included.]

## Skill Version(s):

1.0.0 (source: artifact/SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
