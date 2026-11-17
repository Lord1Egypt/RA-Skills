## Description:

Match and normalize product listings across Indian ecommerce catalogs with variant-aware rules, confidence scoring, false-match prevention, and review queues for ambiguous pairs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anugotta](https://clawhub.ai/user/anugotta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and catalog operations teams use this skill to normalize Indian ecommerce listings, compare candidate product pairs, assign confidence decisions, reject unsafe matches, and queue ambiguous pairs for manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: False matches can affect price comparison quality or downstream catalog decisions.

Mitigation: Tune confidence thresholds by category, validate on labeled test sets, and monitor false-positive rates before production use.

Risk: Missing or conflicting variant, bundle, or condition fields can make a pair ambiguous.

Mitigation: Route medium-confidence or incomplete pairs to manual review and require explainable reason codes for rejects.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anugotta/skills/catalog-sku-matcher-india)
- [Publisher profile](https://clawhub.ai/user/anugotta)
- [Artifact metadata homepage](https://clawhub.ai/Michael-laffin/price-tracker)
- [Matching rules](artifact/matching-rules.md)
- [Confidence scoring guide](artifact/scoring-guide.md)
- [Edge-case examples](artifact/examples.md)
- [Setup guide](artifact/setup.md)
- [Validation checklist](artifact/validation-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with structured match, rejection, and manual-review entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes canonical SKU candidates, matched listings with confidence levels, rejected candidates with reason codes, and manual review queue entries.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
