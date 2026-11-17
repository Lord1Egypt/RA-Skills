## Description:

Import, search, and archive AI conversations from ChatGPT, Claude, and Gemini. Clean indexed formats, full-text search, static HTML archive. No server required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use Chat Lift to import exported AI conversations from ChatGPT, Claude, and Gemini, convert them into portable Markdown, HTML, and JSON archives, and search or browse them offline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted archive data can write HTML outside the intended folder or inject content into generated pages.

Mitigation: Use only trusted platform exports and avoid edited or third-party JSON until filename validation and full HTML escaping are fixed.

Risk: Generated archives may expose sensitive chat contents if shared or synced.

Mitigation: Store archives in a private non-synced directory and redact generated web output before publishing.

## Reference(s):

- [Chat Lift ClawHub Page](https://clawhub.ai/theshadowrose/skills/chat-lift)
- [theshadowrose ClawHub Publisher Profile](https://clawhub.ai/user/theshadowrose)
- [README.md](artifact/README.md)
- [LIMITATIONS.md](artifact/LIMITATIONS.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown, HTML, JSON, static web files, configuration examples, and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local archive output is stored under the configured archive directory; review generated web files before sharing.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
