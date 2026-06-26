## Description: <br>
Alibaba Bailian Fun-ASR recording transcription supports Chinese, English, and other languages with automatic language detection and speaker diarization for subtitles, transcription, and meeting notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run dLazy's hosted Fun-ASR transcription workflow through the dLazy CLI for audio transcription, subtitles, meeting notes, and speaker diarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key and may store it in the local CLI configuration. <br>
Mitigation: Treat the API key as a sensitive credential, prefer least-privilege local access, and rotate or revoke the key when access changes. <br>
Risk: Audio or media paths passed to the CLI may be uploaded to dLazy-hosted services for processing. <br>
Mitigation: Use the skill only with audio or media that is approved for upload to dLazy's API and file hosting endpoints. <br>
Risk: Artifact prose contains a stale package-version reference even though install metadata pins @dlazy/cli@1.2.0. <br>
Mitigation: Confirm the intended @dlazy/cli version before installing or running the skill. <br>


## Reference(s): <br>
- [Dlazy Fun Asr on ClawHub](https://clawhub.ai/dlazyai/dlazy-fun-asr) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI can return synchronous JSON output or an asynchronous task identifier for later polling.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
