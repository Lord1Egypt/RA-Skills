## Description:

Real time video translation and dubbing skill that translates a user-provided video file or URL and returns a preview URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[papawaigo](https://clawhub.ai/user/papawaigo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit a video file or accessible video URL for translation and dubbing, then receive the translated video's preview URL. It supports Chinese, English, French, and Japanese target languages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected video files or video URLs are sent to the external service audiox-api-global.luoji.cn.

Mitigation: Use the skill only for media appropriate for that service's privacy and retention practices.

Risk: The bundled curl helper is example-grade and accepts user-supplied video URLs.

Mitigation: Harden URL validation and request handling before using the helper with untrusted inputs.

Risk: The skill requires a bearer credential through VIDEO_TRANSLATE_SERVICE_API_KEY.

Mitigation: Store the credential in the environment, avoid logging it, and rotate it if exposure is suspected.

## Reference(s):

- [API Contract](references/api-contract.md)
- [DubbingHub ClawHub Page](https://clawhub.ai/papawaigo/skills/dubbing-hub)
- [External Video Translation Service](https://audiox-api-global.luoji.cn)
- [LuoJi Support and Privacy](https://luoji.cn)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown or plain text containing API status, errors, and the final preview URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VIDEO_TRANSLATE_SERVICE_API_KEY; returns preview_url on success or service error text on failure.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
