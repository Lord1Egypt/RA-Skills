## Description:

Reviews post-award construction and government procurement materials for contract consistency, change compliance, personnel performance, subcontracting risks, cost deviations, acceptance, claims, thresholds, audit readiness, and evidence-backed risk decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement, construction, legal, audit, and project management users can use this skill to compare bid, contract, change, acceptance, personnel, cost, claim, and audit materials after award. It produces structured compliance findings with explicit status labels, cited evidence, threshold calculations, and recommended follow-up actions.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Dynamic knowledge-base discovery can introduce untrusted or irrelevant legal and compliance sources.

Mitigation: Restrict IMA usage to the documented trusted knowledge-base IDs or manually confirm newly discovered sources before relying on them.

Risk: Saved archives may contain sensitive project, commercial, or personnel records in local plaintext files.

Mitigation: Keep project state in-session by default; when archive saving is requested, avoid raw personal identifiers, keep files private and out of sync or source control, and use encrypted storage for sensitive records.

Risk: Compliance findings may be mistaken for legal, audit, or administrative determinations.

Mitigation: Use the skill's evidence-chain requirements and disclaimer, and route major determinations such as substantial changes, subcontracting status, or budget overruns to qualified counsel or the relevant authority.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/bid-post-award-compliance-reviewer)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Knowledge base](artifact/references/knowledge-base.md)
- [Output templates](artifact/references/output-templates.md)
- [Constraints](artifact/references/constraints.md)
- [Function routing](artifact/references/function-routing.md)
- [IMA knowledge base catalog](artifact/references/ima_kb_catalog.md)
- [Knowledge base routing](artifact/references/kb_routing.md)
- [Archive schema](artifact/references/archive-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown reports, tables, checklists, risk ratings, threshold calculations, and optional JSON archive structures.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are grounded in supplied project documents and configured knowledge sources; optional archive writing requires explicit user opt-in.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
