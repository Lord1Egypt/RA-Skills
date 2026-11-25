## Description:

抖音公开数据智能获取工具。当用户需要做抖音内容研究、抖音选题、热点观察、竞品内容对比、趋势判断或素材整理时使用。面向内容运营、品牌调研和创作者。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

内容运营、品牌调研人员和创作者可用它查找抖音公开视频、用户、作品详情、评论和热榜数据，并据此整理选题、比较竞品内容或分析趋势。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a benign result with medium confidence, partial coverage (31 of 53 components fully scanned), and a degraded tool-misuse analyzer; disclosure and tool-scope questions remain.

Mitigation: Review the skill's data disclosure and command scope before use, and keep execution within its documented read-only public-data functions.

Risk: The skill sends search keywords or content links to a third-party API and requires a GuaiKei access token.

Mitigation: Make the data transfer clear to the user, keep the token in GUAIKEI_API_TOKEN, and obtain user agreement before paid or large-volume queries.

## Reference(s):

- [Command options](references/options.md)
- [Output contract](references/contract.md)
- [Errors and retry guidance](references/errors.md)
- [Demand mining guide](references/demand-mining.md)
- [Public audience research guide](references/customer-acquisition.md)
- [GuaiKei API access and support](https://www.guaikei.com)
- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/douyin-jingpin-zhixi)

## Skill Output:

**Output Type(s):** [Structured JSON, Analysis, Guidance]

**Output Format:** [Structured JSON results with concise text or Markdown analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public data; returned media and share URLs may expire.]

## Skill Version(s):

1.4.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
