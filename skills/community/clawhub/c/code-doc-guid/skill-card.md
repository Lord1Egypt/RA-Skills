## Description: <br>
Codebase navigation and documentation assistant that helps agents locate definitions, understand dependencies, and keep documentation consistent before and after code changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Omeletee](https://clawhub.ai/user/Omeletee) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding agents use this skill to index a repository, search symbols, inspect dependency impact, and refresh local navigation metadata around code changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores local repository metadata, including file paths, symbols, imports, and docstrings, under .trae. <br>
Mitigation: Add .trae to .gitignore or review generated files before committing them. <br>
Risk: Dependency reports and risk scores are local navigation aids and may be incomplete for unsupported languages or complex import patterns. <br>
Mitigation: Use the reports to guide review, then confirm high-impact changes against the source code before editing. <br>


## Reference(s): <br>
- [Artifact README](README.md) <br>
- [ClawHub skill page](https://clawhub.ai/Omeletee/code-doc-guid) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown, configuration] <br>
**Output Format:** [Markdown guidance with shell commands, JSON or JSONL command summaries, and generated Markdown dependency reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local .trae metadata and dependency report files when its commands are run.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
