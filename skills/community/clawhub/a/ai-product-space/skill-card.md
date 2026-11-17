## Description:

Openclaw Skill connects an agent to AI Product Space to generate ecommerce product images, posters, marketing copy, and short showcase videos from a product photo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[corinbtc](https://clawhub.ai/user/corinbtc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and ecommerce teams use this skill to turn a product photo into marketplace-ready visual assets, marketing copy, workspace status summaries, and product showcase video links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad account access may grant more authority than needed for asset generation.

Mitigation: Verify the OAuth grant before use and prefer a version with narrow OAuth scopes.

Risk: Local file paths and image URLs can expose unintended content if supplied carelessly.

Mitigation: Provide only trusted product image paths or URLs, and avoid private, untrusted, or oversized URL fetches.

Risk: The skill depends on a trusted AI Product Space API endpoint.

Mitigation: Confirm the configured API origin before authorization or upload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/corinbtc/skills/ai-product-space)
- [Publisher profile](https://clawhub.ai/user/corinbtc)
- [AI Product Space homepage](https://renshevy.com)
- [Repository link from package metadata](https://github.com/renshevy/ai-product-space)
- [Support link from package metadata](https://github.com/renshevy/ai-product-space/issues)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown and plain text summaries with generated asset links and inline image references.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include workspace IDs, progress summaries, generated image URLs, video URLs, marketing copy, and user-facing error messages.]

## Skill Version(s):

1.0.4 (source: server release metadata, package.json, claw.json, clawhub.json, CHANGELOG released 2026-03-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
