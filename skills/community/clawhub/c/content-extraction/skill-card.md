## Description:

OpenClaw-native executable content extraction skill for URLs, Feishu, YouTube, and web pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halfmoon82](https://clawhub.ai/user/halfmoon82)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to classify URLs or document links, choose an extraction route, and produce clean Markdown content with source metadata, summaries, fallback notes, and optional save paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can route user-supplied URLs and extracted content through OpenClaw web, browser, Feishu, and possible third-party cleanup services.

Mitigation: Use it only where that processing is acceptable, and add confirmation gates or disable third-party fallbacks for private, signed, internal, or sensitive document URLs.

Risk: The skill may save extracted Markdown locally, which can retain sensitive or private content.

Mitigation: Control local retention paths, review saved files, and avoid long-content saves for sensitive sources unless retention is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/halfmoon82/skills/content-extraction)
- [ClawHub publisher profile](https://clawhub.ai/user/halfmoon82)
- [README](artifact/README.md)
- [Executor spec](artifact/notes/executor-spec.md)
- [Block to Markdown mapping](artifact/notes/block-to-markdown.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON route plans, and executable extraction specifications]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include title, author, source, URL, summary, Markdown body, fallback details, and a local save path for long content.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
