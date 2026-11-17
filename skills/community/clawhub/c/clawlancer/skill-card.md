## Description:

Clawlancer integrates OpenClaw with Clawlancer to automate seller-side listing creation, buyer-side order creation, Kite Chain payment parameter preparation, and purchase status tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fozagtx](https://clawhub.ai/user/fozagtx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketplace operators use this skill to create Clawlancer service listings, create buyer purchases, prepare payment parameters, and monitor purchase status through scripted workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create active marketplace listings and purchases through executable scripts.

Mitigation: Review each listing and order payload before execution, and require explicit wallet and listing IDs for production use.

Risk: Payment preparation output could be forwarded to a signer without sufficient independent verification.

Mitigation: Verify the supplier, token, amount, chain, contract, and order details before signing or submitting any payment transaction.

Risk: Buyer workflows can auto-select the first active listing when no listing ID is provided.

Mitigation: Provide an explicit listing ID when creating purchases, especially for commercial or irreversible workflows.

## Reference(s):

- [Clawlancer Skill Page](https://clawhub.ai/fozagtx/skills/clawlancer)
- [Clawlancer API Base URL](https://clawlancerapi-production.up.railway.app)
- [Clawlancer Supplier Endpoint](https://clawlancersupplier-kite-agent-production.up.railway.app/task)

## Skill Output:

**Output Type(s):** [json, shell commands, configuration, guidance]

**Output Format:** [JSON responses and Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Seller flows return service data; buyer flows may return purchase data, selected listing ID, payment preparation, and final state.]

## Skill Version(s):

1.2.2 (source: server release metadata; artifact frontmatter lists 1.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
