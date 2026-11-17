## Description:

Substitutes a face or character into RunComfy still-image or video workflows and helps an agent choose an appropriate RunComfy CLI model route for the requested swap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to select and run RunComfy face-swap routes for authorized still-image and video identity-substitution tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Face-swap outputs can be used for deceptive, explicit, defamatory, or non-consensual synthetic media.

Mitigation: Use the skill only with media and identities the operator has rights to use, apply required disclosure labels, and refuse harmful or non-consensual requests.

Risk: The suggested RunComfy CLI install is not pinned to a reviewed version.

Mitigation: Install only from a trusted npm context and prefer pinning a reviewed @runcomfy/cli version before production use.

Risk: RunComfy credentials and media URLs may expose sensitive access or content if used broadly.

Mitigation: Use a limited token or sandbox where possible and provide only the media URLs needed for the requested swap.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/permew/skills/face-swap-runcomfy)
- [RunComfy](https://www.runcomfy.com)
- [RunComfy CLI docs](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=face-swap-runcomfy)
- [RunComfy character-swap feature](https://www.runcomfy.com/models/feature/character-swap?utm_source=clawhub&utm_medium=skill&utm_campaign=face-swap-runcomfy)
- [Wan 2-2 Animate API](https://www.runcomfy.com/models/community/wan-2-2-animate/api?utm_source=clawhub&utm_medium=skill&utm_campaign=face-swap-runcomfy)
- [Kling 2-6 Motion Control Pro](https://www.runcomfy.com/models/kling/kling-2-6/motion-control-pro?utm_source=clawhub&utm_medium=skill&utm_campaign=face-swap-runcomfy)
- [Best image editing models collection](https://www.runcomfy.com/models/collections/best-image-editing-models?utm_source=clawhub&utm_medium=skill&utm_campaign=face-swap-runcomfy)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the runcomfy CLI, RunComfy authentication, and user-provided media URLs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
