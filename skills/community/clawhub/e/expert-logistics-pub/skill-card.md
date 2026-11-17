## Description:

物流与运输结算专家 helps reconcile logistics and transportation settlement tables by routing pasted tabular material to one of 10 local checkers and returning line-referenced, recalculable findings or missing-column feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Logistics, warehouse, fleet, courier, and finance operators use this skill to check settlement, insurance, fuel, storage, waybill, receipt, and COD tables before payment or dispute review. It is intended for local reconciliation assistance and should not be treated as final payment authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Settlement findings can be mistaken for authority to pay, withhold, or dispute money.

Mitigation: Treat outputs as reconciliation advice and have a qualified operator review source documents and business rules before financial action.

Risk: The CLI reads pasted settlement data or a local file supplied by the user.

Mitigation: Run it only with data you are permitted to process locally, and avoid pasting unrelated sensitive information.

Risk: Normal use creates a local trial-use counter at ~/.logistics-expert/uses.

Mitigation: Account for this local state file in privacy, endpoint management, and cleanup procedures.

Risk: Missing headers, mixed table types, or incomplete columns can prevent reliable routing and checking.

Mitigation: Provide the full table header and data rows, split mixed materials into separate inputs, and resolve missing-column notices before relying on results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/expert-logistics-pub)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON results from local Node.js CLI commands, with reconciliation findings, missing-input notices, and line-referenced calculation details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normal use reads pasted text or an explicitly supplied local JSON file and maintains a local trial-use counter.]

## Skill Version(s):

1.0.10 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
