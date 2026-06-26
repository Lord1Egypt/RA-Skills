## Description: <br>
Manage how OpenClaw routes Telegram messages to different Claude model backends. Switch between CLI and API providers with simple config changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[josephtandle](https://clawhub.ai/user/josephtandle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect OpenClaw Telegram routing, switch model providers, review gateway logs, and restore default routing behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Routing commands can persistently change OpenClaw Telegram model routing and restart the gateway. <br>
Mitigation: Check the current status, confirm the target provider, and back up ~/.openclaw/openclaw.json before model, fallback, or restore changes. <br>
Risk: CLI-backed routing may send Telegram chat content to a local Claude Code backend with tool access. <br>
Mitigation: Use CLI-backed routing only for Telegram chats you trust and review gateway logs after changes. <br>


## Reference(s): <br>
- [OpenClaw](https://openclaw.ai) <br>
- [ClawHub skill page](https://clawhub.ai/josephtandle/claude-code-switchboard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with command examples, configuration paths, and routing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update ~/.openclaw/openclaw.json and restart the OpenClaw gateway when model, fallback, or restore commands are used.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
