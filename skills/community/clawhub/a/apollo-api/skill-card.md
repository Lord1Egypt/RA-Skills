## Description: <br>
Apollo.io API integration with managed OAuth for searching and enriching people and companies, managing contacts and accounts, and supporting sales prospecting workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and sales-operations developers use this skill to work with Apollo.io through Maton-managed authentication, including lead search, enrichment, contact and account management, and sequence workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses MATON_API_KEY and Maton connection URLs that can expose access to a connected Apollo account if shared. <br>
Mitigation: Keep the API key and connection URLs private, and rotate credentials if they are exposed. <br>
Risk: Requests can read or modify Apollo sales data, including contacts, accounts, opportunities, sequences, and email data. <br>
Mitigation: Approve create, update, delete, or sequence actions only after checking the target resource, connection, and intended change. <br>
Risk: When multiple Apollo connections exist, an action could target the wrong account. <br>
Mitigation: Use the Maton-Connection header to select the intended connection before running account-specific requests. <br>


## Reference(s): <br>
- [Apollo Skill Page](https://clawhub.ai/byungkyu/apollo-api) <br>
- [Publisher Profile](https://clawhub.ai/user/byungkyu) <br>
- [Apollo API Overview](https://docs.apollo.io/reference/introduction) <br>
- [Apollo People Search API](https://docs.apollo.io/reference/people-api-search.md) <br>
- [Apollo People Enrichment API](https://docs.apollo.io/reference/people-enrichment.md) <br>
- [Apollo Organization Search API](https://docs.apollo.io/reference/organization-search.md) <br>
- [Apollo Organization Enrichment API](https://docs.apollo.io/reference/organization-enrichment.md) <br>
- [Apollo Create Contact API](https://docs.apollo.io/reference/create-a-contact.md) <br>
- [Apollo LLM Reference](https://docs.apollo.io/llms.txt) <br>
- [Maton](https://maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with API endpoint examples and Python, JavaScript, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an active Apollo connection through Maton.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
