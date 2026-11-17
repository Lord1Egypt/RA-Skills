## Description:

Reads a single 24h.chichbong.com product page and drafts a compact Vietnamese Zalo Shop listing block with a short intro, marked-up suggested price, safer title, and thumbnail link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiktqd](https://clawhub.ai/user/haiktqd)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and ecommerce operators use this skill to convert one public 24h.chichbong.com product URL into concise Vietnamese Zalo Shop listing content. It helps extract visible product facts, rewrite sensitive claims into safer commerce language, calculate a suggested marked-up selling price, and return the product thumbnail when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested selling prices intentionally mark up the source price by 30% to 50%, which may be unsuitable without business review.

Mitigation: Review generated prices before commercial use and adjust them against current pricing, margin, and marketplace requirements.

Risk: Product details or images may be incomplete when the product page cannot be opened or verified from a trusted same-domain fallback.

Mitigation: Use only visible page or same-domain snippet facts, mark unverifiable fields plainly, and avoid fabricating missing product information.

Risk: Original product pages may contain medical, exaggerated, or ad-sensitive terms that are risky for ecommerce listings.

Mitigation: Rewrite titles and descriptions with neutral, factual benefit language and avoid high-risk claims called out by the skill.

## Reference(s):

- [Style Notes](references/style-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-like Vietnamese text with four fixed sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a short intro, suggested price, rewritten title, and thumbnail URL; uses explicit unavailable-field notices when details cannot be verified.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
