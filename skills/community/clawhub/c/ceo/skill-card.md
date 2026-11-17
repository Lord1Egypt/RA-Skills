## Description:

Acts as a CEO advisory skill for company strategy, capital allocation, board and investor management, executive hiring, crisis decisions, and executive communications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External founders, CEOs, and operators use this skill to pressure-test company-level calls and draft board, investor, people, crisis, fundraising, strategy, and shutdown communications. It is advisory: high-impact decisions and outbound materials require human sign-off.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive company context, including financials, board issues, investor or customer names, personnel matters, and legal strategy, may be stored locally in plaintext under ~/Clawic/data/ceo/.

Mitigation: Review the skill before installing, protect or delete local context files after sensitive sessions, and avoid entering information that should not persist locally.

Risk: CEO guidance can affect consequential legal, financial, personnel, fundraising, M&A, crisis, or shutdown decisions.

Mitigation: Require human executive sign-off before acting on recommendations, and use qualified legal, finance, HR, or tax review for jurisdiction-specific or regulated decisions.

Risk: Default operating assumptions such as seed stage, VC funding model, USD currency, and US-DE jurisdiction may not match the user's company.

Mitigation: Provide the actual stage, runway, funding model, currency, jurisdiction, board composition, and relevant company facts before relying on outputs.

## Reference(s):

- [CEO / Chief Executive Officer on ClawHub](https://clawhub.ai/ivangdavila/skills/ceo)
- [CEO skill homepage](https://clawic.com/skills/ceo)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown prose, checklists, decision memos, board and investor updates, communication drafts, and local YAML or Markdown configuration notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read or write local plaintext context files under ~/Clawic/data/ceo/ when the user declares preferences or company facts.]

## Skill Version(s):

1.1.6 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
