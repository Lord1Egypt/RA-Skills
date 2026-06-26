## Description: <br>
Generates unit and E2E tests for existing projects by analyzing design documents and public function signatures, reviewing testability, producing test code, and reporting coverage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fdingiit](https://clawhub.ai/user/fdingiit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add tests to existing projects, assess API testability, and generate coverage reports with project-specific thresholds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package installation or project file edits can alter dependencies, test configuration, or build behavior. <br>
Mitigation: Review proposed installation commands, generated files, and diffs before running or accepting changes. <br>
Risk: Generated tests and coverage reports may reflect incomplete project understanding or inferred behavior. <br>
Mitigation: Confirm the project understanding and testability reports at the skill's review checkpoints before proceeding to code generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fdingiit/gen-test) <br>
- [coverage-recipes.md](coverage-recipes.md) <br>
- [design-analysis-guide.md](design-analysis-guide.md) <br>
- [testability-checklist.md](testability-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with generated test code, shell commands, and coverage summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose package installation, test configuration changes, Makefile targets, and generated unit or E2E test files after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
