## Description:

Searches for a brand or keyword on selected social platforms and arranges one page of posts per platform into a table with post and engagement details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

Users who track brands or topics use this skill to search up to five selected social platforms and review matching posts, authors, timestamps, and engagement in one table.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to DataXAPI, searches can incur charges, and enforcement of spend limits by the external CLI is unverified.

Mitigation: Review the free plan before running, use a reviewed pinned CLI version and a budget-limited API key, and set a spend cap.

## Reference(s):

- [DataXAPI Skills](https://dataxapi.com/skills/)
- [DataXAPI Mentions on ClawHub](https://clawhub.ai/data-x-api/skills/dataxapi-mentions)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [CSV file containing post details and engagement metrics, with an optional text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to one page per selected platform, with at most five platforms per run; each platform search is charged separately.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
