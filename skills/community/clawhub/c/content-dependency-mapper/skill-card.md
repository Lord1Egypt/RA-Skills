## Description:

Map hidden dependencies across your content library to identify critical assets, orphaned content, and strategic clusters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncreighton](https://clawhub.ai/user/ncreighton)

### License/Terms of Use:

MIT-0

## Use Case:

Content teams, editors, strategists, and developers use this skill to map relationships across content libraries, identify critical and orphaned assets, and prioritize maintenance or consolidation work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process private content exports or API-accessible content and can send selected content to OpenAI for semantic analysis.

Mitigation: Use only approved content sources, avoid unnecessary confidential data, and install only when this data handling is acceptable.

Risk: A troubleshooting curl example has unsafe variable guidance for the Authorization header.

Mitigation: Use a real API token variable for Authorization and keep CONTENT_SOURCE_URL only as the request URL.

Risk: Content scores and dependency recommendations may be incomplete or misleading when analytics, historical data, or semantic matching are imperfect.

Mitigation: Review high-impact recommendations before deleting, merging, or restructuring content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ncreighton/skills/content-dependency-mapper)

## Skill Output:

**Output Type(s):** [analysis, markdown, json, code, shell commands, configuration]

**Output Format:** [Markdown guidance with optional JSON, DOT, GraphML, and HTML dependency graph outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use content source exports or APIs, optional analytics inputs, and OpenAI semantic analysis when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
