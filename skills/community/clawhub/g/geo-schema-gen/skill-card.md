## Description:

Generate complete, validated Schema.org JSON-LD markup for common page and content types, including Organization, FAQPage, Article, Product, HowTo, BreadcrumbList, WebSite, VideoObject, ImageObject, and LocalBusiness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geoly-geo](https://clawhub.ai/user/geoly-geo)

### License/Terms of Use:


## Use Case:

Developers, SEO practitioners, and content teams use this skill to generate and validate Schema.org JSON-LD for webpages, rich results, and AI-readable content attribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL and sitemap generation features fetch arbitrary web pages.

Mitigation: Use the URL and sitemap features only with trusted links, and review fetched content before using generated markup.

Risk: Generated HTML script tags may be unsafe if pasted directly into a live site.

Mitigation: Review and sanitize generated JSON-LD or script-tag output before deployment, especially for script-tag breakout characters.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/geoly-geo/skills/geo-schema-gen)
- [Schema.org](https://schema.org)
- [Schema.org Validator](https://validator.schema.org)
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [JSON-LD Playground](https://json-ld.org/playground/)
- [Schema.org Types Reference](references/schema-types.md)
- [Schema Field Reference](references/field-reference.md)
- [Google Rich Results Guidelines](references/google-guidelines.md)
- [Schema Examples by Industry](references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [JSON-LD, JSON, HTML script tags, or Markdown with validation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch generation may write schema JSON files and a summary JSON file.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
