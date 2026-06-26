## Description: <br>
Access and manage Firefly III finance data programmatically, including transactions, accounts, recurring rules, and automation through the Firefly III API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[josetseph](https://clawhub.ai/user/josetseph) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to interact with a user's Firefly III personal finance instance for account, transaction, recurrence, rule, and related API workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad live access to financial and administrative Firefly III API operations. <br>
Mitigation: Use the least-privileged token available, prefer read-only prompts for routine work, and require explicit human confirmation before mutating, administrative, webhook, rule-trigger, destroy, or purge requests. <br>
Risk: The OAuth token controls access to personal financial data. <br>
Mitigation: Store the token only in secure environment variables, avoid hardcoding or sharing it, and use a trusted network path to the Firefly III instance. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/josetseph/firefly-iii-published) <br>
- [Firefly III API Documentation](https://docs.firefly-iii.org/references/firefly-iii/api/) <br>
- [Firefly III API v6.5.5 OpenAPI Specification](artifact/firefly-iii-6.5.5-v1.yaml) <br>
- [Security Considerations](artifact/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON API responses and concise Markdown or shell-command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FIREFLY_URL and FIREFLY_TOKEN environment variables for live API access.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
