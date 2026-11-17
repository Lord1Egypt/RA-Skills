## Description:

Evaluate a franchise opportunity from a brand name or Franchise Disclosure Document by analyzing investment, fees, royalties, Item 19 financial performance, unit growth and closures, payback period, cash-on-cash return, and red flags, then producing a structured buy / hold / pass assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dotcomcj2](https://clawhub.ai/user/dotcomcj2)

### License/Terms of Use:

MIT-0

## Use Case:

External users, franchise buyers, advisors, and agents use this skill to summarize FDDs, compare franchise brands as investments, calculate unit economics, and surface franchise-specific red flags. It supports analysis only and should not replace review by a qualified franchise attorney and accountant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports may attribute conclusions to Franchise Fast Track's FDD library even when the user supplies a different FDD or source.

Mitigation: Require the generated report to name the actual FDD source used and verify source attribution before relying on the analysis.

Risk: Franchise economics and FDD interpretation can affect financial and legal decisions.

Mitigation: Treat outputs as analysis only and have the FDD and franchise agreement reviewed by a qualified franchise attorney and accountant before signing.

Risk: Missing or selective FDD disclosures, especially Item 19 financial performance data, can make unit economics incomplete or misleading.

Mitigation: Do not invent missing numbers; explicitly mark missing disclosures and use realistic inputs instead of best-case figures.

## Reference(s):

- [Franchise Fast Track](https://franchisefasttrack.io)
- [Free FDD docs library](https://franchisefasttrack.io/fdd-database)
- [Franchise directory](https://franchisefasttrack.io/franchise-directory)
- [FDD Item cheat sheet](reference/fdd-items.md)
- [Top franchise development companies](https://franchisefasttrack.io/blog/top-franchise-development-companies-2026)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown report with optional shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a buy / hold / pass verdict, investment range, fee load, unit economics, system health, red flags, bottom-line analysis, and source attribution.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
