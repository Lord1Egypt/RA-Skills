## Description:

Converts user-provided files and URLs, including documents, images, audio, web pages, and archives, into Markdown using Microsoft MarkItDown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sipingme](https://clawhub.ai/user/sipingme)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert user-provided local files or URLs into Markdown for downstream LLM analysis and content processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires approving installation of an unpinned third-party Python package with broad optional dependencies.

Mitigation: Install only after review in a controlled environment, and pin or mirror dependencies where release governance requires reproducibility.

Risk: Converting remote URLs or YouTube links sends network requests to user-provided destinations.

Mitigation: Convert only URLs the user intentionally provides and apply local network egress controls for sensitive environments.

Risk: Optional OpenAI/API or plugin features can send image or other content to external services when enabled.

Mitigation: Enable API-backed and plugin features only for content approved for that processing path, and keep them disabled for local-only conversion.

## Reference(s):

- [All to Markdown on ClawHub](https://clawhub.ai/sipingme/skills/all-to-markdown)
- [sipingme publisher profile](https://clawhub.ai/user/sipingme)
- [Microsoft MarkItDown](https://github.com/microsoft/markitdown)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files]

**Output Format:** [Markdown emitted to stdout or written to a Markdown file when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the markitdown CLI; remote URL conversion uses network access, and optional OpenAI/API or plugin features require explicit enablement.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter/config list 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
