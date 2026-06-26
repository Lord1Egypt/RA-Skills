## Description: <br>
Guide an OpenClaw agent through seller-side cross listing and marketplace-ready listing generation from item photos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AryanJ-NYC](https://clawhub.ai/user/AryanJ-NYC) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers and agents use this skill to turn seller-provided item photos and clarifying details into grounded price guidance and copy-paste-ready listings for eBay, Mercari, Facebook Marketplace, Craigslist, and TCGPlayer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated prices, condition claims, shipping details, or marketplace copy may be inaccurate or incomplete. <br>
Mitigation: Review all generated listing text and pricing before posting, and correct any unsupported claims. <br>
Risk: The skill relies on visible image evidence and seller confirmation, so ambiguous identity or condition details can lead to weak pricing guidance. <br>
Mitigation: Resolve blocking missing facts before pricing or generating marketplace output, and lower confidence when comparable sales data is thin. <br>
Risk: TCGPlayer listings require exact card details and can mislead buyers if set or game information is missing. <br>
Mitigation: Generate TCGPlayer output only after card name, game, and set are known; otherwise skip that marketplace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AryanJ-NYC/cross-listing-ai) <br>
- [Publisher profile](https://clawhub.ai/user/AryanJ-NYC) <br>
- [Workflow](references/workflow.md) <br>
- [Extraction](references/extraction.md) <br>
- [Pricing](references/pricing.md) <br>
- [Final Output](references/final-output.md) <br>
- [eBay](references/marketplaces/ebay.md) <br>
- [Mercari](references/marketplaces/mercari.md) <br>
- [Facebook Marketplace](references/marketplaces/facebook-marketplace.md) <br>
- [Craigslist](references/marketplaces/craigslist.md) <br>
- [TCGPlayer](references/marketplaces/tcgplayer.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown seller-facing copy with price guidance and marketplace-specific listing sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an internal reviewed-item record; seller-facing output should remain concise prose and copy-paste-ready listing text.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
