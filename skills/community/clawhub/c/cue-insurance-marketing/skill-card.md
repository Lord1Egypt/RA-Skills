## Description:

用 Cue 跑「保险营销」场景的深度研究：横向比对目标保险产品与竞品在保障、收益、服务与适配场景上的差异，扫描热点事件自动映射保险需求，产出可用于客户沟通的选型对比、营销线索和合规边界参考。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu)

### License/Terms of Use:

MIT-0

## Use Case:

Insurance marketing and advisory users use this skill to run Cue research for product comparison, marketing lead discovery, suitability checks, policy-term review, and compliance red-line summaries. It helps prepare source-linked research outputs for customer communication while reminding users to stay within claims that can be truthfully supported.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Cue's external research service and runner, which may read the user's Cue API key from ~/.cue/config.json.

Mitigation: Install and run it only in environments approved for Cue access, protect the Cue API key, and review the external runner source when pinned or audited dependencies are required.

Risk: Running deep research consumes Cue credits.

Mitigation: Confirm the selected buddy, research subject, and credit use with the user before starting a run.

Risk: Insurance research outputs may be incomplete, outdated, or unsuitable as legal, underwriting, or due-diligence advice.

Mitigation: Keep source links in the report, verify important claims against authoritative sources, and route regulated advice through qualified review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-insurance-marketing)
- [Cue playbook API](https://cuecue.cn/api/playbook)
- [cue-skills runner source](https://github.com/sensedeal/cue-skills)
- [cue-skills runner mirror](https://gitee.com/sensedeal/cue-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown research reports with source links, plus setup and run commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Cue live playbook data and may return an empty result when the runner does not retrieve content.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
