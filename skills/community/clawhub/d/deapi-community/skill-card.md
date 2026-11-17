## Description:

Generate images, music, speech, transcriptions, OCR output, video, background removal, upscaling, style transfer, and prompt enhancements through the deAPI media API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zrewolwerowanykaloryfer](https://clawhub.ai/user/zrewolwerowanykaloryfer)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and creators use this skill to have an agent prepare deAPI media API requests for transcription, image generation, text-to-speech, voice cloning, music generation, video generation, OCR, image editing, embeddings, and account-balance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted prompts, URLs, or file paths in documented curl workflows could expose local or internal data.

Mitigation: Use only explicit user-approved media, validate public URLs strictly, verify local file paths before upload, and replace non-file curl -F fields with --form-string.

Risk: Sensitive or confidential media may be sent to deAPI for processing or made available through result URLs.

Mitigation: Avoid sensitive or confidential files unless the operator has confirmed that deAPI data handling and result-link exposure are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zrewolwerowanykaloryfer/skills/deapi-community)
- [deAPI service](https://deapi.ai)
- [deAPI API documentation](https://docs.deapi.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with curl commands, JSON payload examples, and result-handling notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DEAPI_API_KEY; deAPI media operations are asynchronous and typically require polling a request status endpoint before retrieving results.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
