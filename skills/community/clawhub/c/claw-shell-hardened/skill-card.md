## Description:

Run shell commands inside a dedicated tmux session named `claw` and return output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to ask an agent to run local shell commands, keep command execution scoped to a `claw` tmux session, and read command output back into the conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants broad local shell authority, and its advertised tmux and safety boundaries are not reliably enforced.

Mitigation: Review before installation, run only in an isolated low-privilege environment, and prefer a version with strict allowlisted operations and explicit approval controls.

Risk: Shell commands can affect local files, processes, and environment state beyond the agent conversation.

Mitigation: Use OS-level filesystem and network sandboxing around the runtime, and avoid granting access to sensitive directories, credentials, or production systems.

Risk: Commands that pipe local output or file contents to external endpoints can expose data.

Mitigation: Block outbound data-transfer commands unless they are explicitly reviewed and approved within the deployment's security policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/claw-shell-hardened)
- [Faberlens safety evaluation](https://faberlens.ai/explore/claw-shell)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [JSON object containing command output or an error message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Captures recent output from the `claw` tmux session after command execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
