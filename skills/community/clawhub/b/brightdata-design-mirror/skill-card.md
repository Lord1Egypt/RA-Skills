## Description:

Replicate a public website's visual style and apply its colors, typography, spacing, layout rhythm, and component treatment to an existing frontend codebase.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meirk-brd](https://clawhub.ai/user/meirk-brd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and frontend engineers use this skill to capture a public reference site's design language, convert it into a design token map, and apply those visual choices to an existing application while preserving functionality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send reference URLs and fetched page content to Bright Data.

Mitigation: Use it only with public reference sites, and avoid private dashboards, localhost, intranet sites, authenticated pages, and confidential customer or prototype URLs.

Risk: The capture scripts disable TLS certificate verification with curl -k.

Mitigation: Remove curl -k before operational use so HTTPS certificate validation remains enabled.

Risk: The scripts construct JSON request bodies through shell string interpolation.

Mitigation: Validate that target URLs are public HTTPS URLs and construct request JSON with a proper encoder before using untrusted input.

## Reference(s):

- [Design Mirror Skill Page](https://clawhub.ai/meirk-brd/skills/brightdata-design-mirror)
- [Apply Guide](references/apply-guide.md)
- [Capture Guide](references/capture-guide.md)
- [CSS Extraction Playbook](references/css-extraction.md)
- [Bright Data Control Panel](https://brightdata.com/cp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with design token maps, shell commands, and code or configuration edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate screenshots and scraped HTML files during capture, then propose or apply frontend style changes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
