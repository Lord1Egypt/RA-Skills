## Description:

Searches Xiaohongshu for trending cultural tourism posts, ranks them by likes, clusters topics, and generates an HTML visual report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators, tourism professionals, and researchers use this skill to track Xiaohongshu cultural tourism hotspots, compare destination or scenic-spot content, and produce HTML reports for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal report generation calls RedFox with the user's API key.

Mitigation: Use a revocable, low-scope REDFOX_API_KEY and avoid hardcoding or exposing it in code, prompts, logs, or output files.

Risk: Subscription mode installs recurring jobs and may persist the API key.

Mitigation: Avoid subscription mode until it is fixed; if it was already enabled, unsubscribe where possible and rotate the key.

Risk: Generated HTML reports are written locally and opened in a browser.

Mitigation: Review generated reports before sharing them and use a controlled output directory for report files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/redfox-data/skills/cultural-tourism-xiaohongshu-feed)
- [RedFoxHub API Key Settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFoxHub](https://redfox.hk)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown response with a category summary table plus a local HTML report file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY; normal execution calls RedFox, writes an HTML report locally, and may open the report in a browser.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
