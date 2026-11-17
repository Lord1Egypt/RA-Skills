## Description:

Faq Forge helps agents build, maintain, import, and publish customer FAQ documentation as static HTML, Markdown, or plain text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support teams, and content operators use this skill to create and maintain customer-facing FAQ knowledge bases, import existing Markdown or JSON FAQ content, and publish searchable static documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can execute untrusted FAQ content if imported Markdown or JSON is published without sanitization.

Mitigation: Review imported content and escape or sanitize FAQ fields before publishing, especially when hosting output on the same domain as authenticated business applications.

Risk: Delete, import, template apply, and export operations can overwrite or alter local FAQ data.

Mitigation: Keep backups and review changes before publishing or replacing the FAQ database.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/faq-forge)
- [Publisher profile](https://clawhub.ai/user/theshadowrose)
- [README](artifact/README.md)
- [Quick Start](artifact/QUICKSTART.md)
- [Limitations](artifact/LIMITATIONS.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and generated FAQ files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local JSON FAQ data and static HTML, Markdown, or plain text FAQ outputs through the bundled scripts.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
