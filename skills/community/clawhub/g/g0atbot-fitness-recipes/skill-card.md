## Description:

Fitness Recipes AI creates short-form fitness recipe videos with generated food images, voiceovers, rendered video outputs, and optional TikTok/Postiz posting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g0atfac3](https://clawhub.ai/user/g0atfac3)

### License/Terms of Use:

MIT-0

## Use Case:

Fitness influencers, nutrition coaches, and health content creators use this skill to generate single or batch short-form recipe videos for TikTok or manual export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes a hard-coded ElevenLabs credential.

Mitigation: Rotate the exposed credential if you own it and replace hard-coded secrets with isolated environment variables before execution.

Risk: The skill sends content to external media-generation and rendering services.

Mitigation: Run it in a virtual environment with scoped credentials and spending limits, and review what content may be shared before enabling API calls.

Risk: Optional TikTok/Postiz posting may publish generated content if enabled without a clear approval step.

Mitigation: Keep posting disabled until an explicit human approval step is confirmed.

Risk: The security guidance states that --test should not be relied on to prevent live API calls.

Mitigation: Verify execution paths and credentials before running test or batch workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/g0atfac3/skills/g0atbot-fitness-recipes)
- [Publisher profile](https://clawhub.ai/user/g0atfac3)
- [fal.ai](https://fal.ai)
- [ElevenLabs](https://elevenlabs.io)
- [Shotstack](https://shotstack.io)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Code]

**Output Format:** [Markdown usage guidance with Python scripts and generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce MP4 videos, generated images, voiceover audio, and batch-processing logs when executed with configured service credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-03-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
