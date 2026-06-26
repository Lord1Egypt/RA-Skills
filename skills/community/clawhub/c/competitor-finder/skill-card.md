## Description: <br>
Identifies 3-5 competitors for a given brand using SerpAPI, DataForSEO, or an OpenAI fallback, returning competitor names, websites, and optional reasons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AdarshVMore](https://clawhub.ai/user/AdarshVMore) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Marketing analysts and developers use this skill to add competitor discovery to a marketing audit pipeline. It gathers competitor candidates for a brand or domain, filters out the input brand, and returns structured competitor entries for downstream reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Brand names, domains, and search context may be sent to SerpAPI, DataForSEO, and possibly OpenAI. <br>
Mitigation: Use the skill only with provider-approved data, and avoid confidential launch names or sensitive internal domains unless those providers are approved for that data. <br>
Risk: The skill depends on third-party API keys and usage-based services that may fail, exhaust quotas, or incur costs. <br>
Mitigation: Use limited-scope keys where possible, monitor API usage and costs, and keep graceful fallback behavior enabled. <br>
Risk: Competitor identification can be subjective or incomplete, especially when the OpenAI fallback is used. <br>
Mitigation: Treat returned competitors as candidates for marketing review and preserve warning logs when fallback methods are used. <br>


## Reference(s): <br>
- [ClawHub Competitor Finder release](https://clawhub.ai/AdarshVMore/competitor-finder) <br>
- [SerpAPI Google Search endpoint](https://serpapi.com/search.json) <br>
- [DataForSEO Competitor Domain endpoint](https://api.dataforseo.com/v3/dataforseo_labs/google/competitors_domain/live) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with TypeScript interfaces, API configuration details, and JSON-shaped result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The intended collector output is a CompetitorData object with 3-5 competitor entries and an optional error field when collection fails.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
