## Description:

Diagnose ROAS decline, attribution gaps, channel performance, creative effectiveness, conversion friction, retention, budget allocation, and profit quality for DTC storefronts using Convbox first-party attribution data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lcolton](https://clawhub.ai/user/lcolton)

### License/Terms of Use:

MIT-0

## Use Case:

External DTC ecommerce teams and analysts use this skill to turn natural-language marketing questions into quantified diagnostics, attribution comparisons, and decision-ready reports. It supports ROAS and CPA decline diagnosis, Meta and Google versus first-party attribution checks, funnel analysis, budget guidance, and role-specific daily, weekly, monthly, or custom-window reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Convbox API key and can access business analytics for the configured store.

Mitigation: Install only when the publisher is trusted, provide the key through secure environment settings, and rotate the key if it appears in logs, commits, issues, or conversations.

Risk: The health-check utility sends the API key to endpoints defined by access.yaml, so a modified or untrusted access file could redirect credential-bearing requests.

Mitigation: Use a pinned or isolated installation, review access.yaml before running the health checker, and avoid running the checker with modified third-party endpoint definitions.

Risk: Store benchmarks, budget caps, and preferences may persist in memory.md across sessions.

Mitigation: Review or clear memory.md when those values should not be retained.

Risk: Marketing recommendations can affect spend, bids, budgets, campaigns, or storefront decisions if acted on without review.

Mitigation: Treat outputs as recommendations only and require human review before changing advertising platforms, budgets, bids, customer journeys, or storefront content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lcolton/skills/dtc-attribution-doctor)
- [Convbox-DiagClaw Homepage](https://github.com/RTOAI/convbox-diagclaw)
- [README](README.md)
- [Scenario And Data Interface Catalog](functions.md)
- [Convbox API Access Dictionary](access.yaml)
- [Configuration Health Check Utility](utilities/config-health-check/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with metrics, diagnostics, recommendations, configuration guidance, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should cite the analysis plans used, preserve metric-caliber consistency, and treat empty or unavailable data as a stated limitation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
