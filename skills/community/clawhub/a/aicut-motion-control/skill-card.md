## Description:

Make a character from a picture copy the motion of a reference video (a dance, a walk, a gesture) with the aicut CLI (`aicut transform motion-control`). Use when the user wants to animate a character picture with the movement of another clip.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simrunbot](https://clawhub.ai/user/simrunbot)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and video editors use this skill to animate a character image with the movement from a reference video, such as a dance, walk, or gesture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reported that a local reference in SKILL.md did not match a bundled artifact.

Mitigation: Check the reference and decide whether the skill’s stated use fits your needs before installing.

Risk: Video generation uses tokens from the user's aicut balance.

Mitigation: Estimate the price and get the user's explicit approval for that purchase before running the paid command.

Risk: A real person's image could be used without their permission.

Mitigation: Use images only of the user, someone who gave permission, or a fictional or AI-generated character; do not use public figures.

## Reference(s):

- [Setup and exit codes](artifact/references/setup.md)
- [The spend guard](artifact/references/spend.md)

## Skill Output:

**Output Type(s):** [Video, Shell commands, Guidance]

**Output Format:** [Generated video with concise Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a character image, a 3–30 second motion clip (10 seconds for still portraits), and explicit approval after each price estimate before paid generation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
