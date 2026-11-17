## Description:

用 Cue 穿透待核查资讯的表层表述——通过独立信源交叉验证与底层数据复核，精准识别时间错位、数据偏差及误导性信息，产出包含原文对照与纠偏证据的结构化事实核查报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要核对研报、新闻、尽调数据或市场传言的用户，调用 Cue 对原文进行多源交叉验证，检查时间、数据和表述偏差，并生成带来源链接的结构化核查报告。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key setup described by the skill may expose credentials when a key is shared in chat.

Mitigation: Store the key in local configuration or a secret manager, and avoid sending the key in chat.

Risk: The external Cue runner is cloned or updated without a pinned revision.

Mitigation: Review the runner source and pin a trusted revision before installation or updates.

Risk: Some document conversion instructions may not fit the skill's fact-checking purpose.

Mitigation: Review conversion steps and dependencies before use; run them only when document conversion is intended.

## Reference(s):

- [Cue 平台](https://cuecue.cn)
- [示例核查报告](https://cuecue.cn/share/680abf29664d)

## Skill Output:

**Output Type(s):** [Analysis, Markdown]

**Output Format:** [结构化 Markdown 事实核查报告，包含原文对照、核查结论、纠偏证据和来源链接]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [来源不可用时，结论可能为无法核实。]

## Skill Version(s):

1.0.13 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
