## Description:

Integrates agent workflows with Didit Transaction Monitoring for transaction risk screening, crypto wallet checks, Travel Rule exchanges, and monitoring rule management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to integrate transaction monitoring into backend systems and manage risk rules through Didit's API. It also supports crypto wallet screening and Travel Rule workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan flags that withdrawal guidance may allow a transfer before review is approved; scan coverage is partial, so behavior is not fully assessed.

Mitigation: Review the withdrawal approval steps before use. Confirm that transfers require an APPROVED transaction and completed checks, and verify the destination and data sent to the external service.

## Reference(s):

- [Didit Documentation](https://docs.didit.me)
- [Transaction Monitoring API Reference](https://docs.didit.me/management-api/transactions/create)
- [Transaction Monitoring Overview](https://docs.didit.me/transaction-monitoring/overview)
- [Rules API Guide](https://docs.didit.me/transaction-monitoring/rules-api)
- [Travel Rule Guide](https://docs.didit.me/transaction-monitoring/travel-rule)
- [Wallet Screening Guide](https://docs.didit.me/transaction-monitoring/wallet-screening)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Python and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes API request examples and a Python transaction submission helper.]

## Skill Version(s):

1.2.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
