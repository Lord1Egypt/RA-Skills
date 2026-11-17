## Description:

基于用户提供的多维度健康数据，如基本信息、生理指标、生活方式、既往病史和体检结果，进行综合分析与风险评估，并生成结构化、个性化的健康评估报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lantian888](https://clawhub.ai/user/lantian888)

### License/Terms of Use:

MIT-0

## Use Case:

External users provide health history, medication context, lifestyle factors, and lab or examination results so the agent can collect required information, call a remote medical model, and return the resulting health risk assessment. The skill can also create an HTML health report from structured patient and assessment data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive health details and full conversation history may be sent to third-party remote services.

Mitigation: Require explicit user consent and privacy disclosure before use, minimize identifiers and history sent to the API, and document the remote service dependency.

Risk: API credentials or token-fetching behavior may expose or reuse secrets without adequate control.

Mitigation: Rotate and remove exposed credentials, store secrets outside the artifact, and use scoped credentials with clear permission declarations.

Risk: Generated HTML reports and verbatim remote medical output may include untrusted or unsafe content.

Mitigation: Sanitize HTML before rendering or saving reports, constrain report file paths, and require human review before relying on medical content.

Risk: Health risk assessments can be mistaken for diagnosis or treatment advice.

Mitigation: Keep medical disclaimers visible, route urgent symptoms to emergency care, and direct users to qualified clinicians for diagnosis and treatment decisions.

## Reference(s):

- [API docs](references/api_docs.md)
- [ClawHub skill page](https://clawhub.ai/lantian888/skills/geneplus-health-assistant)
- [Publisher profile](https://clawhub.ai/user/lantian888)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown responses and optional HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses streamed remote API output and may preserve returned Markdown verbatim.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
