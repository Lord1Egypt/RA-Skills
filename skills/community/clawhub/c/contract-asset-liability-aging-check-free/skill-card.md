## Description:

Checks contract asset and contract liability ledger text for roll-forward mismatches, total-row issues, duplicate contract numbers, missing required fields, negative aging days, and contracts carrying balances on both sides.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Project finance and accounting users at construction, software, or service companies use this skill before monthly close or reporting to reconcile contract asset and liability ledger excerpts. It is a reconciliation aid and does not replace accounting judgment, audit procedures, or validation of source documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat reconciliation findings as accounting advice, audit work, or validation of contracts, invoices, and other source documents.

Mitigation: Present results as reconciliation support only and require qualified accounting review for classification, revenue recognition, impairment, audit, and source-document decisions.

Risk: The skill operates mainly in Chinese and expects contract asset/liability ledger excerpts with recognizable headers, so unsupported formats or language mismatches may produce insufficient or incomplete checks.

Mitigation: Use ledger text with the required headers and review any insufficient-input or skipped-check messages before relying on the output.

Risk: The free release omits several checks that are listed as outside this package, including long-aging prompts, negative ending balances, and over-carry or over-recognition checks.

Mitigation: Treat the output as limited to the free release's executed checks and perform separate review for checks listed as not run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/contract-asset-liability-aging-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Console text or JSON findings with source evidence for each finding]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js on user-provided ledger text; evidence reports no hidden network, persistence, or destructive behavior.]

## Skill Version(s):

1.0.20 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
