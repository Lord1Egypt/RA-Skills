## Description: <br>
Query Digiforma training management platform via GraphQL API. Use when asked about trainees, sessions, invoices, programs, trainers, or any training data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mibbou](https://clawhub.ai/user/mibbou) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to query Digiforma training-management records through its GraphQL API, including trainees, sessions, invoices, programs, and trainers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated Digiforma queries can retrieve trainee contact details, trainer contact details, and invoice amounts. <br>
Mitigation: Use a least-privileged or read-only API key where possible, paginate requests, and share retrieved personal or financial data only with authorized requesters. <br>


## Reference(s): <br>
- [Digiforma GraphQL API endpoint](https://app.digiforma.com/api/v1/graphql) <br>
- [ClawHub skill page](https://clawhub.ai/mibbou/digiforma) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with curl commands and GraphQL query examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DIGIFORMA_API_KEY for authenticated API requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
