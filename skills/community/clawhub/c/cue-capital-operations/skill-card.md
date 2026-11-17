## Description:

用 Cue 跑「资本运作」场景的深度研究：全量回溯上市公司的并购重组、股份回购、股权激励与分拆商机，多源公开数据交叉、深挖战略意图与市场影响，每个结论都带来源链接可回查。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu)

### License/Terms of Use:

MIT-0

## Use Case:

External finance, management, investment banking, and investor users use this skill to run Cue-assisted capital operations research on listed companies, including M&A, buybacks, equity incentives, spin-offs, disclosures, and related event timelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch or update and then run mutable external Cue runner code outside the reviewed skill package.

Mitigation: Use an already reviewed local checkout or pin the Cue runner to a trusted commit before running it.

Risk: The runner can access the user's Cue API key and consume Cue credits.

Mitigation: Confirm the selected buddy, subject, and credit-spending prompt before starting a run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaoxu/skills/cue-capital-operations)
- [Cue playbook API referenced by the skill](https://cuecue.cn/api/playbook)
- [Cue runner repository referenced by the skill](https://github.com/sensedeal/cue-skills)
- [Cue runner mirror referenced by the skill](https://gitee.com/sensedeal/cue-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown research report with source links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deep research may take several minutes and can consume Cue credits after user confirmation.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
