## Description:

智能自动记账 helps an agent parse natural-language income and expense notes, store local SQLite bookkeeping records, query or delete entries, and generate monthly HTML reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal finance operators use this skill to record expenses or income with short natural-language prompts, review monthly activity, search records, and generate local spending reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-controlled text may be passed through shell command invocation.

Mitigation: Avoid shell-string invocation for user text and pass user input through structured arguments or a reviewed parser boundary.

Risk: Financial records can be deleted without a required confirmation step.

Mitigation: Require explicit user confirmation before deleting records and show the target record before execution.

Risk: Financial records and generated reports may expose sensitive personal finance data.

Mitigation: Require confirmation before exposing records or reports and keep generated files local unless the user explicitly requests sharing.

Risk: Referenced helper scripts are not included in the artifact for audit.

Mitigation: Provide and review the parser, bookkeeper, and reporter scripts before routine use.

Risk: Broad bookkeeping trigger phrases may activate the skill in ambiguous contexts.

Mitigation: Narrow activation triggers or ask for clarification before recording, deleting, or displaying financial data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/auto-bookkeeping)
- [Publisher profile](https://clawhub.ai/user/bettermen)
- [Skill artifact](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Files]

**Output Format:** [Markdown-style agent responses with JSON snippets, shell commands, and generated HTML report file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Python runtime and stores bookkeeping data in a local SQLite database.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
