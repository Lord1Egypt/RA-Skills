## Description:

依据中国工信部《互联网网站适老化通用设计规范》和《移动互联网应用(APP)适老化通用设计规范》，对项目代码进行适老化合规检测，生成问题报告、修改建议，并支持自动修复。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuyuting133](https://clawhub.ai/user/xuyuting133)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit web and mobile app UI code against elderly-accessibility criteria, including typography, contrast, touch targets, captcha alternatives, ads, navigation, and assistive-technology compatibility. It can generate a local HTML report with findings and proposed fixes, and can apply narrowly scoped style fixes when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read UI-related project files and generate elderly-audit-report.html.

Mitigation: Review the generated report before using its findings for compliance or release decisions.

Risk: When fix mode is explicitly requested or approved, the skill may edit style values.

Mitigation: Review generated diffs before committing fixes, especially where web and app checklist items may overlap.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuyuting133/skills/elderly-ui-audit)
- [Server-resolved GitHub provenance](https://github.com/XuYuting133/elderly-ui-audit/tree/main/skills/elderly-ui-audit)
- [Project homepage](https://github.com/XuYuting133/elderly-ui-audit)
- [Issue tracker](https://github.com/XuYuting133/elderly-ui-audit/issues)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus a generated local HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write elderly-audit-report.html and may edit style values only when fix mode is explicitly requested or approved.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
