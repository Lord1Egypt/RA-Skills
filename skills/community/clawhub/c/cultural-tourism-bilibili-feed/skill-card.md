## Description:

文旅B站信息源 searches Bilibili for cultural tourism videos, ranks popular content by engagement, clusters results by topic, and generates a browsable HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External content operators, tourism marketers, and tourism researchers use this skill to monitor Bilibili cultural tourism trends, compare location-specific video activity, and generate category-level reports for planning or research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The subscription feature creates persistent scheduled jobs and was flagged for unsafe command or XML handling and credential exposure risks.

Mitigation: Review before installing, avoid --subscribe until the scheduler code is fixed, and use a revocable RedFox API key through an environment variable.

Risk: Generated HTML reports include remote API values and are opened automatically, so report content should be treated as untrusted web content.

Mitigation: Open reports in a controlled browser context and avoid relying on generated links or embedded values without review.

Risk: Untrusted keywords can affect API queries and scheduled job configuration.

Mitigation: Use trusted, simple keywords and review generated commands or scheduled entries before reuse.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/redfox-data/skills/cultural-tourism-bilibili-feed)
- [RedFox API Key Settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFoxHub](https://redfox.hk)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown conversation summary plus generated HTML report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a RedFox API key and the requests Python package; the HTML report includes category cards, cover images, engagement metrics, and outbound video links.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
