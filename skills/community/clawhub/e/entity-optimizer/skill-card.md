## Description:

Entity Optimizer helps agents audit, reconcile, and maintain machine-facing entity identity facts for Knowledge Graph, Wikidata, schema.org, sameAs, disambiguation, and AI-recognition workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and agent operators use this skill to audit entity recognition, reconcile duplicate or conflicting identities, and prepare source-backed actions for knowledge graph, schema, and AI disambiguation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect and potentially update an entity registry when authorized.

Mitigation: Review proposed registry changes before persistence, require explicit authorization for writes, and keep canonical updates tied to event IDs, offsets, and revisions.

Risk: Entity recommendations involving people, About pages, social profiles, or public knowledge-base edits can affect public identity records.

Mitigation: Confirm lawful basis for natural-person records, avoid raw contact or credential data, and use dedicated GEO or content skills for page-copy changes.

Risk: Adjacent GEO and page-content guidance can be mistaken for automatic authority.

Mitigation: Treat recommendations as advisory, keep Unknown distinct from failure, and verify facts against source-backed evidence before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/entity-optimizer)
- [Publisher profile](https://clawhub.ai/user/aaron-he-zhu)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [Entity Signal Checklist](artifact/references/entity-signal-checklist.md)
- [Entity Type Reference](artifact/references/entity-type-reference.md)
- [Knowledge Graph Guide](artifact/references/knowledge-graph-guide.md)
- [Knowledge Panel and Wikidata Optimization Guide](artifact/references/knowledge-panel-wikidata-guide.md)
- [Example Entity Optimization Report](artifact/references/example-audit-report.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown reports with optional JSON requests, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce registry event proposals or authorized updates when host capability and user authorization are available.]

## Skill Version(s):

17.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
