## Description: <br>
Match and normalize product listings across Indian ecommerce catalogs with variant-aware rules, confidence scoring, false-match prevention, and review queues for ambiguous pairs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anugotta](https://clawhub.ai/user/anugotta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Catalog, marketplace, and ecommerce teams use this skill to normalize Indian ecommerce listings, match equivalent products across stores, and route ambiguous pairs for review before using matches in price comparison or catalog operations. <br>

### Deployment Geography for Use: <br>
India <br>

## Known Risks and Mitigations: <br>
Risk: Automatic SKU matches can be wrong when catalog data is incomplete, ambiguous, or missing variant fields. <br>
Mitigation: Validate thresholds against labeled category data, route medium-confidence pairs to manual review, and monitor false-positive rates before production use. <br>
Risk: Published homepage metadata appears to reference a different price-tracker page. <br>
Mitigation: Confirm the metadata link before using it as product, support, or provenance documentation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anugotta/catalog-sku-matcher-india) <br>
- [Matching rules](matching-rules.md) <br>
- [Confidence scoring guide](scoring-guide.md) <br>
- [Setup guide](setup.md) <br>
- [Validation checklist](validation-checklist.md) <br>
- [Edge-case examples](examples.md) <br>
- [Metadata homepage](https://clawhub.ai/Michael-laffin/price-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with structured match decisions, confidence levels, reason codes, and review queue entries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces canonical SKU candidates, matched listings, rejected candidates, and manual review entries; no code execution or credential use indicated.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
