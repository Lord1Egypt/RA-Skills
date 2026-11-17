## Description:

Create, convert, and download AI-generated 3D models using Neural4D APIs. Optimized for commercial pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[6e6e6e](https://clawhub.ai/user/6e6e6e)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide text-to-3D, image-to-3D, and 3D format conversion workflows with Neural4D APIs, especially when generated assets need downloadable model files or manufacturing-oriented export formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill sends prompts and uploaded images to Neural4D and may consume API points.

Mitigation: Confirm point costs and remaining balance before bulk runs, and only submit prompts or images approved for the external Neural4D service.

Risk: The skill uses a bearer token and downloads generated model files from an external service.

Mitigation: Protect the NEURAL4D_API_TOKEN, avoid exposing it in logs or shared files, and store downloaded assets in a project directory for review before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/6e6e6e/skills/ai-3d-generation)
- [Neural4D API base endpoint](https://alb.neural4d.com:3000/api)
- [Neural4D text-to-3D endpoint](https://alb.neural4d.com:3000/api/generateModelWithText)
- [Neural4D format conversion endpoint](https://alb.neural4d.com:3000/api/convertToFormat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include API endpoints, bearer-token configuration, asynchronous polling steps, point-cost checks, and download handling for generated model files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
