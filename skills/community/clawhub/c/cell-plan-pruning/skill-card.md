## Description:

Use when reviewing, downgrading, or comparing mobile phone plans and bills — family plans, multiline waste, per-line data reality vs bucket size, add-on insurance, autopay/paperless discounts, or switching carriers / MVNOs. Audits the bill line-by-line and computes annual savings of pruning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT-0

## Use Case:

Consumers reviewing an individual or family mobile bill use this skill to classify recurring plan charges, compare per-line data use with plan tiers, assess device protection, and estimate annual savings from plan changes. It also guides users through coverage, device-lock, installment, and number-porting checks before they decide on a carrier switch.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: A recommendation to drop a cloud storage add-on may overlook stored data, available replacement capacity, backup migration, or the provider's retention terms.

Mitigation: Before cancelling cloud storage, check actual usage, replacement capacity, backup migration, and retention terms; approve each account change separately.

Risk: Estimated savings or plan recommendations may not account for current coverage, hotspot limits, device locks, installment balances, or expiring promotional credits.

Mitigation: Verify current plan terms and coverage, check unlock and payoff requirements, and include lost credits and switching costs before deciding; have the new carrier initiate a number port.

## Reference(s):

- [MVNO Reference — US Market Map & Porting Mechanics](references/mvno-guide.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text]

**Output Format:** [Markdown summary with line-item classifications, comparisons, and estimated annual savings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Estimates depend on the bill, usage, and plan assumptions provided; verify current carrier pricing and terms before acting.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
