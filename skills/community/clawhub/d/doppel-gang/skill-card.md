## Description:

Review author-written applications, essays, bios, proposals, and important correspondence through explicitly synthetic, contrasting review lenses while preserving the author's voice and final editorial authority.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antreasantoniou](https://clawhub.ai/user/antreasantoniou)

### License/Terms of Use:

MIT

## Use Case:

Writers, applicants, researchers, and developers use this skill to obtain structured critique of author-written drafts through synthetic review lenses while preserving author control over revisions and submission decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command shown in the release is unpinned, so users could install a different future package state than the reviewed evidence.

Mitigation: Install from a pinned release or inspect the repository before running the unpinned command.

Risk: The optional helper emits the full supplied draft in its JSON packet, which can expose sensitive personal or application content if shared or sent to a model provider without authorization.

Mitigation: Use the helper only with drafts approved for local processing and downstream agent handling; keep packets private and review provider boundaries before processing sensitive material.

Risk: Synthetic review lenses can produce mistaken or misleading critique if treated as expert validation or author approval.

Mitigation: Keep outputs labeled as synthetic advice, separate factual questions from taste, and require the author to accept, reject, or defer revisions before any submission.

## Reference(s):

- [Synthetic council method](references/review-method.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with optional JSON review packet output from the local helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The optional helper includes the supplied draft text in its JSON packet; keep generated packets private and handle downstream model review only with authorization.]

## Skill Version(s):

1.0.0 (source: release evidence and CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
