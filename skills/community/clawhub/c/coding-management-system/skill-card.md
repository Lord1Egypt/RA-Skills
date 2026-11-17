## Description:

Keeps drifting or half-finished software projects under control by clarifying goals, sizing scope, authorizing bounded agent work, and separating delivery evidence from independent QA acceptance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[englandtong](https://clawhub.ai/user/englandtong)

### License/Terms of Use:

MIT-0

## Use Case:

External users, project owners, and developers use this skill to turn vague goals or conflicted project records into a compact delivery authority with explicit scope, non-goals, acceptance evidence, and QA posture. It is intended for project governance, drift recovery, rebaseline decisions, milestone/work-order authorization, and final acceptance review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose or write governance state such as Active Packets, rebaseline records, archive moves, work orders, or QA decisions.

Mitigation: Review any proposed state change before allowing writes, especially when production, credentials, paid resources, protected data, destructive actions, deployment, or rebaseline decisions are involved.

Risk: Project-governance records may accidentally capture sensitive project, counterparty, contract, financial, or personal information.

Mitigation: Do not record personal contact data or confidential materials in governance artifacts, and do not upload private files or documents to cloud services without explicit confirmation.

Risk: Insufficient evidence can lead to overstated completion or acceptance claims.

Mitigation: Require delivery-class evidence, use weaker claim status when evidence conflicts, and mark unresolved cases for review or cannot-confirm instead of accepting them.

## Reference(s):

- [Quickstart](QUICKSTART.md)
- [Security](SECURITY.md)
- [Skill Definition](SKILL.md)
- [Alignment, Rebaseline, Audit, And Finish Line 2.1](references/en/alignment-and-rebaseline.md)
- [Anti-Involution 2.2](references/en/anti-involution.md)
- [Controller, Stage Reviewer, And Independent QA 2.1](references/en/controller-qa.md)
- [Cross-Plugin File Contracts (CDH)](references/en/cross-plugin-file-contracts.md)
- [Execution Contract 2.1](references/en/execution-contract.md)
- [Goal Discovery 2.1](references/en/goal-discovery.md)
- [Governance Profiles And Files 2.1](references/en/governance-profiles.md)
- [Legacy Bootstrap 2.1](references/en/legacy-bootstrap.md)
- [Planning And Sizing 2.1](references/en/planning-and-sizing.md)
- [ClawHub skill page](https://clawhub.ai/englandtong/skills/coding-management-system)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with structured status fields, optional JSON or shell command snippets, and governance files when writes are explicitly authorized]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responds in the user's language and keeps machine-readable keys and enum values in English.]

## Skill Version(s):

2.2.1 (source: SKILL.md body and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
