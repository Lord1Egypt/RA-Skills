## Description:

Finds three to five competitors for a brand by querying SerpAPI, then DataForSEO, and using an OpenAI fallback only when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adarshvmore](https://clawhub.ai/user/adarshvmore)

### License/Terms of Use:


## Use Case:

Developers and marketing-audit agents use this skill to collect competitor names, websites, and short rationale for a brand or domain. The results support competitor landscape analysis while allowing graceful degradation when external data providers fail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Brand names and domains may be shared with SerpAPI, DataForSEO, and OpenAI during fallback execution.

Mitigation: Confirm the data-sharing posture before installation and avoid sending sensitive brand or domain inputs unless those providers are approved.

Risk: API credentials for SerpAPI, DataForSEO, and OpenAI are required for the external lookup and fallback paths.

Mitigation: Store credentials in environment variables and do not hardcode them in skill files, prompts, or logs.

Risk: DataForSEO lookup behavior is configured around English and United States locale settings in the artifact.

Mitigation: Adjust locale settings for non-US or non-English audits when the implementation supports it.

## Reference(s):

- [Competitor Finder Adarsh on ClawHub](https://clawhub.ai/adarshvmore/skills/competitor-finder-adarsh)
- [Publisher profile: adarshvmore](https://clawhub.ai/user/adarshvmore)
- [SerpAPI Google Search endpoint](https://serpapi.com/search.json)
- [DataForSEO Competitor Domain API endpoint](https://api.dataforseo.com/v3/dataforseo_labs/google/competitors_domain/live)

## Skill Output:

**Output Type(s):** [Text, Structured data, API calls, Guidance]

**Output Format:** [JSON-compatible competitor entries with names, websites, optional reasons, and optional error text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns three to five competitors when available and uses an error field instead of blocking the wider pipeline.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
