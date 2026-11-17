## Description:

Deploy and configure CLIProxyAPI, expose its dashboard safely, connect OAuth providers such as Claude Code, Gemini, Codex, Qwen, and iFlow, generate a reusable API endpoint and API key, and integrate it with OpenClaw or other OpenAI-compatible tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayder21](https://clawhub.ai/user/ayder21)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy a CLIProxyAPI service, onboard OAuth-backed providers, create a reusable OpenAI-compatible endpoint, and configure OpenClaw or another compatible client to route model requests through it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and run a persistent CLIProxy service.

Mitigation: Review the planned service location, startup method, and restart behavior before execution, and keep logs inspectable after deployment.

Risk: The install workflow tells the agent to read current upstream instructions, which can be unpinned.

Mitigation: Use a trusted and pinned CLIProxyAPI source or release before installing dependencies or starting the service.

Risk: Dashboard or management access can expose sensitive controls if opened too broadly.

Mitigation: Keep the dashboard private by default, expose only the required ports, and prefer HTTPS plus a reverse proxy for remote access.

Risk: The smoke-test script accepts API keys and sends test requests.

Mitigation: Use the script only against local or trusted HTTPS endpoints, avoid long-lived keys when possible, and rotate any key that may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ayder21/skills/cliproxy-openclaw)
- [Install CLIProxyAPI](references/install.md)
- [Dashboard and remote access](references/dashboard.md)
- [Providers and account onboarding](references/providers.md)
- [OpenClaw integration](references/openclaw-integration.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include service commands, dashboard URLs, API endpoint and key handling guidance, model names, client configuration values, and smoke-test commands.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-03-24)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
