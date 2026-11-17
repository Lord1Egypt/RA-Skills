## Description:

Manage affiliate marketing programs via the Affonso CLI, including affiliates, referrals, commissions, payouts, and program settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zilvestro](https://clawhub.ai/user/zilvestro)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to manage Affonso affiliate, referral, partner, commission, payout, coupon, marketplace, and program settings workflows from an agent-controlled CLI session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad authenticated control over affiliate, commission, payout, tracking, and CLI endpoint settings.

Mitigation: Use a narrowly scoped Affonso API key and require explicit human approval before payout, commission, auto-approval, auto-payout, delete, or bulk configuration changes.

Risk: Secrets may be exposed if API keys are passed directly on command lines or stored in unsafe shell history.

Mitigation: Use the AFFONSO_API_KEY environment variable and avoid passing secrets as command-line arguments.

Risk: A custom CLI base URL can redirect authenticated requests to an untrusted endpoint.

Mitigation: Do not set a custom base URL unless the endpoint is fully trusted.

Risk: Installing or updating the Affonso CLI package without verification can introduce supply-chain risk.

Mitigation: Pin or otherwise verify the @affonso/cli package before use.

## Reference(s):

- [Affonso homepage](https://affonso.io)
- [Affonso CLI Command Reference](references/COMMAND_REFERENCE.md)
- [Program Settings Guide](references/PROGRAM_SETTINGS_GUIDE.md)
- [Workflow Recipes](references/WORKFLOWS.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON-oriented CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require the affonso binary and AFFONSO_API_KEY; every Affonso CLI command should use --json.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
