## Description:

文旅抖音信息源 searches Douyin cultural-tourism content, ranks popular works by engagement, clusters topics, and generates an HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External content operators, tourism marketers, and researchers use this skill to monitor recent Douyin cultural-tourism trends, compare topics, and produce shareable HTML reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's subscription and report-generation behavior has avoidable security risks.

Mitigation: Prefer one-time runs until subscription handling, HTML escaping, and credential storage have been reviewed and fixed.

Risk: The skill sends RedFoxHub API queries and depends on a local API key.

Mitigation: Use a revocable API key, keep it out of prompts, logs, and generated reports, and confirm its scope and expiration before use.

Risk: Generated local HTML reports may include data returned from an external service and can be opened automatically.

Mitigation: Avoid automatically opening reports from untrusted data sources and review generated HTML before sharing it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/redfox-data/skills/cultural-tourism-douyin-feed)
- [RedFoxHub API Key Settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [Publisher Profile](https://clawhub.ai/user/redfox-data)

## Skill Output:

**Output Type(s):** [text, markdown, files, configuration]

**Output Format:** [Terminal text and Markdown-style summary with an HTML report file and JSON article summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a RedFoxHub API key; optional subscription mode creates a recurring local scheduled job.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
