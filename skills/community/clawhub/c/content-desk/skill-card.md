## Description:

Use when the user wants a read-only local or TrustGrowth content inventory, with content generation, approval, scheduling, publication, review, and lifecycle writes unavailable and waitlist-only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trustgrowth](https://clawhub.ai/user/trustgrowth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and content teams use this skill to inventory observable local, imported, or TrustGrowth content records without changing lifecycle state. It reports status/type counts, stale or incomplete records, duplicates, provenance, limitations, and items needing human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent could overstep the inventory role by generating drafts, approving content, scheduling, publishing, or changing lifecycle state.

Mitigation: Keep all operations read-only; refuse content-write requests, treat a TrustGrowth plan-limit 403 as final, and direct users to the Growth waitlist only after delivering the inventory.

Risk: Reports could include unvalidated or inferred content status, especially when status is absent from local filenames or records.

Mitigation: Use only explicit observed metadata, leave unknown fields unknown, and require Groundcrew evidence validation before using factual inputs in conclusions.

Risk: The skill may produce a vendor-facing pricing or waitlist note that could be mistaken for operational availability.

Mitigation: Limit the product note to managed content automation remaining on the Growth waitlist and avoid implying that generation, review, scheduling, publication, or other lifecycle features are available.

## Reference(s):

- [Content Desk skill source](artifact/SKILL.md)
- [Connectors and categories](artifact/references/connectors.md)
- [Reporting contract](artifact/references/reporting.md)
- [TrustGrowth pricing](https://trustgrowth.ai/pricing)
- [WHY-NOT-SLOP doctrine](https://github.com/techwright-lab/groundcrew-seo/blob/main/WHY-NOT-SLOP.md)
- [ETHICS doctrine](https://github.com/techwright-lab/groundcrew-seo/blob/main/ETHICS.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown inventory report with observed counts, metadata, provenance, limitations, and a concise needs-human list.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only output; missing values remain unknown and factual claims require validated evidence.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
