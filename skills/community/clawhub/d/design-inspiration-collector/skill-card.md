## Description:

Collects design inspiration entry points from Dribbble and Pinterest, filters for official search, tag, and topic pages, and produces a local Markdown report with trend prompts and related design directions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benson126](https://clawhub.ai/user/benson126)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, product teams, and developers use this skill to gather UI, UX, and visual design reference links for a requested topic from Dribbble and Pinterest. It helps create a concise inspiration report while avoiding personal portfolio, board, and individual item URLs where the skill's filters apply.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Design search topics are sent to Tavily when Dribbble search is used.

Mitigation: Avoid using confidential product names, customer identifiers, or sensitive design briefs as search topics unless sharing them with Tavily is approved.

Risk: Generated links are collected search results or constructed platform URLs and are not guaranteed to be safe or authoritative.

Mitigation: Review links before opening or sharing them, and treat the report as a starting point for design research rather than a verified source list.

Risk: The script writes Markdown and JSON files under ~/design_inspirations.

Mitigation: Run the skill in an environment where writing reports to that directory is acceptable, and review generated files before distributing them.

Risk: The Tavily dependency is not pinned in the artifact metadata.

Mitigation: Pin and review the tavily-python package version in managed deployments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/benson126/skills/design-inspiration-collector)
- [Publisher Profile](https://clawhub.ai/user/benson126)
- [Tavily API](https://app.tavily.com/)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Guidance]

**Output Format:** [Markdown report and structured JSON data written as local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are written under ~/design_inspirations with filenames based on the topic and timestamp.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact files report 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
