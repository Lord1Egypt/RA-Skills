## Description:

Helps agents access and manage Clio legal-practice records through a connected Maton account, with approval required before changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Legal-practice staff and their agents use this skill to retrieve and manage matters, contacts, tasks, documents, calendars, time entries, and billing in Clio Manage. It also describes optional connected automations that require separate approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive legal-practice records or client details could be disclosed through excessive retrieval or forwarding.

Mitigation: Retrieve only records needed for the task; keep client data out of unnecessary summaries and third-party destinations.

Risk: Writes, deletions, or billing changes could alter or lose important records.

Mitigation: Default to read-only operations and obtain explicit approval for each change, including its exact target ID and intended effect.

Risk: Connected automations or event destinations could create persistent forwarding or unintended actions.

Mitigation: Approve new connections and automations separately, avoid third-party destinations, and remove unused connections or triggers promptly.

## Reference(s):

- [Clio skill release](https://clawhub.ai/byungkyu/skills/clio)
- [Clio API documentation](https://docs.developers.clio.com/api-reference/)
- [Maton documentation](https://docs.maton.ai)
- [Maton](https://maton.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected Clio record details or instructions for approved changes.]

## Skill Version(s):

1.2.9 (source: ClawHub release evidence; skill frontmatter states 1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
