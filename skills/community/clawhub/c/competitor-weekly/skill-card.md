## Description:

经确认后生成主品与已授权竞品的证据周报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers use this skill to create an evidence-based weekly comparison of a primary product and authorized competitors after reviewing the quote and confirming paid work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The approval-first weekly-report description conflicts with instructions that can allow account-level automatic credit spending and broader recurring monitoring.

Mitigation: Prefer a corrected report-only package that requires acceptance of the current total price. If using this version, disable account auto-confirmation, explicitly request manual collection, and review recurring schedules.

Risk: Authorization saves a reusable ARI API key locally.

Mitigation: Authorize only on a trusted device, keep the key out of reports and shared logs, and revoke it if exposed.

## Reference(s):

- [Competitor weekly workflow](references/operation-workflow.md)
- [ARI API reference](references/reference.md)
- [ARI operations](https://ari.funewa.com/zh/operations)
- [ARI product management](https://ari.funewa.com/zh/products)
- [ARI monitoring center](https://ari.funewa.com/zh/monitor)
- [ARI reports](https://ari.funewa.com/zh/reports)
- [ARI billing](https://ari.funewa.com/zh/billing)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown evidence report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Compares the primary product with authorized competitors using available product, snapshot, and review evidence; states data scope and limitations when relevant.]

## Skill Version(s):

1.5.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
