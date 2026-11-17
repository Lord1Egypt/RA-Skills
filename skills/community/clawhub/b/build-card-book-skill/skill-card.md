## Description:

Transforms a book or topic into a single-file HTML, page-flipping card book using bundled JSON-to-HTML templates, a generator script, and a checker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-acheng](https://clawhub.ai/user/ai-acheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-producing agents use this skill to turn structured book or topic notes into a responsive, browser-openable HTML card book with cover, usage page, index, topic cards, and back cover.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated pages can include unsafe injected browser content when untrusted JSON is used.

Mitigation: Use only controlled and reviewed JSON inputs, and do not publish generated HTML under a trusted web origin until the attribute-escaping issue identified by ClawHub security evidence is fixed.

Risk: The bundled templates use Chinese-only text, a default promotional back cover, browser localStorage for display preferences, and a remote Unsplash cover image request.

Mitigation: Review generated pages before distribution, adjust public-facing copy and defaults for the target audience, and confirm that the optional remote image request is acceptable for the deployment context.

## Reference(s):

- [Prompt Reference](references/prompt.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON input structure, Python shell commands, and generated single-file HTML artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated HTML is intended for local browser use and includes inline CSS and JavaScript, with an optional remote hero image in the bundled templates.]

## Skill Version(s):

0.2.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
