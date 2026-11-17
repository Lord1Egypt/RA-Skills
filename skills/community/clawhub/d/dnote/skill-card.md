## Description:

Dnote helps agents save, retrieve, and manage a personal knowledge base through the Dnote CLI, including adding notes, searching content, viewing books and notes, editing, removing, exporting, and syncing notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m1n-74316d65](https://clawhub.ai/user/m1n-74316d65)

### License/Terms of Use:


## Use Case:

Developers, operators, and other external users use this skill to capture command references, code snippets, troubleshooting notes, and task context in Dnote, then retrieve or export those notes for later agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance includes a pipe-to-shell command.

Mitigation: Prefer Homebrew or a pinned, verified Dnote release before installing.

Risk: Notes and configuration may contain secrets or sensitive local information.

Mitigation: Avoid storing secrets in notes and review any config output before sharing it with an agent session.

Risk: Wrapper commands can delete notes or books with limited guardrails.

Mitigation: Require explicit user confirmation before running delete commands.

Risk: Sync can upload local notes to the Dnote service.

Mitigation: Run sync only after the user confirms remote upload is acceptable.

## Reference(s):

- [Dnote CLI Documentation](https://www.getdnote.com/docs/cli/)
- [Dnote CLI Installation](https://www.getdnote.com/docs/cli/installation/)
- [ClawHub Skill Page](https://clawhub.ai/m1n-74316d65/skills/dnote)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional Dnote CLI text or JSON output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Dnote CLI; may read or write the local Dnote database and can optionally sync notes with the Dnote service.]

## Skill Version(s):

1.0.0 (source: evidence release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
