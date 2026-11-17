## Description:

Generate and edit images with Vidu Q2 using text prompts and optional reference images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative users can generate or edit images from text prompts and optional reference images, then receive image URLs or save results locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment is benign with medium confidence and partial analysis; it flags an unexplained login step and a formatting issue in the Chinese guide, and does not establish that the login flow supports the advertised image-generation workflow.

Mitigation: Before installing, review the login and installation details, inspect the padded section of the Chinese guide for concealed text, and verify that the login flow is needed for image generation.

## Reference(s):

- [dLazy service and product information](https://dlazy.com)
- [dLazy CLI homepage listed in metadata (release provenance unavailable)](https://github.com/dlazy-ai/cli)
- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy API key setup](https://dlazy.com/dashboard/organization/api-key)

## Skill Output:

**Output Type(s):** [Images, JSON, Files]

**Output Format:** [JSON result with generated image URLs and task status; optionally saved image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation can run asynchronously; results can be saved locally.]

## Skill Version(s):

1.3.41 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
