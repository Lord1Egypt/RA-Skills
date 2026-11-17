## Description:

提供酒店项目P&L分析，包括损益表、投资回报、多店对标、成本异常诊断和偏差校准。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoliuzhu](https://clawhub.ai/user/chaoliuzhu)

### License/Terms of Use:

MIT-0

## Use Case:

Hotel operators, finance teams, and investment reviewers use this skill to collect hotel operating inputs, calculate P&L and return metrics, compare stores, identify cost anomalies, and generate management recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hotel operating and financial inputs may be commercially sensitive.

Mitigation: Use the skill only with data you are comfortable processing locally.

Risk: Provenance is unavailable, so claims such as official group data require confirmation before business reliance.

Mitigation: Verify the ClawHub publisher profile and release provenance before relying on publisher or data-source claims.

Risk: Optional chart generation depends on Python packages that may be installed by the user.

Mitigation: Install optional dependencies in an isolated environment with pinned versions when charts are needed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/chaoliuzhu/skills/delonix-pl-analysis)
- [酒店P&L数据分析模板](artifact/references/data_template.md)
- [德胧集团经营模型分析报告](artifact/references/delonix_model.md)
- [德胧集团开元名庭经营模型（真实数据）](artifact/references/delonix_real_model.md)
- [酒店P&L分析术语表](artifact/references/glossary.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with tables, formulas, optional Python-generated JSON chart configurations, and shell command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional chart generation uses Python dependencies; calculation outputs should be reviewed against source financial data before business decisions.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
