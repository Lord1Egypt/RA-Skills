## Description: <br>
Manage contacts, companies, products, tags, documents, brands, automations, team members, organization data, block plugin records, and operation plugin records on an erxes instance through GraphQL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erxes](https://clawhub.ai/user/erxes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External erxes workspace operators and developers use this skill to authenticate to an erxes instance and manage CRM, SaaS block, and operations records through GraphQL while applying confirmation checks for risky changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad owner-level access to erxes business data. <br>
Mitigation: Use a test or least-privileged account where possible, and install only when agent-managed erxes administration is intended. <br>
Risk: OAuth tokens or session details could be exposed through shared command output. <br>
Mitigation: Avoid sharing output that contains tokens, keep sessions in memory only, and do not write tokens to project files. <br>
Risk: Write, invite, email, contract, invoice, payment, automation, and team-management actions can materially change business records. <br>
Mitigation: Require explicit approval before those actions and verify the exact record and ERXES_BASE_URL before execution. <br>


## Reference(s): <br>
- [ClawHub erxes Skill Release](https://clawhub.ai/erxes/erxes-skill) <br>
- [erxes Publisher Profile](https://clawhub.ai/user/erxes) <br>
- [erxes Quick Login](artifact/erxes-app-token-auth.md) <br>
- [erxes GraphQL API](artifact/erxes-graphql-api.md) <br>
- [block_api SaaS Workflow Reference](artifact/block-api.md) <br>
- [operation_api SaaS Workflow Reference](artifact/operation-api.md) <br>
- [Browser Login Helper](artifact/scripts/login.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, GraphQL requests, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ERXES_BASE_URL and an OAuth session; handles sensitive tokens in memory for the current task.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
