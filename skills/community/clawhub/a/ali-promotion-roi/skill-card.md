## Description:

Analyze Alibaba International promotion ROI by comparing promotion spend with completed orders, revenue, CPO, and promotion-type performance from pre-loaded MySQL data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloudcode-hans](https://clawhub.ai/user/cloudcode-hans)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business operators use this skill to generate Alibaba International promotion ROI reports, compare standard and sitewide promotion performance, and audit differences between promotion-reported orders and completed orders. It reads existing sql-linker-cli/MySQL data and does not ingest source spreadsheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically approves database credential access for sql-linker-cli.

Mitigation: Use a database account limited to SELECT on alibaba_intl_orders and alibaba_intl_promotion_daily, and review or remove automatic credential approval before installation.

Risk: The skill depends on a hard-coded DBBridge import path.

Mitigation: Verify that the configured sql-linker-cli path points to a trusted, non-writable dependency location.

Risk: ROI reports and JSON output can expose sensitive business performance and order data.

Mitigation: Treat generated reports as sensitive business data and restrict where outputs are stored or shared.

## Reference(s):

- [ROI metrics reference](references/metrics.md)
- [Alibaba ROI table schema](references/schema.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Console text reports or JSON with summary, by-type, and by-date ROI sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports month filtering, USD/CNY exchange-rate override, promotion-type view, daily view, and JSON output.]

## Skill Version(s):

1.0.2 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
