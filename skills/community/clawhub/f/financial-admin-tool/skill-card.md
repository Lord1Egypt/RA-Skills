## Description:

Financial Admin helps fund administration and finance operations teams run GL reconciliations, trace breaks, prepare accruals and roll-forwards, write variance commentary, and perform NAV tie-outs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Finance operations and fund accounting teams use this skill during daily and month-end fund administration to reconcile GL and subledger data, trace breaks, prepare accrual and roll-forward schedules, draft variance commentary, and tie LP statements to NAV packs. Outputs are review artifacts and draft recommendations for controller or operations approval, not posted financial changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may work with sensitive fund accounting, general ledger, subledger, NAV, LP statement, invoice, or vendor data.

Mitigation: Install only in environments where the agent is authorized to read fund accounting data, and keep connected finance MCP permissions scoped as narrowly and read-only as practical.

Risk: Draft journal entries, action labels, variance explanations, or reconciliation flags could be mistaken for approved financial actions.

Mitigation: Treat all outputs as recommendations that require normal controller, accounting, or operations approval before posting, adjustment, suppression, or distribution.

Risk: Untrusted financial extracts and supporting documents may contain incorrect data or embedded instructions.

Mitigation: Use those files only as data sources, cite support for calculations, compare against authoritative systems such as GL or NAV packs, and surface unclear drivers instead of inventing explanations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/financial-admin-tool)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown tables and narratives, with JSON objects for traced reconciliation breaks and draft journal-entry text where applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces review artifacts, flags, draft journal entries, and action recommendations; it does not post entries or make financial adjustments.]

## Skill Version(s):

1.0.0 (source: target metadata, release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
