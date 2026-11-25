## Description:

用 Cue 穿透待核查资讯的表层表述——通过独立信源交叉验证与底层数据复核，精准识别时间错位、数据偏差及误导性信息，产出包含原文对照与纠偏证据的结构化事实核查报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

面向研究分析师、记者及尽调人员，用于核查研报、新闻、经营数据和市场传言中的事实。它通过多源对照识别时间错位、数字偏差或误导性表述，并生成带有纠偏证据和来源链接的报告。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that an unpinned external runner executes with the agent’s permissions.

Mitigation: Avoid installation until the runner is pinned to a reviewed version; inspect and approve the runner before use.

Risk: The skill’s API key setup could lead users to share a secret in chat.

Mitigation: Store the API key in the local configuration or CUE_API_KEY environment variable and do not paste it into chat.

Risk: The scan reports a mismatch between the fact-checking description and some behavior, and its results are incomplete.

Mitigation: Review the skill behavior before use and independently verify report claims against cited sources.

## Reference(s):

- [事实核查技能发布页](https://clawhub.ai/panting09266-ai/skills/cue-fact-check)
- [Cue 平台](https://cuecue.cn)
- [Cue API Key 管理](https://cuecue.cn/api-key?src=clawhub-fact-check)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [结构化中文事实核查报告（Markdown）]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [逐条呈现待核查原文、结论、纠偏证据、独立信源对照、偏差分析和来源链接。]

## Skill Version(s):

1.0.17 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
