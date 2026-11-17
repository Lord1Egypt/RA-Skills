## Description:

EU AI Act Compliance Check helps users assess AI systems against 12 core requirements from Regulation (EU) 2024/1689, with an offline preview and optional cloud scoring through compliancehub.cn.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

External users, compliance teams, developers, and deployers use this skill to preview EU AI Act checklist items and run a scored self-assessment that returns text, JSON, or HTML reporting with risk levels and remediation suggestions. It is general compliance guidance and does not replace legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scored runs transmit checklist answers and either an API key or anonymous trial id to compliancehub.cn.

Mitigation: Use the offline preview for sensitive projects and run scored checks only when the user accepts cloud transmission.

Risk: Generated HTML reports may include fields returned by the remote scoring service.

Mitigation: Review generated reports before sharing and treat remote report content cautiously until escaping is confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwumit/skills/ai-act-check)
- [ComplianceHub cloud scoring service](https://compliancehub.cn)
- [ComplianceHub account page](https://compliancehub.cn/account.html?skill=ai-act-check)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [CLI text, JSON, and HTML reports; guidance may include Markdown with shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scored runs send checklist answers to compliancehub.cn; offline preview lists bundled checklist items without contacting the cloud.]

## Skill Version(s):

1.0.2 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
