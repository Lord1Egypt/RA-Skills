## Description:

为 Fast Claw 付费演示微服务获取、保存、充值并使用持久 API key，支持发起购买或充值 checkout 流程、缓存 API key、查询账户余额，并携带 API key 调用 Fast Claw 微服务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[coder-pig](https://clawhub.ai/user/coder-pig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to manage a local Fast Claw API key, start purchase or top-up checkout flows, inspect account status, invoke the paid service, and poll longer-running report jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable payment-service credentials are cached locally and can authorize paid Fast Claw requests.

Mitigation: Treat ~/.fast-claw/api-key.json and any path set through FAST_CLAW_API_KEY_PATH or FAST_CLAW_TOKEN_PATH as secrets; avoid sharing, logging, or storing them in synchronized folders.

Risk: Configured service endpoints receive prompts and API keys, and paid actions can spend account credits.

Mitigation: Use only a trusted HTTPS Fast Claw service URL and confirm before purchase, top-up, invoke, or report commands.

Risk: Passing API keys as command-line arguments can expose them through shell history or process listings.

Mitigation: Prefer existing local API key storage or controlled environment-specific secret handling instead of passing credentials directly on the command line.

## Reference(s):

- [Fast Claw 服务接口说明](references/service-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON service responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local API key status, checkout URLs, masked credentials, account balance responses, invocation responses, report job IDs, and completed report text.]

## Skill Version(s):

0.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
