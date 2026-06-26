## Description: <br>
Generates a personalized holographic Claude Buddy trading card using a Claude Code account identity, deterministic buddy attributes, and Gemini image generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dyz2102](https://clawhub.ai/user/dyz2102) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude Code users use this skill to calculate their Claude Buddy attributes, generate a themed trading-card image, and save or regenerate the result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs the agent to read a Claude Code OAuth token from macOS Keychain. <br>
Mitigation: Install only from a trusted publisher, review and explicitly approve credential access, and prefer a design that uses a user-provided non-secret seed instead of OAuth credentials. <br>
Risk: The workflow makes external network calls to fetch the Claude account UUID and to send generated prompt data to Google/Gemini for image generation. <br>
Mitigation: Review the exact data being sent before approval, use a dedicated Google API key, and avoid including secrets or personal data in the image prompt. <br>
Risk: The skill writes the generated card image to the local Downloads folder by default. <br>
Mitigation: Confirm the output path before running and choose a user-specified path when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dyz2102/buddy-card) <br>
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) <br>
- [Google AI Studio API keys](https://aistudio.google.com/apikey) <br>
- [Claude Code source leak article referenced by the artifact](https://techstartups.com/2026/03/31/anthropics-claude-source-code-leak-goes-viral-again-after-full-source-hits-npm-registry-revealing-hidden-capybara-models-and-ai-pet/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance, Image file] <br>
**Output Format:** [Markdown-style agent guidance with shell commands, generated buddy JSON, and a saved JPEG image] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS Keychain access, Claude Code credentials, a Google API key, and Node.js or Bun.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
