## Description:

Routes LLM requests to the cheapest capable model across 8 providers (Anthropic, Google, OpenAI, DeepSeek, xAI, Moonshot, Mistral, Ollama) and 25+ models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liekzejaws](https://clawhub.ai/user/liekzejaws)

### License/Terms of Use:


## Use Case:

Developers and engineers use Clawd Throttle as an OpenClaw MCP server or optional local HTTP proxy to classify prompt complexity, route requests across configured LLM providers, and review routing and cost metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional HTTP proxy mode can expose paid model accounts if reachable by untrusted clients.

Mitigation: Keep HTTP proxy mode disabled unless needed; if enabled, bind it to loopback, protect it with authentication, and do not expose port 8484 to a LAN or the internet.

Risk: Provider API keys and endpoint settings can route paid requests to unintended services if misconfigured.

Mitigation: Use restricted provider API keys, verify every configured base URL, and review routing configuration before use.

Risk: Local configuration may contain credentials.

Mitigation: Store the local config file with appropriate filesystem permissions and prefer environment variables or a managed secret store where available.

## Reference(s):

- [Clawd Throttle ClawHub release](https://clawhub.ai/liekzejaws/skills/clawd-throttle)
- [liekzejaws publisher profile](https://clawhub.ai/user/liekzejaws)
- [Server-resolved provenance](unavailable)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Text and JSON responses with routing metadata; Markdown guidance with shell commands for setup and use.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call configured provider APIs and returns routing tier, selected model, score, request id, and cost-tracking metadata where available.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
