## Description: <br>
Set up and use 1Password CLI (op) for installation, desktop app integration, sign-in, and reading, injecting, or running secrets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hansolero](https://clawhub.ai/user/hansolero) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install and operate the 1Password CLI from an agent workflow while preserving authentication state in tmux and avoiding accidental secret disclosure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can allow an agent to access secrets through the 1Password CLI. <br>
Mitigation: Specify the exact account, vault, item, and field the agent may access, and review the skill before installation. <br>
Risk: CLI examples can expose secrets in terminal output or logs. <br>
Mitigation: Avoid --no-masking and do not paste secrets into logs, chat, code, or captured command output. <br>
Risk: Examples that write secrets to files can persist sensitive material on disk. <br>
Mitigation: Prefer op run or op inject; when writing a secret file is necessary, use restrictive permissions, keep it out of source control, and delete it promptly. <br>


## Reference(s): <br>
- [1Password CLI get-started](https://developer.1password.com/docs/cli/get-started/) <br>
- [get-started.md](references/get-started.md) <br>
- [cli-examples.md](references/cli-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the 1Password CLI binary, a 1Password account, and tmux-mediated command execution for authenticated CLI workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
