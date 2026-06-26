## Description: <br>
CodeRules is an AI coding-standards assistant that detects a project's technology stack, loads language and framework rule packs, helps generate compliant code, reviews existing code for rule violations, and suggests fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoxulaila](https://clawhub.ai/user/xiaoxulaila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to apply consistent code quality, security, performance, and testing rules while generating, reviewing, or repairing code across TypeScript, Python, Go, React, Vue, and Next.js projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may influence routine coding tasks because its trigger terms and role are broad. <br>
Mitigation: Enable it only when coding-standard enforcement is desired and review generated or modified code before use. <br>
Risk: A project-level .coderules.json can override the default rules and change the guidance the agent applies. <br>
Mitigation: Review .coderules.json in the target project before relying on the generated recommendations. <br>
Risk: The analyzer reads local project files to infer language, framework, package manager, test framework, and lint configuration. <br>
Mitigation: Run the analyzer only against the intended project directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaoxulaila/coderules) <br>
- [Publisher profile](https://clawhub.ai/user/xiaoxulaila) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with code blocks, shell commands, rule summaries, file lists, and self-checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include analyzer results, applied rule names, generated or revised source code, and recommended project configuration changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
