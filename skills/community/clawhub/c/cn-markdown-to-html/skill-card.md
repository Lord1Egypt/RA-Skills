## Description:

Convert Markdown to HTML with basic styling for headers, bold, italic, links, and code blocks using the Python standard library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content maintainers use this skill to convert local Markdown files into complete HTML documents for lightweight publishing or preview workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML may be unsafe when Markdown content is untrusted or served from a trusted browser origin.

Mitigation: Add HTML escaping, URL validation, and sanitization before using converted output in a website or trusted browser context.

Risk: The converter is basic and may produce incomplete or low-quality HTML for Markdown outside its supported subset.

Mitigation: Review converted output and limit use to supported Markdown elements unless the script is extended and tested.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/freedompixels/skills/cn-markdown-to-html)
- [Publisher profile](https://clawhub.ai/user/freedompixels)

## Skill Output:

**Output Type(s):** [HTML, Shell commands, Guidance]

**Output Format:** [HTML document emitted from a local Python command, with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pure Python standard library implementation; no API key required.]

## Skill Version(s):

1.1.1 (source: ClawHub release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
