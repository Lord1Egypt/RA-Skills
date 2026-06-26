## Description: <br>
Fast, explicit terminal execution via OpenClaw exec for users who type the exact command to run. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuwujijay](https://clawhub.ai/user/liuwujijay) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and power users use this skill to quickly dispatch exact terminal commands through OpenClaw when they already know the command they want to run. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-supplied shell commands can modify or delete local state when the command is destructive. <br>
Mitigation: Prefer read-only commands by default and double-check paths before running commands that delete, overwrite, or move files. <br>
Risk: Secrets placed directly in command lines can be exposed through shell history, logs, or process inspection. <br>
Mitigation: Avoid putting tokens, API keys, cookies, or other secrets in command arguments. <br>
Risk: Remote download-and-execute pipelines can run untrusted code. <br>
Mitigation: Do not run curl-or-download pipelines that execute immediately unless the source is fully trusted and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuwujijay/agi-term-helper) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Raw shell command text with terminal output returned by the runtime] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are user-supplied and forwarded without model rewriting.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
