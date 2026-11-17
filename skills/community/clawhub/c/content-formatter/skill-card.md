## Description:

Formats Markdown content for target publishing platforms using Markdown passthrough, generic HTML, platform-specific HTML, or plain-text conversion strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Content publishers and developers use this skill to convert a source Markdown draft into platform-appropriate HTML, Markdown, or text before publishing across supported channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The --content-file option reads the file path provided by the caller and can return that content in formatted output.

Mitigation: Only pass paths for documents intended to be formatted and shared with the agent workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/content-formatter)
- [Business rules](references/business_rules.md)
- [Error codes](references/error_codes.md)
- [Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code]

**Output Format:** [JSON containing formatted HTML, Markdown, or plain text plus status fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes format_used and layer fields; some text outputs may be platform-length constrained.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
