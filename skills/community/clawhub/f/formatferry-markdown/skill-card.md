## Description:

Converts local documents or stdin to Markdown in platform-specific formats, with optional server-side URL extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[britrik](https://clawhub.ai/user/britrik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use the skill to convert documents and web content into Markdown tailored to their target platform.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL extraction sends the URL and API key to the FormatFerry API for server-side fetching.

Mitigation: Use URL mode only with the user's agreement, and avoid internal, private, or signed URLs.

Risk: A stored license key can trigger an entitlement check with the license service during local conversion.

Mitigation: Use --offline for local conversions when you want to skip the entitlement check.

Risk: The benign security verdict has limited assurance because one scanner's review was partial.

Mitigation: Treat the verdict as a summary of completed checks, not a guarantee of zero risk.

## Reference(s):

- [FormatFerry project homepage](https://github.com/britrik/FormatFerry)
- [ClawHub skill release](https://clawhub.ai/britrik/skills/formatferry-markdown)
- [FormatFerry CLI reference](artifact/references/cli-reference.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands]

**Output Format:** [Markdown text in the selected flavor, with optional CLI command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Converts supported local inputs or stdin; output flavor can be selected.]

## Skill Version(s):

1.1.6 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
