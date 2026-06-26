## Description: <br>
A sleep and relaxation skill that sends AI-generated bedtime audio stories mixed with ambient background music as a voice message on WhatsApp, WeChat, or Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tiansyao](https://clawhub.ai/user/tiansyao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to request bedtime stories, ambient sounds, music-only tracks, or children's sleep content through linked chat platforms. The agent selects from the DozyTale theme catalog, prepares an audio track with ffmpeg, and sends the result as a chat voice message. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local OpenClaw WeChat account context files to identify a message target. <br>
Mitigation: Install only after confirming the linked chat account is appropriate, and verify the target account before enabling scheduled sends. <br>
Risk: The skill can create an ongoing daily scheduled sender named dozytale-nightly. <br>
Mitigation: Confirm the delivery time before setup, and use OpenClaw cron listing and removal commands to audit or disable the job. <br>
Risk: The skill downloads audio assets and sends media through linked WhatsApp, WeChat, or Feishu accounts. <br>
Mitigation: Use it only in environments where external audio downloads and chat-account message delivery are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/tiansyao/dozytale-skill) <br>
- [DozyTale](https://dozytale.ai) <br>
- [OpenClaw skills documentation](https://docs.openclaw.ai/skills) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with bash command blocks and generated audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates temporary MP3 or OGG audio files and may configure a daily OpenClaw cron job for scheduled bedtime delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
