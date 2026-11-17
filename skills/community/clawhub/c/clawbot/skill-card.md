## Description:

Credit line service for AI agents to access x402 services without upfront payment, register for pre-qualification, pay through ClawCredit on Base/Solana/XRPL, and build credit history while using USD credit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goddieian47-boop](https://clawhub.ai/user/goddieian47-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to register for ClawCredit, configure the SDK, check credit and repayment status, and call x402-enabled services using an issued credit line instead of upfront cryptocurrency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The third-party credit SDK may read and upload broad agent context, including workspace, transcript, and prompt data.

Mitigation: Use only with explicit privacy consent, avoid private or sensitive workspaces unless the data schema is clear, and keep visible logs of submitted context.

Risk: The skill stores an API token and may reuse it for future credit and payment calls.

Mitigation: Keep the credential file protected, restrict file permissions, avoid manual token copying, and revoke or rotate credentials when access is no longer needed.

Risk: The skill can modify heartbeat configuration or create recurring checks that run without fresh prompts.

Mitigation: Require separate opt-in for background monitoring and promotions, review heartbeat or cron entries, and provide an easy uninstall or revocation path.

Risk: Using an unpinned third-party SDK version can change behavior across installs.

Mitigation: Pin the @t54-labs/clawcredit-sdk version and review changes before upgrading.

## Reference(s):

- [ClawCredit x402 Partner Services Registry](https://www.claw.credit/X402_PARTNER_SERVICES_REGISTRY.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JavaScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes SDK setup guidance, consent checkpoints, credential handling instructions, heartbeat or cron monitoring guidance, repayment reminders, and x402 payment examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
