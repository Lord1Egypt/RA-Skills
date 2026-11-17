## Description:

Family Financial Planner helps agents collect household financial details, model China-specific financial scenarios for major life decisions, and produce an interactive single-file HTML dashboard with key findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ramos-dev](https://clawhub.ai/user/ramos-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to evaluate family finances before resignation, entrepreneurship, relocation, full-time caregiving, gap-year, or similar major life decisions. It models assets, debts, cash flow, runway, stop-loss thresholds, and return-to-work salary needs using China-specific tax, social insurance, housing fund, and city cost assumptions.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Sensitive household financial information may be embedded in generated executable HTML.

Mitigation: Review the generated dashboard locally before sharing, avoid uploading it to third-party services, and remove or redact personal financial details when distribution is required.

Risk: User-provided text and financial values may be inserted into HTML without a defined escaping step.

Mitigation: Escape or safely serialize all user-provided values before opening the dashboard, especially names, notes, scenario descriptions, and free-form text.

Risk: The dashboard template loads Google Fonts even though the report is otherwise described as local.

Mitigation: Remove the Google Fonts import or replace it with local fonts when fully offline or private report generation is required.

Risk: The built-in assumptions are China-specific and city data may become stale after annual July social insurance and housing fund adjustments.

Mitigation: Use the skill for China-specific planning, verify current city parameters before relying on results, and adapt assumptions explicitly for other jurisdictions.

## Reference(s):

- [Financial Model Specification](references/financial-model-spec.md)
- [City Profiles](references/city-profiles.md)
- [ClawHub Skill Page](https://clawhub.ai/ramos-dev/skills/family-financial-planner)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance and generated single-file HTML dashboard code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The dashboard embeds user-specific household financial data in local HTML and may include inline JavaScript calculations.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
