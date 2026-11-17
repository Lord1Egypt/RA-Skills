## Description:

Call Aliyun Bailian via DashScope; support OCR, TTS, text-to-image and image-to-image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yab](https://clawhub.ai/user/yab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Bailian Studio to call Aliyun DashScope for OCR text extraction, TTS synthesis or playback, and text-to-image or image-to-image generation. Local image inputs can be uploaded to OSS when a remote image URL is required by the service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images and text submitted through the skill may be sent to Aliyun DashScope, and local images may be uploaded to OSS.

Mitigation: Use only non-sensitive media and text unless that external processing is acceptable; prefer private buckets, short-lived URLs, and narrowly scoped credentials.

Risk: Untrusted endpoint overrides could expose credentials or private media.

Mitigation: Use documented Aliyun HTTPS endpoints and avoid untrusted DASHSCOPE_BASE_URL, --base-url, or OSS_ENDPOINT values.

Risk: Runtime dependency or environment drift could affect command behavior.

Mitigation: Run the skill in an isolated virtual environment with reviewed, pinned dependencies.

## Reference(s):

- [Bailian Studio on ClawHub](https://clawhub.ai/yab/skills/bailian-studio)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Plain text, command-line output, saved PNG files, and optional WAV files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DashScope credentials; OSS credentials are required when local images need to be uploaded before cloud processing.]

## Skill Version(s):

0.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
