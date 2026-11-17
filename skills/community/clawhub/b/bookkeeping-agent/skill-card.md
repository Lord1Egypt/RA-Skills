## Description:

Helps an agent import bill attachments or local bookkeeping files, check duplicates, query transactions, view summaries, record individual income or expenses, manage budgets, and launch the local bookkeeping dashboard through the local bookkeeping CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lastarla](https://clawhub.ai/user/lastarla)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route personal bookkeeping requests to a local CLI for bill import, duplicate checks, transaction lookup, summaries, single-entry recording, budget checks, and dashboard startup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes local bill attachments and updates a local financial database.

Mitigation: Install only when the user trusts the local bookkeeping CLI and review imported files before allowing mutations.

Risk: Reset, re-import, and batch attachment processing can change or remove financial records at larger scope.

Mitigation: Require explicit confirmation for database reset, reset followed by re-import, and multi-attachment batch processing.

Risk: Attachment files may be misidentified when inbound filenames do not preserve CSV or XLSX extensions.

Mitigation: Use original attachment names or MIME metadata for type checks and ask the user to choose when multiple candidate bill files exist.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lastarla/skills/bookkeeping-agent)
- [Bookkeeping Agent Repository](https://github.com/lastarla/bookkeeping-agent)
- [Bookkeeping Tool Repository](https://github.com/lastarla/bookkeeping-tool.git)
- [Install](references/install.md)
- [Quickstart](references/quickstart.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with CLI-backed JSON result summaries when available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the local bookkeeping command on PATH; supported bill attachment inputs are CSV and XLSX.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
