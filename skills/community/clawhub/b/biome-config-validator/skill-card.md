## Description: <br>
Validate and lint Biome (biome.json) configuration files for structure, rule conflicts, deprecated options, and best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to check Biome configuration files for syntax, structure, rule placement, deprecated options, formatter settings, and best-practice issues before applying or sharing those configs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a bundled Python validator against a user-selected local configuration file. <br>
Mitigation: Review the Python script when source approval is required and run it only on intended Biome config files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/biome-config-validator) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Markdown instructions with command examples and optional plain-text, JSON, or summary validator output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Validator exits with 0 for no errors, 1 when errors are found, and 2 for invalid input.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
