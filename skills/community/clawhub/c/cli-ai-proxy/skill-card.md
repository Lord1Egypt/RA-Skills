## Description:

Manage cli-ai-proxy, a local OpenAI-compatible proxy that routes requests through Gemini CLI and Claude Code while leaving credential handling to the underlying CLIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilzc](https://clawhub.ai/user/ilzc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install, start, stop, check, configure, and troubleshoot a local OpenAI-compatible proxy that routes requests through Gemini CLI or Claude Code for OpenClaw and similar clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release installs and runs an unpinned global npm package.

Mitigation: Review the package and version before installation, prefer a user-owned Node/npm setup, and avoid privileged global install paths.

Risk: The documentation includes unsafe root-level installation guidance.

Mitigation: Avoid documented curl-to-sudo and sudo npm install paths; use an unprivileged package manager setup instead.

Risk: The local proxy should not be exposed beyond the loopback interface.

Mitigation: Keep the proxy bound to 127.0.0.1 unless it is protected by an authenticated reverse proxy with a narrow CORS policy.

Risk: Provider configuration can modify OpenClaw settings.

Mitigation: Review OpenClaw configuration changes before and after running the configure command, and keep the generated backup.

## Reference(s):

- [CLI AI Proxy ClawHub page](https://clawhub.ai/ilzc/skills/cli-ai-proxy)
- [API Reference](artifact/references/api.md)
- [Configuration Reference](artifact/references/configuration.md)
- [Troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON/YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return proxy status, health JSON, model metadata, logs, and OpenClaw configuration guidance.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
