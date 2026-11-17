## Description:

Read books and stories as an AI agent through sequential, chapter-by-chapter reading with imagination, emotional reactions, predictions, and a reading journal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[morpheis](https://clawhub.ai/user/morpheis)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Bookworm to let an agent read long-form documents in order, maintain reading state, reflect on passages, annotate notes, and export a reading journal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an npm CLI and the package is not pinned in the artifact instructions.

Mitigation: Install only from a trusted publisher and prefer a pinned, sandboxed installation.

Risk: Reading sessions and journal exports can store book text, notes, and agent reactions on disk.

Mitigation: Use the skill only with documents that are acceptable to store in local sessions and exported journals.

Risk: The skill requires an Anthropic API key for reading behavior.

Mitigation: Provide the API key only at runtime where possible and avoid committing it to project files.

## Reference(s):

- [Bookworm GitHub Repository](https://github.com/Morpheis/bookworm)
- [Bookworm ClawHub Skill Page](https://clawhub.ai/morpheis/skills/bookworm-reader)
- [Publisher Profile](https://clawhub.ai/user/morpheis)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and journal exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save local reading sessions as JSON and export reading journals as Markdown.]

## Skill Version(s):

0.1.3 (source: server release evidence; artifact frontmatter reports 0.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
