## Description: <br>
Read-only exploration and planning skill for safe code analysis. This skill should be used when the user asks to enter plan mode, analyze before changing, create a plan first, or wants a safe exploration phase before making edits. Enforces read-only tool access, produces a numbered plan under a Plan: header, and tracks step completion with [DONE:n] markers during execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[orangon](https://clawhub.ai/user/orangon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to explore code safely before editing, produce a numbered implementation plan, and track completion of planned steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create a Markdown plan file in the repository. <br>
Mitigation: Review the generated plan path and contents before committing or treating it as approved project guidance. <br>
Risk: Read-only environment or network inspection commands can expose sensitive workspace information when used around secrets. <br>
Mitigation: Avoid environment and network inspection commands in secret-bearing workspaces unless that inspection is explicitly intended. <br>


## Reference(s): <br>
- [Bash Command Safety Reference for Plan Mode](references/safe-commands.md) <br>
- [ClawHub release page](https://clawhub.ai/orangon/along-plan) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown plan with numbered steps, checklist items, acceptance criteria, and [DONE:n] completion markers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a Markdown plan file at docs/plan-<topic>.md or doc/plan-<topic>.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
