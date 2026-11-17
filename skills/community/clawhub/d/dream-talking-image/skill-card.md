## Description:

Generate talking videos from static image and audio URLs using the Dreamface/NewportAI Talking Image API, including support for non-human faces such as pets or animated characters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hy-1990](https://clawhub.ai/user/hy-1990)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure a DreamAPI key and call the Talking Image API to create talking videos from supplied image and audio URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image and audio URLs are processed by the third-party Dreamface/NewportAI service using the user's API key.

Mitigation: Avoid submitting private, regulated, or non-consensual photos or voice recordings unless third-party handling is acceptable.

Risk: Long audio inputs may cause memory errors or failed processing.

Mitigation: Keep audio under the documented two-minute recommendation and prefer m4a format where practical.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hy-1990/skills/dream-talking-image)
- [NewportAI Talking Image API Reference](https://api.newportai.com/api-reference/talking-image)
- [NewportAI API Get Started](https://api.newportai.com/api-reference/get-started)
- [Dreamface AI Tools](https://tools.dreamfaceapp.com/home)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON request examples, and API endpoint guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DREAMTALKINGIMAGE_API_KEY and user-supplied photoUrl and audioUrl values.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
