## Description: <br>
DeepTask helps an agent decompose software work into reviewed sessions, subtasks, minimum functional units, unit tests, and traceable Git commits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spaceack](https://clawhub.ai/user/spaceack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use DeepTask to manage coding work as a structured loop: task decomposition, human review, implementation, unit-test validation, and Git commit tracing. It is intended for local project automation where SQLite-backed task records and commit metadata help audit progress. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local code or toolchain commands using test code stored in the project database. <br>
Mitigation: Install and run it only in a dedicated disposable workspace or repository, keep secrets out of the project tree, and inspect database test_code before running cycles. <br>
Risk: The skill can initialize Git, stage all changes, and create commits automatically after unit tests pass. <br>
Mitigation: Review git status and generated changes before and after execution, and use it only in repositories where broad staging and automated commits are acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/spaceack/deeptask) <br>
- [DeepTask database schema](references/schema.md) <br>
- [MoonBit syntax reference](references/moonbit-syntax.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated local project artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create SQLite task records, code files, unit-test results, and Git commits in the configured workspace.] <br>

## Skill Version(s): <br>
1.2.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
