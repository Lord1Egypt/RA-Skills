## Description:

ALAPI 接口对接助手，帮助开发者搜索 ALAPI 接口、读取 ALAPI 文档、提取参数、生成 ALAPI 对接代码，并在用户明确提供 token 且确认后调用 ALAPI 接口。

This skill is ready for commercial/non-commercial use.

## Publisher:

[anhao](https://clawhub.ai/user/anhao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to find ALAPI endpoints, read API documentation and OpenAPI specs, identify required parameters and response fields, and generate integration code. It can also perform a live ALAPI call only when the user explicitly requests it and a token is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live calls may send ALAPI_TOKEN and request parameters to ALAPI.

Mitigation: Make live calls only after explicit user request, prefer environment or server-side token storage, avoid token-bearing shell history or shareable snippets, and rotate any token that may have been logged.

Risk: Installing from an untrusted or moving source may change the skill behavior.

Mitigation: Install only from a trusted source and pin the reviewed source revision before deployment.

Risk: Incomplete API documentation could lead to incorrect parameters, response assumptions, or generated code.

Mitigation: Treat undocumented parameters and response fields as unconfirmed, present uncertainties to the user, and avoid fabricating defaults or fields.

## Reference(s):

- [ALAPI code examples](references/code-examples.md)
- [ALAPI API documentation pattern](https://www.alapi.cn/api/{id}/introduction)
- [ALAPI API base URL](https://v3.alapi.cn)
- [ClawHub skill page](https://clawhub.ai/anhao/skills/alapi)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON summaries and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live API-call results may include ALAPI response summaries; tokens should not be echoed in final responses.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
