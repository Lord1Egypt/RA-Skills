## Description:

Amazon Listing Optimization helps sellers create keyword-optimized Amazon listings, audit existing listings, identify keyword gaps, benchmark competitors, and generate revised listing copy across supported Amazon marketplaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phheng](https://clawhub.ai/user/phheng)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and marketplace operators use this skill to create new Amazon listings from product details, keywords, and competitor ASINs, or to audit and optimize existing listings for keyword coverage, SEO quality, and conversion-oriented copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation command uses an unpinned global package install path.

Mitigation: Install only from a trusted source and prefer a pinned installer version or reviewed commit before deployment.

Risk: ASINs, product-page URLs, and listing requests may be sent to Amazon or web search/fetch tools.

Mitigation: Avoid using the skill with confidential launch plans or sensitive product strategy unless that exposure is acceptable.

Risk: Generated listing copy, SEO scores, and marketplace recommendations may be inaccurate or unsuitable for a seller's policy obligations.

Mitigation: Review all generated copy and recommendations before pasting them into Seller Central or making listing changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phheng/skills/amazon-listing-optimization)
- [Amazon keyword research companion skill](https://github.com/nexscope-ai/Amazon-Skills/tree/main/amazon-keyword-research)
- [Nexscope suite](https://github.com/nexscope-ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with ready-to-use listing copy, audit tables, keyword coverage reports, and optional bash command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include titles, bullet points, descriptions, backend search terms, before-and-after copy, scoring tables, and marketplace-language-specific recommendations.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
