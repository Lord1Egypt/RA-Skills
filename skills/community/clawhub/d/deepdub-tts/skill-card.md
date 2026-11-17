## Description:

Generate speech audio using Deepdub and attach it as a MEDIA file for agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuval-deepdub](https://clawhub.ai/user/yuval-deepdub)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to convert text into spoken audio through Deepdub and return the generated MP3 as a MEDIA attachment for channels such as Telegram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared trial credentials may be rate-limited and are not appropriate for real work.

Mitigation: Use your own Deepdub API key and voice prompt ID before production use.

Risk: The unpinned deepdub dependency may change behavior across installations.

Mitigation: Pin or lock the deepdub package before production deployment.

Risk: Generated audio files are written to the configured media directory.

Mitigation: Set OPENCLAW_MEDIA_DIR to a directory intended for generated audio and run the skill in an isolated, unprivileged environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuval-deepdub/skills/deepdub-tts)
- [Deepdub](https://deepdub.ai)

## Skill Output:

**Output Type(s):** [files, text]

**Output Format:** [MEDIA path string plus generated MP3 audio file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes audio files to OPENCLAW_MEDIA_DIR and requires DEEPDUB_API_KEY and DEEPDUB_VOICE_PROMPT_ID.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
