## Description: <br>
Generate AI images using MiniMax or fal.ai (Grok Imagine) and send to messaging channels via OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HonestQiao](https://clawhub.ai/user/HonestQiao) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External OpenClaw users and agent builders use this skill to generate persona-based selfie images from prompts and deliver them to messaging channels through OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can modify persistent OpenClaw identity and configuration files. <br>
Mitigation: Inspect or back up IDENTITY.md, SOUL.md, and openclaw.json before running the installer, and test in a controlled OpenClaw environment. <br>
Risk: Generated images and captions can be posted to external messaging channels. <br>
Mitigation: Avoid sensitive prompts or private channels, verify target channel values before sending, and keep gateway tokens scoped and protected. <br>
Risk: The TypeScript CLI path is reported as command-injection-prone. <br>
Mitigation: Do not use the TypeScript CLI path until shell execution is replaced with argument-safe execution or a direct API call. <br>
Risk: API keys may be exposed if configuration is shared. <br>
Mitigation: Use environment variables for API keys and rotate any fal.ai or MiniMax keys after testing if configuration may have been shared. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/HonestQiao/clawra-selfie-minimax) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [fal.ai API Keys](https://fal.ai/dashboard/keys) <br>
- [MiniMax Platform](https://platform.minimaxi.com) <br>
- [Clawra Reference Image](https://cdn.jsdelivr.net/gh/SumeLabs/clawra@main/assets/clawra.png) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, image] <br>
**Output Format:** [Markdown instructions with shell command examples; runtime scripts emit JSON summaries and image media or URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires external image-generation API keys and OpenClaw channel configuration.] <br>

## Skill Version(s): <br>
1.2.0 (source: evidence.release.version and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
