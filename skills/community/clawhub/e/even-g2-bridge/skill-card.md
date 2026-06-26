## Description: <br>
Connects Even Realities G2 smart glasses to OpenClaw through a Cloudflare Worker so voice commands can reach the user's OpenClaw Gateway, return short responses on the glasses, and send longer or image-generation outputs through Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dAAAb](https://clawhub.ai/user/dAAAb) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and technical users use this skill to deploy and configure a bridge between Even Realities G2 smart glasses and an OpenClaw Gateway. It supports setup, troubleshooting, short voice interactions, background long-running tasks, and optional rich-content delivery through Telegram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bridge creates a high-authority voice-controlled path to the main OpenClaw agent. <br>
Mitigation: Use a strong G2_TOKEN, verify unauthenticated POST requests return 401, prefer a scoped Gateway token or separate low-privilege agent, and keep confirmations enabled for mutating tools. <br>
Risk: Raw prompts and generated results may be sent to third-party services when Telegram, OpenAI, or Anthropic integrations are enabled. <br>
Mitigation: Enable only the services needed for the deployment and use the skill only with content that is acceptable to send to those services. <br>
Risk: Lost or shared glasses could expose the G2 bearer token. <br>
Mitigation: Rotate G2_TOKEN when glasses are lost or access should be revoked; keep GATEWAY_TOKEN stored only as a Worker secret. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dAAAb/even-g2-bridge) <br>
- [Source repository listed in skill metadata](https://github.com/dAAAb/openclaw-even-g2-bridge-skill) <br>
- [G2 Protocol Reference](artifact/references/g2-protocol.md) <br>
- [Even Hub SDK](https://evenhub.evenrealities.com/) <br>
- [Even Realities demo app](https://github.com/even-realities/EvenDemoApp) <br>
- [Even G2 protocol reference implementation](https://github.com/i-soxi/even-g2-protocol) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and code/configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Cloudflare Worker deployment steps, OpenClaw Gateway setup, G2 token configuration, troubleshooting guidance, and optional Telegram, OpenAI, or Anthropic integration notes.] <br>

## Skill Version(s): <br>
5.2.0 (source: server release metadata; artifact frontmatter reports 5.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
