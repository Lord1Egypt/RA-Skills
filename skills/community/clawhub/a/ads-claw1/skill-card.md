## Description:

Telegram-first ads operations assistant for reporting, budget pacing, proposals, and competitor notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phap1106](https://clawhub.ai/user/phap1106)

### License/Terms of Use:

MIT-0

## Use Case:

External advertising operators and campaign teams use this skill to review Telegram-first campaign status, budget pacing, alerts, draft proposals, and competitor notes before approved action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send campaign, account, customer, or competitor data to search, scraping, Apify, Meta, or arbitrary REST endpoints.

Mitigation: Install only with trusted connected tools, scoped credentials, API allowlists, and explicit approval for external scraping or POST requests.

Risk: Recommendations can affect advertising spend or delivery decisions.

Mitigation: Treat recommendations as draft proposals and require operator approval before execution.

Risk: Campaign-health claims can be misleading when local snapshots are missing or stale.

Mitigation: Require a current ads-manager brief or snapshot refresh before relying on live decision guidance.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/phap1106/skills/ads-claw1)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, API calls]

**Output Format:** [Concise Markdown status reports, alerts, plans, proposal drafts, and command-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend Telegram commands and call connected search, scraping, Meta, Apify, ads-manager, or REST tools when available.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
