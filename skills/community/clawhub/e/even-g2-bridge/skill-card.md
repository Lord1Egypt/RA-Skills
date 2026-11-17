## Description:

Connect Even Realities G2 smart glasses to OpenClaw via Cloudflare Worker, routing G2 voice commands to an OpenClaw Gateway for short replies on glasses, long-task delivery through Telegram, and optional DALL-E image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daaab](https://clawhub.ai/user/daaab)

### License/Terms of Use:

MIT

## Use Case:

Developers and advanced users use this skill to deploy and configure a Cloudflare Worker bridge between Even Realities G2 smart glasses and an OpenClaw Gateway. It supports voice-driven agent requests, short G2 display responses, background long tasks, troubleshooting, and optional Telegram or image-generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The public Worker can fail open if G2_TOKEN is missing.

Mitigation: Patch the Worker to fail closed when G2_TOKEN is missing and verify the token is configured before deployment.

Risk: Voice prompts and generated outputs may be forwarded through the Gateway and, when configured, Telegram, Anthropic, and OpenAI.

Mitigation: Avoid sensitive prompts, disable Telegram, image-generation, or fallback features that are not needed, and install only when this data flow is acceptable.

Risk: The Worker uses Gateway access to reach the main OpenClaw agent.

Mitigation: Use a dedicated least-privilege Gateway token or dedicated agent instead of broad main-agent access.

Risk: A public Worker may receive large or excessive requests.

Mitigation: Add rate limits and request-size limits before deployment.

## Reference(s):

- [G2 Protocol Reference](references/g2-protocol.md)
- [Skill Repository](https://github.com/dAAAb/openclaw-even-g2-bridge-skill)
- [Even Hub SDK](https://evenhub.evenrealities.com/)
- [Even Demo App](https://github.com/even-realities/EvenDemoApp)
- [Even G2 Protocol Reference Implementation](https://github.com/i-soxi/even-g2-protocol)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a Cloudflare Worker script, Wrangler configuration, required secret names, setup steps, troubleshooting guidance, and G2 protocol reference material.]

## Skill Version(s):

5.2.0 (source: ClawHub release metadata; artifact frontmatter metadata.version states 5.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
