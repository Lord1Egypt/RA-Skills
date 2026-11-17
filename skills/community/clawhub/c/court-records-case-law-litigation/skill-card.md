## Description:

Court records, case law, and litigation search for AI agents that searches US court opinions and case law by keyword via CourtListener for due diligence, legal research, and risk checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colinhughes2121](https://clawhub.ai/user/colinhughes2121)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search US court opinions by keyword, find litigation involving a company or person, and retrieve case-law signals for due diligence, legal research, and risk checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords are sent to GoCreative's API and may include sensitive client, company, or personal information.

Mitigation: Avoid confidential facts, secrets, or unnecessary personal data in lookup terms unless sharing them with the provider is acceptable.

Risk: Each lookup may trigger a small USDC x402 payment.

Mitigation: Review payment behavior and wallet configuration before enabling repeated or automated lookups.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/colinhughes2121/skills/court-records-case-law-litigation)
- [GoCreative case-law lookup API](https://api.gocreativeai.com/v1/lookup/case-law/{keyword})

## Skill Output:

**Output Type(s):** [API Calls, Guidance]

**Output Format:** [Markdown guidance describing HTTPS GET calls and JSON lookup results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lookup keywords are sent to GoCreative's API and may trigger a small USDC x402 payment.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
