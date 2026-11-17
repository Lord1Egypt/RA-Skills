## Description:

用 Cue 帮你看清被套的股票上方还有哪几道坎——从筹码分布定位套牢盘、用均线校验阻力强度、推演反弹每一步需要的量能，产出可复核的解套压力线底稿，辅助判断反弹到哪容易卡住、哪里该减仓。

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

投资者可用此技能梳理单只股票上方的套牢筹码、技术阻力和反弹所需量能，并查看结构化报告以辅助判断反弹可能受阻的位置。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to share an API key in chat.

Mitigation: Configure the API key locally instead of sharing it in chat.

Risk: The skill installs or updates an external runner without pinning its version before execution.

Mitigation: Review the runner source and verify its version before execution.

Risk: The security review is incomplete because a referenced local path was missing.

Mitigation: Review the missing path and complete the scan before relying on the assessment.

## Reference(s):

- [Cue platform](https://cuecue.cn)
- [Runner source described by the skill](https://github.com/sensedeal/cue-skills)
- [Runner mirror described by the skill](https://gitee.com/sensedeal/cue-skills)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Structured Markdown report with analysis, risk notes, and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A report about one stock; findings depend on the available market data and Cue service.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
