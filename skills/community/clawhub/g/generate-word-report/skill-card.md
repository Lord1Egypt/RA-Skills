## Description:

根据采集的市场数据，生成结构化的每日金融市场 Word 日报，不依赖外部 Word 模板。

This skill is ready for commercial/non-commercial use.

## Publisher:

[szrw1825](https://clawhub.ai/user/szrw1825)

### License/Terms of Use:

MIT-0

## Use Case:

Financial-market analysts and operators use this skill to turn collected market data into a formatted daily Word report covering global markets, policy, technology events, other markets, and upcoming economic data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The report script loads executable configuration from a hard-coded external workspace path before generating the document.

Mitigation: Review and trust the external configuration directory before installation; prefer a packaged or non-executable configuration file and narrower trigger wording before routine use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/szrw1825/skills/generate-word-report)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Word document generated from Python scripts and market_data.json inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a .docx daily financial market report at the configured output path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
