## Description:

A sleep and relaxation skill that sends AI-generated bedtime audio stories mixed with ambient background music as a voice message on WhatsApp, WeChat, or Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tiansyao](https://clawhub.ai/user/tiansyao)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to request a calming bedtime story, ambient music, white noise, or children's sleep content through chat. The agent selects a theme, prepares mixed audio when possible, and sends it through a connected OpenClaw chat channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create a daily recurring OpenClaw task for bedtime messages.

Mitigation: Ask for explicit scheduling consent, state the schedule clearly, and provide an easy stop command before enabling recurring delivery.

Risk: The skill reads local WeChat account context files to infer a message recipient.

Mitigation: Avoid context-token file access when possible and require the user to confirm the recipient before sending proactive messages.

Risk: The skill sends media and text through connected chat channels.

Mitigation: Review the destination channel and generated message before sending, especially when multiple chat channels are connected.

Risk: The skill appends promotional tracked DozyTale links after delivery.

Mitigation: Disclose promotional links and make marketing follow-up optional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tiansyao/skills/dozytale-skill)
- [OpenClaw skills documentation](https://docs.openclaw.ai/skills)
- [OpenClaw](https://openclaw.ai)
- [DozyTale](https://dozytale.ai)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, audio file, chat messages]

**Output Format:** [Chat text with inline shell commands and generated OGG or MP3 media output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ffmpeg and ffprobe to mix or convert audio; can send media and text through connected OpenClaw channels.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter declares 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
