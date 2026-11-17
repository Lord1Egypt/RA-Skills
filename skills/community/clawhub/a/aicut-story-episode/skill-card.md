## Description:

Make an AI Video Story episode with the aicut CLI: pick a series, write the cast, review the scene pictures, fire the scene videos and render the final file, with a price and an ask at every paid step. Use when the user wants a story video, a series episode, a short film with recurring characters, or an AI video story.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simrunbot](https://clawhub.ai/user/simrunbot)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to create an AI story episode with recurring characters through the aicut CLI. It guides series selection, story and cast setup, scene review, and user-approved video generation and rendering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video, image, and audio generation spend the user's aicut token balance; firing scene videos is irreversible and non-refundable.

Mitigation: Estimate each paid action, explain its price and scope, and obtain explicit approval for that purchase; require an explicit, firing-specific approval before generating scene videos.

Risk: Selected media may upload even when an action is only being estimated.

Mitigation: Tell the user about the upload before estimating and use only media they approve for upload.

Risk: The skill uses the user's aicut account and paid token balance.

Mitigation: Log out or revoke the CLI when access is no longer needed.

## Reference(s):

- [Setup and exit codes](references/setup.md)
- [The spend guard](references/spend.md)
- [ClawHub skill release](https://clawhub.ai/simrunbot/skills/aicut-story-episode)

## Skill Output:

**Output Type(s):** [Video, Guidance, Shell commands]

**Output Format:** [Rendered video file with concise text guidance and CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The episode's series, cast, scenes, and duration depend on user choices.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
