## Description:

摩天轮开放接口二次封装技能。当用户需要对接摩天轮(MTL)开放平台接口、创建MTL HTTP接口、封装摩天轮API时触发。支持自动检测并添加mtl-open-sdk-consumer依赖、初始化ApiClient Bean、创建MtlRestController、根据原生接口定义生成HTTP接口代码。

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to wrap native Motianlun (MTL) open platform APIs as Spring Boot HTTP endpoints. It guides dependency setup, ApiClient bean initialization, controller creation, route generation for GET and POST requests, and optional logging when the target project already provides the expected logging class.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's examples include MTL credential placeholders and generated proxy endpoints that require application-specific security review.

Mitigation: Load credentials from a secrets manager or protected runtime configuration, and require authentication and authorization on every generated route.

Risk: Generated endpoints may expose broad MTL operations or return sensitive implementation details if adapted without controls.

Mitigation: Restrict exposed operations to an allowlist, avoid returning raw exception messages, and redact or omit request and response payloads from logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/chuyao-aa)
- [Publisher profile](https://clawhub.ai/user/1688aiinfra)

## Skill Output:

**Output Type(s):** [code, configuration, guidance]

**Output Format:** [Markdown guidance with Java and XML code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated code requires project-specific review before use with live MTL credentials or exposed HTTP routes.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
