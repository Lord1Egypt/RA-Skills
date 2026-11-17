## Description:

A family ledger skill for recording, querying, summarizing, and deleting household expense entries through natural-language requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nimil](https://clawhub.ai/user/nimil)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage a local household expense ledger from an agent interface, including adding expenses, listing records, summarizing spending, deleting entries, and viewing household roles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad command-execution permissions can allow unintended shell commands if installed without review.

Mitigation: Review or narrow the execution rules before installation and restrict command execution to structured invocations of ledger.py.

Risk: The skill can delete ledger records by ID.

Mitigation: Require confirmation before deletion and keep a backup of ledger.db when records matter.

Risk: Natural-language inputs are converted into command arguments for local expense operations.

Mitigation: Validate role, amount, date, count, and note fields before execution and avoid shell-string templates.

Risk: The local ledger can contain household financial information.

Mitigation: Keep ledger.db local, limit filesystem access to trusted users, and avoid syncing or sharing the database unless intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nimil/skills/family-ledgersimple)
- [Agent Skills specification](https://agentskills.io/specification)
- [Claude Code](https://claude.ai/code)
- [OpenClaw](https://openclaw.ai)
- [Hermes Agent](https://hermes-agent.nousresearch.com)
- [Codex](https://openai.com/codex)
- [Gemini CLI](https://ai.google.dev/gemini-api/docs)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Markdown]

**Output Format:** [Natural-language response with CLI command execution and plain-text ledger tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local ledger operations for add, list, summary, delete, and roles commands backed by a SQLite database.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
