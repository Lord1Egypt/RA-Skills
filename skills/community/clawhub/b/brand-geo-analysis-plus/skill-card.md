## Description:

Analyzes Chinese online brand perception through trending topics, recent social-media discussion, and brand visibility in AI search answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Brand and marketing teams, market researchers, and GEO practitioners use this skill to track Chinese-platform trends, compare social-media sentiment and competitors, and assess how brands appear in Doubao, Kimi, and DeepSeek answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A credential-safety flaw affects hub connections.

Mitigation: Do not use a sensitive API key until the hub TLS verification issue is fixed; check key scope and revocation options before use.

Risk: Brand, topic, competitor, and AI-search questions are sent to RedFox-backed services.

Mitigation: Avoid confidential launches, unreleased campaigns, regulated personal data, and sensitive investigations.

Risk: Local report and temporary-file retention is unclear.

Mitigation: Review generated files and local retention before analyzing sensitive material.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/redfox-data/skills/brand-geo-analysis-plus)
- [RedFoxHub API key setup](https://redfox.hk/settings/api-keys?source=clawhub)
- [GEO metrics and limitations](artifact/references/geo-metrics.md)
- [Social-media research output rules](artifact/references/cn30-output-rules.md)
- [Trending-hub instructions](artifact/references/hub-instructions.md)

## Skill Output:

**Output Type(s):** [Markdown, HTML reports, JSON data, Guidance]

**Output Format:** [Markdown summaries and tables, JSON results, and interactive HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a REDFOX_API_KEY; findings reflect the queried platforms and analysis time.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
