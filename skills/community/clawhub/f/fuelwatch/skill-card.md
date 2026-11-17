## Description:

Build, deploy, and extend the FuelWatch crowdsourced fuel availability tracker for South Africa.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stefanferreira](https://clawhub.ai/user/stefanferreira)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to build, deploy, fix, and extend FuelWatch, a mobile-first crowdsourced fuel price and availability tracker for South African fuel stations.

### Deployment Geography for Use:

South Africa

## Known Risks and Mitigations:

Risk: The planned backend and WhatsApp reporting flow may allow anonymous or automated public report writes without documented server-side abuse controls.

Mitigation: Before implementing Phase 2 or Phase 3, add Supabase RLS, a trusted validation endpoint, rate limits, field allowlists, database constraints, and moderation or quarantine for submitted reports.

Risk: Crowdsourced fuel reports can become stale or inaccurate and may mislead users during a shortage.

Mitigation: Treat report data as unverified user-generated content, preserve age and verification indicators, and review deployment changes before release.

Risk: Frontend dependencies added through external CDNs can change or be unavailable if they are not controlled.

Mitigation: Pin exact dependency versions or bundle reviewed frontend dependencies before production deployment.

## Reference(s):

- [Fuelwatch ClawHub Skill Page](https://clawhub.ai/stefanferreira/skills/fuelwatch)
- [stefanferreira ClawHub Publisher Profile](https://clawhub.ai/user/stefanferreira)
- [FuelWatch Backend Plan](artifact/references/backend-plan.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include deployment steps, frontend and backend code changes, and configuration guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
