## Description: <br>
ClawBB is a macOS voice-to-text helper for dictating text into applications with Google Gemini. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dyz2102](https://clawhub.ai/user/dyz2102) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators on macOS use ClawBB to dictate prompts, code-adjacent notes, and other text into the active application without switching context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing ClawBB requires trusting an external native macOS app with microphone, Accessibility, and Gemini API access. <br>
Mitigation: Verify the DMG checksum, confirm you trust the GitHub release or source, and grant macOS permissions only if that access is acceptable. <br>
Risk: Dictated audio is sent to Google Gemini for transcription. <br>
Mitigation: Avoid dictating secrets or sensitive material unless that processing is acceptable for the user's environment. <br>
Risk: The Gemini API key may be stored locally for app use. <br>
Mitigation: Use a dedicated Gemini API key when possible and protect the local key file with restrictive permissions. <br>


## Reference(s): <br>
- [ClawBB on ClawHub](https://clawhub.ai/dyz2102/clawbb) <br>
- [XiaBB Website](https://xiabb.lol) <br>
- [XiaBB GitHub Repository](https://github.com/dyz2102/xiabb) <br>
- [Google AI Studio API Key](https://aistudio.google.com/apikey) <br>
- [XiaBB v1.1.3 macOS DMG](https://github.com/dyz2102/xiabb/releases/download/v1.1.3/XiaBB-v1.1.3-macOS-arm64.dmg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with installation commands, setup steps, and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Gemini API key and local macOS permissions for microphone and Accessibility access.] <br>

## Skill Version(s): <br>
1.1.5 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
