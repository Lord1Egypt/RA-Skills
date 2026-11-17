## Description:

Design or implement a paper-management workflow built on a Feishu bot plus OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ch1hyaanon](https://clawhub.ai/user/ch1hyaanon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, implement, or review a Feishu bot and OpenClaw workflow for ingesting academic papers, storing PDFs or source-link index docs, writing normalized paper metadata, and refining reusable tags every 50 canonical papers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow stores papers, links, message metadata, summaries, and tags in durable Feishu docs and tables.

Mitigation: Configure bot permissions, data retention, sharing access, and consent expectations before using it with private chats, confidential manuscripts, or restricted links.

Risk: Webhook retries or concurrent events can create duplicate uploads or rows if idempotency is not enforced.

Mitigation: Use event-and-candidate idempotency keys plus canonical paper fingerprints, and perform deduplication before cloud-doc or table writes.

Risk: Taxonomy backfills can leave inconsistent labels if a threshold review is only partially completed.

Mitigation: Persist review checkpoints only after backfill succeeds, and make taxonomy review resumable for each 50-paper threshold.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ch1hyaanon/skills/feishu-paper-manager)
- [API Contracts](references/api-contracts.md)
- [Event Flows](references/event-flows.md)
- [Table Schema](references/table-schema.md)
- [Tag Taxonomy](references/tag-taxonomy.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with schemas, implementation notes, code examples, and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Feishu table schemas, payload contracts, event flows, taxonomy rules, and review findings.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
