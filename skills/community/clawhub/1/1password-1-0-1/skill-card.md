## Description: <br>
Set up and use 1Password CLI (op). Use when installing the CLI, enabling desktop app integration, signing in (single or multi-account), or reading/injecting/running secrets via op. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daggerkun007](https://clawhub.ai/user/daggerkun007) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to install and authenticate the 1Password CLI, verify account access, and safely run secret read, inject, and command execution workflows through op. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Secret values could be exposed in terminal output, logs, chat, or generated files. <br>
Mitigation: Avoid commands that print secrets, avoid --no-masking unless explicitly required, and prefer op run or op inject workflows that keep secret material out of logs. <br>
Risk: Examples that write secret material to disk can leave plaintext credentials behind. <br>
Mitigation: Write secret outputs only to protected paths with restrictive permissions, exclude those files from version control, and delete plaintext files after use. <br>
Risk: Agent commands may use the user's active 1Password CLI authentication context. <br>
Mitigation: Install only when the agent is trusted to use that context, run op commands inside the required tmux session, and verify account identity with op whoami before reading secrets. <br>


## Reference(s): <br>
- [1Password CLI get started](https://developer.1password.com/docs/cli/get-started/) <br>
- [Skill reference: get-started.md](references/get-started.md) <br>
- [Skill reference: cli-examples.md](references/cli-examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/daggerkun007/1password-1-0-1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the op CLI and a tmux session for authenticated commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
