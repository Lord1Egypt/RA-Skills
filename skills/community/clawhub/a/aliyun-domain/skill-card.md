## Description:

Manage Alibaba Cloud domain assets through OpenAPI, including domain lookup, renewal, transfer, registration, contact updates, policy consultation, local knowledge retrieval, monitoring, and domain-name suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevin850115](https://clawhub.ai/user/kevin850115)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect and manage Alibaba Cloud domain portfolios, retrieve Alibaba Cloud domain guidance from local documentation, monitor domain health signals, and prepare domain registration, renewal, transfer, DNS, and contact-management operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad Alibaba Cloud domain authority and some sensitive domain changes can run without the confirmation promised in the documentation.

Mitigation: Review the skill before installation, use a narrowly scoped RAM user, and require separate confirmation of the exact operation and target domain before transfer, DNS, auto-renew, or registrant-profile actions.

Risk: Alibaba Cloud AccessKey credentials may be exposed if stored in shell profiles or repository-local files.

Mitigation: Avoid storing AccessKey secrets in shell profiles or repo-local files; prefer managed secrets or short-lived environment configuration and rotate credentials regularly.

Risk: Purchase links and investment rankings may be mistaken for financial advice.

Mitigation: Treat purchase links, price comparisons, and investment rankings as suggestions that require independent review before spending money or changing ownership.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kevin850115/skills/aliyun-domain)
- [Alibaba Cloud Domain API reference](https://next.api.aliyun.com/api/Domain/2018-01-29)
- [Alibaba Cloud Domain documentation](https://help.aliyun.com/product/35836.html)
- [Alibaba Cloud domain quick start](https://help.aliyun.com/zh/dws/getting-started/domain-name-quick-start)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline code, command examples, configuration snippets, API guidance, and generated purchase or renewal links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Alibaba Cloud API operation summaries, domain availability results, monitoring summaries, RAG citations to bundled help files, and confirmation prompts for sensitive operations.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
