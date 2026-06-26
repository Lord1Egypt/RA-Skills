## Description: <br>
Your AI waifu companion that sends anime-style selfies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swancho](https://clawhub.ai/user/swancho) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users with configured fal.ai and Telegram credentials use this skill to generate anime-style selfie images from short scene prompts and send them to a configured Telegram chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selfie prompts, generated image URLs, and captions are sent to external fal.ai/xAI and Telegram services. <br>
Mitigation: Use the skill only when that data sharing is acceptable, and prefer explicit selfie requests or confirmation before sending. <br>
Risk: The skill requires credentials that can generate images and send messages to a Telegram chat. <br>
Mitigation: Keep FAL_KEY, BOT_TOKEN, and TELEGRAM_CHAT_ID private; use a dedicated Telegram bot and the intended chat ID. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/swancho/clawaifu-selfie) <br>
- [fal.ai API keys dashboard](https://fal.ai/dashboard/keys) <br>
- [Grok Imagine Edit endpoint](https://fal.run/xai/grok-imagine-image/edit) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Shell execution with terminal status text and a generated image URL; successful runs also send an image to Telegram.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FAL_KEY, BOT_TOKEN, and TELEGRAM_CHAT_ID environment variables.] <br>

## Skill Version(s): <br>
1.0.14 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
