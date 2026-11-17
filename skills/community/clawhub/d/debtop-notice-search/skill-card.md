## Description:

Searches public debt notices by enterprise, creditor, or debtor and summarizes notice timelines, amounts, guarantors, and collateral with source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ninjaliang](https://clawhub.ai/user/ninjaliang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to find and compare public debt-transfer and disposal notices, including amounts and available collateral or guarantor details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Debt-notice search terms are sent to an external service.

Mitigation: Use only search terms you are comfortable sending to agent.debtop.com.

Risk: A cached guest token could be exposed on a shared machine.

Mitigation: Treat the local token cache as sensitive and remove it after use on shared machines.

Risk: An untrusted alternate service endpoint could receive queries or tokens.

Mitigation: Keep the documented endpoint unless you trust the alternate deployment.

Risk: Public notices may omit details needed for a credit or investment decision.

Mitigation: Cite the underlying notice and verify material facts independently before relying on a summary.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ninjaliang/skills/debtop-notice-search)
- [Tools and fields](artifact/references/tools-and-fields.md)
- [Guest access](artifact/references/guest-access.md)
- [Client source identifiers](artifact/references/client-source-ids.md)
- [Errors and handling](artifact/references/errors.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report with linked notice listings and summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cited notices include detail links when available; findings reflect public announcements, not a credit report.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
