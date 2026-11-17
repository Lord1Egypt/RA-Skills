## Description:

Helps agents inspect and manage Genius Referrals accounts, advocates, referrals, bonuses, redemptions, and reports through the API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alainhl](https://clawhub.ai/user/alainhl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business operators use this skill to inspect referral activity, produce reports, and manage advocates, referrals, bonuses, and redemption requests in Genius Referrals accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An API token may permit account changes, payouts, redemption updates, forced bonuses, or deletions.

Mitigation: Use a least-privilege token and verify the publisher before granting access.

Risk: The request helper does not enforce the skill's promised confirmations before non-GET calls.

Mitigation: Require a human-reviewed dry run and explicit approval before any non-GET request.

Risk: Changing the API base URL could send credentials to an unintended host.

Mitigation: Keep the base URL on the official Genius Referrals API host.

## Reference(s):

- [Genius Referrals API documentation](https://api.geniusreferrals.com/doc)
- [Endpoint catalog](references/endpoint-catalog.md)
- [ClawHub skill release](https://clawhub.ai/alainhl/skills/genius-referrals-api)

## Skill Output:

**Output Type(s):** [Text, API calls, JSON]

**Output Format:** [Text summaries and structured API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report request status, endpoint, resource identifiers, and next action.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
