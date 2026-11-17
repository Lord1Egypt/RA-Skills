## Description:

Use when a client needs to estimate China individual income tax on overseas brokerage or bank statements, prepare documents for the tax bureau, or offset annual stock gains and losses from local agent chats such as WorkBuddy or 豆包 Work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[masterbenc](https://clawhub.ai/user/masterbenc)

### License/Terms of Use:

MIT-0

## Use Case:

External tax preparers, local agent users, and clients use this skill to estimate China individual income tax exposure from overseas brokerage or bank statements and prepare a concise, reviewable document package for the tax bureau. It supports local statement parsing, FIFO cost matching, annual gain/loss offsetting, and plain-language follow-up questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive brokerage or bank statements and CLI JSON output can contain names, full account identifiers, addresses, holdings, balances, and transactions.

Mitigation: Process only local, redacted copies of the minimum statements needed; handle generated JSON, estimates, and reports as sensitive financial records.

Risk: The tax estimate may be unreliable for mixed years, mixed currencies, partial records, non-HTSC brokers, or bank statements.

Mitigation: Require manual tax review before relying on the number for formal filing or payment decisions, and clearly mark assumptions and unsupported inputs.

Risk: Missing buy records can cause sold positions to be excluded from the estimate.

Mitigation: List unmatched sales and missing statements in the output so reviewers can collect records before treating the estimate as complete.

## Reference(s):

- [小白问询话术](references/interview.md)
- [成本匹配](references/matching.md)
- [测算口径](references/tax-estimate.md)
- [税局材料建议](references/documents.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, local JSON extraction output, and concise client-facing tax estimate text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should identify assumptions, unmatched sales, missing documents, and the need for human review before formal filing.]

## Skill Version(s):

3.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
