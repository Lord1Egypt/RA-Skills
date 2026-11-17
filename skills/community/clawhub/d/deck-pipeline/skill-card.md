## Description:

Deck Pipeline helps an agent translate Chinese presentation decks into polished English, audit layout integrity, and produce handoff artifacts for review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinadu-ai](https://clawhub.ai/user/tinadu-ai)

### License/Terms of Use:

MIT

## Use Case:

Developers, consultants, and analysts use this skill to process presentation decks through a staged workflow for translation, McKinsey-style English polishing, layout audit, Excel comparison, reverse sync, and session handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Excel audit files can contain active formulas from untrusted deck text.

Mitigation: Open generated XLSX files in protected mode, treat source decks and edit JSON as trusted input, and review generated spreadsheets before using them.

Risk: Processing decks from outside the organization can expose the workflow to untrusted document content.

Mitigation: Review before installing for external deck workflows and install from a verified repository in a virtual environment with pinned dependencies.

Risk: The skill's overflow checks are estimators and cannot render slides directly.

Mitigation: Use PowerPoint or Keynote export to visually verify final decks, especially when many high-risk overflow findings are reported.

## Reference(s):

- [DeckGlobalizer](https://clawhub.ai/tinadu-ai/deckglobalizer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON edit batches, shell commands, and generated PPTX/XLSX/HANDOFF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce translated or polished presentation files, comparison spreadsheets, layout-change spreadsheets, and handoff notes depending on the selected mode.]

## Skill Version(s):

3.0.0 (source: server release metadata; artifact frontmatter and changelog list 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
