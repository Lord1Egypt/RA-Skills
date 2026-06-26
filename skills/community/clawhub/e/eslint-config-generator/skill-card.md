## Description: <br>
Generates ESLint configuration for common JavaScript, React, Vue, TypeScript, Airbnb, Standard, and Prettier presets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunshine-del-ux](https://clawhub.ai/user/Sunshine-del-ux) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill to create local ESLint configuration for JavaScript, React, Vue, and TypeScript projects and to identify related ESLint dependencies to install. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the bundled shell script overwrites .eslintrc.json in the current working directory. <br>
Mitigation: Check for an existing .eslintrc.json and back it up or choose a disposable branch before running the script. <br>
Risk: Following optional npm install guidance can modify package files and execute normal package lifecycle scripts. <br>
Mitigation: Review npm install commands before execution and install only trusted ESLint packages appropriate for the project. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Sunshine-del-ux/eslint-config-generator) <br>


## Skill Output: <br>
**Output Type(s):** [configuration, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled shell script writes .eslintrc.json in the current working directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
