## Description:

Generate audiobooks from novels and long-form text with chapter management and character voices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content teams, and accessibility teams use this skill to convert books, novels, long-form articles, and e-learning material into narrated audiobook outputs with chapter structure and distinct narrator or character voices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input text is sent to SenseAudio's external TTS API.

Mitigation: Do not submit confidential, regulated, private, or rights-restricted manuscripts unless approved for that external service.

Risk: Generated MP3 and metadata files remain on disk after creation.

Mitigation: Store outputs only in approved locations and delete generated files when they are no longer needed.

## Reference(s):

- [SenseAudio Homepage](https://senseaudio.cn)
- [SenseAudio API Key Portal](https://senseaudio.cn/platform/api-key)
- [ClawHub Skill Page](https://clawhub.ai/scikkk/skills/audiobook-generator)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration, Files]

**Output Format:** [Markdown with inline Python code blocks and generated audio or metadata file descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide generation of MP3 audiobook files, chapter timestamps, and metadata files through SenseAudio API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
