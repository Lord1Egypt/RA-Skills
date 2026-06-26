## Description: <br>
Set up and use 1Password CLI (op) for installation, desktop app integration, sign-in, and secret read, injection, or runtime workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when they need an agent to help with 1Password CLI setup, account authorization, and guarded secret access workflows. It emphasizes local verification, tmux isolation, and avoiding secret exposure in chat, logs, files, or network commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help operate 1Password CLI workflows that involve sensitive credentials. <br>
Mitigation: Install only for intended 1Password CLI use, keep 1Password app approvals under user control, and require op whoami verification before secret access. <br>
Risk: Resolved secrets could be exposed through chat, logs, files, clipboard tools, or network-transmitting commands. <br>
Mitigation: Do not paste secret values into chat or logs, prefer op run or op inject over writing secrets to disk, and refuse piping op output to network commands. <br>
Risk: Unquoted vault, item, account, or field names in shell commands could allow shell metacharacter injection. <br>
Mitigation: Single-quote user-provided values in op command arguments before proposing or running shell commands. <br>


## Reference(s): <br>
- [1Password CLI get started](https://developer.1password.com/docs/cli/get-started/) <br>
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/1password-hardened) <br>
- [Faberlens safety evaluation](https://faberlens.ai/explore/1password) <br>
- [SAFETY.md](artifact/SAFETY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command proposals and operational guidance; secret values should remain masked or local-only.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
