## Description:

Fiches Clients helps accounting agents manage the lifecycle of French client records, including creation, validation, updates, renames, merges, archives, listing, and lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trendex](https://clawhub.ai/user/trendex)

### License/Terms of Use:

MIT-0

## Use Case:

Accounting staff and agents use this skill to maintain client records as business entities, including French identifiers, contact data, status transitions, and per-client folders. It is intended to coordinate client-record lifecycle work alongside a separate document-organization skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad mutation authority over client records and folders can cause lasting incorrect merges, archives, deletions, renames, or document moves.

Mitigation: Require explicit user confirmation before merge, archive, reject-draft deletion, slug rename, and bulk document moves.

Risk: Audit logs and status messages may expose sensitive client values such as IBANs, contact details, addresses, SIREN/SIRET, or previous field values.

Mitigation: Redact or omit raw sensitive values in logs and user-facing summaries unless the user explicitly needs them.

Risk: Client registry and folder state can become inconsistent after mutative operations.

Mitigation: Validate uniqueness and registry-to-folder consistency after writes, and preserve an audit trail for each mutation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/trendex/skills/fiches-clients)
- [Cohabitation with organisation-documents](references/cohabitation.md)
- [Client record schema](references/schema-fiche-client.md)
- [Example client record](data/fiche-client.example.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration]

**Output Format:** [Concise French status messages plus JSON-backed client record, folder, and audit files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mutates client registry data and per-client folders; may handle sensitive accounting identifiers, contact details, addresses, and IBAN values.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
