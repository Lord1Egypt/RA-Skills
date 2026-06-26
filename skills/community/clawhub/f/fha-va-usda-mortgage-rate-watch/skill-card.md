## Description: <br>
Daily FHA, VA, and USDA government-backed mortgage rate monitoring, comparison, and newsletter-style summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[li-chi](https://clawhub.ai/user/li-chi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External homebuyers, mortgage shoppers, and agents use this skill to gather public FHA, VA, and USDA rate snapshots, compare government-backed loan options, estimate principal-and-interest payments, and prepare newsletter-style summaries. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: Public mortgage-rate summaries may lag real-time lender pricing or omit borrower-specific factors. <br>
Mitigation: Verify current rates with cited public sources or a licensed lender before relying on the output. <br>
Risk: Rate comparisons and payment estimates could be mistaken for personalized mortgage advice. <br>
Mitigation: Treat outputs as educational, avoid guaranteeing rates or approval, and consult a licensed mortgage professional for decisions. <br>
Risk: Scheduled alerts may run recurring checks and store last-known rate data locally. <br>
Mitigation: Enable scheduling and local state only after reviewing the cadence and storage path. <br>


## Reference(s): <br>
- [Loan Program Quick Reference](references/loan-programs.md) <br>
- [Newsletter Template](references/newsletter-template.md) <br>
- [Freddie Mac Primary Mortgage Market Survey](https://www.freddiemac.com/pmms) <br>
- [HUD FHA Program Information](https://www.hud.gov) <br>
- [VA Home Loans](https://www.va.gov/housing-assistance/home-loans) <br>
- [USDA Rural Development](https://www.rd.usda.gov) <br>
- [ClawHub Skill Page](https://clawhub.ai/li-chi/fha-va-usda-mortgage-rate-watch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries, comparison tables, newsletter drafts, and optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May cite public rate sources; payment estimates are informational and depend on the loan amount, rate, and term used.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
