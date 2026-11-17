## Description:

Rebuild an Apollo contact list in Cargo and compare verified coverage and credit costs on the same sample before deciding whether to migrate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Revenue operations and GTM engineering teams use this skill to compare Apollo enrichment with Cargo's multi-provider waterfall on a small exported sample, measuring verified contact coverage and credits spent before deciding on a full migration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contact records may contain personal or confidential information.

Mitigation: Use only contact records you are authorized to share with Cargo and its providers.

Risk: Enrichment and verification calls consume credits, and a full-list run can increase costs.

Mitigation: Start with 10–20 records, report the measured cost, and get approval for a full run after stating the row count and estimated credits.

Risk: The CLI, any separately downloaded skill pack, and the linked external playbook are outside this artifact review.

Mitigation: Review the CLI and any additional skill pack separately before use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/cargo-ai/skills/apollo-to-cargo)
- [Cargo GTM skills project homepage](https://github.com/getcargohq/gtm-skills)
- [Apollo.io provider playbook](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/provider-playbooks/apolloio.md)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Shell commands]

**Output Format:** [Markdown with inline shell command examples and comparative results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Compares verified contact coverage and credits spent on a sample; results depend on the records and providers used.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
