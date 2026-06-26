## Description: <br>
Set up and use 1Password CLI (op) for installation, desktop app integration, account sign-in, and reading, injecting, or running secrets through op. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaozewen0519](https://clawhub.ai/user/zhaozewen0519) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up 1Password CLI, authenticate inside a tmux session, verify account access, and run common op workflows for vault reads, secret injection, and command execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through workflows that access sensitive 1Password vault data. <br>
Mitigation: Approve access only for the intended account and item, and verify `op whoami` before any secret read. <br>
Risk: Some op examples can expose secrets in terminal output or generated files. <br>
Mitigation: Avoid commands that print secrets, prefer `op run` or `op inject`, and avoid writing keys or passwords to disk unless explicitly required. <br>
Risk: Authenticated tmux sessions or generated files may retain sensitive context after use. <br>
Mitigation: Close the dedicated tmux session and clean up generated files after completing the workflow. <br>


## Reference(s): <br>
- [1Password CLI get-started](https://developer.1password.com/docs/cli/get-started/) <br>
- [Skill release page](https://clawhub.ai/zhaozewen0519/1password-bak) <br>
- [get-started.md](references/get-started.md) <br>
- [cli-examples.md](references/cli-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the 1Password CLI binary `op`; examples are intended to run in a dedicated tmux session.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
