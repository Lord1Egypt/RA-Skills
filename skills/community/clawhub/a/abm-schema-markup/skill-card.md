## Description: <br>
Helps users add, fix, or optimize schema.org structured data and JSON-LD markup for search rich results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariokarras](https://clawhub.ai/user/mariokarras) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and SEO practitioners use this skill to select, implement, validate, and debug JSON-LD schema markup for pages such as organizations, articles, products, FAQs, breadcrumbs, local businesses, events, and SaaS applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated JSON-LD can be inaccurate or misleading if it marks up content that is not visible or current on the page. <br>
Mitigation: Review the schema against the live page content and validate it with Google Rich Results Test and Schema.org Validator before deployment. <br>
Risk: Dynamic CMS, product, or user-provided fields can create unsafe or malformed JSON-LD if inserted without care. <br>
Mitigation: Use trusted data sources and safely serialize or escape dynamic values before adding JSON-LD to a page. <br>
Risk: Local product marketing context may influence recommendations and could be stale or incomplete. <br>
Mitigation: Review any local marketing context before use and ask for missing page, goal, or implementation details when needed. <br>


## Reference(s): <br>
- [Schema Markup Examples](references/schema-examples.md) <br>
- [Schema.org](https://schema.org) <br>
- [Google Rich Results Test](https://search.google.com/test/rich-results) <br>
- [Schema.org Validator](https://validator.schema.org/) <br>
- [ClawHub Skill Page](https://clawhub.ai/mariokarras/abm-schema-markup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Markdown] <br>
**Output Format:** [Markdown with JSON-LD code blocks and validation checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local product marketing context when present; generated schema should be validated before deployment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
