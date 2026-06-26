## Description: <br>
BytePlan API wrapper that supports login authentication, model queries, data fetching, and reuse by related BytePlan skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dbfu](https://clawhub.ai/user/dbfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to authenticate to BytePlan, manage user and tenant context, query available models, fetch model records, and retrieve field values for DIM, LIST, LOV, and LEVEL field types. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores reusable BytePlan credentials and tokens in plaintext. <br>
Mitigation: Install only from a trusted publisher, use a dedicated working directory, avoid sharing the credential file, and rotate credentials if they are written to the wrong location. <br>
Risk: Credential storage locations in behavior and documentation may not match. <br>
Mitigation: Check which .env file the skill will modify before login and avoid generic USER_NAME or PASSWORD environment variables in projects that use the skill. <br>
Risk: The development environment sends passwords without the UAT RSA encryption path. <br>
Mitigation: Prefer the UAT environment when possible and reserve development login for trusted test accounts. <br>


## Reference(s): <br>
- [ClawHub byteplan-api release page](https://clawhub.ai/dbfu/byteplan-api) <br>
- [BytePlan development API endpoint](https://dev.byteplan.com) <br>
- [BytePlan UAT API endpoint](https://uatapp.byteplan.com) <br>


## Skill Output: <br>
**Output Type(s):** [code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples and environment configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update BytePlan credential and token settings during authentication workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
