## Description:

Design and manage OpenClaw GEO content operations including sources, topic clusters, content tasks, publish targets, LLM-friendly artifacts, receipts, and visibility analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators, marketers, and developers use this skill to plan and audit GEO content systems across source catalogs, topic clusters, content tasks, publication targets, receipts, LLM-readable artifacts, and visibility analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help coordinate workflows that may post, deploy, update, or unpublish live content when paired with separate tools.

Mitigation: Before using those tools, verify the target, credentials, approval path, and receipts.

Risk: Planning output may be mistaken for evidence of live publication, indexing, crawler visits, rankings, or AI citations.

Mitigation: Require durable receipts before making production, visibility, or citation claims.

## Reference(s):

- [OpenClaw Integration](references/openclaw-integration.md)
- [GEOFlow Patterns For OpenClaw](references/geoflow-patterns.md)
- [English README](docs/readme/README_en.md)
- [Task Brief Example](examples/task.example.json)
- [Receipt Example](examples/receipt.example.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, text]

**Output Format:** [Markdown guidance with JSON task and receipt structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are planning and audit artifacts; live publication, indexing, crawler, ranking, or citation claims require receipts.]

## Skill Version(s):

0.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
