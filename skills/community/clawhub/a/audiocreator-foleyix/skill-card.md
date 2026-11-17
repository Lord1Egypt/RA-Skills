## Description:

Helps create and refine Foleyix prompts for music, speech, sound effects, and ambience, and can generate and download private WAV audio through a connected Foleyix account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvyinchao](https://clawhub.ai/user/lvyinchao)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to draft or repair audio prompts and, when requested, generate music, narration, dialogue, podcasts, effects, and ambience with their Foleyix account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account login stores a Foleyix access token locally.

Mitigation: Approve the browser-based login yourself and keep the private Foleyix configuration directory protected; do not share credentials with the agent.

Risk: Requested audio generation consumes account quota, including time reserved by queued tasks.

Mitigation: Check available quota before generating and reuse existing task IDs when recovering a timed-out or interrupted request.

Risk: Uploading a reference voice can expose audio or use a voice without permission.

Mitigation: Upload only WAV recordings the user is authorized to use and require the separately approved voice-write permission.

Risk: Generated WAV downloads may contain private account content.

Mitigation: Save results only to user-selected paths and avoid sharing private downloads without authorization.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/lvyinchao/skills/audiocreator-foleyix)
- [Foleyix skill homepage](https://foleyix.com/skill)
- [Foleyix CLI reference](references/cli.md)
- [Audio capabilities](references/audio-capabilities.json)
- [Prompt writing guide](references/prompt-writing.md)

## Skill Output:

**Output Type(s):** [Text guidance, Shell commands, Audio files]

**Output Format:** [Markdown prompts and guidance; WAV files when generation is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt drafting needs no login; audio generation requires a connected account and available quota.]

## Skill Version(s):

1.5.0 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
