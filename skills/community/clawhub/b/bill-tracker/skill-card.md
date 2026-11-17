## Description:

Access Bill Tracker financial data - upcoming bills, account balances, and affordability checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielsimons1](https://clawhub.ai/user/danielsimons1)

### License/Terms of Use:


## Use Case:

External users and their agents use this skill to query upcoming bills, account balances, and affordability against a configured Bill Tracker API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive financial data through a configured Bill Tracker server.

Mitigation: Install only when the configured BILL_TRACKER_URL is trusted and use HTTPS for remote servers.

Risk: The session token is long-lived and can authorize access to the user's Bill Tracker data.

Mitigation: Keep BILL_TRACKER_SESSION_TOKEN out of logs and shared shell history, and rotate or revoke it if exposure is suspected.

## Reference(s):

- [Bill Tracker Skill on ClawHub](https://clawhub.ai/danielsimons1/skills/bill-tracker)
- [danielsimons1 publisher profile](https://clawhub.ai/user/danielsimons1)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline bash commands and summarized JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BILL_TRACKER_URL and BILL_TRACKER_SESSION_TOKEN environment variables.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
