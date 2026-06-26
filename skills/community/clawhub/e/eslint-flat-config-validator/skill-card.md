## Description: <br>
Validate ESLint v9+ flat config files exported as JSON for structural correctness, language options, rules configuration, plugin hygiene, file patterns, and best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit JSON-exported ESLint v9+ flat configs, enforce config standards in CI, and review eslint.config.js changes before merging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented Node export command loads eslint.config.js, which executes code from the target configuration as part of producing the JSON snapshot. <br>
Mitigation: Export configs only from trusted projects or isolated environments, then run the Python validator against the generated JSON snapshot. <br>
Risk: Validation results apply to the exported JSON snapshot and may become stale if eslint.config.js changes afterward. <br>
Mitigation: Regenerate the JSON snapshot immediately before validation, especially in CI or pre-merge checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/eslint-flat-config-validator) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with command examples; validator output can be text, JSON, or summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit codes distinguish clean results, validation failures, and file or parse errors.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
