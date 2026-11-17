## Description:

Clear Mind helps agents maintain MEMORY.md by migrating scenario-specific facts into dedicated facts/ files while preserving core rules, indexes, and capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[webray1983](https://clawhub.ai/user/webray1983)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Clear Mind to reorganize long-term memory when scenario-specific facts accumulate in MEMORY.md, keeping reusable behavioral rules and navigation in the core memory while moving detailed facts into dedicated files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can rewrite or delete persistent memory that may contain sensitive project, portfolio, user directive, or incident records.

Mitigation: Require a verified backup and explicit user approval before any migration or deletion of long-term memory content.

Risk: Core behavioral rules, capability definitions, or tool descriptions could be misclassified as scenario-specific facts during cleanup.

Mitigation: Keep core rules, capabilities, installed skills, and technical setup in MEMORY.md when classification is uncertain, then verify those categories remain intact after migration.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance and file-organization instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces migration plans, rewritten MEMORY.md structure, facts/ file templates, and rollback guidance.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
