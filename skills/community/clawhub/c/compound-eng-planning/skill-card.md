## Description: <br>
Software implementation planning with file-based persistence (.plan/) for code changes touching three or more files or ambiguous implementation scope. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iliaal](https://clawhub.ai/user/iliaal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this workflow to decide when to create a plan, scaffold local .plan/ state files, break implementation work into verifiable phases, and preserve findings and progress across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the helper script may create or overwrite local .plan/ planning files and may append .plan/ to .gitignore. <br>
Mitigation: Run it from the intended repository root, review existing .plan/ contents first, and preserve important planning notes before scaffolding a new task. <br>
Risk: A plan can carry incorrect assumptions forward if vague requirements or stale code observations are not checked before execution. <br>
Mitigation: Review the plan before implementation and verify scope, assumptions, file paths, and test commands against the current codebase. <br>


## Reference(s): <br>
- [ia-planning Specification](SPEC.md) <br>
- [Operational Patterns](references/operational-patterns.md) <br>
- [Plan Deepening](references/plan-deepening.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated planning files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script can create or overwrite .plan/task_plan.md, .plan/findings.md, and .plan/progress.md, and can append .plan/ to .gitignore.] <br>

## Skill Version(s): <br>
4.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
