## Description:

Local calorie logging and visual reporting (auto-refreshes and returns report image after each log)

This skill is ready for commercial/non-commercial use.

## Publisher:

[vintlin](https://clawhub.ai/user/vintlin)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use Calorie Visualizer to log meals locally, look up nutrition values from a local food database with optional USDA fallback, and generate a daily report image for calorie and protein tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads body metrics from a workspace USER.md profile by default.

Mitigation: Set an explicit daily_goal or configure user_refused_profile=True when profile-based goal calculation is not desired.

Risk: Food search terms can be sent to the USDA API when USDA_API_KEY is configured.

Mitigation: Use --offline for local-only lookup or leave USDA_API_KEY unset when external lookup is not acceptable.

Risk: Diet data is stored locally in calorie_data.db.

Mitigation: Run the skill in a trusted workspace and control access to the generated database and report image files.

Risk: HTML rendering has weak controls for untrusted meal names until escaping is fixed.

Mitigation: Avoid untrusted meal names and review logged input before rendering reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vintlin/skills/calorie-visualizer)
- [README](README.md)
- [Quick Start](QUICK_START.md)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration]

**Output Format:** [Plain text CLI output with summaries, REPORT_IMAGE paths, generated PNG report images, and local SQLite records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local calorie_data.db storage and may cache USDA lookup results when online fallback is enabled.]

## Skill Version(s):

1.0.0 (source: CHANGELOG, package.json, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
