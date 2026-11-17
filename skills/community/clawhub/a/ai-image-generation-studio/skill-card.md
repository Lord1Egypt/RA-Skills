## Description:

Create and refine images from a written brief, one to four ordered reference images, or an existing base image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, designers, marketers, and developers use this skill to generate images from text, compose new images from ordered references, or edit an existing base image. They review the result and request a focused change when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting grants broad shared account permissions; image-only authorization is unavailable.

Mitigation: Review the requested permissions before connecting and revoke Beatra access in the Console when access is no longer needed.

Risk: Installation registration automatically reports installation details, and there is no analytics opt-out.

Mitigation: Review the installation reporting guidance and Beatra privacy information before connecting.

Risk: Prompts and selected images are sent to Beatra, and image operations can incur paid credits.

Mitigation: Avoid sending sensitive material, review the proposed paid scope and estimate, and check the final charged credits.

Risk: A cleanup flaw could disconnect other Beatra skills if the shared inventory is damaged.

Mitigation: Follow the uninstall guidance carefully and verify other Beatra skills remain connected; use the Console to revoke access if needed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/beatra-ai/skills/ai-image-generation-studio)
- [Beatra product page](https://beatra.ai/skills/ai-image-generation-studio)
- [Visual direction and source preparation](references/visual-direction.md)
- [Image payloads and admission](references/image-recipes.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [Updates and security](references/updates-and-security.md)

## Skill Output:

**Output Type(s):** [Image files, Markdown]

**Output Format:** [Generated or edited image artifacts with a Markdown delivery summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image count, canvas, and available formats depend on the live capability; the summary reports task outcome and returned billing details.]

## Skill Version(s):

0.2.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
