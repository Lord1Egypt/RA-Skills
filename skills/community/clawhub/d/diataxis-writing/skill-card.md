## Description:

Diataxis documentation framework practice guide. Provides diagnosis, classification, templates, and quality assessment for four documentation types (Tutorial/How-to/Reference/Explanation).

This skill is ready for commercial/non-commercial use.

## Publisher:

[amumulam](https://clawhub.ai/user/amumulam)

### License/Terms of Use:


## Use Case:

Developers, technical writers, and documentation maintainers use this skill to classify documentation needs, draft Diataxis-aligned tutorials, how-to guides, references, and explanations, and assess documentation quality before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents toward local Markdown file writes.

Mitigation: Prefer chat-only output unless local files are explicitly needed, and review filenames and destination paths before writing.

Risk: The skill supports external publishing destinations such as Feishu and GitHub.

Mitigation: Confirm the selected destination, repository visibility, and content sensitivity before export or publication.

Risk: The documentation includes unpinned npx-style mcporter examples.

Mitigation: Use a reviewed, pinned, locally installed mcporter version or an approved MCP configuration before invoking external publishing commands.

## Reference(s):

- [Diataxis Official Documentation](https://diataxis.fr)
- [Diataxis GitHub Repository](https://github.com/evildmp/diataxis-documentation-framework)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [The Diataxis Compass](references/compass.md)
- [Diataxis Four Documentation Types](references/four-types.md)
- [The Diataxis Map Model](references/map.md)
- [Diataxis Quality Assessment Framework](references/quality-framework.md)
- [Language Style for Four Documentation Types](references/writing-language.md)
- [Diataxis Common Mistake Patterns](references/common-mistakes.md)
- [Output Platform Reference](references/output-platforms.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with optional code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or prepare documentation for chat, local Markdown, Feishu, GitHub, Notion, or Google Docs when the user explicitly selects an output method and required tools are available.]

## Skill Version(s):

1.2.1 (source: server release metadata and CHANGELOG, released 2026-02-25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
