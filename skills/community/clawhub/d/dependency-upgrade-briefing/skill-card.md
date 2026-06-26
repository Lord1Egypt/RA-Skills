## Description: <br>
Drafts structured dependency-upgrade briefings that explain benefits, risks, rollback plans, business impact, and recommended rollout pace from user-provided upgrade details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering leads, and release stakeholders use this skill to turn dependency name, version-change, and changelog-summary inputs into reviewable Markdown briefings for upgrade decisions, technical-debt planning, and release communication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Briefings may be incomplete or misleading if the user supplies partial upgrade details or omits upstream changelog context. <br>
Mitigation: List missing information as confirmation items and require review before using the briefing for release decisions. <br>
Risk: The local script can write generated output to a user-specified file path. <br>
Mitigation: Prefer stdout or dry-run for quick drafts and check output paths before writing files. <br>
Risk: Inputs may include sensitive business or release-planning details. <br>
Mitigation: Avoid feeding sensitive information unless it is needed for the briefing, and redact unnecessary personal or confidential details first. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/dependency-upgrade-briefing) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [Skill README](README.md) <br>
- [Output template](resources/template.md) <br>
- [Structured briefing spec](resources/spec.json) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, guidance, shell commands] <br>
**Output Format:** [Markdown briefing or JSON wrapper containing the generated report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write to stdout or to a user-specified output file; supports dry-run mode and a sample-size limit.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
