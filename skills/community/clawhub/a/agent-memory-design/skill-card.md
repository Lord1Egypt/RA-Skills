## Description:

Designs persistent memory architectures for AI agents that need recall across context windows, session resets, and long-running workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vnesin-sarai](https://clawhub.ai/user/vnesin-sarai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to map agent data into memory tiers, design file organization, choose write and retrieval triggers, plan compaction safety, and define maintenance routines for persistent agent memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory designs may encourage broad long-term storage of conversations, profile details, documents, emails, and session state without privacy controls.

Mitigation: Require explicit policies for what may be remembered, what must never be saved, user opt-in and deletion, retention periods, and exclusion or protection of private files, messages, credentials, and regulated data.

Risk: Accumulated memory can become stale or noisy, causing future agent responses to rely on outdated or misleading records.

Mitigation: Use scheduled curation, source-of-truth updates after errors, archival of stale notes, and retrieval checks before promoting information into always-loaded memory.

## Reference(s):

- [ClawHub release: Agent Memory Design](https://clawhub.ai/vnesin-sarai/skills/agent-memory-design)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance with structured checklists, tables, and file layout examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces memory-tier mapping, file organization, write-trigger, compaction-safety, retrieval-infrastructure, and maintenance guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
