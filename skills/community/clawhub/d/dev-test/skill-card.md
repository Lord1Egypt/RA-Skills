## Description: <br>
Structured development and testing SOP for implementing code changes. Covers codebase study, minimal focused implementation, test writing patterns, test execution, and diff review. Applies to any development work - bug fixes, features, refactors, or open-source contributions. Use when you need a disciplined development workflow with built-in quality checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sliverp](https://clawhub.ai/user/sliverp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to follow a disciplined workflow for bug fixes, feature work, refactors, and open-source contributions. It guides codebase study, focused implementation, test writing, test execution, diff review, and commit preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can steer an agent toward repository edits and commits when applied to development tasks. <br>
Mitigation: For planning-only questions or quick code advice, tell the agent explicitly that repository edits or commits are not wanted. <br>
Risk: Generated code changes or test guidance may be incorrect or incomplete for the target project. <br>
Mitigation: Review the diff, run the relevant tests, and confirm any pre-existing failures before relying on the result. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, markdown] <br>
**Output Format:** [Markdown guidance with inline shell command examples and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts the agent to produce committed code changes, tests, and a clean reviewable diff when the user asks for repository edits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
