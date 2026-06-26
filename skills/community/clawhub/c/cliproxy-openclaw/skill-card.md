## Description: <br>
Deploy and configure CLIProxyAPI, expose its dashboard safely, connect OAuth providers such as Claude Code, Gemini, Codex, Qwen, and iFlow, generate a reusable API endpoint and API key, and integrate it with OpenClaw or other OpenAI-compatible tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ayder21](https://clawhub.ai/user/ayder21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to turn subscription-based CLI or OAuth accounts into a working OpenAI-compatible API layer. It guides installation, dashboard exposure, provider onboarding, OpenClaw configuration, and smoke testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide deployment actions that install services, change firewall or reverse-proxy exposure, or affect a host system. <br>
Mitigation: Use a dedicated host or VM, review sudo and install commands before running them, inspect the environment first, and confirm port or public exposure changes explicitly. <br>
Risk: Dashboard credentials, API keys, OAuth tokens, and session cookies may be exposed if handled carelessly. <br>
Mitigation: Treat generated tokens and provider credentials as sensitive, avoid binding management surfaces to public interfaces unless explicitly intended, and prefer HTTPS for internet-facing access. <br>
Risk: A completed installation may still fail because of authentication, model naming, quota, routing, network, or streaming compatibility issues. <br>
Mitigation: Verify the process, listener, provider state, available models, OpenClaw connectivity, and a real smoke-test response before considering the setup complete. <br>


## Reference(s): <br>
- [CLIProxy FREE API ClawHub page](https://clawhub.ai/ayder21/cliproxy-openclaw) <br>
- [Install CLIProxyAPI](artifact/references/install.md) <br>
- [Dashboard and remote access](artifact/references/dashboard.md) <br>
- [Providers and account onboarding](artifact/references/providers.md) <br>
- [OpenClaw integration](artifact/references/openclaw-integration.md) <br>
- [Troubleshooting](artifact/references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API base URLs, bearer-token configuration, model names, service commands, reverse-proxy guidance, and smoke-test requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
