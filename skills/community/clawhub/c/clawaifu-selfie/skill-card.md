## Description:

Your AI waifu companion that sends anime-style selfies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swancho](https://clawhub.ai/user/swancho)

### License/Terms of Use:


## Use Case:

External users invoke this skill when they want an agent to generate an anime-style selfie from a short scene or situation description and send it to a configured Telegram chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, generated images, captions, and Telegram destination details leave the local machine through third-party services.

Mitigation: Use a dedicated low-privilege Telegram bot and Fal key, verify the chat ID, and avoid sensitive captions or context.

Risk: Security evidence reports a verified file-disclosure bug in the Telegram upload command.

Mitigation: Fix the curl form handling to use literal form values before using this skill where local files or credentials matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/swancho/skills/clawaifu-selfie)
- [Fal API key dashboard](https://fal.ai/dashboard/keys)
- [Grok Imagine Edit endpoint](https://fal.run/xai/grok-imagine-image/edit)

## Skill Output:

**Output Type(s):** [shell commands, text, configuration]

**Output Format:** [Shell command invocation with status text and a generated image URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FAL_KEY, BOT_TOKEN, and TELEGRAM_CHAT_ID environment variables; sends generated image content through Fal and Telegram.]

## Skill Version(s):

1.0.14 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
