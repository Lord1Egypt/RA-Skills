## Description:

Use this skill whenever an APS production scheduling agent needs to read, search, maintain, or propose updates to a local filesystem-based knowledge base for APS rules, client memory, problem schemas, decision history, vector indexes, and audit-tracked knowledge changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasondzs](https://clawhub.ai/user/jasondzs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and APS scheduling agents use this skill to navigate a local APS knowledge base, retrieve relevant scheduling rules, load customer and problem context, propose knowledge updates for human review, and keep rule indexes and audit history current.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist customer rules, scheduling decisions, source quotes, and client memory in a local Git-backed knowledge base.

Mitigation: Use only approved knowledge-base paths, avoid storing secrets or raw sensitive conversation quotes, and define retention and deletion rules before use with real customer data.

Risk: The documented commit flow stages broad filesystem changes inside the knowledge base.

Mitigation: Restrict Git staging to reviewed files and tighten path validation before confirming or committing knowledge updates.

Risk: Incorrect proposed rules or memory updates could affect later scheduling decisions.

Mitigation: Keep all additions in pending_review until a human reviews and explicitly confirms them, then rebuild or refresh indexes after approved changes.

Risk: Dependency drift could change vector-index behavior or local execution characteristics.

Mitigation: Run the skill in a pinned dependency environment and rebuild the vector index after bulk imports or dependency changes.

## Reference(s):

- [Aps Filesystem Agent on ClawHub](https://clawhub.ai/jasondzs/skills/aps-filesystem-agent)
- [APS Knowledge Base JSON Schemas](references/schemas.md)
- [APS Knowledge Base Utility Scripts](references/scripts.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and bash code blocks, JSON schemas, and operational checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs focus on local filesystem knowledge-base operations, pending-review proposals, vector index maintenance, and Git-backed audit workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
