## Description:

Audits catalyst preparation and evaluation materials for whether they provide enough detail to execute experiments, reproduce conditions, compare controls, attribute variables, and validate performance or mechanism claims.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External users, researchers, and technical reviewers use this skill to pre-audit catalyst preparation steps, paper methods, patent examples, research proposals, and draft experimental plans before relying on them for laboratory execution or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit script can recursively delete the selected output directory before report generation.

Mitigation: Run it only with a dedicated empty output directory such as outputs, and do not point --out at a project folder, home directory, shared workspace, or any directory containing files that need to be preserved.

Risk: The skill depends on an external MCP service for full functionality.

Mitigation: Confirm the provider account, data flow, and retention terms before sending proprietary experimental materials through the configured MCP integration.

## Reference(s):

- [Skill page](https://clawhub.ai/yuanzhian-patsnap/skills/catalyst-method-auditor)
- [审核方法说明](artifact/references/methodology.md)
- [智慧芽开放平台](https://open.zhihuiya.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Concise chat guidance plus generated JSON, HTML, and Word report files when the audit script is executed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill is designed to produce one report context JSON file, one HTML report, and one Word report in the selected output directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact VERSION and changelog report 0.4.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
