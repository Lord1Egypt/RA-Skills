## Description:

Daily briefing of startups and funds that just raised private money, built from new SEC Form D filings. Use when the user wants a funded-startup radar, alerts on new fund launches, or a daily/weekly digest of companies raising under Regulation D (Rule 506(b), 506(c), 504). Runs the magnova/sec-form-d-monitor Actor through the Apify plugin for OpenClaw; each filing record costs $0.01 on the user's own Apify account, empty days are free.

This skill is ready for commercial/non-commercial use.

## Publisher:

[memeanalyst](https://clawhub.ai/user/memeanalyst)

### License/Terms of Use:

MIT-0

## Use Case:

People tracking private fundraising can use this skill to receive a daily or weekly summary of new Regulation D filings, with filters for amount, state, industry, and exemption. It presents public filings as filed and is not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan could not resolve a referenced state file, so its contents were not assessed.

Mitigation: Review the referenced state file and confirm it is appropriate before installing or running the skill.

Risk: Actor runs bill the user's Apify account at $0.01 per filing record delivered.

Mitigation: Set result limits and review expected per-record charges before each run; the documented 200-record cap costs up to $2.00.

## Reference(s):

- [Apify SEC Form D Monitor Actor](https://apify.com/magnova/sec-form-d-monitor)
- [ClawHub skill release](https://clawhub.ai/memeanalyst/skills/daily-funded-startup-radar)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown briefing with filing details and source links, plus setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranks matching filings by amount sold and includes up to 15 entries. Amounts and filing details are reported as returned by the data source.]

## Skill Version(s):

1.0.0 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
