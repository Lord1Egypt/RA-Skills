## Description:

A local Chinese-language CLI skill that checks hazardous-chemical in-and-out and requisition ledgers for six disclosed arithmetic and consistency issues, with findings tied to source line numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

EHS, warehouse, finance, and operations teams use this skill to run local pre-review checks on pasted or file-based hazardous-chemical inventory ledgers. It helps identify table-level arithmetic, duplicate-entry, missing-field, numeric-format, and book-versus-count issues before monthly inventory or safety review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill does not replace legal, safety, regulatory, or physical inventory review.

Mitigation: Treat outputs as table-level pre-review findings and require qualified human review for compliance, safety, and physical inventory decisions.

Risk: The free edition performs only the six disclosed checks and omits other hazardous-chemical controls such as storage limits, expiry, dual sign-off, storage-condition continuity, and consolidated warehouse summaries.

Mitigation: Review the reported checks_not_run and checks_out_of_scope fields, then run separate controls for omitted safety and compliance checks.

Risk: Insufficient or malformed input can prevent the checker from producing conclusions.

Mitigation: Provide ledger material with headers and required columns, and treat insufficient_input results as no conclusion rather than a pass.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/chemical-inventory-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON from a local Node CLI, including finding levels, categories, source line numbers, messages, advice, summaries, executed checks, and checks not run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library; the free edition executes six disclosed ledger checks and lists unexecuted or out-of-scope checks.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
