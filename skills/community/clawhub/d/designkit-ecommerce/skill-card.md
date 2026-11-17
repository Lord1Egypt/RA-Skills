## Description:

Routes ecommerce image requests to Designkit workflows for background removal, transparent or white backgrounds, blurry photo restoration, and listing image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaorenaishu](https://clawhub.ai/user/xiaorenaishu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn product or marketing images into ecommerce-ready assets, including cutouts, clearer photos, and listing image sets with guided input collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports a shell runner code-injection flaw.

Mitigation: Review before installing and prefer the pinned ClawHub install path for this release.

Risk: Image inputs are sent to Designkit/OpenClaw API and upload destinations are not tightly constrained.

Mitigation: Use only non-sensitive images and avoid endpoint override variables unless the destination is controlled.

Risk: The skill depends on DESIGNKIT_OPENCLAW_AK for API access.

Mitigation: Set the access key only in a constrained environment and keep request logging disabled unless needed.

## Reference(s):

- [Designkit OpenClaw](https://www.designkit.com/openClaw)
- [ClawHub skill page](https://clawhub.ai/xiaorenaishu/skills/designkit-ecommerce)
- [ClawHub publisher profile](https://clawhub.ai/user/xiaorenaishu)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown responses with image links, user-facing guidance, runner JSON status, and downloaded image files when rendering succeeds.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DESIGNKIT_OPENCLAW_AK. Local or URL images may be uploaded to Designkit/OpenClaw to complete the requested image-processing task.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 1.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
