## Description: <br>
Set up and use 1Password CLI (op) for installation, desktop app integration, sign-in, and reading, injecting, or running secrets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangfeng1995](https://clawhub.ai/user/huangfeng1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure and operate the 1Password CLI in agent workflows that need authenticated access to vaults and secrets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copyable examples can expose real secrets in terminal output. <br>
Mitigation: Do not use examples that print secrets or use --no-masking with real credentials; keep secrets out of logs, chat, and source files. <br>
Risk: Secret material can persist in local files when commands write credentials to disk. <br>
Mitigation: Prefer op run or op inject; when files are unavoidable, use restrictive permissions, exclude them from source control and backups, and delete them promptly. <br>
Risk: Unauthenticated or interrupted 1Password sessions can cause failed secret reads or repeated authorization prompts. <br>
Mitigation: Run op commands in a dedicated tmux session, authorize with op signin, verify access with op whoami before reading secrets, and close the session when finished. <br>


## Reference(s): <br>
- [1Password CLI get started](https://developer.1password.com/docs/cli/get-started/) <br>
- [ClawHub release page](https://clawhub.ai/huangfeng1995/1password-old) <br>
- [references/get-started.md](references/get-started.md) <br>
- [references/cli-examples.md](references/cli-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the 1Password CLI binary and a signed-in 1Password account for secret access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
