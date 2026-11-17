## Description:

为中国大陆高德打车用户处理实时与预约叫车、订单查询和取消，并提供发票及客服指引。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lbs-amap](https://clawhub.ai/user/lbs-amap)

### License/Terms of Use:

MIT-0

## Use Case:

在高德打车覆盖的中国大陆城市出行的用户，可通过自然语言规划实时或预约行程、确认叫车、查询或取消订单，并获得发票与客服指引。

### Deployment Geography for Use:

中国大陆（高德打车服务覆盖的城市）

## Known Risks and Mitigations:

Risk: Using the ride service involves sharing trip locations, timing, and preferences with Amap.

Mitigation: Review the service's data handling before use, and avoid committing saved home or work addresses to shared files.

Risk: The configured Amap Key identifies the account and payer for ride orders.

Mitigation: Use only the user's own Key; never use another person's Key or store it in scripts or version control.

## Reference(s):

- [MCP 鉴权与 Key 配置](artifact/references/auth.md)
- [高德打车 MCP 工具契约](artifact/references/tool-contracts.md)
- [错误码与失败处理](artifact/references/errors.md)
- [定时任务模板](artifact/references/scheduling.md)
- [高德开放平台 Key 申请](https://lbs.amap.com/api/webservice/create-project-and-key)

## Skill Output:

**Output Type(s):** [Text, Markdown, MCP tool calls, Configuration guidance]

**Output Format:** [Natural-language guidance and structured MCP tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requests user confirmation before placing or cancelling an order.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
