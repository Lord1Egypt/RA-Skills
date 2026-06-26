## Description: <br>
Validate Babel config files (babel.config.json, .babelrc, .babelrc.json, package.json#babel) for deprecated presets, plugin conflicts, ordering issues, and best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and build engineers use this skill to validate Babel transpiler configuration files during build audits, Babel migrations, and CI linting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The validator reads the Babel config path supplied by the user and may inspect nearby Babel or package.json configuration files in that project directory. <br>
Mitigation: Run it only in projects where the active agent session is allowed to read those local configuration files. <br>
Risk: Validation findings can influence build or migration decisions. <br>
Mitigation: Review the findings before applying changes to project configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/babel-config-validator) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional text, JSON, or summary validator output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CI-friendly exit codes: 0 for no errors, 1 for validation errors, and 2 for missing files or invalid input.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
