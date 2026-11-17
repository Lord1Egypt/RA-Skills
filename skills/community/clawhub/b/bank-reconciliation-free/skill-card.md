## Description:

把银行流水和企业账面记录逐笔配对，列出未达账项、重复记录和两侧合计差异，并保留原文日期与金额供复核。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External finance, bookkeeping, and operations users use this skill to reconcile pasted bank statement lines against book entries, find unmatched items, identify duplicate same-date same-amount records, and review count and amount totals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may over-rely on reconciliation output as accounting, tax, legal, or audit advice.

Mitigation: Review results manually and treat the skill as a reconciliation aid only; it does not make accounting entries or provide professional advice.

Risk: The skill processes bank and bookkeeping records supplied by the user.

Mitigation: Install and use it only when comfortable pasting those records into a local tool; security evidence shows no network access, credential use, persistence, or data mutation.

Risk: The free version has a fixed scope and may miss issues outside exact amount/date matching, unmatched-item lists, duplicate detection, and totals comparison.

Mitigation: Verify findings against source records and use separate review for unsupported cases such as near matches, cross-period matches, reconciliation identity checks, and custom tolerances.

Risk: The skill does not verify statement authenticity or connect to bank or accounting systems.

Mitigation: Confirm source documents, balances, and required accounting treatment independently before taking action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/bank-reconciliation-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown or plain text with optional JSON output and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided bank and book records; no network access, credential use, persistence, or data mutation is shown in the security evidence.]

## Skill Version(s):

1.0.72 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
