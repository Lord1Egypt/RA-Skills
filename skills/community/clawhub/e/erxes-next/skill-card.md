## Description: <br>
Manage contacts, companies, products, tags, documents, brands, automations, team members, and organization data on an erxes instance through GraphQL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wlkr123](https://clawhub.ai/user/wlkr123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to authenticate to an erxes workspace, call its GraphQL API, and view, create, update, merge, or remove CRM and organization records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate an erxes workspace with the authority of the OAuth account and may change business or user-account data. <br>
Mitigation: Use a least-privilege account where possible and require explicit confirmation before deletes, merges, team-member changes, organization changes, and automation changes. <br>
Risk: The login flow prints session JSON that contains access and refresh tokens. <br>
Mitigation: Treat the session JSON as secret, keep it only in memory for the current task, and do not save it to project files. <br>
Risk: A wrong or untrusted erxes endpoint could receive authentication requests or API calls. <br>
Mitigation: Verify the erxes endpoint before login and before sending GraphQL requests. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wlkr123/erxes-next) <br>
- [erxes Quick Login](artifact/erxes-app-token-auth.md) <br>
- [erxes GraphQL API](artifact/erxes-graphql-api.md) <br>
- [Browser login helper](artifact/scripts/login.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, GraphQL examples, JSON payloads, and HTTP headers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ERXES_BASE_URL and optional ERXES_CLIENT_ID; OAuth session JSON is printed to stdout and should be treated as secret.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
