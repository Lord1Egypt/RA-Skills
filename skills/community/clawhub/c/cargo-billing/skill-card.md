## Description:

Reports Cargo credit balances, usage by workflow, connector, or agent, subscription details, and invoices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Workspace administrators use this skill to review credit balances, usage across workflows and resources, subscription details, invoices, and payment setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review rates the skill suspicious because cost estimation can launch a live workflow, causing side effects beyond reporting.

Mitigation: Review the do-not-install guidance and inspect the workflow action before use; require explicit user approval before launching a workflow.

Risk: The CLI install metadata uses an unpinned latest package, so the installed version may change over time.

Mitigation: Select and verify an approved CLI version before installing it.

Risk: Security guidance flags unsafe handling instructions for payment details.

Mitigation: Use the documented --card-stdin option or the Stripe-hosted form instead of passing card details as command-line flags.

Risk: The security review says missing local references prevented complete analysis, so the scan does not establish that unreviewed material is safe.

Mitigation: Review the complete skill bundle and its referenced material before installation.

## Reference(s):

- [Cargo Skills project homepage](https://github.com/getcargohq/cargo-skills)
- [Cargo Billing on ClawHub](https://clawhub.ai/cargo-ai/skills/cargo-billing)
- [Usage metrics examples](references/examples/usage-metrics.md)
- [Response shapes](references/response-shapes.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands, Guidance]

**Output Format:** [JSON billing data summarized in text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include credit balances, usage breakdowns, subscription and invoice details, or payment setup guidance.]

## Skill Version(s):

2.1.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
