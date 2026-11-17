## Description:

Helps agents manage Alibaba Cloud AIContent through OpenAPI or SDK workflows, including asset listing, content generation configuration, task status checks, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to guide Alibaba Cloud AIContent OpenAPI or SDK tasks, including discovery, configuration changes, generation workflow operations, status checks, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide create, update, modify, or set operations against Alibaba Cloud AIContent resources.

Mitigation: Use least-privilege Alibaba Cloud credentials and review every proposed mutating operation before execution.

Risk: Generated output files or saved API responses could include sensitive cloud data if the user asks to persist raw results.

Mitigation: Store outputs only in the dedicated output directory and avoid saving secrets or sensitive response bodies.

Risk: Using an incorrect or assumed region can target the wrong Alibaba Cloud environment.

Mitigation: Confirm the region and resource identifiers before API calls, and ask the user when the region is unclear.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/cinience/skills/aliyun-aicontent-generate)
- [Sources](references/sources.md)
- [Alibaba Cloud OpenAPI product page for AiContent](https://api.aliyun.com/product/AiContent)
- [AiContent 20240611 API list metadata](https://api.aliyun.com/meta/v1/products/AiContent/versions/20240611/api-docs.json)
- [AiContent 20240611 single API metadata pattern](https://api.aliyun.com/meta/v1/products/AiContent/versions/20240611/apis/{ApiName}/api.json)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, markdown]

**Output Format:** [Markdown guidance with inline shell commands, configuration notes, and generated output files when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save API inventories, response summaries, and task evidence under output/aliyun-aicontent-generate/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
