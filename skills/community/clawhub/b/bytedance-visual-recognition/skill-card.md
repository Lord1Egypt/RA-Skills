## Description: <br>
ByteDance Visual Recognition uses Doubao-Seed multimodal models through Volcengine Ark to recognize images and videos, produce text descriptions, and generate code from visual inputs with automatic model fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[etmnb](https://clawhub.ai/user/etmnb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send selected image or video files to Volcengine/Doubao for visual understanding, OCR-style description, UI-to-code conversion, video-to-text analysis, and follow-up questions on the last recognition result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images, videos, and prompts are sent to Volcengine/Doubao for recognition. <br>
Mitigation: Use the skill only with media you are permitted to share with that cloud service, and avoid confidential, regulated, or sensitive files unless that transfer is approved. <br>
Risk: Batch mode can process broad directories and upload many local media files. <br>
Mitigation: Run batch mode only on a reviewed, narrow folder that contains intended files, and avoid broad or sensitive directories. <br>
Risk: The script keeps local temporary copies, recognition history, token counters, and last-response metadata. <br>
Mitigation: Clear Temp, vision_history.json, and .last_response after sensitive use, or configure storage paths to controlled locations. <br>
Risk: The skill requires Ark API credentials and optional Volcengine IAM credentials. <br>
Mitigation: Use least-privilege credentials, keep them out of shared repositories and logs, and rotate them if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/etmnb/bytedance-visual-recognition) <br>
- [Volcengine Ark Doubao API documentation](https://www.volcengine.com/docs/82379/1569618) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text, with generated code when code mode is selected] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include model name, token usage, remaining daily quota, recognition text or generated code, and status/history summaries.] <br>

## Skill Version(s): <br>
3.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
