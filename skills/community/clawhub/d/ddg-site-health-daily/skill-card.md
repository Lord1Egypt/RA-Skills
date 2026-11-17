## Description:

Run a daily site health check for any URL list: audit the page, check the URL's reputation, and pull fresh search context, then diff against yesterday. Use when monitoring a site you own or one you are evaluating, before a launch, or when a reputation change needs an explanation. One script, three paid calls per URL per day.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcircuitbreaker](https://clawhub.ai/user/0xcircuitbreaker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this workflow to monitor authorized websites on a daily schedule. It combines page audits, reputation checks, and search context, saves daily JSON history, and reports changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended paid retries could incur charges without a user-approved spending cap.

Mitigation: Choose free-only operation or explicitly authorize payments with enforced per-call and daily limits; stop on unexpected prices, verify current charges, and restrict any payment wallet's funds.

Risk: Target URLs are sent to DDG for audits, reputation checks, and search context.

Mitigation: Submit only URLs you are comfortable sharing with DDG, and probe only targets you are authorized to assess.

## Reference(s):

- [DDG Agent Service](https://agents.daedalusdevelopmentgroup.com)
- [ClawHub Skill Release](https://clawhub.ai/0xcircuitbreaker/skills/ddg-site-health-daily)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Text]

**Output Format:** [Daily JSON history and structured audit and reputation results, including a Markdown audit report and concise text change alerts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Compares daily results and reports changes in risk level, threat signals, and audit finding counts.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
