## Description: <br>
Designs or implements a paper-management workflow built on a Feishu bot plus OpenClaw for ingesting papers, storing PDFs or source links, maintaining searchable metadata, and refining tags every 50 added papers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ch1hyaAnon](https://clawhub.ai/user/Ch1hyaAnon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workflow owners use this skill to design, implement, or review a Feishu paper-ingestion system that stores paper assets, writes normalized metadata into a Feishu multi-dimensional table, and evolves a reusable tag taxonomy over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A real Feishu bot could access more chats, folders, or tables than intended. <br>
Mitigation: Restrict the Feishu app to the intended paper-sharing chat, cloud-docs folder, and table before deployment. <br>
Risk: The OpenClaw handoff endpoint could expose ingestion or write actions if left unprotected. <br>
Mitigation: Protect the handoff endpoint with authentication and request verification. <br>
Risk: Message excerpts, sender identifiers, and download URLs may contain sensitive or personal information. <br>
Mitigation: Avoid logging those fields, and retain only the metadata needed for retry and audit. <br>
Risk: Taxonomy backfills can rewrite many existing table rows. <br>
Mitigation: Require review before bulk taxonomy updates and make backfills resumable. <br>


## Reference(s): <br>
- [API Contracts](references/api-contracts.md) <br>
- [Event Flows](references/event-flows.md) <br>
- [Table Schema](references/table-schema.md) <br>
- [Tag Taxonomy](references/tag-taxonomy.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with workflow steps, schemas, and implementation examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Feishu table fields, payload contracts, idempotency rules, event sequences, retry guidance, and taxonomy review logic.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
