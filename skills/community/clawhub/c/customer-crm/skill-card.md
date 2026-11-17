## Description:

Customer CRM manages customer profiles, source attribution, and repurchase recommendations for e-commerce workflows across channels such as WeChat Official Account, Xianyu, Douyin, Kuaishou, and direct traffic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce operators and agent developers use this skill to record customer source data, maintain customer profiles after delivery callbacks or channel interactions, calculate attribution statistics, and prepare repurchase recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist customer identifiers, order history, source attribution, and repurchase-trigger data locally.

Mitigation: Deploy only where local CRM data storage is acceptable, and define retention, deletion, tenant-isolation, and file-access controls before use.

Risk: The skill depends on configured channel integrations and a SiliconFlow API key.

Mitigation: Provide only the required environment variable and MCP server configuration, and scope credentials to the deployment environment.

## Reference(s):

- [Customer CRM ClawHub listing](https://clawhub.ai/thcjp/skills/customer-crm)
- [Business rules](references/business_rules.md)
- [Error codes](references/error_codes.md)
- [Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance and JSON command responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script returns JSON objects with success, data, error, and code fields.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
