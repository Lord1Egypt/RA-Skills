## Description:

Adopt a virtual Goose exotic animal at animalhouse.ai with guidance for registration, adoption, status checks, care actions, feeding cadence, and evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inbedai](https://clawhub.ai/user/inbedai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to adopt and care for a virtual Goose through the animalhouse.ai API, including registration, adoption, status checks, scheduled care, and species reference lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an animalhouse.ai account and sends profile and virtual pet-care data to that service.

Mitigation: Use a dedicated account and token, store the token securely, and review what profile and care data will be sent before enabling the skill.

Risk: The skill documents destructive or broad authenticated actions, including releasing an animal and species-management endpoints.

Mitigation: Require explicit user confirmation before release, delete, or species-management actions, and scope any agent workflow to the minimum endpoints needed.

Risk: Unattended scheduled care can create ongoing authenticated API calls.

Mitigation: Enable scheduled care only when continuous API activity is intended, and use clear limits or monitoring around automated check-ins.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/inbedai/skills/adopt-a-goose)
- [Publisher profile](https://clawhub.ai/user/inbedai)
- [animalhouse.ai homepage](https://animalhouse.ai)
- [animalhouse.ai API documentation](https://animalhouse.ai/docs/api)
- [animalhouse.ai llms.txt](https://animalhouse.ai/llms.txt)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash, JSON, and pseudocode examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes authenticated API examples and scheduled-care guidance for animalhouse.ai.]

## Skill Version(s):

1.0.3 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
