## Description: <br>
Calls the remote Flight Scout commercial API to search flights, check price calendars, run hidden-city searches, query asynchronous jobs, and return structured JSON results after the user configures an API base URL and API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ebolaboy](https://clawhub.ai/user/ebolaboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call a configured Flight Scout API for flight search, airport autocomplete, price calendar, hidden-city search, job status, and account usage workflows. It is useful when responses should preserve the service's structured JSON fields, errors, request IDs, and quota metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Flight searches, quota checks, and the API key are sent to the configured Flight Scout API endpoint. <br>
Mitigation: Install only when the configured endpoint is trusted, prefer HTTPS, and keep FLIGHT_SCOUT_API_KEY in the local skill .env file or shell environment. <br>
Risk: API calls can consume quota and may return quota_exceeded errors with usage metadata. <br>
Mitigation: Use the usage workflow to inspect remaining quota, and preserve service-provided quota fields and error details in responses. <br>


## Reference(s): <br>
- [API Contract](artifact/references/api-contract.md) <br>
- [Flight Scout Skill README](artifact/README.md) <br>
- [Flight Scout homepage](https://github.com/EBOLABOY/flight-scout) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Structured JSON API envelopes with concise Markdown guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FLIGHT_SCOUT_API_BASE_URL and FLIGHT_SCOUT_API_KEY; sends flight queries and the API key to the configured service endpoint.] <br>

## Skill Version(s): <br>
0.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
