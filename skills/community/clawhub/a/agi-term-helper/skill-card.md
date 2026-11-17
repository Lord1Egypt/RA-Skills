## Description:

Fast, explicit terminal execution via OpenClaw exec (direct dispatch; you type the exact command).

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuwujijay](https://clawhub.ai/user/liuwujijay)

### License/Terms of Use:


## Use Case:

Developers and power users use this skill to run exact terminal commands through OpenClaw when they already know the command they want and need quick deterministic shell execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill forwards raw terminal commands exactly as typed, so destructive commands can delete or overwrite files.

Mitigation: Review commands before execution, prefer read-only checks by default, and double-check paths before running commands that modify state.

Risk: Secrets placed in command lines may be exposed through shell history, process listings, logs, or terminal output.

Mitigation: Avoid putting tokens, API keys, cookies, or other secrets directly in `/term` command arguments.

Risk: Remote execution one-liners can run unreviewed downloaded code.

Mitigation: Avoid `curl ... | sh` and other download-and-execute pipelines; inspect remote content before running it.

Risk: Sandbox and host execution behavior may differ, including environment variable availability.

Mitigation: Use sandboxing where possible and explicitly configure required environment variables for the runtime that executes the command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuwujijay/skills/agi-term-helper)
- [Publisher profile](https://clawhub.ai/user/liuwujijay)

## Skill Output:

**Output Type(s):** [shell commands, text, guidance]

**Output Format:** [Plain text terminal output with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Forwards the user's raw command string to the configured exec tool without rewriting.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
