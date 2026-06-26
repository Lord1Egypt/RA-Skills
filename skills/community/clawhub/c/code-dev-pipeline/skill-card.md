## Description: <br>
Coordinates a multi-role coding workflow for complex software development tasks, including analysis, architecture, implementation, review, testing, validation, and optional UI design. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawaizhang](https://clawhub.ai/user/clawaizhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to structure complex coding work across defined roles for requirements analysis, architecture, coding, review, testing, and final validation. It is especially suited to multi-file feature work, frontend or UI projects, and tasks that need explicit quality checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow gives an agent broad control over coding requests and repository changes without enough user-directed scoping. <br>
Mitigation: Use it only in repositories where agent-created or agent-modified workflow artifacts are acceptable, keep tasks explicitly scoped by the user, and inspect diffs before accepting edits. <br>
Risk: Automated development output could stage or commit changes, or include sensitive data in logging examples. <br>
Mitigation: Do not allow automatic git add or commit behavior unless the diff has been inspected and explicitly approved, and redact sensitive data from logs and examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawaizhang/code-dev-pipeline) <br>
- [Workflow reference](references/workflow.md) <br>
- [Analyst role reference](references/analyst.md) <br>
- [Architect role reference](references/architect.md) <br>
- [Coder role reference](references/coder.md) <br>
- [Reviewer role reference](references/reviewer.md) <br>
- [Tester role reference](references/tester.md) <br>
- [Validator role reference](references/validator.md) <br>
- [Coordinator role reference](references/coordinator.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with code, test, review, and validation artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include implementation files, tests, coverage reports, review findings, and technical debt notes depending on the coding task.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
