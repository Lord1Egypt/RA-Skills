## Description:

Set up and use the 1Password CLI (`op`) for installation, desktop app integration, sign-in, and secret reads or injection with explicit security guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install and operate the 1Password CLI, authenticate safely, and retrieve or inject secrets without exposing them in logs, chat, network transfers, or shell-expanded arguments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A signed-in 1Password CLI session can expose secrets if command arguments are built unsafely or shell metacharacters are expanded.

Mitigation: Pass vault, item, account, and field names as separate argv elements or use proven shell escaping; verify access with `op whoami` before secret reads.

Risk: Resolved secrets can be leaked through logs, chat, files, clipboard tools, or network-transmitting commands.

Mitigation: Keep resolved secret values local, prefer `op run` or `op inject`, retain masking, and avoid piping `op read` or injected output to network commands.

## Reference(s):

- [1Password CLI get started](https://developer.1password.com/docs/cli/get-started/)
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/1password-hardened)
- [Faberlens safety evaluation](https://faberlens.ai/explore/1password)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and step-by-step operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the 1Password CLI (`op`) and tmux for authenticated CLI workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
