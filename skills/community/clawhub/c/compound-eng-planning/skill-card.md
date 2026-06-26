## Description: <br>
Provides a workflow for planning software implementation work with file-based `.plan/` persistence when changes span multiple files, have ambiguous scope, or require architectural decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iliaal](https://clawhub.ai/user/iliaal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to decide when to create structured implementation plans, persist planning state in `.plan/`, and prepare phase-by-phase handoffs for code changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the helper script can overwrite existing `.plan/` planning files and modify `.gitignore`. <br>
Mitigation: Review or preserve any existing `.plan/` files before running the script, run it from the intended repository root, and inspect the resulting file changes. <br>
Risk: Planning guidance can send implementation work in the wrong direction if the task goal is vague or unverifiable. <br>
Mitigation: Use the goal quality gate and review the generated plan for measurable outcomes, scope boundaries, and concrete verification steps before implementation. <br>


## Reference(s): <br>
- [Operational Patterns](references/operational-patterns.md) <br>
- [Plan Deepening](references/plan-deepening.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown planning documents with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or overwrite `.plan/task_plan.md`, `.plan/findings.md`, and `.plan/progress.md`; the helper script may also append `.plan/` to `.gitignore`.] <br>

## Skill Version(s): <br>
4.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
