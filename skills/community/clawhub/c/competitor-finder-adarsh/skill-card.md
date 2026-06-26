## Description: <br>
Finds 3-5 competitors for a brand using SerpAPI, DataForSEO, and a minimal OpenAI fallback, returning competitor names, websites, and reasons when available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AdarshVMore](https://clawhub.ai/user/AdarshVMore) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, agents, and marketing analysts use this skill to collect competitor candidates for a brand and feed a marketing audit or competitor landscape workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends brand names and optional domains to external search, SEO, and AI providers. <br>
Mitigation: Use approved API accounts, avoid sensitive unreleased brand data, and follow the organization's data-sharing requirements before execution. <br>
Risk: Competitor results can be subjective, incomplete, or affected by API quota and fallback behavior. <br>
Mitigation: Treat results as candidate inputs, review them before relying on a marketing report, and monitor fallback warnings and API failures. <br>
Risk: The skill depends on API keys and paid third-party services. <br>
Mitigation: Store credentials in environment variables, monitor usage and quotas, and handle exhausted or invalid credentials through the documented graceful error path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AdarshVMore/competitor-finder-adarsh) <br>
- [SerpAPI Google Search endpoint](https://serpapi.com/search.json) <br>
- [DataForSEO Competitor Domain endpoint](https://api.dataforseo.com/v3/dataforseo_labs/google/competitors_domain/live) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with TypeScript examples and JSON-shaped competitor data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs 3-5 competitor entries with name, website, and optional reason; failures return a valid object with an error field.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
