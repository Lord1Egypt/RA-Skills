## Description:

Cross-platform rolling ad-spend cap that blocks overspend across multiple ad platforms combined, not just per-platform daily limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roberthill0475-lang](https://clawhub.ai/user/roberthill0475-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add a shared rolling spend gate before ad purchases across multiple platforms. It is intended to help prevent combined campaign spend from exceeding a configured cap when agents operate on more than one ad platform.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Budget enforcement can allow overspend if live purchases proceed without an atomic reservation or transaction mechanism.

Mitigation: Use an atomic reservation, lock, or transaction before allowing platform purchases, and record spend consistently before releasing the reservation.

Risk: Malformed or unexpectedly missing ledger data can make true ad spend unverifiable.

Mitigation: Fail closed on malformed, unreadable, or unexpectedly missing ledgers, and require operator repair before permitting new spend.

Risk: Invalid monetary inputs can produce incorrect cap or spend decisions.

Mitigation: Validate all cap and spend amounts as finite, non-negative USD values before calling the budget check or updating the cap.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roberthill0475-lang/skills/ad-budget-governor)

## Skill Output:

**Output Type(s):** [Code, Configuration, Guidance]

**Output Format:** [Python module with Markdown usage instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; reads JSON spend ledgers and returns budget status or spend approval decisions.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
