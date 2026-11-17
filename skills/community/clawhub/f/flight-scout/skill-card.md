## Description:

Flight Scout calls a configured remote commercial Flight Scout API to search flights, fetch price calendars, run hidden-city queries, check asynchronous job status, and return structured JSON results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ebolaboy](https://clawhub.ai/user/ebolaboy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Flight Scout to connect an agent to their configured Flight Scout API for flight search, price-calendar, hidden-city, airport lookup, and account-usage workflows while preserving the API's JSON envelope for downstream handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send a stored API key and travel details to any configured API base URL.

Mitigation: Use only a trusted HTTPS Flight Scout API base URL and rotate the API key if it was ever used with an untrusted or plaintext endpoint.

Risk: Search and usage commands may expose account quota or billing consumption.

Mitigation: Avoid broad or production API keys in shared skill environments and review quota fields before acting on usage or upgrade guidance.

## Reference(s):

- [API Contract](references/api-contract.md)
- [Flight Scout homepage](https://github.com/EBOLABOY/flight-scout)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration]

**Output Format:** [Structured JSON returned from the Flight Scout API, with optional shell commands for invoking the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FLIGHT_SCOUT_API_BASE_URL and FLIGHT_SCOUT_API_KEY; responses may include request IDs, quota metadata, errors, and asynchronous job IDs.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
