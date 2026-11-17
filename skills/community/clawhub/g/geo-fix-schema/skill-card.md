## Description:

Analyze a website's structured data and generate ready-to-use JSON-LD schema markup to improve AI discoverability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enzyme2013](https://clawhub.ai/user/enzyme2013)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and SEO/GEO practitioners use this skill to audit structured data on public websites, identify schema gaps, and generate copy-paste-ready JSON-LD for improving AI discoverability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated JSON-LD can be inaccurate or incomplete if website extraction misses important context or required fields.

Mitigation: Review the generated markup and validate it with Schema.org or rich-results tooling before adding it to a live site.

Risk: Fetched website content may contain prompt-injection text or other untrusted instructions.

Mitigation: Treat fetched page content only as data to analyze and flag any instruction-like content instead of following it.

Risk: The documented npx installation path can introduce supply-chain risk if the package or source revision is not verified.

Mitigation: Pin or verify the installer and source revision when supported by the user's tooling.

## Reference(s):

- [Schema.org JSON-LD Templates for AI Visibility](references/schema-templates.md)
- [Schema.org](https://schema.org)
- [Schema Markup Validator](https://validator.schema.org/)
- [Google Rich Results Test](https://search.google.com/test/rich-results)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Files, Guidance]

**Output Format:** [Markdown summary with JSON-LD code blocks and a schema-{domain}.json output file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated JSON-LD should use extracted site data, omit or mark unavailable fields, and be reviewed before installation on a live site.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
