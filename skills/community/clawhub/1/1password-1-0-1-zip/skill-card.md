## Description: <br>
Set up and use 1Password CLI (op), including installation, desktop app integration, sign-in, account selection, and reading, injecting, or running secrets through op. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cuiday1975](https://clawhub.ai/user/cuiday1975) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure and operate the 1Password CLI safely from an agent workflow. It is intended for installation checks, app integration, sign-in, account selection, and controlled secret access using op references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to access high-impact 1Password vault secrets without narrow built-in scoping. <br>
Mitigation: Use the least-privileged 1Password account or vault available, provide exact op:// secret references, and approve each secret access yourself. <br>
Risk: Commands that print, unmask, or write secrets can expose sensitive values in logs, chat, shell history, or files. <br>
Mitigation: Avoid --no-masking and commands that print secrets, prefer op run or op inject over writing secrets to disk, and clean up tmux sessions and secret files after use. <br>


## Reference(s): <br>
- [1Password CLI get-started documentation](https://developer.1password.com/docs/cli/get-started/) <br>
- [Skill page on ClawHub](https://clawhub.ai/cuiday1975/1password-1-0-1-zip) <br>
- [get-started.md](artifact/references/get-started.md) <br>
- [cli-examples.md](artifact/references/cli-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the op CLI and a dedicated tmux session for op commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
