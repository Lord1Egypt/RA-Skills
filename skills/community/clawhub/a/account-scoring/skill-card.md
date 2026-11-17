## Description:

Scores companies against an ICP on a schedule, recording a tier, rationale, and supporting evidence in a Cargo model with optional CRM writeback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

RevOps, sales leaders, and GTM engineers use this skill to keep company accounts tiered against their ICP and a maintained rubric. It records an auditable rationale and evidence for each tier, with optional CRM updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company data and internal scoring context may be sent to AI and search providers.

Mitigation: Confirm which fields and context may be shared, and minimize data sent to external providers.

Risk: Bulk backfills and scheduled scoring can incur substantial agent-run and search costs.

Mitigation: Pilot ten rows, estimate costs from actual usage, and approve the deployment plan before bulk scoring or enabling the schedule.

Risk: CRM connector failures may not stop a run, leaving account fields unwritten or incorrect.

Mitigation: Keep CRM writeback off unless needed and verify the configured fields on a piloted CRM record.

Risk: External installers and dependency revisions can change or introduce supply-chain risk.

Mitigation: Review external installers and pin dependency revisions where possible.

## Reference(s):

- [Skill source](https://github.com/getcargohq/gtm-skills/tree/main/account-scoring)
- [ClawHub release](https://clawhub.ai/cargo-ai/skills/account-scoring)

## Skill Output:

**Output Type(s):** [code, configuration, guidance, text]

**Output Format:** [Cargo TypeScript project resources and structured account records containing a tier, rationale, evidence URL, and timestamp.]

**Output Parameters:** [Tiers are A, B, C, or disqualified; CRM writeback is optional and limited to configured fields.]

**Other Properties Related to Output:** [Decisions follow the consumer's ICP and rubric. The example must be adapted to the consumer project and does not deploy or score accounts by itself.]

## Skill Version(s):

0.5.4

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
