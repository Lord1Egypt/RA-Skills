## Description: <br>
AI media generation via deAPI for transcription, image generation and transformation, text-to-speech, OCR, background removal, upscaling, video creation, embeddings, and account balance checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AleGlowa](https://clawhub.ai/user/AleGlowa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to call deAPI services for AI media workflows, including generating images, audio, and video, extracting text, transcribing media, creating embeddings, and configuring result delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, text, media URLs, and uploaded files are sent to deAPI for cloud processing. <br>
Mitigation: Use the skill only for data approved for deAPI processing, and avoid secrets or regulated data unless deAPI is approved for that use. <br>
Risk: The skill uses a bearer API key for deAPI requests. <br>
Mitigation: Store a dedicated DEAPI_API_KEY in the environment and rotate it if exposed. <br>
Risk: Some commands download user-provided media URLs to temporary files before upload. <br>
Mitigation: Verify URLs before processing and delete temporary files when handling sensitive media. <br>


## Reference(s): <br>
- [deAPI skill page](https://clawhub.ai/AleGlowa/deapi-ai) <br>
- [deAPI website](https://deapi.ai) <br>
- [deAPI webhooks documentation](https://docs.deapi.ai/execution-modes-and-integrations/webhooks) <br>
- [deAPI WebSockets documentation](https://docs.deapi.ai/execution-modes-and-integrations/websockets) <br>
- [Kokoro voices reference](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown with inline bash, JSON, JavaScript, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return or link to generated images, audio, videos, transcripts, OCR text, embeddings, and account balance data from deAPI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
