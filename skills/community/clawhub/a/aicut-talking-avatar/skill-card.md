## Description:

Make a picture of a person speak a script with the aicut CLI: a voice-over first, then a lip-synced video of the picture. Use when the user asks for a talking head, a presenter or spokesperson video, an AI avatar, or a lip-sync video from a photo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simrunbot](https://clawhub.ai/user/simrunbot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to turn an approved portrait and script into a spoken voice-over and lip-synced presenter video through aicut.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is incomplete because a referenced local path was missing from the bundled artifact.

Mitigation: Resolve the missing reference and review its contents before relying on the skill.

Risk: Audio and video generation uses tokens from the user's aicut balance.

Mitigation: Estimate each command, explain the quoted price, wait for explicit approval for that purchase, and cap the spend at the approved quote.

Risk: A generated avatar could depict a real person without permission or depict a public figure.

Mitigation: Use only the user's own image, an image used with the person's permission, or a fictional or AI-generated character; decline public-figure requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simrunbot/skills/aicut-talking-avatar)
- [Setup and exit codes](artifact/references/setup.md)
- [The spend guard](artifact/references/spend.md)

## Skill Output:

**Output Type(s):** [Shell commands, Audio, Video, Guidance]

**Output Format:** [Shell commands with user-facing pricing prompts, progress updates, and generated media links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audio and video generation spend tokens; each purchase requires its own quoted price and explicit user approval.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
