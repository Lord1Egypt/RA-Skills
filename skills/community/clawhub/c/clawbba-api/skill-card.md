## Description: <br>
ClawBBA x OpenClaw connects OpenClaw to ClawBBA with one platform API key for chat, image, and video models across web chat, WeChat, Telegram, and other channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawbba-ux](https://clawhub.ai/user/clawbba-ux) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure OpenClaw for ClawBBA-backed text chat, image generation, and video generation. The skill guides API key setup, OpenClaw configuration, media delivery, troubleshooting, and recovery when generated media is delayed or not delivered. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow can change OpenClaw configuration, persist the ClawBBA API key locally, patch OpenClaw runtime files, and restart the gateway. <br>
Mitigation: Review the package before installation, run it only in an approved OpenClaw environment, validate the resulting configuration, and keep the API key private. <br>
Risk: The security summary flags unverified remote code and broad local OpenClaw changes that are not fully reviewable in the submitted artifact. <br>
Mitigation: Prefer a download-and-review install flow with checksums or signatures before executing any remote installer. <br>
Risk: Prompts or uploaded reference media may be sent to remote providers for generation. <br>
Mitigation: Do not submit confidential prompts or media unless the data handling path is approved for that use. <br>
Risk: The skill requires a sensitive CLAWBBA_API_KEY credential. <br>
Mitigation: Avoid pasting production keys into shared logs or screenshots, store keys locally with restricted permissions, and rotate any exposed key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawbba-ux/clawbba-api) <br>
- [ClawBBA API keys](https://www.clawbba.com/agent/api-keys) <br>
- [ClawBBA website](https://www.clawbba.com) <br>
- [OpenClaw documentation](https://docs.openclaw.ai/) <br>
- [OpenClaw Agent behavior](references/openclaw-agent-behavior.md) <br>
- [OpenClaw integration spec](references/openclaw-integration-spec.md) <br>
- [Media dispatch spec](references/media-dispatch-spec.md) <br>
- [Media capabilities](references/media-capabilities.md) <br>
- [Troubleshooting](references/SKILL-troubleshooting.md) <br>
- [OpenClaw release manifest](references/openclaw-release-manifest.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, local file paths, and MEDIA path delivery conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to invoke OpenClaw image_generate or video_generate tools and to recover or redeliver existing media instead of regenerating billed jobs.] <br>

## Skill Version(s): <br>
2.0.33 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
