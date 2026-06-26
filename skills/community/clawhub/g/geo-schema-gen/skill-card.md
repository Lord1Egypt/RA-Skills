## Description: <br>
Generate complete, validated Schema.org JSON-LD markup for common content types including Organization, FAQPage, Article, BlogPosting, Product, HowTo, BreadcrumbList, WebSite, VideoObject, ImageObject, and LocalBusiness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geoly-geo](https://clawhub.ai/user/geoly-geo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, marketers, and site operators use this skill to generate and validate Schema.org JSON-LD for webpages, product pages, FAQs, articles, and sitemap batches before publishing structured data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URL and sitemap modes can process external content and should be limited to sites the user controls or trusts. <br>
Mitigation: Use URL and sitemap inputs only for public sites you control or trust, and review generated structured data before publishing it. <br>
Risk: File input and output paths can read or write local JSON artifacts chosen by the user. <br>
Mitigation: Use file input only on JSON files you intend to process, and choose the output directory deliberately. <br>
Risk: Generated structured data may be incomplete, stale, or inconsistent with visible page content. <br>
Mitigation: Validate generated JSON-LD with Schema.org and rich-results tooling, then confirm that all fields accurately match the target page before deployment. <br>


## Reference(s): <br>
- [Schema Type Reference](references/schema-types.md) <br>
- [Field Reference](references/field-reference.md) <br>
- [Google Guidelines](references/google-guidelines.md) <br>
- [Examples by Industry](references/examples.md) <br>
- [Schema.org](https://schema.org) <br>
- [Schema.org Validator](https://validator.schema.org) <br>
- [Google Rich Results Test](https://search.google.com/test/rich-results) <br>
- [JSON-LD Playground](https://json-ld.org/playground/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON-LD, JSON, HTML script tags, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local JSON schema files and validation reports when the bundled scripts are used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
