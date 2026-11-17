## Description:

Integrates OpenClaw with Claude Code CLI to delegate coding tasks via JSON queues for advanced multi-turn code collaboration and analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gesilajerry](https://clawhub.ai/user/gesilajerry)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to let OpenClaw hand coding or analysis prompts to Claude Code through local JSON queues and consume result JSON for continued collaboration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a hardcoded external API credential.

Mitigation: Remove the credential from the artifact, rotate any exposed secret, and provide credentials through a protected environment or secret manager.

Risk: Queued prompts are executed with normal Claude Code permission checks disabled.

Mitigation: Restore normal permission checks and run the skill only in a tightly controlled, low-privilege workspace.

Risk: Queue directories can trigger automatic execution of local task files.

Mitigation: Restrict write access to queue directories and validate task files before allowing the bridge to process them.

Risk: Prompts, outputs, status, and logs may be sent to the configured external provider or stored locally.

Mitigation: Confirm the data handling policy before use and protect local queue, result, status, and log files.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/gesilajerry/skills/claude-code-collaboration)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [JSON result files containing task status, prompt, stdout, stderr, return code, and completion timestamp.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts, responses, status, and logs may be stored in local workspace files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
