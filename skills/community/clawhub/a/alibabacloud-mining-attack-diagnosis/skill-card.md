## Description:

Diagnoses suspected cryptomining incidents in Alibaba Cloud Security Center by reviewing alerts, indicators, affected assets, attack surface, and remediation priorities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud security operators and developers use this skill to investigate suspected cryptomining activity in Alibaba Cloud Security Center, review affected assets and indicators, and prepare prioritized manual remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The investigation can expand a narrow request into account-wide checks and may produce misleading conclusions.

Mitigation: Confirm the intended account scope and queried period, and verify that retrieval succeeded before treating a clean result as conclusive or acting on remediation guidance.

Risk: Saved reports can contain infrastructure details.

Mitigation: Protect investigation reports and limit access to people who need them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-mining-attack-diagnosis)
- [Detection flow](references/detection_flow.md)
- [Mining indicators reference](references/mining_indicators.md)
- [Remediation best practices](references/module5_remediation_best_practices.md)
- [Alibaba Cloud CLI setup documentation](https://help.aliyun.com/document_detail/121541.html)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Guidance]

**Output Format:** [Markdown or JSON investigation report with findings, indicators, affected assets, risk assessment, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report contents vary by account scope and lookback period; the skill provides read-only investigation and manual response guidance.]

## Skill Version(s):

0.0.2 (source: references/manifest.json and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
