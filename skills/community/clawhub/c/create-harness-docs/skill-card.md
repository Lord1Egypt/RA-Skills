## Description: <br>
Analyzes a repository and scaffolds Harness Engineering documentation for common web and backend project types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangjiayu139](https://clawhub.ai/user/zhangjiayu139) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to initialize or validate repository-local Harness Engineering documentation, including AGENTS.md, architecture docs, quality grading docs, CI workflow configuration, and Java architecture tests when applicable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill modifies the current repository by creating or overwriting documentation, CI workflow, and Java architecture-test files. <br>
Mitigation: Run it only from the intended repository and review the resulting diffs, especially AGENTS.md, docs/, .github/workflows/harness-ci.yml, and generated Java architecture tests before committing or allowing CI to run. <br>


## Reference(s): <br>
- [Create Harness Docs on ClawHub](https://clawhub.ai/zhangjiayu139/create-harness-docs) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Generator script](artifact/scripts/create-harness-docs.js) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Repository files plus command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes files in the current working directory; generated content varies by detected project type.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
