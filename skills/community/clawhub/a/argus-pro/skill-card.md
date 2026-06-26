## Description: <br>
Argus Pro scans Python and JavaScript codebases with 40+ rules covering security, bugs, performance, and code quality, then returns prioritized findings, fix suggestions, and CI-ready reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to scan Python and JavaScript projects for security issues, likely bugs, performance patterns, and quality concerns before sharing reports or using CI gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads source files under SOURCE_PATH and can include code snippets in generated reports. <br>
Mitigation: Set SOURCE_PATH and IGNORE_PATHS deliberately, and review generated Markdown and JSON reports before sharing or committing them. <br>
Risk: The setup command may modify the system Python environment if run directly. <br>
Mitigation: Use a virtual environment for installation instead of modifying system Python. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/occupythemilkyway/argus-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Console findings plus local Markdown and JSON report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are written as argus_pro_report_DATE.md and argus_pro_report_DATE.json; CI runs can fail on critical findings when configured.] <br>

## Skill Version(s): <br>
1.0.4 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
