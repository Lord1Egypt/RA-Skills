## Description:

Fetches public Douyin search results, creator posts, video comments, and real-time hot-list data through Guaikei CLI commands for research and analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to collect public Douyin data for content research, competitor monitoring, sentiment analysis, and trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Douyin search terms, creator or video URLs, requested limits, and GUAIKEI_API_TOKEN are sent to www.guaikei.com.

Mitigation: Use only with data and credentials approved for that service, and rotate or revoke the token if it is exposed.

Risk: The security guidance flags token-in-query-string authentication.

Mitigation: Avoid sensitive workflows until token transport is reviewed or corrected.

Risk: The security guidance flags runtime contact or promotional token-error messages and an overly broad trigger rule.

Mitigation: Review runtime errors and trigger behavior before deployment, and require explicit user confirmation before broad short-video research tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/douyin-quick-fetch-public-guaikei)
- [Guaikei token and usage site](https://www.guaikei.com)
- [Complete option reference](references/options.md)
- [Changelog](references/changelog.md)
- [Input and output JSON schemas](assets/*.schema.json)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [CLI commands with structured JSON responses and local JSON log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; command outputs are intended to be parseable JSON on stdout.]

## Skill Version(s):

1.0.0 (source: release evidence, package.json, references/changelog.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
