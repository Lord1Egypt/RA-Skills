## Description: <br>
AI-powered ingestion of CSV, JSON, and XLSX files with automatic schema generation and Supabase database integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sschepis](https://clawhub.ai/user/sschepis) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and data engineers use this skill to import CSV, JSON, and XLSX datasets into Supabase while automatically generating schemas, mapping fields, and batching uploads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The importer can use powerful Supabase credentials to create schema and upload data. <br>
Mitigation: Use a test or staging Supabase project first, avoid production service-role keys where possible, and back up data before importing. <br>
Risk: Local files, samples, or records may be sent to an LLM provider and Supabase during import. <br>
Mitigation: Do not import confidential or regulated files unless that data flow is acceptable for the project. <br>
Risk: The installed npm package and publisher should be trusted before execution. <br>
Mitigation: Verify the package identity, publisher, and release contents before installing or running the importer. <br>
Risk: API keys and database credentials are required for normal use. <br>
Mitigation: Keep credentials in environment variables or secret storage and out of source control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sschepis/flexible-data-importer) <br>


## Skill Output: <br>
**Output Type(s):** [SQL schema, Database records, Shell commands, Configuration] <br>
**Output Format:** [CLI or API execution that generates relational schema mappings and uploads records to Supabase] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a file path plus Supabase and LLM credentials supplied by the user or runtime environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
