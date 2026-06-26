## Description: <br>
Config Modification guards local OpenClaw JSON configuration changes with intercept checks, four-stage validation, filesystem watching, and automatic rollback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[halfmoon82](https://clawhub.ai/user/halfmoon82) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to review, monitor, and recover from local OpenClaw configuration changes. It helps catch JSON syntax errors, risky config edits, missing rollback coverage, and gateway health failures before or after config changes are applied. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic rollback and persistent filesystem monitoring can change local OpenClaw configuration state without further prompts once the guard workflow is enabled. <br>
Mitigation: Review target paths, snapshot behavior, and rollback scope in a non-production OpenClaw setup before enabling the background guard. <br>
Risk: Gateway restarts and local diff logging can affect availability or expose sensitive configuration details on systems that contain API keys. <br>
Mitigation: Use least-privilege local execution, inspect log destinations, avoid including secrets in review output, and require human approval for production configuration changes. <br>


## Reference(s): <br>
- [Config Modification on ClawHub](https://clawhub.ai/halfmoon82/config-modification) <br>
- [fswatch integration design](references/fswatch-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands, Python snippets, and local validation output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local snapshots, log validation results, trigger rollback, and restart a local OpenClaw gateway when the user enables the guard workflow.] <br>

## Skill Version(s): <br>
2.6.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
