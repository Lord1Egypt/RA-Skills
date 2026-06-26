## Description: <br>
API Gateway lets agents call third-party APIs through Maton-managed OAuth connections for services such as Slack, HubSpot, Salesforce, Google Workspace, and Stripe. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IceMasterT](https://clawhub.ai/user/IceMasterT) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to make authenticated API calls and manage OAuth-backed connections to supported third-party services through Maton. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can invoke broad write, delete, admin, email, payment, public posting, and webhook actions across connected services. <br>
Mitigation: Require human confirmation before POST, PUT, PATCH, DELETE, email/send, admin, payment, public posting, or webhook actions. <br>
Risk: Connected third-party services may expose more data or privileges than a task requires. <br>
Mitigation: Use least-privilege OAuth scopes and prefer read-only service connections when possible. <br>
Risk: Stale or unused Maton connections can retain access to external services. <br>
Mitigation: Review active connections regularly and revoke unused Maton connections promptly. <br>


## Reference(s): <br>
- [Maton homepage](https://maton.ai) <br>
- [Maton API Reference](https://www.maton.ai/docs/api-reference) <br>
- [Slack Routing Reference](references/slack.md) <br>
- [HubSpot Routing Reference](references/hubspot.md) <br>
- [Salesforce Routing Reference](references/salesforce.md) <br>
- [Gmail Routing Reference](references/google-mail.md) <br>
- [Stripe Routing Reference](references/stripe.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Code, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and authorized OAuth connections for target services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
