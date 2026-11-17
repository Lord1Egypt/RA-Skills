## Description:

Helps agents add, fix, and optimize schema.org structured data and JSON-LD for search-rich results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariokarras](https://clawhub.ai/user/mariokarras)

### License/Terms of Use:

MIT-0

## Use Case:

External site owners, marketers, and developers use this skill to plan and produce structured data for web pages, including Organization, Article, Product, FAQPage, BreadcrumbList, LocalBusiness, Event, and related schema types. The skill also guides validation with rich-result and schema validators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated React or Next.js JSON-LD can create cross-site scripting risk if dynamic CMS, catalog, seller, or user-controlled values are inserted into script tags without escaping.

Mitigation: Review generated code before production and use a serializer that escapes characters such as '<' before placing dynamic values inside application/ld+json script tags.

## Reference(s):

- [Schema Markup Examples](references/schema-examples.md)
- [Schema.org](https://schema.org)
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Schema.org Validator](https://validator.schema.org/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration instructions]

**Output Format:** [Markdown with JSON-LD code blocks and validation checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include implementation notes for static sites, React or Next.js, CMS platforms, and WordPress.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter metadata.version is 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
