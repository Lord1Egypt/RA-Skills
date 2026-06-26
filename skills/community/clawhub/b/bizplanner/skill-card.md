## Description: <br>
Create business plans, lean canvases, and financial projections. Use when pitching investors, planning startups, or modeling revenue scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, founders, and operators can use this skill to record business-planning notes from the command line, search prior entries, view simple activity statistics, and export accumulated logs for reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-entered business data is saved in local log files under the home directory. <br>
Mitigation: Avoid entering confidential information unless local storage in ~/.local/share/bizplanner/ is acceptable, and review or remove local logs before sharing the environment. <br>
Risk: The release presents business-planning language, but security evidence characterizes the artifact as a local command-line data logger rather than a full plan or financial-model generator. <br>
Mitigation: Treat outputs as logged notes and simple exports, and review any planning or financial conclusions separately before relying on them. <br>


## Reference(s): <br>
- [ClawHub Bizplanner release page](https://clawhub.ai/bytesagain1/bizplanner) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and plain-text status or export output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI stores user-entered data locally under ~/.local/share/bizplanner/ and can export entries as JSON, CSV, or text.] <br>

## Skill Version(s): <br>
2.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
