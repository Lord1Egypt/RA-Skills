## Description:

Generates podcast audio from a topic, webpage, downloadable document, uploaded file text, or long text using Volcengine Doubao PodcastTTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents use this skill to turn a short topic, webpage, file URL, uploaded document text, or long text into a podcast-style audio file and segmented transcript.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential management behavior is under-disclosed and may create or persist speech-service credentials.

Mitigation: Use a pre-provisioned MODEL_SPEECH_API_KEY and review local environment handling before installation.

Risk: Custom ARK_SKILL_API_BASE values can direct credential-management requests to an untrusted endpoint.

Mitigation: Set ARK_SKILL_API_BASE only to a verified HTTPS service endpoint, or leave it unset.

Risk: Submitted documents, private URLs, prompts, and generated text are sent to an external Volcengine/Bytedance speech-service workflow and may appear in logs.

Mitigation: Avoid confidential inputs unless the user accepts that external processing and logging exposure.

## Reference(s):

- [Volcengine Doubao Podcast product documentation](https://www.volcengine.com/docs/6561/1668014?lang=zh)

## Skill Output:

**Output Type(s):** [text, files, shell commands, configuration, guidance]

**Output Format:** [JSON status output with local audio file path, optional audio URL, and segmented transcript text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audio output can be mp3, wav, or ogg_opus; successful runs may include a time-limited service audio URL.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
