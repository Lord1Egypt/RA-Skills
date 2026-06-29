## Description: <br>
Use when the user asks to create, improve, fix, or audit a README.md file, score their README, document an open source project, or set up new project docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thomaszhou22](https://clawhub.ai/user/thomaszhou22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to audit, score, and generate README files for open source projects, libraries, CLI tools, apps, agent skills, and data resources. It helps classify project type, choose a README template, produce Markdown, and run a pre-publish checklist. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The onboarding flow can inventory public GitHub repositories if the user agrees to repo-wide README evaluation. <br>
Mitigation: Decline repo-wide evaluation unless it is needed, or select specific repositories before the skill audits README files. <br>
Risk: Generated README content or proposed documentation edits may be inaccurate, incomplete, or not match the project maintainer's intent. <br>
Mitigation: Review the README preview and checklist results before allowing file changes or publishing generated documentation. <br>


## Reference(s): <br>
- [Better Readme on ClawHub](https://clawhub.ai/thomaszhou22/better-readme) <br>
- [Scoring Rubric](references/scoring-rubric.md) <br>
- [README Templates](references/templates.md) <br>
- [Pre-Publish Checklist](references/pre-publish-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown README content, audit reports, JSON score output, and shell command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce English README.md by default and additional language README files only when requested.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
