## Description:

A Chinese-language algae feeding calculator that parses daily hatchery reports and produces per-pool feeding volumes for small and large algae across supported pool sizes, strains, days, and morning or afternoon periods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheney87](https://clawhub.ai/user/cheney87)

### License/Terms of Use:

MIT-0

## Use Case:

External hatchery operators and aquaculture staff use this skill to convert algae feeding daily-report text into grouped feeding instructions with liters per pool and algae-type totals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect parsing or calculation could produce feeding amounts that do not match the farm standard.

Mitigation: Review calculated outputs against the algae feeding standard before operational use.

Risk: Untrusted or oversized daily-report text may trigger weak input-validation behavior.

Mitigation: Use bounded, trusted report text and add pool-number bounds and validation before broader operational deployment.

## Reference(s):

- [Algae Feeding Standard](references/algae-feeding-standard.md)
- [Daily Report Parsing Guide](references/parsing-guide.md)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text feeding calculation report in Chinese]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Groups results by algae type, workshop, and pool range; includes liters per pool and total liters where supported.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
