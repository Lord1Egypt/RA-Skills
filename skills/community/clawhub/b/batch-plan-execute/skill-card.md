## Description: <br>
Use when the user wants AI to turn a requirement text, requirement document, and existing reviewed plan files into dependency-ordered implementation plans and, only after an explicit execution command, implement those plans with subagents in parallel where safe and in sequence where required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[micooz](https://clawhub.ai/user/micooz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to convert requirements, requirement files, or existing plan directories into dependency-aware implementation plans. After an explicit execution command, it guides implementation through reviewed plans with conservative dependency sequencing and validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Execution mode can modify repository files and run project validation commands after the user explicitly starts implementation. <br>
Mitigation: Use the skill in version-controlled workspaces, review generated plans before execution, and reserve execution phrases such as "implement now" or "apply the plan" for approved work. <br>
Risk: Plan and state files can persist implementation assumptions across revisions. <br>
Mitigation: Review generated plan files and plans/.batch-plan-state.json when requirements change, especially before executing revised or obsolete-plan work. <br>
Risk: Validation commands in untrusted repositories can execute project code. <br>
Mitigation: Inspect repository scripts and run the skill only in trusted or sandboxed projects when validation commands may execute local code. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/micooz/batch-plan-execute) <br>
- [Plan Mode Contract](artifact/docs/plan.md) <br>
- [Execute Mode Contract](artifact/docs/execute.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown plans, repository file changes, shell commands, and concise execution summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update plans/.batch-plan-state.json and plan Markdown files; execution mode is gated by an explicit user command.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
