## Description:

Helps agents set up consent-based product tracking, analyze funnels, paths, retention, and experiments, and recommend a focused growth action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dannyshmueli](https://clawhub.ai/user/dannyshmueli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to instrument their own products with consent, interpret product analytics, and choose a measurable next growth action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external analytics CLI requires browser-approved access to a product analytics account.

Mitigation: Confirm the project goal and event plan before setup, and grant access only after reviewing the browser approval.

Risk: Tracking changes could collect unnecessary user data or alter product code.

Mitigation: Review tracker and code changes, collect only goal-linked events with consent, and verify the first useful event.

Risk: Stored authentication or product context could disclose sensitive information.

Mitigation: Keep .openclaw/agent-analytics/config.json out of git and exclude PII, secrets, and temporary notes from context.

## Reference(s):

- [Agent Analytics ClawHub release](https://clawhub.ai/dannyshmueli/skills/agent-analytics)
- [Agent Analytics website](https://agentanalytics.sh)
- [Projects, surfaces, and portfolios guide](https://docs.agentanalytics.sh/guides/projects-surfaces-portfolios/)
- [Setup and authentication](references/setup-auth.md)
- [Product analytics operating model](references/product-analytics-operating-model.md)
- [Growth recipes](references/growth-recipes.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with metrics, recommendations, and optional code or shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes metric definitions, evidence, caveats, and one bounded next action.]

## Skill Version(s):

4.0.37 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
