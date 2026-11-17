## Description:

Creates a visual garment preview by applying the material, texture, sheen, and drape shown in a fabric swatch to a garment reference image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Fashion designers, apparel product teams, and ecommerce creators can preview how a garment design may look in different fabrics before making physical samples. The result is a visual preview, not a physical sample or a guarantee of fabric hand-feel or weight.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided garment and fabric images may be sent to an external image service, and the security scan was partial.

Mitigation: Before use, confirm which provider receives the images and review its privacy and retention practices. Use confidential designs only with approval, and review files not covered by the partial scan.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/fabric-on-body)
- [model-flags.md](artifact/references/model-flags.md)
- [provider-cli.md](artifact/references/provider-cli.md)
- [dLazy](https://dlazy.com)

## Skill Output:

**Output Type(s):** [Images, Guidance]

**Output Format:** [Generated image files, typically JPEG; PNG and WebP are also supported]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Visual previews only; they do not establish physical fabric hand-feel or weight.]

## Skill Version(s):

1.0.33 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
