## Description:

判定 Python 代码是原创还是演绎作品，给出与上游最长相同表达片段、逐条豁免依据和风险清单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ffseika0304](https://clawhub.ai/user/ffseika0304)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to compare Python code against an upstream reference, identify likely derivative-work risk, and produce preview or full audit reports for source-code ownership review. It is intended as an engineering self-check, not legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid certification involves a remote payment service, an external Alipay wallet CLI, and real payment actions.

Mitigation: Require explicit user approval before installing or running payment tooling, and keep the audit workflow local until the user chooses paid certification.

Risk: Certified output may not be reliable while the receipt verification flaw described by the security evidence remains unresolved.

Mitigation: Do not rely on certified reports as authoritative proof until receipt verification is fixed and reviewed.

Risk: The security evidence marks the release suspicious due to under-scoped paid unlock behavior and payment-tool installation risk.

Mitigation: Review the paid unlock path, external installer use, and certification flow before installing or deploying the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ffseika0304/skills/code-ownership-audit)
- [Project homepage](https://xiaping.coze.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [CLI output, JSON reports, Markdown reports, and payment or verification command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preview reports withhold code locations and fixes; full paid reports can include detailed findings, remediation guidance, exportable files, and a signed certification receipt.]

## Skill Version(s):

1.3.3 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
