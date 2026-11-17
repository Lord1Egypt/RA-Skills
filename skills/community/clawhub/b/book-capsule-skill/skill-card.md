## Description:

Condenses a book, author, or reading theme into a locally generated card-style excerpt article that can be saved as HTML or prepared for publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouq2039-lang](https://clawhub.ai/user/zhouq2039-lang)

### License/Terms of Use:

MIT

## Use Case:

External users and content creators use this skill to turn curated book or author notes into polished Chinese book-excerpt capsule articles. The agent gathers or prepares structured JSON content, runs the bundled local Python generator, and returns an HTML file path for review or publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted JSON or scraped text can be inserted into generated HTML and execute in a browser.

Mitigation: Use trusted content sources, review generated HTML before opening or publishing it, and avoid untrusted text unless the generator is updated to escape or sanitize HTML.

Risk: The skill writes local files and runs its bundled Python generator automatically.

Mitigation: Install and run it only in environments where local file creation and script execution are acceptable, and review generated outputs before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhouq2039-lang/skills/book-capsule-skill)
- [README.md](README.md)
- [template-usage.md](template-usage.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Structured JSON input, generated HTML article file, and concise Markdown delivery note]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated HTML is intended for local browser review and optional publication after content verification.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
