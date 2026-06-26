## Description: <br>
Access and query Cogmate personal knowledge systems for knowledge retrieval, semantic search, and Q&A using a valid CogNexus access token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MaxiiWang](https://clawhub.ai/user/MaxiiWang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Cogmate knowledge bases, search facts, inspect profiles and statistics, and receive answers through authenticated Cogmate API endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Access tokens are passed in query parameters and may appear in URLs, shell history, logs, or monitoring systems. <br>
Mitigation: Use HTTPS-only Cogmate endpoints, prefer narrow token scopes, avoid sharing command transcripts that include tokens, and rotate any token that may have been exposed. <br>
Risk: Queries and retrieved answers may expose private knowledge from the target Cogmate instance. <br>
Mitigation: Use the skill only with trusted Cogmate endpoints and tokens, and avoid sending sensitive questions unless the endpoint owner and access scope are appropriate. <br>


## Reference(s): <br>
- [Cogmate API Details](references/api-details.md) <br>
- [CogNexus](https://github.com/MaxiiWang/CogNexus) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with bash examples; helper scripts return plain text or JSON-derived summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Cogmate API URL and access token; protected endpoints pass the token as a query parameter.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
