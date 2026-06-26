## Description: <br>
Set up and use 1Password CLI (op). Use when installing the CLI, enabling desktop app integration, signing in (single or multi-account), or reading/injecting/running secrets via op. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miguelguerra200022-sudo](https://clawhub.ai/user/miguelguerra200022-sudo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to install and validate the 1Password CLI, enable desktop app integration, sign in to one or more accounts, and use op commands for reading, injecting, or running commands with secrets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands that read secrets, use --no-masking, or write files such as key.pem or config.yml can expose sensitive values. <br>
Mitigation: Review those commands before execution, avoid logged terminals and CI, protect generated files, exclude them from source control and backups, and remove them when no longer needed. <br>


## Reference(s): <br>
- [1Password CLI get-started documentation](https://developer.1password.com/docs/cli/get-started/) <br>
- [ClawHub skill page](https://clawhub.ai/miguelguerra200022-sudo/1password-zito) <br>
- [1Password CLI get-started summary](references/get-started.md) <br>
- [op CLI examples](references/cli-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that access or write secrets and should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
