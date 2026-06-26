## Description: <br>
Convert text into high-quality, emotional speech reading using Kling TTS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate speech from text through the dLazy CLI and hosted Kling TTS service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key and may save credentials in the local CLI config. <br>
Mitigation: Prefer the DLAZY_API_KEY environment variable when credentials should not be persisted, and rotate or revoke keys through the dLazy dashboard when needed. <br>
Risk: Prompts and referenced files are sent to dLazy's hosted service for text-to-speech generation. <br>
Mitigation: Use the skill only with content that is appropriate to send to dLazy, and review dLazy's service terms and CLI behavior before use. <br>
Risk: Using the global npm install path adds a third-party CLI to the user's environment. <br>
Mitigation: Review the @dlazy/cli package or source before installation, or run the pinned package on demand with npx. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-keling-tts) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated audio output is returned through dLazy result URLs; asynchronous calls may return a task identifier for later polling.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
