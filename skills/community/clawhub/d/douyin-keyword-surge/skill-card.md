## Description:

Retrieves Douyin keyword-search results, current hot topics, creator posts, public video details, and comments as structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Content strategists and analysts use it to retrieve public Douyin search, trend, creator, video, and comment data for content planning and market monitoring. Do not rely on it for advertised seven-day likes-growth rankings until the publisher corrects and verifies that capability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The advertised seven-day likes-growth rankings are not supported by this release's commands.

Mitigation: Ask the publisher to correct the advertised capability and routing, and verify the corrected release before relying on those rankings.

Risk: Search queries and public-data requests are sent to a third-party API and may incur charges.

Mitigation: Check the service plan and ensure the user intends to send the query or link before making a request.

Risk: The API token and locally saved query/result logs may expose sensitive information.

Mitigation: Keep GUAIKEI_API_TOKEN secret and protect or remove local logs according to the user's data-handling needs.

## Reference(s):

- [Usage options](references/options.md)
- [Comment analysis guide](references/demand-mining.md)
- [Release notes](references/changelog.md)
- [Skill release page](https://clawhub.ai/why20261/skills/douyin-keyword-surge)
- [GuaiKei API service and support](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON records with command usage and analysis guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are also saved as local JSON log files; agents can summarize search, trend, creator, video, and comment data.]

## Skill Version(s):

1.4.2 (source: frontmatter, package.json, changelog released 2026-11-04, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
