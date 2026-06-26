## Description: <br>
Converts and transcodes audio formats and encoding settings with Volcengine LAS, including sample rate, bitrate, channels, compression, quality, TOS paths, and local uploads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare audio for downstream workflows by converting files among formats such as wav, mp3, flac, m4a, ogg, and aac, adjusting encoding parameters, and handling local or TOS-hosted inputs through Volcengine LAS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow can fetch remote metadata and install or upgrade a remote SDK without explicit integrity verification. <br>
Mitigation: Preinstall or independently verify the Volcengine LAS SDK before use, and review the setup script before sourcing it. <br>
Risk: The skill requires sensitive cloud credentials and may send selected audio files to Volcengine/TOS. <br>
Mitigation: Use least-privilege temporary credentials, process only approved audio, and keep credential files such as env.sh out of shared or version-controlled folders. <br>
Risk: Region or TOS bucket mismatches can cause permission errors or failed uploads. <br>
Mitigation: Confirm LAS_REGION, API key scope, and TOS bucket region before uploading or processing audio. <br>
Risk: Cloud processing can incur charges that differ from estimates. <br>
Mitigation: Estimate cost from audio duration, disclose that billing is an estimate, and wait for explicit user confirmation before submitting work. <br>


## Reference(s): <br>
- [las_audio_convert API Reference](references/api.md) <br>
- [Pricing Information](references/prices.md) <br>
- [Volcengine LAS Pricing](https://www.volcengine.com/docs/6492/1544808) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local data/result JSON files and invoke LAS/TOS APIs after user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
