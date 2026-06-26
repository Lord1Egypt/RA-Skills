## Description: <br>
Manage and deploy cursor2api to proxy Cursor IDE AI conversations into Anthropic and OpenAI-compatible API formats, including service configuration, token refresh, and uninstallation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xcjl](https://clawhub.ai/user/0xcjl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install, configure, operate, refresh tokens for, and uninstall a cursor2api proxy for OpenClaw, Claude Code, or CC Switch workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide a sensitive Cursor session token to a third-party proxy container. <br>
Mitigation: Install only if you trust the third-party container, prefer a reviewed or pinned image, keep the proxy local when possible, and rotate or revoke the token if exposure is suspected. <br>
Risk: The documented setup can place tokens in shell startup files, command history, or plain HTTP requests. <br>
Mitigation: Store tokens securely, avoid long-lived plaintext shell configuration for secrets, avoid sending tokens over plain HTTP beyond a trusted local loopback setup, and review commands before running them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/0xcjl/cursor2api) <br>
- [Installation Guide](references/installation.md) <br>
- [Token Management](references/token.md) <br>
- [Configuration Reference](references/configuration.md) <br>
- [Quick Reference](references/quick-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, environment variables, Docker examples, and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose commands that start Docker containers, update shell environment variables, and handle sensitive Cursor session tokens.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
