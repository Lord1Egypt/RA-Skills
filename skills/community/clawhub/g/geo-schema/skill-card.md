## Description:

Schema.org structured data audit and generation optimized for AI discoverability: detect, validate, and generate JSON-LD markup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SEO practitioners, and site maintainers use this skill to audit structured data on web pages, identify missing or weak Schema.org markup, and generate ready-to-use JSON-LD recommendations for AI discoverability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches external URLs and could be used on internal, staging, or otherwise unapproved targets.

Mitigation: Use only public or explicitly approved URLs, restrict allowed schemes and destinations, and block internal or staging hosts before execution.

Risk: The documented URL-fetching workflow uses a shell command pattern that may be unsafe if URLs are not handled strictly as data.

Mitigation: Quote and pass URLs as data arguments, validate URL schemes and destinations, and avoid command construction that can interpret URL content as shell syntax.

Risk: sameAs audits may resolve external profile links beyond the initially approved target site.

Mitigation: Resolve external profile links only after user approval and keep the allowed destination set explicit.

## Reference(s):

- [Schema.org full type hierarchy](https://schema.org/docs/full.html)
- [Schema.org](https://schema.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown report with JSON-LD code blocks and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces GEO-SCHEMA-REPORT.md with detected schemas, validation results, missing schema recommendations, sameAs audit results, generated JSON-LD, and implementation notes.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
