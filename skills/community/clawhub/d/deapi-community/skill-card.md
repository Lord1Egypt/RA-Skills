## Description: <br>
Generate images, music, speech, transcriptions, OCR, video, background removal, upscaling, style transfer, embeddings, and prompt enhancements through the deAPI REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zrewolwerowanykaloryfer](https://clawhub.ai/user/zrewolwerowanykaloryfer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide an agent in making deAPI media API calls for generation, transcription, OCR, transformation, embeddings, prompt enhancement, and account-balance checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a deAPI API key and may expose account credit if the key is overprivileged or mishandled. <br>
Mitigation: Use a dedicated or low-balance API key and keep DEAPI_API_KEY out of prompts, logs, and shared artifacts. <br>
Risk: Prompts, media files, voice samples, and URLs selected by the user are sent to deAPI for processing. <br>
Mitigation: Avoid confidential or third-party media unless the user understands provider handling and has permission to process it. <br>
Risk: Voice cloning can be misused without consent from the speaker. <br>
Mitigation: Get consent before using voice cloning and reject requests that appear to impersonate someone without authorization. <br>
Risk: Shell examples that include user-supplied URLs, JSON, or file paths can be unsafe if inputs are substituted directly. <br>
Mitigation: Build JSON with jq, validate URLs and file paths, and avoid passing raw user input directly into shell strings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zrewolwerowanykaloryfer/deapi-community) <br>
- [deAPI service site](https://deapi.ai) <br>
- [deAPI API documentation](https://docs.deapi.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash, curl, JSON, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DEAPI_API_KEY and sends selected prompts, media files, voice samples, and URLs to deAPI for processing.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
