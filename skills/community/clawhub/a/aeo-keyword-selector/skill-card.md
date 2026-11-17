## Description:

Selects a single question-format AEO blog keyword from a business topic by checking sitemap coverage, page intent, cannibalization risk, and Semrush validation signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coreydomidocs-droid](https://clawhub.ai/user/coreydomidocs-droid)

### License/Terms of Use:

MIT-0

## Use Case:

Content, SEO, and agent workflow users use this skill before article drafting to decide whether a business topic should become a new URL, be expanded into an existing page, or be rejected. It is especially aimed at SaaS, ecommerce, and service-brand keyword qualification where avoiding cannibalization matters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled sitemap parser can recursively fetch arbitrary URLs without same-origin, private-network, redirect, or response-size limits.

Mitigation: Use only trusted HTTPS sitemaps from known domains, and constrain sitemap inputs before running the parser.

Risk: Keyword decisions may introduce misleading SEO guidance or duplicate page intent if the evidence review is incomplete.

Mitigation: Review the sitemap, fetched page intent, Semrush validation, and final decision before handing a keyword to a writing workflow.

## Reference(s):

- [DomiDocs profile](references/domidocs-profile.md)
- [Semrush playbook](references/semrush-playbook.md)
- [Verdict rubric](references/verdict-rubric.md)
- [DomiDocs sitemap](https://domidocs.com/sitemap_index.xml)
- [ClawHub skill page](https://clawhub.ai/coreydomidocs-droid/skills/aeo-keyword-selector)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text decision block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns exactly one final decision with selected_keyword, business_topic, best_existing_url_match, cannibalization_risk, decision, and reasoning.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
