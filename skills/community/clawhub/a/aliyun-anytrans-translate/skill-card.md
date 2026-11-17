## Description:

Helps agents manage Alibaba Cloud TongyiTranslate (AnyTrans) resources via OpenAPI or SDK workflows, including listing, creating, updating, checking task status, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to discover AnyTrans APIs, configure least-privilege Alibaba Cloud credentials, run list/create/update/status workflows, and capture reproducible evidence for translation service resource administration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud administration workflows can change Alibaba Cloud AnyTrans resources if create, update, modify, or set operations are executed with privileged credentials.

Mitigation: Use least-privilege Alibaba Cloud credentials and review every mutating action before it runs.

Risk: Saved command output or API summaries could expose access keys, secrets, resource identifiers, or other sensitive operational details.

Mitigation: Avoid saving access keys or secret-bearing output in output/aliyun-anytrans-translate/ and review evidence files before sharing them.

## Reference(s):

- [Skill source references](references/sources.md)
- [Alibaba Cloud AnyTrans OpenAPI product page](https://api.aliyun.com/product/AnyTrans)
- [AnyTrans OpenAPI metadata API list](https://api.aliyun.com/meta/v1/products/AnyTrans/versions/2025-07-07/api-docs.json)
- [AnyTrans single API metadata definition](https://api.aliyun.com/meta/v1/products/AnyTrans/versions/2025-07-07/apis/{ApiName}/api.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python command examples; generated evidence files may be JSON or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses output/aliyun-anytrans-translate/ for saved artifacts, command outputs, and API response summaries.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
