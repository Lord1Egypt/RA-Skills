## Description:

Monitors daily FHA, VA, and USDA government-backed mortgage rates, compares program trends, calculates payment impact, and drafts newsletter-style summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[li-chi](https://clawhub.ai/user/li-chi)

### License/Terms of Use:

MIT-0

## Use Case:

External users, mortgage researchers, and content teams use this skill to track public FHA, VA, and USDA mortgage-rate information, compare program options, estimate payment impact, and prepare educational rate-watch summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mortgage-rate summaries can be mistaken for financial advice or guaranteed lender pricing.

Mitigation: Present outputs as educational information, include disclaimers, and direct users to verify current rates and eligibility with official sources or a licensed mortgage professional.

Risk: Recurring cron alerts may create local scheduled checks that users forget to remove.

Mitigation: Only configure recurring alerts when explicitly requested, explain the local scheduling behavior, and include how to remove or disable the cron entry.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/li-chi/skills/fha-va-usda-mortgage-rate-watch)
- [Publisher Profile](https://clawhub.ai/user/li-chi)
- [Government-Backed Loan Programs](references/loan-programs.md)
- [Weekly Rate Watch Newsletter Template](references/newsletter-template.md)
- [Freddie Mac PMMS](https://freddiemac.com/pmms)
- [Mortgage News Daily](https://mortgagenewsdaily.com)
- [Bankrate Mortgage Rates](https://bankrate.com/mortgages)
- [NerdWallet Mortgage Rates](https://nerdwallet.com/mortgages/mortgage-rates)
- [HUD FHA](https://hud.gov)
- [VA Home Loans](https://va.gov/housing-assistance/home-loans)
- [USDA Rural Development](https://rd.usda.gov)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, comparison tables, calculator output, and optional cron setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include source attribution and educational disclaimers; rate data may lag real-time lender pricing.]

## Skill Version(s):

1.4.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
