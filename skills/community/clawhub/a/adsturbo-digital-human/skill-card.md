## Description:

Turn a script into a talking avatar: choose a platform digital human, clone a custom one from a photo and voice sample, or lip-sync a single portrait to an audio track. Includes TTS voiceover and avatar management. Requires an AdsTurbo account; users can sign up or log in right in the chat with an email code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adsturbo](https://clawhub.ai/user/adsturbo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to make a talking-head video from a script and selected or custom avatar, generate TTS audio, or lip-sync a portrait to supplied audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portrait and voice files are uploaded and may be publicly accessible. The security evidence flags the absence of a privacy warning or consent step and describes its assessment as medium-confidence and incomplete.

Mitigation: Before uploading, confirm users understand and agree to the handling of their portrait and voice files, including possible public accessibility.

## Reference(s):

- [Digital human commands](references/digital_human.md)
- [Login guide](references/login.md)
- [Media upload guide](references/upload.md)
- [Async task guide](references/work.md)
- [AdsTurbo API key management](https://adsturbo.ai/iris/api)
- [AdsTurbo pricing](https://adsturbo.ai/pricing)
- [ClawHub skill page](https://clawhub.ai/adsturbo/skills/adsturbo-digital-human)

## Skill Output:

**Output Type(s):** [Video, Audio, Avatar details, Result URLs]

**Output Format:** [Generated media and result links, with JSON status details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asynchronous video and avatar jobs may take several minutes; custom avatar creation requires a Pro plan, and 1080p or higher video requires a subscription.]

## Skill Version(s):

1.4.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
