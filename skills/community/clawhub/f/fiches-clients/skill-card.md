## Description: <br>
Manages the full lifecycle of French accounting client records, including creation, validation, updates, renames, merges, archiving, lookup, and exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trendex](https://clawhub.ai/user/trendex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Accounting firm staff use this skill to manage client records as business entities rather than documents. It owns user-driven create, update, validation, merge, archive, list, and search workflows for the OpenClaw client registry. <br>

### Deployment Geography for Use: <br>
France <br>

## Known Risks and Mitigations: <br>
Risk: Broad authority over persistent client records can affect accounting data when a rename, merge, archive, reject-draft, or delete-like request has an ambiguous target. <br>
Mitigation: Require explicit target confirmation before those mutative operations and record the confirmed actor and target in the audit log. <br>
Risk: Client folder mutations can become inconsistent with companion document indexes if ownership of index rewrites is unclear. <br>
Mitigation: Clarify the handoff for index-global.json and per-client index rewrites, then test rename and merge flows before deployment. <br>
Risk: The skill handles client identifiers, contact details, and banking fields such as SIREN, SIRET, email addresses, and IBAN. <br>
Mitigation: Keep operations inside the approved OpenClaw workspace/container and review audit logs after mutative actions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/trendex/fiches-clients) <br>
- [README](README.md) <br>
- [Cohabitation with organisation-documents](references/cohabitation.md) <br>
- [Client record schema](references/schema-fiche-client.md) <br>
- [Example client record](data/fiche-client.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Concise Markdown status messages, JSON-backed record updates, and workspace file operations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill is designed for inline execution and short accounting-workflow responses.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
