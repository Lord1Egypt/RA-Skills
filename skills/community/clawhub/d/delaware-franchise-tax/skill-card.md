## Description:

File Delaware annual franchise tax and annual reports with guided tax calculation, eCorp portal filing steps, and payment handoff support for Delaware C-Corps, LLCs, LPs, and GPs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu)

### License/Terms of Use:

MIT-0

## Use Case:

External users with Delaware-formed entities use this skill to collect filing inputs, compare Delaware franchise tax calculation methods, navigate the official eCorp filing flow, preserve confirmation records, and set annual filing reminders.

### Deployment Geography for Use:

United States (Delaware franchise tax filings)

## Known Risks and Mitigations:

Risk: The skill may involve sensitive Delaware entity details, officer and director information, share counts, and asset figures.

Mitigation: Share only the information needed for the filing task, keep records in user-controlled storage, and review all populated values before submission.

Risk: Incorrect or outdated filing rules, tax calculations, deadlines, or payment thresholds could lead to filing errors.

Mitigation: Verify current requirements against official Delaware Division of Corporations sources and consult a tax professional for entity-specific tax advice.

Risk: Browser automation could populate portal fields incorrectly or expose payment workflows to the agent.

Mitigation: Use automation only with user opt-in, have the user confirm every filing field, and require the user to enter banking or card details directly.

Risk: Deceptive solicitations or non-official payment channels could mislead users during the filing process.

Mitigation: Use the official Delaware eCorp portal and verify suspicious notices through the Delaware Division of Corporations or the registered agent.

## Reference(s):

- [Delaware Franchise Tax Calculation Reference](reference/tax-calculation.md)
- [Delaware Franchise Tax Filing Instructions](reference/filing-instructions.md)
- [Delaware Franchise Tax FAQ](reference/faq.md)
- [Delaware eCorp Portal Playwright Automation Notes](reference/ecorp-portal-playwright-notes.md)
- [Delaware Division of Corporations Franchise Tax](https://corp.delaware.gov/paytaxes/)
- [Delaware Franchise Tax Calculator Reference](https://corp.delaware.gov/frtaxcalc/)
- [Delaware eCorp Tax Portal](https://icis.corp.delaware.gov/ecorp/logintax.aspx)
- [ClawHub Skill Page](https://clawhub.ai/stevenobiajulu/skills/delaware-franchise-tax)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with step-by-step instructions, tax calculation summaries, and optional shell or Playwright code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided entity details, stock information, gross assets, officer and director data, and portal confirmations; payment credentials remain user-entered.]

## Skill Version(s):

0.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
