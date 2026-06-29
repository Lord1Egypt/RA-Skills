## Description: <br>
Use the AutoGLM Image Recognition API to analyze and describe image content, including object or scene recognition, OCR-like text extraction, and general image descriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[khurramjamil12](https://clawhub.ai/user/khurramjamil12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send public image URLs, or uploaded local images, to AutoGLM for image description, object or scene recognition, and OCR-style text extraction. It is useful when a user needs a concise interpretation of image content returned as text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images, image URLs, and prompts are sent to AutoGLM, and local images may be uploaded to a public URL before processing. <br>
Mitigation: Use only with content appropriate for external processing; avoid confidential screenshots, IDs, private documents, and sensitive photos. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/khurramjamil12/autoglm-image-recognition) <br>
- [AutoGLM Image Recognition API endpoint](https://autoglm-api.autoglm.ai/agentdr/v1/assistant/skills/image-recognition) <br>
- [AutoGLM upload endpoint](https://autoglm-api.autoglm.ai/agentdr/v1/assistant/upload-mix) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands] <br>
**Output Format:** [JSON responses from helper scripts and user-facing text or Markdown derived from the recognition result] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local images must be uploaded first to obtain a public image URL before recognition.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
