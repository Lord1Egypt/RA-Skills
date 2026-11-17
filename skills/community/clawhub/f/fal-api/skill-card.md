## Description:

Fal.ai API generates images, videos, and audio transcriptions through fal.ai models such as FLUX, SDXL, MiniMax, WAN, and Whisper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricanwarfare](https://clawhub.ai/user/ricanwarfare)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to submit fal.ai media-generation or transcription jobs, poll for completion, and return generated media URLs or transcript results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, media URLs, audio content, and the fal.ai API key are sent to fal.ai for processing.

Mitigation: Use the skill only for data that may be processed by fal.ai, avoid private recordings, secrets, regulated data, and signed internal URLs, and prefer a scoped or revocable API key.

Risk: The skill requires network access and a valid paid or quota-backed fal.ai account to complete media jobs.

Mitigation: Confirm account credits, rate limits, and network policy before using the skill in automated workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ricanwarfare/skills/fal-api)
- [Publisher profile](https://clawhub.ai/user/ricanwarfare)
- [fal.ai API keys](https://fal.ai/dashboard/keys)
- [fal.ai dashboard](https://fal.ai/dashboard)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Code]

**Output Format:** [Text output with generated media URLs, transcription results, errors, and command-line or Python usage snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a FAL_KEY credential and network access to fal.ai.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
