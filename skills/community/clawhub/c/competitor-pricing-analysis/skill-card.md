## Description:

Scores user-verified competitor prices against weighted criteria to show US SaaS and ecommerce teams how their own pricing compares.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US SaaS and ecommerce pricing owners, founders, revenue managers, and analysts use this skill to compare verified competitor prices with their own plan, understand relative positioning, and identify terms to confirm before repricing. Keep comparisons internal unless they have been reviewed for external publication.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The optional Windows application is unsigned and was not inspected.

Mitigation: The bundled Python workflow is sufficient; only download or run the optional application after independently assessing and accepting that trust risk.

Risk: The script overwrites ranking.md in its output folder.

Mitigation: Use a dedicated output folder to avoid replacing other work.

Risk: Unreviewed scoring assumptions can produce misleading rankings or repricing guidance.

Mitigation: Verify criteria, weights, and ranking direction before relying on results or changing prices.

## Reference(s):

- [Pricing comparison guidance](references/pricing-comparison.md)
- [Publisher homepage (Clawdis metadata)](https://github.com/rapidworker1)
- [ClawHub release page](https://clawhub.ai/rapidworker1/skills/competitor-pricing-analysis)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown pricing comparison with ranked scores, price details, positioning notes, and decision gaps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-verified, date-stamped prices and stated scoring criteria; review assumptions and terms before repricing.]

## Skill Version(s):

1.0.7 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
