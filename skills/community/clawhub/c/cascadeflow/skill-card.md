## Description: <br>
OpenClaw-native domain cascading for cost and latency reduction, domain-aware model assignment, OpenClaw-native event handling, and command setup including /model cflow and optional /cascade stats commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[saschabuehrle](https://clawhub.ai/user/saschabuehrle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure CascadeFlow as an OpenAI-compatible OpenClaw provider that routes requests through domain-aware drafter/verifier cascades. It helps set up installation, credentials, localhost or protected remote access, /model cflow, and optional health, stats, and savings commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup installs and runs an external CascadeFlow package that handles LLM requests. <br>
Mitigation: Review the package source and artifacts before installation, and prefer exact version and hash pinning where possible. <br>
Risk: Provider API keys and service tokens are required for routing requests. <br>
Mitigation: Use separate least-privilege provider keys, keep test and production keys separate, and use strong random auth and stats tokens. <br>
Risk: Remote exposure of the provider endpoint could allow unauthorized chat or stats access. <br>
Mitigation: Keep the server bound to 127.0.0.1 by default; expose remote access only behind TLS or a reverse proxy with strong tokens. <br>
Risk: Background mode can continue using provider keys after the setup command returns. <br>
Mitigation: Track and stop the running CascadeFlow process when it is no longer needed, and monitor logs and usage during operation. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/saschabuehrle/cascadeflow) <br>
- [CascadeFlow OpenClaw provider guide](https://github.com/lemony-ai/cascadeflow/blob/main/docs/guides/openclaw_provider.md) <br>
- [CascadeFlow GitHub repository](https://github.com/lemony-ai/cascadeflow) <br>
- [ClawHub Publish Pack](references/clawhub_publish_pack.md) <br>
- [Market Positioning For ClawHub](references/market_positioning.md) <br>
- [OpenClaw ClawHub docs](https://docs.openclaw.bot/guide/clawhub) <br>
- [OpenClaw slash commands docs](https://docs.openclaw.bot/guide/faq/slash-commands) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and JSON configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes provider setup steps, credential guidance, health and stats checks, and optional command configuration.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
