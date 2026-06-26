## Description: <br>
Checks CSS style convention issues in Vue single-file components and reports guidance for issues such as missing scoped styles, !important usage, ID selectors, deep selectors, non-kebab-case class names, and deep nesting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yueguangshun123](https://clawhub.ai/user/yueguangshun123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scan Vue single-file components for common CSS style convention issues and decide which warnings to fix. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script reads all .vue files below the current working directory. <br>
Mitigation: Run it only from the Vue project intended for inspection. <br>
Risk: The output is a set of style warnings rather than an automatic fix. <br>
Mitigation: Review each warning before changing source code. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yueguangshun123/check-vue-style) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Text warnings with file paths, line numbers, and concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally, reads .vue files under the current directory, and does not modify files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
