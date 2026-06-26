## Description: <br>
Generate images via OpenRouter (google/gemini-2.5-flash-image) and send to Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drones277](https://clawhub.ai/user/drones277) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and automation agents use this skill to generate AI images from a prompt through OpenRouter and deliver the resulting image to a Telegram chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may fetch unvalidated URLs returned by the model response. <br>
Mitigation: Validate or allowlist downloaded image URLs before fetching them. <br>
Risk: The Telegram workflow may send unintended temporary files if a broad file glob is used. <br>
Mitigation: Send only the exact file paths returned by the generation script. <br>
Risk: Generated image prompts and API credentials may expose sensitive data to external services. <br>
Mitigation: Use a revocable OpenRouter API key and avoid sensitive prompts. <br>
Risk: Generated temporary images may remain after delivery. <br>
Mitigation: Delete temporary image files after they are sent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drones277/gemini-tg-image-gen) <br>
- [OpenRouter chat completions API](https://openrouter.ai/api/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [files, text, shell commands, configuration, guidance] <br>
**Output Format:** [Telegram text and image messages, local image files, and JSON path output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENROUTER_API_KEY and writes generated image files under the OpenClaw workspace temporary directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
