## Description: <br>
Search the Andara Ionic RAG knowledge base (3,800+ records) for business intel, research, products, team, meetings, and any indexed content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atiati82](https://clawhub.ai/user/atiati82) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and authorized Andara staff use this skill to search business, product, research, meeting, CMS, order, customer, and team data through read-only PostgreSQL queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive customer, revenue, team equity, meeting, subscriber, or business data through broad SQL search access. <br>
Mitigation: Install only for authorized users and agents, use a dedicated read-only DATABASE_URL limited to approved tables or redacted views, and review queries before returning sensitive results. <br>
Risk: A write-capable or production database credential could let an agent exceed the skill's intended read-only posture. <br>
Mitigation: Provide a database role that cannot INSERT, UPDATE, DELETE, alter schema, or access unapproved tables, and avoid production credentials when a safer reporting replica or view is available. <br>
Risk: Large or raw content fields may disclose more information than needed for the user's question. <br>
Mitigation: Keep default LIMIT values low, truncate long content fields, and return only the columns needed to answer the request. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/atiati82/andara-rag-search) <br>
- [Publisher profile](https://clawhub.ai/user/atiati82) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline PostgreSQL shell commands and SQL query examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides concise, read-only PostgreSQL searches over the configured Andara database and recommends result limits and content truncation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
