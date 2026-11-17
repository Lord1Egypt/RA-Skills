## Description:

Generates ElevenLabs eleven_v3 multi-voice dialogue audio from per-line text and voice assignments, with support for up to 10 voices and expressive audio tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers can use the skill to synthesize dialogue, podcasts, and short skits with assigned voices and expressive tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is described as ElevenLabs dialogue generation, while its supplied instructions focus on dLazy login and authentication; scanner coverage is partial.

Mitigation: Verify the command's documented behavior and returned asset type before relying on it.

Risk: Prompts and local media passed through the CLI are sent to dLazy-hosted services.

Mitigation: Avoid sending sensitive content unless its use with that service is approved.

Risk: The CLI requires a dLazy API key.

Mitigation: Use an organization-approved key, keep it confidential, and rotate or revoke it if exposed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-elevenlabs-dialogue)
- [CLI repository (listed in skill metadata)](https://github.com/dlazy-ai/cli)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Audio, JSON]

**Output Format:** [Generated audio asset or hosted audio URL, with JSON generation metadata and status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The description specifies up to 20 dialogue lines and 10 unique voices. Async mode can return task status before the audio is ready; the result can also be saved locally.]

## Skill Version(s):

1.3.41 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
