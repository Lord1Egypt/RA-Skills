## Description:

提供中国体育彩票大乐透开奖信息，支持查询开奖号码、中奖规则及指定期号详情。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenchaoqun](https://clawhub.ai/user/chenchaoqun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up China Sports Lottery 大乐透 draw results, check a specific issue number, compare ticket numbers, and review prize rules.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Third-party lottery sources may be stale, incomplete, or inconsistent with official results.

Mitigation: Prefer the official lottery.gov.cn source and verify important ticket checks against it.

Risk: Outbound requests to lottery websites can fail because of network issues, site changes, dynamic loading, or access controls.

Mitigation: Treat fetch failures as lookup failures, retry later, or visit the official site directly.

Risk: Lottery result lookup can be mistaken for betting or prediction guidance.

Mitigation: Use the skill for results and rules only, not for purchase recommendations, predictions, or financial advice.

## Reference(s):

- [大乐透数据源配置](references/data_sources.md)
- [大乐透详细规则](references/rules.md)
- [中国体彩网大乐透开奖列表](https://www.lottery.gov.cn/kj/kjlb.html?dlt)
- [ClawHub release page](https://clawhub.ai/chenchaoqun/skills/dlt-lottery)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown with draw numbers, issue details, source labels, and prize-rule summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contact listed lottery websites; third-party-source results are advisory and should be checked against the official lottery.gov.cn source for important ticket decisions.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
