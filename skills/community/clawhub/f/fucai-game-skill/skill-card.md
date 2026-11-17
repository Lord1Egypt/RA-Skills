## Description:

福彩筛选 helps agents query China Welfare Lottery results and produce filtering, trend-analysis, charting, and number-selection guidance for 双色球, 福彩3D, 七乐彩, 快乐8, 东方6+1, and 15选5.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xljcheng](https://clawhub.ai/user/xljcheng)

### License/Terms of Use:

MIT-0

## Use Case:

External users interested in China Welfare Lottery workflows use this skill to query recent results, filter candidate number sets, inspect hot/cold and trend statistics, and generate lottery-number suggestions and charts across six supported games. Recommendations should be treated as reference or entertainment, not reliable predictions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes a documented remote installer command that pipes curl output into a shell.

Mitigation: Review and verify the installer source and integrity before running it; prefer a pinned or inspected installer path during deployment.

Risk: Lottery-number recommendations can be mistaken for reliable predictions.

Mitigation: Present recommendations as entertainment or reference material and remind users that lottery draws are random independent events.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xljcheng/skills/fucai-game-skill)
- [福彩过滤规则参考](artifact/references/filter-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, lottery number lists, command snippets, and generated chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local CSV caches and generate PNG charts when charting workflows are invoked.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
