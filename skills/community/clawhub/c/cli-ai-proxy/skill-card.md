## Description: <br>
Manage cli-ai-proxy: local OpenAI-compatible proxy that routes requests through Gemini CLI and Claude Code. The proxy itself reads no credentials; the underlying CLIs handle their own auth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ilzc](https://clawhub.ai/user/ilzc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install, operate, inspect, and configure a local OpenAI-compatible proxy for Gemini CLI and Claude Code workflows. It is useful when an agent or local tool needs a unified REST interface while the underlying CLI tools continue to manage authentication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The proxy exposes an unauthenticated local HTTP API and uses permissive CORS headers; binding it beyond localhost could let other hosts or browser pages drive local CLI sessions. <br>
Mitigation: Keep the server bound to 127.0.0.1. If remote access is required, place it behind a reverse proxy that enforces authentication and a narrow CORS policy. <br>
Risk: The install path uses a public npm package installed globally, so users depend on the package they choose to install from the npm registry. <br>
Mitigation: Install only if the public npm package is trusted for the environment, and review package identity and version before global installation. <br>
Risk: The OpenClaw configuration command modifies ~/.openclaw/openclaw.json. <br>
Mitigation: Run the configuration command only when that provider change is intended, and review the generated backup and resulting configuration. <br>


## Reference(s): <br>
- [API Reference](references/api.md) <br>
- [Configuration Reference](references/configuration.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ilzc/cli-ai-proxy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands, JSON examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start or stop a local proxy, report health and status, install a public npm package, or modify OpenClaw provider configuration when the user explicitly runs the configuration command.] <br>

## Skill Version(s): <br>
0.1.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
