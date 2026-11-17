## Description:

Bid Proposal Manager parses bid, business, and research announcement files or URLs, extracts deadlines and submission requirements, stores searchable vectors in PostgreSQL with pgvector, and can create structured Notion project pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkbeomjun-gkgkgk](https://clawhub.ai/user/parkbeomjun-gkgkgk)

### License/Terms of Use:

MIT-0

## Use Case:

Proposal teams, business development staff, researchers, and developers use this skill to turn bid, RFP, grant, and research announcements into structured project records, checklists, and searchable context for proposal preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive proposal, contact, and requirement content may be persisted in PostgreSQL, embedded, or transmitted to Notion or remote embedding providers.

Mitigation: Review data flows before use, bind PostgreSQL to localhost with a unique password, disable remote embedding providers unless explicitly intended, and confirm before storing proposal content or creating/updating Notion pages.

Risk: URL fetching can ingest untrusted or unexpected web content into the proposal workflow.

Mitigation: Restrict URL fetching to trusted public announcement domains and review parsed content before using it for downstream checklists, embeddings, or Notion updates.

Risk: Broad package installation can alter the host Python environment.

Mitigation: Use a virtual environment, pin dependencies, and avoid --break-system-packages during installation.

## Reference(s):

- [Setup Guide](artifact/references/setup_guide.md)
- [Database Schema](artifact/references/db_schema.sql)
- [Field Taxonomy](artifact/references/field_taxonomy.json)
- [Notion Template](artifact/templates/notion_template.json)
- [pgvector Windows Setup](https://github.com/pgvector/pgvector#windows)
- [PostgreSQL Windows Downloads](https://www.postgresql.org/download/windows/)
- [Notion Integrations](https://www.notion.so/my-integrations)
- [Ollama](https://ollama.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, code]

**Output Format:** [Markdown guidance with shell command examples, JSON analysis artifacts, checklist text, and Notion page updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local documents or URLs, write JSON artifacts, store embeddings in PostgreSQL/pgvector, and create or update Notion pages when credentials are provided.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
