## Description:

GEO Pulse delivers client-ready GEO (Generative Engine Optimization) reports that measure brand visibility across AI search outputs, including mention rate, link reference rate, sentiment, platform breakdown, competitor benchmarking, and historical trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sjinping](https://clawhub.ai/user/sjinping)

### License/Terms of Use:

MIT-0

## Use Case:

Brand, marketing, and GEO/SEO analysts use this skill to generate client-ready AI visibility audit and trend reports for a named brand or domain. It helps compare brand mentions, link references, sentiment, platform performance, competitors, and historical changes across AI search outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Brand names, domains, metrics requests, and generated analysis may be sent to an external service at a default plaintext HTTP endpoint.

Mitigation: Configure a trusted HTTPS GEO_PULSE_BASE_URL before use and avoid sending confidential or unreleased client information.

Risk: Command examples can be unsafe if brand names are substituted directly into shell JSON payloads.

Mitigation: Serialize JSON safely before running curl commands, and review generated commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sjinping/skills/geo-pulse)
- [Publisher profile](https://clawhub.ai/user/sjinping)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline shell command examples and API-derived tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces GEO audit reports, historical trend summaries, fallback messages, and recommendations based on external service responses.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
