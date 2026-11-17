## Description:

Identifies 3-5 competitors for a given brand using SerpAPI, DataForSEO, or an OpenAI fallback, returning names, websites, and optional reasons for competition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adarshvmore](https://clawhub.ai/user/adarshvmore)

### License/Terms of Use:


## Use Case:

Developers and marketing operations teams use this skill to collect competitor candidates for a brand and feed competitor landscape analysis in marketing audit workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Brand names and domains may be sent to SerpAPI, DataForSEO, and potentially OpenAI during fallback processing.

Mitigation: Confirm that the deployment is allowed to share those inputs with the configured API providers before use.

Risk: Untrusted brand or domain values could produce malformed or misleading competitor data for downstream reports.

Mitigation: Validate inputs and enforce structured output validation before feeding results into automated reports.

Risk: Competitor results can be incomplete or subjective, especially for niche or unknown brands.

Mitigation: Review generated competitor lists before relying on them for strategic analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adarshvmore/skills/competitor-finder)
- [Publisher profile](https://clawhub.ai/user/adarshvmore)
- [SerpAPI Google Search endpoint](https://serpapi.com/search.json)
- [DataForSEO competitor domain endpoint](https://api.dataforseo.com/v3/dataforseo_labs/google/competitors_domain/live)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with TypeScript schemas and API integration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns competitor names, websites, and optional reasons; recommends graceful error handling and fallback behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
