## Description: <br>
Turns a codebase into an interactive browser-based course that explains how the code works for non-technical learners. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yaki6](https://clawhub.ai/user/yaki6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, AI-assisted builders, and learners use this skill to turn a local project or provided GitHub repository into an interactive course with modules, visualizations, quizzes, and plain-English code explanations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the selected project or clones a provided GitHub repository, so it may process private or sensitive source code. <br>
Mitigation: Run it only on projects intended for analysis, avoid folders containing secrets or unrelated private code, and review the generated course before sharing. <br>
Risk: Generated course files can include exact source-code snippets from the analyzed project. <br>
Mitigation: Check the output for confidential implementation details or proprietary snippets before distributing the course. <br>


## Reference(s): <br>
- [Codebase to Course ClawHub release](https://clawhub.ai/yaki6/codebase-to-course-generator) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Design system reference](artifact/references/design-system.md) <br>
- [Interactive elements reference](artifact/references/interactive-elements.md) <br>
- [Content philosophy reference](artifact/references/content-philosophy.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Directory of HTML, CSS, JavaScript, Markdown briefs when needed, and an assembled single-page HTML course] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated course content may include exact source-code snippets from the selected project.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
