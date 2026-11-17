## Description:

企业AI应用诊断工具帮助企业评估AI应用价值、计算ROI并规划实施路径，适用于企业AI应用咨询和转型评估场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickyhu1699](https://clawhub.ai/user/nickyhu1699)

### License/Terms of Use:

MIT-0

## Use Case:

Business owners, startup teams, and digital transformation leads use this skill to evaluate where AI may help their organization, estimate ROI, and draft phased implementation plans and reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Questionnaires and reports may contain sensitive business information.

Mitigation: Use only non-confidential business information unless the user is comfortable with how generated reports and questionnaires will be shared.

Risk: Generated HTML reports from untrusted input may create unsafe report content.

Mitigation: Avoid generating or hosting HTML reports from untrusted input until HTML escaping is added and reviewed.

Risk: Custom report filenames may be unsafe without path validation.

Mitigation: Do not pass custom filenames to report-saving functions until path validation is added.

Risk: Reports include hardcoded contact details.

Mitigation: Remove the hardcoded contact details or make them explicitly configurable before using reports with clients or customers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nickyhu1699/skills/enterprise-ai-diagnosis)
- [Artifact README](artifact/README.md)
- [Assessment questionnaire template](artifact/templates/questionnaire.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, HTML report files, Python snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save generated reports when the provided scripts are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
