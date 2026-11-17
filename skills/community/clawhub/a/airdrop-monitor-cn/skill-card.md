## Description:

Monitors configured airdrop announcement and documentation pages for content changes, deadline clues, high-risk keywords, suspicious links, and daily action items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dll-create](https://clawhub.ai/user/dll-create)

### License/Terms of Use:


## Use Case:

External users and operators use this skill to run local or scheduled monitoring of configured airdrop sources and receive a concise report of page changes, deadline clues, risk flags, and prioritized actions. The skill can run without billing or, when SkillPay environment variables are configured, charge a user before running.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured monitoring sources can point to arbitrary URLs.

Mitigation: Use trusted HTTPS-only source configuration, avoid local or private-network URLs, and review source lists before scheduled runs.

Risk: SkillPay billing can create real charges when billing environment variables are set.

Mitigation: Keep paid billing separate from scheduled runs unless repeated charges are intentional, and run verify_billing.py only with non-production credentials or when a real charge is intended.

Risk: The release has a suspicious security verdict from the authoritative scan source.

Mitigation: Review the billing and URL-fetching behavior before deployment, pin dependencies, and run in a constrained environment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dll-create/skills/airdrop-monitor-cn)
- [SkillPay billing API endpoint](https://skillpay.me/api/v1/billing)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown report with optional JSON result object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include monitored source counts, changed sources, extracted deadline clues, risk flags, and prioritized daily actions.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
