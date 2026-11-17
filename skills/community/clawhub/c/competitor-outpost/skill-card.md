## Description:

Monitors competitors across selected sources and produces sourced intelligence reports with reliability and impact ratings and suggested actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijinhongucl-pixel](https://clawhub.ai/user/lijinhongucl-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Market researchers and business teams use this skill to track competitor announcements, pricing, hiring, and other developments and produce actionable daily or weekly intelligence reports with source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled HTML demo can contact third-party APIs automatically through live refresh.

Mitigation: Review the HTML before use, disable default live refresh, and obtain consent before contacting external sources.

Risk: Live external feed content may be displayed unsafely in the HTML report.

Mitigation: Sanitize and escape external feed fields before rendering or sharing reports.

Risk: Custom-source credentials or automated distribution could expose sensitive data or reach unintended recipients.

Mitigation: Store keys in environment variables or secret storage and enable scheduled jobs, email, chat, or publishing only for confirmed destinations.

## Reference(s):

- [Competitor Outpost on ClawHub](https://clawhub.ai/lijinhongucl-pixel/skills/competitor-outpost)

## Skill Output:

**Output Type(s):** [Analysis, Markdown reports, HTML reports, JSON data]

**Output Format:** [Markdown tables, HTML dashboard, or structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Source links, P0–P3 reliability and I1–I3 impact ratings, publication and collection dates, and action recommendations; optional scheduled email or IM delivery.]

## Skill Version(s):

3.3.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
