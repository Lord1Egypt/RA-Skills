## Description: <br>
A developer toolkit skill for Git workflows, project scaffolding, CI/CD checks, testing, formatting, code review, technical debt tracking, dependency analysis, diff summaries, and refactoring guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[g1776933879](https://clawhub.ai/user/g1776933879) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate and run local development workflow commands for repository review, formatting, testing, scaffolding, dependency checks, technical debt tracking, and lightweight project diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can add global Node and Python development tools on the local machine. <br>
Mitigation: Review install.sh before running it and execute it only in an environment where global npm and pip installs are acceptable. <br>
Risk: Formatting and scaffolding commands can modify or create files in the working directory. <br>
Mitigation: Run dev-tk fmt --check before formatting changes and review generated files before committing them. <br>
Risk: Review and dependency commands are convenience checks, not authoritative security or dependency audits. <br>
Mitigation: Use project security scanning, dependency audit tooling, and human review before relying on release or commit decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/g1776933879/skills/dev-toolkit-pro) <br>
- [Node.js](https://nodejs.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with inline shell commands, generated project files, JSON debt records, and report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write scaffolded project files, project specification files, technical debt records, dependency reports, diff reports, and refactoring suggestion reports under the working directory.] <br>

## Skill Version(s): <br>
2.2.1 (source: release evidence and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
