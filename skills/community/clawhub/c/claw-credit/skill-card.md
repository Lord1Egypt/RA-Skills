## Description:

Credit line service for AI agents to access x402 services without upfront payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergiochan](https://clawhub.ai/user/sergiochan)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to register for a ClawCredit credit line, configure SDK tracing, pay x402-enabled services through credit, monitor repayment status, and direct users to the dashboard for repayment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The SDK may share prompts, transcripts, reasoning traces, workspace files, environment details, and payment context with a third-party service.

Mitigation: Use it only in workspaces where that sharing is acceptable, and avoid workspaces containing secrets, private transcripts, or sensitive customer data.

Risk: The skill stores reusable payment credentials in a local credential file.

Mitigation: Keep the credential file out of backups and logs, restrict file permissions, and rotate or re-register credentials when tokens expire or may have been exposed.

Risk: The troubleshooting example can print the full API token.

Mitigation: Do not run snippets that print API tokens; inspect token metadata without logging secret values.

Risk: Installing an unpinned third-party SDK can change behavior over time.

Mitigation: Pin and verify the SDK package version before installing or running the integration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sergiochan/skills/claw-credit)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JavaScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes SDK registration, payment, context configuration, dashboard-link, repayment-monitoring, and troubleshooting examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
