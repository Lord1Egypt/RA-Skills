## Description: <br>
Connects AI agents to WLdPass for supplier and buyer discovery, demand publishing, matching workflows, messaging, webhook automation, and business intelligence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wld-bot](https://clawhub.ai/user/wld-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business operators use this skill to let agents interact with WLdPass commerce workflows, including finding suppliers or buyers, posting demands, sending messages, registering webhooks, and checking market intelligence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WLdPass credentials and submitted business data are sensitive. <br>
Mitigation: Install only if you trust WLdPass, use a dedicated or revocable token, and protect ~/.openclaw/openclaw.json. <br>
Risk: The skill can send messages, post demands, create public or community content, and enable auto-replies. <br>
Mitigation: Require user confirmation before allowing an agent to perform externally visible or automated communication actions. <br>
Risk: Registered webhooks may receive future message, match, contact, watch, and digest events. <br>
Mitigation: Register webhooks only to endpoints you control and review webhook behavior before enabling automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wld-bot/ai-business) <br>
- [WLdPass developers](https://wldpass.com/developers) <br>
- [WLdPass OpenClaw skill manifest](https://wldpass.com/api/v1/openclaw/skill-manifest) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with curl commands, setup commands, tables, and structured summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a WLdPass API token and may configure OpenClaw credentials or register a webhook when requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
