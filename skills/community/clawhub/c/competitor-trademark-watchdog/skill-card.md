## Description:

Monitors public USPTO filings for selected companies and brands and reports new trademark applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[memeanalyst](https://clawhub.ai/user/memeanalyst)

### License/Terms of Use:

MIT-0

## Use Case:

Brand, marketing, and competitive intelligence teams use the skill to monitor USPTO filings by company or brand and receive new-filing alerts or recent-filings reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The referenced local state file was unavailable to the security review.

Mitigation: Check that the workspace state file exists and contains the intended watchlist and seen serial numbers before relying on ongoing alerts.

Risk: Each returned trademark record incurs a $0.004 charge on the user's Apify account.

Mitigation: Keep watchlists and backfill windows scoped to the user's needs and review returned-record charges.

Risk: Filing results do not establish whether a mark conflicts with another brand or indicate a product launch.

Mitigation: Present filings as reported data and leave legal or launch interpretation to the user; consult qualified trademark counsel for legal advice.

## Reference(s):

- [Apify USPTO Trademark Search Actor](https://apify.com/magnova/uspto-trademark-search)
- [ClawHub skill page](https://clawhub.ai/memeanalyst/skills/competitor-trademark-watchdog)
- [Publisher profile](https://clawhub.ai/user/memeanalyst)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Text filing alerts and reports, with JSON watchlist state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Alerts include filing details and an official record link; watchlist state tracks owners, the last check date, and seen serial numbers.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
