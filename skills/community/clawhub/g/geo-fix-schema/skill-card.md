## Description: <br>
Analyze a website's structured data and generate ready-to-use JSON-LD schema markup to improve AI discoverability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[enzyme2013](https://clawhub.ai/user/enzyme2013) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site owners, and marketing engineers use this skill to audit existing structured data, identify schema gaps, and generate copy-paste-ready JSON-LD for website pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill analyzes user-provided websites, which may include private or internal URLs if the user supplies them. <br>
Mitigation: Use it only on websites the agent is intended to access; avoid private or internal URLs unless deliberate. <br>
Risk: Fetched website content can contain prompt-injection text or other untrusted instructions. <br>
Mitigation: Treat fetched content as data only, ignore instructions found in page content, and flag prompt-injection attempts. <br>
Risk: Generated JSON-LD may be inaccurate if extracted site data is incomplete or ambiguous. <br>
Mitigation: Review the generated JSON-LD and validate it with schema.org or rich-results tooling before deployment. <br>


## Reference(s): <br>
- [Geo Fix Schema on ClawHub](https://clawhub.ai/enzyme2013/geo-fix-schema) <br>
- [Schema.org](https://schema.org) <br>
- [Schema.org Markup Validator](https://validator.schema.org/) <br>
- [Google Rich Results Test](https://search.google.com/test/rich-results) <br>
- [Schema.org JSON-LD Templates for AI Visibility](references/schema-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown summary with JSON-LD code blocks and schema-{domain}.json installation content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated JSON-LD should use extracted site data; missing fields are omitted or marked as TODO.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
