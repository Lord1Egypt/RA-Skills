## Description: <br>
Parses bid, project, and research announcements from PDF, HWP/HWPX, DOCX, and web pages, extracts proposal requirements, stores searchable vectors, and builds Notion project pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkbeomjun-gkgkgk](https://clawhub.ai/user/parkbeomjun-gkgkgk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Proposal, bid, and research administration teams use this skill to turn announcement documents into structured project records, requirement checklists, semantic-search data, and Notion workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive proposal or bid text may be stored in PostgreSQL, sent to Notion, or sent to an external embedding provider. <br>
Mitigation: Use a dedicated database, least-privilege Notion integration, and local embeddings for confidential documents unless external processing is approved. <br>
Risk: Web URL parsing may fetch untrusted pages from sensitive networks. <br>
Mitigation: Review source URLs before parsing and avoid fetching untrusted URLs from restricted or internal network environments. <br>
Risk: API keys and database credentials are configured through environment variables. <br>
Mitigation: Keep secrets out of shared shell profiles and rotate credentials if they are exposed. <br>
Risk: The vectorizer includes a delete command that can permanently remove project data. <br>
Mitigation: Back up the database and add operational confirmation controls before using deletion in a shared or production environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/parkbeomjun-gkgkgk/bid-proposal-manager) <br>
- [Setup guide](artifact/references/setup_guide.md) <br>
- [Database schema](artifact/references/db_schema.sql) <br>
- [Field taxonomy](artifact/references/field_taxonomy.json) <br>
- [Notion page template](artifact/templates/notion_template.json) <br>
- [pgvector Windows setup reference](https://github.com/pgvector/pgvector#windows) <br>
- [Notion integrations](https://www.notion.so/my-integrations) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance, JSON analysis files, shell commands, database records, and Notion page content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update PostgreSQL records and Notion pages when configured; embedding can be local or API-backed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
