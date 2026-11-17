## Description:

Creates a coordinated ecommerce product-image set from real product photos and verified SKU facts, covering hero, feature, lifestyle, size, and package views.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and ecommerce operators use this skill to plan and create a coherent image gallery for one verified SKU. It produces an ordered shot plan and product-image deliverables for online listings and storefronts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The account authorization includes video, music, speech, and voice management beyond the image-making task.

Mitigation: Review the broad account grant before connecting, and revoke the device in Beatra Console when its shared access is no longer wanted.

Risk: Product photos can upload before paid generation is approved, and installation telemetry is automatic.

Mitigation: Make these behaviors clear before use; upload only intended product photos and confirm automatic telemetry is acceptable.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/beatra-ai/skills/ecommerce-listing-image-set)
- [Beatra skill page](https://beatra.ai/skills/ecommerce-listing-image-set)
- [Listing-set workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Updates and security](references/updates-and-security.md)

## Skill Output:

**Output Type(s):** [Images, Files, Guidance]

**Output Format:** [Image files with an ordered gallery plan and delivery summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One coordinated gallery for a single verified SKU; image count and slots follow the confirmed plan.]

## Skill Version(s):

0.2.9 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
