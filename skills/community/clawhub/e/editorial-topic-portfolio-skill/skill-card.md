## Description:

This skill evaluates technology, AI, data, cloud, and enterprise software topics, selects a writing portfolio, and prepares a confirmed Notion change preview.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Editors and research teams use this skill to assess a batch of technology topics, compare evidence, originality, timeliness, and fit, then choose one primary topic and two backups. It can prepare a Notion change preview for review before any writeback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security review confidence is medium because one JavaScript file was only partially inspected.

Mitigation: Review the adapter behavior before relying on Notion operations, especially writeback.

Risk: Topic details may include confidential or unpublished editorial ideas when external research is used.

Mitigation: Get authorization before sending topic details to external search; redact queries or skip external research when needed.

Risk: Notion writeback can change topic records.

Mitigation: Review the change preview and confirm both the portfolio and writeback before updating records.

## Reference(s):

- [Editorial Topic Portfolio on ClawHub](https://clawhub.ai/haiyangchenbj/skills/editorial-topic-portfolio-skill)
- [Evaluation Gates](references/evaluation-gates.md)
- [Scoring Model](references/scoring-model.md)
- [Portfolio Rules](references/portfolio-rules.md)
- [Notion Adapter Interface](references/notion-adapter-interface.md)
- [Replay Evaluation](references/replay-evaluation.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON]

**Output Format:** [Markdown and JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Topic evaluations, portfolio decisions, and a reviewable Notion change preview]

## Skill Version(s):

1.0.11 (source: artifact SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
