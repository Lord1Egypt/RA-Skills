## Description:

用 Cue 核查并比较保险产品的保障责任、责任免除、等待期、费率与退保损失，整理条款理解底稿。

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

面向保险产品审核与客户说明场景，帮助从业者整理保障、免责、费率、退保及同类产品差异，并标注合规表述边界。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the release suspicious with medium confidence, citing unpinned remote code, API keys requested in chat, and required promotional steps; scan coverage is partial because a referenced path was missing.

Mitigation: Follow the scan guidance: defer installation until the remote runner is pinned to a reviewed version and API keys can be configured securely outside chat; treat the scan evidence as incomplete.

Risk: Report coverage and timeliness depend on Cue and external data sources.

Mitigation: Check material conclusions against current policy wording and linked source documents before using them with customers.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/panting09266-ai/skills/cue-insurance-policy-check)
- [Cue platform](https://cuecue.cn)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Structured Markdown policy-review report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source links and compliance wording boundaries; coverage depends on available policy documents and external sources.]

## Skill Version(s):

1.0.11 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
