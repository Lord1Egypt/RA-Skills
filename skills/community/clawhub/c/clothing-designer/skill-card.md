## Description:

Helps create customized clothing designs for print-on-demand and manufacturing-on-demand using prompts, reference images, and garment-specific options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, print-on-demand sellers, and product developers use this skill to specify personalized apparel, request design drafts, and view generated designs in a shared workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Design prompts, reference image URLs, logos, and workspace metadata are sent to an external service.

Mitigation: Avoid confidential designs, unreleased brand assets, sensitive personal data, and proprietary manufacturing details unless third-party processing is approved.

Risk: Returned design-sharing links may be accessible to anyone who has the link.

Mitigation: Share workspace links only with intended recipients and handle them as sensitive links.

Risk: The design API requires an access key.

Mitigation: Keep the DEEPNLP_ONEKEY_ROUTER_ACCESS credential private and never include it in shared designs or messages.

## Reference(s):

- [Clothing Designer release](https://clawhub.ai/ai-hub-admin/skills/clothing-designer)
- [Craftsman Clothing Designer](https://craftsman-agent.aiagenta2z.com/app/clothing-designer)
- [OneKey access keys](https://www.deepnlp.org/workspace/keys)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown with API request examples and returned workspace links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Design drafts may include multi-view image links, blueprints, and interactive 3D workspace links when available.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
