## Description:

Real-time GEO metrics monitoring and alerting orchestrator for tracking, visualizing, and reacting to AI GEO performance metrics over time, including AIGVR, Share of Model, AI citation volume, and related indicators across generative engines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geoly-geo](https://clawhub.ai/user/geoly-geo)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, SEO/GEO, analytics, and data teams use this skill to design ongoing monitoring systems for AI visibility metrics, dashboards, alert rules, and operating routines. It helps turn one-off GEO reports and AI answer samples into time-series tracking plans for AIGVR, Share of Model, citation volume, coverage, and anomaly response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Teams may feed logs, analytics exports, or AI answer samples containing unnecessary sensitive or personal data into monitoring workflows designed from this skill.

Mitigation: Scope collected data to the minimum fields needed for GEO metrics, remove unnecessary personal data, and review data-source access before implementation.

Risk: Users may mistake the skill for a live monitoring service or direct connector to third-party tools and models.

Mitigation: Treat outputs as planning artifacts and templates; separately review and secure any connectors, scheduled jobs, dashboards, or alerting systems built from the guidance.

## Reference(s):

- [Geo Metrics Tracker ClawHub release](https://clawhub.ai/geoly-geo/skills/geo-metrics-tracker-2)
- [GEO Metrics Tracker reference templates](references/metrics-templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with tables, pseudo-YAML or pseudo-JSON examples, and optional Python or shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces planning artifacts such as metrics catalogs, tracking schemas, dashboard specifications, alert rules, runbooks, and implementation-oriented snippets; it does not directly pull data from third-party tools or models.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
