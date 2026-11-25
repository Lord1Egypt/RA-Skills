## Description:

Generates images with Alibaba Bailian Qwen Image 2 Pro, with support for detailed scenes and text-rich layouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use the skill to generate images from text prompts, including designs with detailed scenes and rendered text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and local reference images are sent to dLazy's hosted services for generation.

Mitigation: Submit only prompts and images approved for processing by the hosted service.

Risk: The security scan has medium confidence and is partial; it observed a login command that does not demonstrate the advertised image-generation purpose and did not establish the CLI's internal behavior.

Mitigation: Review the linked CLI and package before installing, and confirm its login behavior matches your expectations.

Risk: The dLazy API key is saved in the local CLI configuration when using the login flow.

Mitigation: Protect the local configuration and rotate or revoke the key if it is exposed.

## Reference(s):

- [dLazy CLI source link (listed in skill metadata)](https://github.com/dlazy-ai/cli)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service website](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Images, JSON]

**Output Format:** [JSON response with generated image URLs and task status for asynchronous jobs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image size is configurable; up to three reference images are accepted, and generation can run asynchronously.]

## Skill Version(s):

1.3.44 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
