## Description:

锅炉压力容器定期检验与台账核对（免费版）对中文锅炉和压力容器台账执行 6 项本地检查，逐行复算检验有效期、证件覆盖、安全阀压力表校验、重复登记、合计行和字段合法性，并在每条结论中引用原文行号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Equipment, safety, facilities, and operations teams use this skill during periodic Chinese boiler and pressure-vessel ledger reviews to check whether required ledger fields are present and internally consistent. It helps flag overdue dates, expired or missing certificates, invalid fields, duplicate equipment IDs, and mismatched totals from copied table text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill checks ledger text locally and does not verify official certificates, inspection reports, or regulatory status online.

Mitigation: Use findings as a triage aid and confirm certificate authenticity, inspection conclusions, and legal compliance with authoritative records or qualified personnel.

Risk: Missing or malformed Chinese-format table headers can prevent checks from running or make the output incomplete.

Mitigation: Provide the required headers and source rows from the ledger, and treat insufficient-input output as no conclusion rather than as a clean result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/boiler-pressure-vessel-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable console output or JSON containing executed checks, missing-input guidance, and ledger findings with cited source lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard-library code; requires copied table text with required headers and does not verify official certificates online.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
