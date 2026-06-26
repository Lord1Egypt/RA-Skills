## Description: <br>
Run a structured quality control audit on any codebase, covering tests, imports, type checking, static analysis, smoke tests, documentation, and comparisons over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IsonaEi](https://clawhub.ai/user/IsonaEi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to run a structured quality-control pass across Python, TypeScript, GDScript, and general codebases. It helps produce PASS, WARN, or FAIL findings with supporting checks for tests, imports, typing, linting, smoke behavior, file consistency, and documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can ask an agent to run real quality-control commands, including tests, imports, package scripts, and project-specific tooling that may execute code from the target repository. <br>
Mitigation: Use a clean git branch or isolated environment for unfamiliar repositories, inspect package and test scripts before a full audit, and review command output before relying on results. <br>
Risk: Fix mode can modify files through automatic linting or formatting. <br>
Mitigation: Use fix mode only when prepared to review diffs, keep changes under version control, and approve or revert generated edits before deployment. <br>


## Reference(s): <br>
- [Code QC on ClawHub](https://clawhub.ai/IsonaEi/code-qc) <br>
- [Python QC Profile](references/python-profile.md) <br>
- [TypeScript QC Profile](references/typescript-profile.md) <br>
- [GDScript QC Profile](references/gdscript-profile.md) <br>
- [General QC Profile](references/general-profile.md) <br>
- [Ruff Rules](references/ruff-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, JSON baselines, shell command guidance, and concise text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save qc-report.md and .qc-baseline.json when the agent follows the skill workflow; fix mode can propose or apply automatic code formatting and lint fixes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
