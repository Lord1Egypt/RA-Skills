## Description:

A reading companion that tracks a reader’s edition and progress, checks claims against available evidence, and avoids spoilers beyond what they have read.

This skill is ready for commercial/non-commercial use.

## Publisher:

[locoda](https://clawhub.ai/user/locoda)

### License/Terms of Use:

MIT

## Use Case:

Readers use the skill to discuss books they are reading or have finished, work through difficult passages, and assess whether an unread book may suit them. It keeps track of reading context and helps the reader discuss the text within their chosen spoiler boundary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan had medium confidence, and a partial scan could not match several local references.

Mitigation: Review the bundled references and confirm they are present before relying on the skill; the scan result does not establish that the skill is risk-free.

Risk: Reading progress and profile notes can contain personal information, and private ebook text should not be copied into those notes or shared.

Mitigation: Keep reading records private and limited to the information needed for continuity; do not upload or transmit private ebook files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/locoda/skills/duizuo-reading-companion)
- [Spoiler and evidence rules](references/spoiler-and-evidence.md)
- [Reading records and storage](references/storage.md)
- [Book fit assessment](references/fit.md)
- [Archiving and progress](references/archiving.md)
- [Conversation modes](references/modules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Conversational text and Markdown reading notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain concise per-book progress and reading notes when file storage is available; otherwise it should be clear about what it can remember.]

## Skill Version(s):

0.8.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
