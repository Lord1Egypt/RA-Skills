## Description: <br>
Call Aliyun Bailian through DashScope for OCR, TTS, text-to-image, and image-to-image workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yab](https://clawhub.ai/user/yab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Alibaba Cloud DashScope/Bailian media tasks, including extracting text from images, synthesizing speech, and generating or transforming images from prompts and optional references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, OCR text, and selected local images may be sent to Alibaba Cloud DashScope and related OSS storage. <br>
Mitigation: Avoid confidential documents, private images, and sensitive prompts unless retention, access control, and deletion behavior are acceptable. <br>
Risk: Local images used for OCR or image-to-image workflows may be uploaded to configured OSS storage before processing. <br>
Mitigation: Use URL inputs or non-sensitive local files when possible, and verify OSS bucket access controls and cleanup expectations before use. <br>
Risk: TTS can play generated audio in the local environment. <br>
Mitigation: Use the WAV output option or confirm the playback environment is appropriate before running TTS in shared spaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yab/bailian-studio) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; runtime scripts produce plain text, local PNG files, WAV files, or audio playback.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images default to local PNG files under tmp/bailian-studio; OCR prints recognized text; TTS can play audio or save WAV output.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
