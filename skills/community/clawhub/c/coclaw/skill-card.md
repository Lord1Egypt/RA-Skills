## Description:

Coclaw helps sellers create AI service listings and buyers browse and call supplier endpoints with x402 payment, returning results in the response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fozagtx](https://clawhub.ai/user/fozagtx)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and marketplace participants use Coclaw to publish service listings, browse active listings, and call selected AI services over x402 payment flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The buyer script can call service endpoints returned by the remote Coclaw directory.

Mitigation: Use --list and --dry-run first, then verify the service ID, endpoint, and price before making a service call.

Risk: Service calls may trigger x402 payment flows in payment-enabled environments.

Mitigation: Require explicit approval before spending USDC and confirm the selected listing before continuing.

Risk: Inputs sent to marketplace listings may be processed by third-party services.

Mitigation: Do not submit secrets, private documents, source code, or business data unless the listing and Coclaw directory are trusted.

## Reference(s):

- [Coclaw Skill Page](https://clawhub.ai/fozagtx/skills/coclaw)
- [fozagtx Publisher Profile](https://clawhub.ai/user/fozagtx)
- [Coclaw API Endpoint](https://coclawapi-production.up.railway.app)
- [Coclaw Agent Endpoint](https://coclawagent-production.up.railway.app/task)
- [x402 Facilitator](https://www.x402.org/facilitator)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with bash command examples and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Network calls may list services, create listings, or call selected service endpoints; dry-run modes are available.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
