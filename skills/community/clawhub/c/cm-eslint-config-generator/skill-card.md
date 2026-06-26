## Description: <br>
Generate optimal ESLint configurations based on project type, framework, and team preferences - flat config format, plugin selection, and rule tuning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to generate or migrate ESLint flat configurations after inspecting project metadata, framework dependencies, TypeScript usage, existing ESLint plugins, and rule conflicts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated ESLint configuration or plugin recommendations may not match a project's intended linting policy or compatibility constraints. <br>
Mitigation: Review generated eslint.config.mjs content, plugin recommendations, and rule changes before committing them. <br>
Risk: Project inspection can involve local metadata such as package.json and existing ESLint configuration files. <br>
Mitigation: Use the skill on repositories where that metadata is appropriate to inspect, and avoid sharing sensitive project details unnecessarily. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/cm-eslint-config-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and ESLint configuration code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include project analysis notes, generated eslint.config.mjs content, plugin recommendations, migration guidance, and rule conflict audit findings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
