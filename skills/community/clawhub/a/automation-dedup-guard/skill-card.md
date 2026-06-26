## Description: <br>
Automation Dedup Guard helps WorkBuddy users detect and remove duplicate automation tasks while keeping the newest task in each name group. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vic276344-dotcom](https://clawhub.ai/user/vic276344-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and WorkBuddy users use this skill to inspect and clean duplicate WorkBuddy automation records, especially when task lists grow from repeated same-name automations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The cleanup script can permanently delete WorkBuddy automation tasks and related run history without confirmation or automatic backup. <br>
Mitigation: Run with --dry-run first, verify the database path and proposed deletions, and back up automations.db before executing cleanup. <br>
Risk: Scheduled automatic cleanup can remove task records repeatedly without manual review. <br>
Mitigation: Enable recurring cleanup only after validating dry-run output and accepting permanent deletion of duplicate tasks and associated run history. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vic276344-dotcom/automation-dedup-guard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled Python script prints a terminal report and uses exit code 1 when duplicates are detected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
