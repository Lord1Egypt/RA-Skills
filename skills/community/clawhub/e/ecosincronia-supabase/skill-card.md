## Description: <br>
Connect to Supabase for database operations, vector search, and storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EcosincronIA](https://clawhub.ai/user/EcosincronIA) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run Supabase SQL, CRUD, RPC, table inspection, and pgvector similarity search from an agent using configured Supabase credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent high-impact Supabase database authority through service-role credentials, including writes, deletes, raw SQL, and schema changes. <br>
Mitigation: Use a least-privileged key or staging project when possible, avoid production service-role credentials unless necessary, and require explicit confirmation before writes, deletes, raw SQL, or schema-changing operations. <br>
Risk: Vector-search queries may be sent to OpenAI for embedding generation. <br>
Mitigation: Treat vector-search query text as data shared with OpenAI and avoid sending sensitive content unless that transfer is approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EcosincronIA/ecosincronia-supabase) <br>
- [Publisher profile](https://clawhub.ai/user/EcosincronIA) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON database responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SUPABASE_URL and SUPABASE_SERVICE_KEY; vector search also requires OPENAI_API_KEY.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
