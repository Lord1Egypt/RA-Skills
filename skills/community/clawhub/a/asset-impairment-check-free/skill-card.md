## Description:

资产减值测试表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounting users use this skill to locally check Chinese-language asset impairment test tables during close, reconciliation, or review workflows. It performs bounded arithmetic, total-row, duplicate-row, blank-field, and negative-amount checks and cites source rows for each finding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A clean result could be mistaken for a full accounting or audit opinion even though the free version omits advanced checks.

Mitigation: Treat results as bounded table-checking assistance only; review omitted checks and rely on qualified accounting judgment for impairment conclusions.

Risk: Incomplete or unrecognized table input can prevent meaningful checking.

Mitigation: Provide a complete asset impairment table with recognizable headers and treat insufficient-input responses as no conclusion.

Risk: Financial table contents may be sensitive.

Mitigation: Run the packaged local Node.js checker on copied table data; server evidence reports bounded local checks without network use or persistence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/asset-impairment-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)
- [Sample input template](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Human-readable text or JSON from a local Node.js command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source rows; insufficient input returns missing-field guidance instead of a clean-result conclusion.]

## Skill Version(s):

1.0.54 (source: server release and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
