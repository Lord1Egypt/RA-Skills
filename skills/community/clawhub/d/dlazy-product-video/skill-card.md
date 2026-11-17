## Description:

Turns product photos, links, specifications, or listings into product showcase and advertising videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers and ecommerce teams use this skill to turn product photos, product information, or marketplace listings into product showcase and advertising videos, with multilingual voiceover and an optional virtual host.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was only partially complete, and some references related to CLI installation were unresolved.

Mitigation: Review the pinned CLI installation details before running it; the skill documents on-demand use with npx @dlazy/cli@1.2.3 as an alternative to a global install.

Risk: Project listing can expose organization project information beyond the stated video-creation task.

Mitigation: Use project listing only when needed and confirm it is appropriate for the organization before accessing project information.

Risk: Prompts and attached files are sent to dLazy services, and attached files are uploaded to its media storage.

Mitigation: Avoid sending confidential material unless approved for the service, and manage the organization API key through the documented login, rotation, and revocation controls.

## Reference(s):

- [Product Video skill release](https://clawhub.ai/dlazyai/skills/dlazy-product-video)
- [dLazy service](https://dlazy.com)
- [dLazy CLI project listed in release metadata](https://github.com/dlazy-ai/cli)
- [dLazy CLI package](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy API key setup](https://dlazy.com/dashboard/organization/api-key)

## Skill Output:

**Output Type(s):** [Video, Text]

**Output Format:** [Product showcase or advertising video with textual status and guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video content varies with the brief; multilingual voiceover and an optional virtual host are supported.]

## Skill Version(s):

1.0.38 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
