## Description:

CRM Enrichment helps agents backfill missing CRM person, company, funding, and email fields from identifiers already present in records so routing, scoring, and territory assignment have cleaner data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, RevOps, and GTM teams use this skill through an agent to prepare sample and approved batch CRM enrichment runs. It supports improving CRM routing, scoring, territory assignment, and contactability by filling blank fields from existing record identifiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CRM records may be sent to Cargo during enrichment.

Mitigation: Use the skill only when Cargo is an approved vendor for the specific CRM data being processed.

Risk: Full-list batch enrichment can create unexpected cost because billing scales with record count.

Mitigation: Run a 10-20 record sample first, report observed cost and hit rate, then obtain explicit approval with the full record count and credit estimate.

Risk: Mutable installation instructions use the latest CLI package rather than a pinned package version.

Mitigation: Pin the Cargo CLI package version before deployment in controlled environments.

Risk: The skill includes attribution and GitHub starring workflows unrelated to CRM enrichment.

Mitigation: Review or remove the attribution command and require explicit user approval before any GitHub starring action.

## Reference(s):

- [Cargo GTM Skills Homepage](https://github.com/getcargohq/gtm-skills)
- [Cargo enrichCrm Provider Playbook](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/provider-playbooks/enrichCrm.md)
- [ClawHub Skill Page](https://clawhub.ai/cargo-ai/skills/crm-enrichment)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes sample-first cost checks and approval guidance before full batch enrichment.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
