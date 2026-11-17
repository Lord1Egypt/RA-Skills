## Description:

Coordinates Fuxin Office tasks across Word, Excel, and PowerPoint, including document editing, read-only questions, and multi-step workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foxitnet](https://clawhub.ai/user/foxitnet)

### License/Terms of Use:

MIT-0

## Use Case:

Office users can ask an agent to draft and revise Word documents, analyze Excel sheets, prepare presentations, answer questions about open documents, and coordinate tasks across applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can modify the active Word, Excel, or PowerPoint document.

Mitigation: Install only if local document access is intended; check the active document and review edits before saving.

Risk: Saving document changes is not covered by ordinary undo.

Mitigation: Require user confirmation before saving; use the available undo guidance for ordinary edits.

## Reference(s):

- [Fuxin Office skill on ClawHub](https://clawhub.ai/foxitnet/skills/fuxin-office)
- [Connection and preflight reference](artifact/reference/bridge.md)
- [Document question-answering reference](artifact/reference/doc-qa.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese-language progress updates and results summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can also modify open Office documents through the local Fuxin Office bridge.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
