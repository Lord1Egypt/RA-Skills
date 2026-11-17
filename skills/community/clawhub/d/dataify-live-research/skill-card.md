## Description:

Research an open-ended question with current multi-source web evidence and produce a cited brief with facts, uncertainty, and recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to run bounded live-web research through Dataify, collect source evidence, and produce cited decision briefs for industry, policy, technology, company, or market questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries, target URLs, and collected public-web content are sent to Dataify using DATAIFY_API_TOKEN.

Mitigation: Use only for content that can be shared with Dataify, minimize submitted scope, and avoid sending sensitive or confidential material.

Risk: The package includes under-disclosed business-intelligence paths for competitor analysis, lead generation, and platform-specific review scraping.

Mitigation: Review or remove business_workflow.py and catalog_builder.py before use if those workflows are not intended.

Risk: Credentials may have appeared in URL logs when wait_for_task.py was used.

Mitigation: Rotate DATAIFY_API_TOKEN after use with this version and prefer flows that do not place credentials in query strings.

## Reference(s):

- [Dataify documentation](https://doc.dataify.com)
- [Dataify support](https://www.dataify.com/)
- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-live-research)
- [Research brief contract](references/report-template.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Shell commands, Configuration guidance]

**Output Format:** [Markdown research brief plus JSON status and report files with raw evidence files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DATAIFY_API_TOKEN; output may include report.md, report.json, state.json, evidence.json, and fetched source extracts.]

## Skill Version(s):

1.1.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
