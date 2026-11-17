## Description:

Parse bank statements, store transactions locally, and answer personal spending questions from a JSON transaction history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[safaiyeh](https://clawhub.ai/user/safaiyeh)

### License/Terms of Use:

MIT

## Use Case:

Developers and personal finance users use this skill with an OpenClaw agent to extract transactions from uploaded statements, maintain a local transaction store, and query spending by category, merchant, or date range.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive bank statements and transaction history are stored locally in the OpenClaw workspace without strong local protection described in the release evidence.

Mitigation: Use the skill only on trusted machines, restrict permissions on ~/.openclaw/workspace/finance, and avoid retaining raw statements unless needed.

Risk: Parsed or manual transaction imports can update financial records without clear confirmation controls.

Mitigation: Review extracted transaction counts, categories, and totals against the statement before importing transactions or accepting manual entries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/safaiyeh/skills/finance-skill)
- [Publisher profile](https://clawhub.ai/user/safaiyeh)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown or plain text responses with JSON transaction objects and bash commands when importing or querying data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include spending summaries, filtered transaction lists, and commands that read or update the local finance workspace.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
