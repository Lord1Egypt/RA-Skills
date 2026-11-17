## Description:

根据公司资料起草七节投决备忘录，为数字附上来源定位并列出缺失信息，同时保留正反依据供人工复核。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

投研人员可用它整理公司投前材料并生成便于逐条回查的内部讨论稿。备忘录仅供人工复核，不提供评级、目标价、买卖建议或最终决议。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional online setup may expose the API key if request destinations or redirects are not validated.

Mitigation: Use the local workflow without credentials until authenticated requests validate destinations and handle redirects safely; review and pin optional integrations.

Risk: Citation checks can be bypassed, and a passing format check does not establish that a claim is factually correct.

Mitigation: Manually verify citations against the cited source and review the draft before relying on it.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huhoo/skills/cue-ic-memo-cn)
- [Cue data access setup](https://cuecue.cn/hub/mcp)
- [Cue material parsing setup](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Markdown, JSON, JSONL]

**Output Format:** [Seven-section Markdown memo, JSON run account, and JSONL source index]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft for human review; missing information is listed, and numeric claims include source locators.]

## Skill Version(s):

0.3.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
