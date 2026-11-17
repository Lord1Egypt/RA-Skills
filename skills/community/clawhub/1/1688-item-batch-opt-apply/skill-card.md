## Description:

Coordinates batch optimization requests for 1688 products and media by confirming tasks, delegating work to execution skills, tracking results, and preparing exports and user-approved product updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

1688 seller support agents use this skill to turn a batch of product or media requests into confirmed optimization tasks, delegate each task, review and export results, and guide user-approved listing changes. Product updates wait until the user reviews the results and asks to apply them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Export may install an additional package automatically when the spreadsheet dependency is missing.

Mitigation: Choose CSV export without package installation, or provision a reviewed dependency in an isolated environment.

Risk: Changes could be applied to the wrong products or with unintended final values.

Mitigation: Keep per-product confirmations and verify the selected products and final changes before applying.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/1688aiinfra/skills/1688-item-batch-opt-apply)
- [1688 offer property query](https://1688bot.alibaba-inc.com/#/tool/detail?code=query_offer_prop)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Files]

**Output Format:** [Structured task and result data, Markdown summaries, and Excel or CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-task results and export files; product updates require user approval through the relevant execution flow.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
