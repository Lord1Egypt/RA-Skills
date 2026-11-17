## Description:

Helps agents write and refine audio prompts, generate music, speech, ambience, and effects with Foleyix, and retrieve finished audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvyinchao](https://clawhub.ai/user/lvyinchao)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to draft or repair audio prompts and, when requested, generate and download Foleyix music, songs, podcasts, narration, dialogue, ambience, and sound effects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested generation sends prompts and selected voice IDs to Foleyix and may consume account quota.

Mitigation: Use the account only for requested generation; review prompt content and quota before submission.

Risk: Browser-approved login leaves local account state until logout.

Mitigation: Keep the local config directory private and log out when the connection is no longer needed.

## Reference(s):

- [Foleyix skill page](https://foleyix.com/skill)
- [ClawHub release](https://clawhub.ai/lvyinchao/skills/foleyix)
- [Prompt-writing guide](references/prompt-writing.md)
- [CLI reference](references/cli.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files]

**Output Format:** [Ready-to-use audio prompts and status guidance in text or Markdown; WAV files when generation is requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt writing works offline; audio generation and retrieval require a Foleyix account and network access.]

## Skill Version(s):

1.4.1 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
