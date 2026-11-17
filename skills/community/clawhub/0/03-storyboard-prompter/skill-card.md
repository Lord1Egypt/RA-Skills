## Description:

Converts short drama scene data into AI art storyboard prompt entries with consistent vertical cinematic styling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ghwyever](https://clawhub.ai/user/ghwyever)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to convert short drama scene arrays into consistent storyboard prompts for downstream AI image generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scene text is transformed directly into prompt strings, so inaccurate or sensitive input can carry into downstream image-generation prompts.

Mitigation: Review input scenes and generated shot_list entries before using them with an image-generation system.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ghwyever/skills/03-storyboard-prompter)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON object containing a shot_list array of storyboard prompt entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each shot_list entry includes shot_id, prompt, and duration when duration is supplied.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
