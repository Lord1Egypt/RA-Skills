## Description: <br>
Detects liveness from a single selfie image via the Didit standalone API, supporting checks for physical presence, spoofing or presentation attacks, passive liveness verification, and face quality and luminance metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rosasalberto](https://clawhub.ai/user/rosasalberto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and identity-verification teams use this skill to call Didit's passive liveness endpoint for selfie-based anti-spoofing checks, face-quality review, and liveness scoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive face images through Didit for biometric liveness analysis. <br>
Mitigation: Use only with appropriate consent and clear retention expectations before submitting selfie images. <br>
Risk: Didit API credentials could be exposed through prompts, logs, or shared command history. <br>
Mitigation: Use a dedicated API key and avoid placing credentials in prompts, logs, or committed files. <br>
Risk: Saved API requests may affect retention expectations. <br>
Mitigation: Review Didit's retention and Business Console settings, especially where saved API requests are enabled by default. <br>


## Reference(s): <br>
- [Didit documentation](https://docs.didit.me) <br>
- [Didit Passive Liveness API reference](https://docs.didit.me/standalone-apis/passive-liveness) <br>
- [Didit liveness overview](https://docs.didit.me/core-technology/liveness/overview) <br>
- [ClawHub release page](https://clawhub.ai/rosasalberto/didit-liveness-detection) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with code examples, shell commands, and JSON API response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DIDIT_API_KEY and sends a user selfie image to the Didit API.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
