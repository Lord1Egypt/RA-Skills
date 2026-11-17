## Description:

Manage and deploy cursor2api to convert Cursor IDE AI conversations into Anthropic Messages API and OpenAI Chat Completions API formats, including environment configuration, token refresh, and uninstallation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcjl](https://clawhub.ai/user/0xcjl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy and manage a cursor2api proxy for OpenClaw, Claude Code, and CC Switch workflows. It provides setup, configuration, token handling, verification, troubleshooting, and uninstall guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes prompts through a third-party cursor2api proxy container using a Cursor browser session token.

Mitigation: Use only after accepting that trust boundary, bind the proxy to loopback where possible, and use HTTPS, SSH, or VPN tunneling for any remote access.

Risk: The Cursor session token can grant account access if exposed in files, command history, logs, screenshots, or shared shell configuration.

Mitigation: Store the token in a secret manager or locked-down environment file, avoid command-line token arguments and shell history, and rotate the token after any suspected exposure.

Risk: Using an unpinned container tag can change the deployed proxy implementation without review.

Mitigation: Pin the container image to a reviewed digest before installing or updating the service.

Risk: Using third-party proxies may violate Cursor's Terms of Service.

Mitigation: Review the applicable Cursor terms and organizational policy before deploying the proxy.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/0xcjl/skills/cursor2api)
- [Publisher Profile](https://clawhub.ai/user/0xcjl)
- [Installation Guide](references/installation.md)
- [Token Management](references/token.md)
- [Configuration Reference](references/configuration.md)
- [Quick Reference](references/quick-reference.md)
- [Cursor](https://cursor.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JSON, and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Docker commands, environment variables, API endpoint examples, token refresh steps, and uninstall commands.]

## Skill Version(s):

1.0.2 (source: server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
