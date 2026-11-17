## Description:

Guide an OpenClaw agent through seller-side cross listing and marketplace-ready listing generation from item photos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aryanj-nyc](https://clawhub.ai/user/aryanj-nyc)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and marketplace operators use this skill to turn item photos and seller-confirmed facts into price recommendations and copy-paste-ready listings for eBay, Mercari, Facebook Marketplace, Craigslist, and TCGPlayer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Seller photos and item details may include sensitive personal, location, or transaction information.

Mitigation: Ask only for details needed to identify, condition, price, and list the item; keep the reviewed-item record internal and surface only concise seller-facing summaries.

Risk: Image-based extraction and pricing research can produce incorrect condition, identity, authenticity, or value claims.

Mitigation: Ground facts in visible evidence or seller confirmation, block pricing or final copy when material facts are unresolved, use live sold comps first, and state confidence and uncertainty clearly.

Risk: Maintainer publishing scripts run external tooling when executed.

Mitigation: Do not run publishing scripts during normal skill use; maintainers should run them only in a clean isolated environment with the skills CLI dependency pinned or locked.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aryanj-nyc/skills/cross-listing-ai)
- [Workflow](references/workflow.md)
- [Extraction](references/extraction.md)
- [Pricing](references/pricing.md)
- [Final Output](references/final-output.md)
- [eBay](references/marketplaces/ebay.md)
- [Mercari](references/marketplaces/mercari.md)
- [Facebook Marketplace](references/marketplaces/facebook-marketplace.md)
- [Craigslist](references/marketplaces/craigslist.md)
- [TCGPlayer](references/marketplaces/tcgplayer.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with concise natural-language summaries and marketplace-specific listing sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include price recommendations, expected sale ranges, confidence levels, comp summaries, seller notes, and skipped-marketplace notes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
