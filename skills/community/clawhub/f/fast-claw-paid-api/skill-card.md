## Description: <br>
为 Fast Claw 付费演示微服务获取、保存、充值并使用持久 API key。适用于需要发起购买或充值 checkout 流程、把返回的 API key 本地缓存、查询账户余额，或携带 API key 调用 Fast Claw 微服务的场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coder-pig](https://clawhub.ai/user/coder-pig) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to purchase or top up Fast Claw credits, cache a local API key, check account status, and invoke the paid Fast Claw service through the bundled client. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores the Fast Claw API key locally in plaintext. <br>
Mitigation: Treat the API-key file as a sensitive secret, set a controlled path when needed, and remove it with clear-api-key when no longer required. <br>
Risk: The checkout flow can initiate paid Fast Claw purchases or top-ups. <br>
Mitigation: Review the checkout page, credit amount, and service URL before completing payment. <br>
Risk: A misconfigured service URL could send prompts or API keys to the wrong endpoint. <br>
Mitigation: Verify FAST_CLAW_SERVICE_URL before invoking the service or starting checkout. <br>


## Reference(s): <br>
- [Fast Claw service API reference](references/service-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON service responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local plaintext API-key cache and a configurable Fast Claw service URL.] <br>

## Skill Version(s): <br>
0.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
