## Description:

Entity Registry helps agents audit, reconcile, and maintain canonical machine-facing entity identity records for Knowledge Graph, Wikidata, schema.org, sameAs, disambiguation, and AI-recognition evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and operators use this skill to audit entity recognition, reconcile identity conflicts, and prepare authorized canonical registry updates for organizations, people, products, brands, creative works, and events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent registry updates could introduce incorrect or misleading canonical entity facts.

Mitigation: Review proposed writes before approval, require explicit authorization and host capability for canonical changes, and leave unresolved identity conflicts open.

Risk: Checklist items can drift into PR, topical content, robots/crawlability, or page-level GEO recommendations.

Mitigation: Treat those recommendations as handoffs to the appropriate downstream skill rather than automatic actions by this skill.

Risk: Natural-person records may create privacy or compliance concerns if over-collected or recreated after erasure.

Mitigation: Confirm an applicable lawful basis before persistence, minimize fields, exclude raw contact details and credentials, and honor tombstone or erasure state unless the user explicitly authorizes a new record.

## Reference(s):

- [Entity Signal Checklist](references/entity-signal-checklist.md)
- [Entity Type Reference](references/entity-type-reference.md)
- [Example Entity Optimization Report](references/example-audit-report.md)
- [Knowledge Graph Guide](references/knowledge-graph-guide.md)
- [Knowledge Panel and Wikidata Optimization Guide](references/knowledge-panel-wikidata-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/aaron-he-zhu/skills/entity-registry)
- [Project Homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional JSON request drafts and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce audit reports, proposed registry-event requests, handoff summaries, and prioritized action lists; persistent writes require user authorization and host capability.]

## Skill Version(s):

19.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
