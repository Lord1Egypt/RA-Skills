## Description: <br>
Use when the user wants GPT-Image-2 image generation or image-to-image through an official OpenAI permission code/API key, a custom Responses-compatible proxy, or a reserved purchased-capacity relay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[etherstrings](https://clawhub.ai/user/etherstrings) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate or transform PNG images through an official OpenAI API key, a Responses-compatible proxy, or a reserved purchased-capacity relay while keeping credentials redacted in outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected images may be sent to OpenAI, a configured proxy, or a reserved-capacity relay. <br>
Mitigation: Use only trusted endpoints and avoid submitting sensitive images or confidential prompts through untrusted relays. <br>
Risk: The skill requires sensitive API, proxy, relay, or purchase credentials at runtime. <br>
Mitigation: Pass credentials through environment variables or a local secret manager, use scoped or disposable credentials where possible, and keep returned summaries redacted. <br>
Risk: Reserved mode can redeem purchase keys or consume quota. <br>
Mitigation: Require explicit user confirmation before reserved-mode generation, quota consumption, or purchase-key redemption. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/etherstrings/autogenimageskill) <br>
- [Access Modes](references/access-modes.md) <br>
- [Runtime Notes](references/runtime.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Configuration guidance] <br>
**Output Format:** [Markdown with shell commands and generated PNG file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the absolute output image path plus access mode, endpoint or relay job ID, provider name when available, byte size, and revised prompt when returned; credentials remain redacted.] <br>

## Skill Version(s): <br>
0.1.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
