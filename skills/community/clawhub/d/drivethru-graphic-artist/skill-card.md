## Description:

Creates reviewed garment mockups, cleans up flat artwork, and prepares DTF decoration files for production.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmtucker](https://clawhub.ai/user/zmtucker)

### License/Terms of Use:

MIT-0

## Use Case:

Design and merchandising teams use this skill to place artwork on product photos, review mockups, restore degraded flat art, and prepare DTF files and decoration records for printing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled jobs and production workflows can change storefront images and decoration records.

Mitigation: Run only where catalog edits are authorized, with tightly scoped Odoo credentials; review proposed changes and job outcomes.

Risk: The web-image routine fetches external image URLs without URL validation.

Mitigation: Restrict outbound network access and avoid unattended web-image runs until URL validation or an egress allowlist is in place.

Risk: Independent mockup review sends images to a configured vision provider.

Mitigation: Choose the provider deliberately and confirm that image sharing is permitted before enabling review.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zmtucker/skills/drivethru-graphic-artist)
- [Decoration specifications](references/decoration_spec.md)
- [Production-ready workflow](references/production_ready.md)
- [Web-image routine](references/web_image_routine.md)
- [rembg background-removal project](https://github.com/danielgatis/rembg)

## Skill Output:

**Output Type(s):** [PNG image files, JSON receipts, Guidance]

**Output Format:** [PNG mockups and production artwork, JSON job results, and brief text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Production artwork is sized for its print location at 300 DPI; mockups require review before delivery.]

## Skill Version(s):

0.18.1 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
