## Description: <br>
ElevenLabs scribe_v1 speech-to-text with auto language detection and optional speaker diarization, suitable for subtitles, transcription, and meeting notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to invoke dLazy's ElevenLabs speech-to-text workflow for audio transcription, subtitles, and meeting notes. It supports cloud API authentication, local or remote audio input, language selection, optional diarization, and asynchronous task polling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials for dLazy API access. <br>
Mitigation: Use `dlazy login`, `dlazy auth set`, or `DLAZY_API_KEY` only in trusted environments, rotate keys from the dLazy dashboard when needed, and avoid exposing keys in shared logs or prompts. <br>
Risk: Audio files may be uploaded to dLazy-hosted API and media storage endpoints for processing. <br>
Mitigation: Use the skill only with audio that the user is permitted to send to dLazy's hosted service, and review service terms before processing sensitive recordings. <br>
Risk: Installing `@dlazy/cli@latest` can reduce reproducibility because the installed CLI version may change over time. <br>
Mitigation: Review the current @dlazy/cli release before installation, or pin a specific trusted version for repeatable deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-elevenlabs-stt) <br>
- [dLazy publisher profile](https://clawhub.ai/user/dlazyai) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy service homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, json, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npm or npx, a dLazy API key, and network access to dLazy API and file endpoints.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
