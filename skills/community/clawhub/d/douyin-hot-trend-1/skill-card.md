## Description:

Fetches Douyin hot search and trending-list data, returning ranked topics with heat values and Douyin links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noah-1106](https://clawhub.ai/user/noah-1106)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and social media operators use this skill to retrieve Douyin trending topics for content monitoring, trend analysis, and marketing planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requests to Douyin and stores fetched trend data under the local data directory.

Mitigation: Review before installing, use reasonable request frequency, and confirm local storage behavior is acceptable for the deployment environment.

Risk: The generated HTML report can render fetched titles, labels, inline JSON, and links without sufficient sanitization.

Mitigation: Do not host or rely on the generated report until displayed values are escaped and URL schemes are restricted to safe Douyin HTTPS links.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/noah-1106/skills/douyin-hot-trend-1)
- [Douyin web data source](https://www.douyin.com/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, files]

**Output Format:** [Console text, JSON arrays, local SQLite data, and optional generated HTML report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default retrieval is 50 items, with a user-supplied count supported by the command-line scripts.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
