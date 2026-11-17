## Description:

Add JSON-LD structured data to a website to improve SEO, qualify pages for richer search result previews, and help LLM crawlers correctly identify and cite the site.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jrrembert](https://clawhub.ai/user/jrrembert)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site maintainers use this skill to add Schema.org JSON-LD to personal sites, blogs, portfolios, and software showcase pages so crawlers can understand page entities and relationships.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated JSON-LD may expose public site metadata, including Person.sameAs profile links or knowledge-graph identifiers.

Mitigation: Review generated JSON-LD before publishing, especially profile links and identifiers that become public metadata.

Risk: The skill may be invoked for broad SEO or site-discoverability requests.

Mitigation: Confirm the target pages, canonical domain, and intended structured data before applying generated markup.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/jrrembert/skills/tree/main/add-json-ld)
- [ClawHub skill page](https://clawhub.ai/jrrembert/skills/add-json-ld)
- [Schema.org vocabulary](https://schema.org)
- [Google structured data documentation](https://developers.google.com/search/docs/appearance/structured-data/search-gallery)
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Schema.org Validator](https://validator.schema.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with JSON-LD and HTML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include page-specific JSON-LD graphs, placement guidance, and validation links.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
