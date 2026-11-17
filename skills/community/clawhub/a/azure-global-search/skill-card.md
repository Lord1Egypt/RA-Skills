## Description:

Query Microsoft Azure product information, documentation, parameters, features, and pricing from official sources without login.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangbingpeng](https://clawhub.ai/user/wangbingpeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud architects, and technical buyers use this skill to find Azure product documentation, compare specifications and pricing, identify service parameters, and produce bilingual summaries or starter examples from official public sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Azure CLI, SDK, REST, or deployment examples could create, modify, or delete Azure resources if run without review.

Mitigation: Review all commands and code before execution, test in a non-production subscription when possible, and use least-privilege Azure roles instead of broad Contributor access.

Risk: Azure pricing, quotas, regions, and product limits can change after the skill provides an answer.

Mitigation: Verify current pricing and service limits on official Microsoft Azure sources before making purchasing or deployment decisions.

Risk: Examples may require Azure subscription identifiers, tenant identifiers, client identifiers, or secrets.

Mitigation: Keep credentials as placeholders in shared output, avoid pasting secrets into prompts, and use secure secret-management practices for any real deployment.

## Reference(s):

- [Azure Global Search on ClawHub](https://clawhub.ai/wangbingpeng/skills/azure-global-search)
- [Azure Product Query Examples](examples.md)
- [Azure Homepage](https://azure.microsoft.com/)
- [Azure China](https://www.azure.cn/)
- [Microsoft Learn Azure Documentation](https://learn.microsoft.com/azure/)
- [Azure Pricing](https://azure.microsoft.com/pricing/)
- [Azure REST API Reference](https://learn.microsoft.com/rest/api/azure/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, links, and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bilingual English and Chinese content, Azure CLI examples, SDK snippets, REST endpoint references, pricing notes, and official-source links.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
