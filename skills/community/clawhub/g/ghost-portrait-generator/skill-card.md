## Description:

Generate haunting ghost portraits and inner demon shadow photos from text prompts using the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create ghost portrait, gothic horror, Halloween, and spectral apparition images from prompts, with optional size selection and reference image input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts and a user-provided Neta API token to an external image generation service.

Mitigation: Use a revocable token and avoid submitting sensitive personal, proprietary, or confidential details in prompts.

Risk: Examples pass the token on the command line, where it may be captured in shell history or process logs.

Mitigation: Handle tokens cautiously, rotate them if exposed, and prefer safer secret handling when adapting the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/blammectrappora/skills/ghost-portrait-generator)
- [Neta AI Token Access](https://www.neta.art/open/)
- [Neta Image Generation API](https://api.talesofai.com/v3/make_image)

## Skill Output:

**Output Type(s):** [Text, Shell commands]

**Output Format:** [Plain text URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a direct image URL after polling the image generation task; requires a Neta API token.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
