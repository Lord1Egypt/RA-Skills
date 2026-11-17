## Description:

Provides internal-control leaders with an end-to-end risk dashboard that combines complaints, logistics anomalies, and supplier scores to generate risk heat maps, alerts, daily reports, weekly reports, and trend forecasts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nic-yuan](https://clawhub.ai/user/nic-yuan)

### License/Terms of Use:

MIT-0

## Use Case:

Internal control managers and operations risk teams use this skill to turn complaint, logistics, and supplier-risk inputs into daily or weekly risk summaries, heat maps, and priority action lists for management review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may contain complaints, supplier-risk signals, logistics anomalies, and estimated losses.

Mitigation: Route reports only to controlled internal recipients, channels, and schedules approved by internal policy.

Risk: Automated delivery of daily reports, weekly reports, or event alerts may broaden access to sensitive risk information.

Mitigation: Configure push delivery conservatively and review recipient lists before enabling automatic report distribution.

Risk: Risk thresholds and trend judgments may be unreliable when data is incomplete or not calibrated to actual operations.

Mitigation: Require the report to identify data gaps and periodically calibrate thresholds against observed operational outcomes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nic-yuan/skills/07-risk-dashboard)
- [ClawHub publisher profile](https://clawhub.ai/user/nic-yuan)
- [GLOSSARY.md](docs/GLOSSARY.md)
- [INSUFFICIENCY-HANDLING.md](docs/INSUFFICIENCY-HANDLING.md)
- [RULE-UPDATE-SOP.md](docs/RULE-UPDATE-SOP.md)
- [LINKING-SOP.md](docs/LINKING-SOP.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style operational reports, tables, checklists, heat maps, alerts, and concise natural-language risk summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided operational data to produce daily reports, weekly reports, heat maps, alerts, and trend analyses; no executable code is included.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.7.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
