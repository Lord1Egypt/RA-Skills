## Description: <br>
Generate audiobooks from novels and long-form text with chapter management and character voices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to guide audiobook generation from novels, long-form articles, e-learning content, and other written material using SenseAudio text-to-speech. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input text submitted for narration is sent to SenseAudio and may include confidential, unpublished, copyrighted, or personal content. <br>
Mitigation: Review SenseAudio privacy, retention, billing, and rights terms before use, and avoid sensitive or unlicensed inputs unless approved. <br>
Risk: The workflow requires a SenseAudio API key. <br>
Mitigation: Store the key in an environment variable or secret manager, do not embed it in shared code, and rotate it if exposed. <br>
Risk: Generated MP3 audio and metadata files are saved locally. <br>
Mitigation: Choose a controlled output directory and manage or delete generated files according to retention and access requirements. <br>


## Reference(s): <br>
- [SenseAudio](https://senseaudio.cn) <br>
- [SenseAudio API Key Portal](https://senseaudio.cn/platform/api-key) <br>
- [ClawHub Audiobook Release](https://clawhub.ai/scikkk/audiobook-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown with Python code examples and file output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of MP3 audio files, JSON chapter timestamps, and metadata files.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
