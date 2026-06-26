## Description: <br>
Interact with Apollo.io REST API (people/org enrichment, search, lists). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JhumanJ](https://clawhub.ai/user/JhumanJ) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run Apollo.io API helper commands for people search, organization enrichment, and related list or account lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a user-provided Apollo API key to the configured Apollo base URL. <br>
Mitigation: Use a dedicated or least-privileged API key, verify APOLLO_BASE_URL before running commands, and protect the local environment file. <br>
Risk: Generic POST calls can reach Apollo endpoints that may consume credits or modify account data. <br>
Mitigation: Review endpoint paths and request bodies before execution, especially for generic POST helper usage. <br>
Risk: Apollo endpoints may require paid-plan or master API-key access and may return rate-limit responses. <br>
Mitigation: Handle 403 and 429 responses during use and confirm the account plan supports the selected endpoint. <br>


## Reference(s): <br>
- [Apollo skill page on ClawHub](https://clawhub.ai/JhumanJ/apollo) <br>
- [Apollo API base URL](https://api.apollo.io) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, JSON] <br>
**Output Format:** [Shell command output from Apollo REST API calls, typically JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APOLLO_BASE_URL and APOLLO_API_KEY configuration before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
