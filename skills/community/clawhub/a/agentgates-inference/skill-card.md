## Description:

Ask confidential or open models in the standard chat format, one request one x402 USDC payment, priced before the model runs; prepaid balances and bearer keys for volume.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentgates](https://clawhub.ai/user/agentgates)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to request text completions from confidential or open models through Agentgates, with request pricing and USDC payment handled through its chat API. Users should approve each payment or stay within a budget they set.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to an external inference provider, and open-tier models do not include attestation.

Mitigation: Send only content you intend Agentgates to process; check the model tier and its privacy and attestation assurances before sharing sensitive material.

Risk: Inference requests spend USDC, and prepaid balances and bearer keys can authorize additional spending.

Mitigation: Approve payments individually or set a spending budget, and protect wallet credentials and bearer keys.

Risk: A low token ceiling can produce an incomplete answer while still incurring a charge.

Mitigation: Set an adequate max_tokens ceiling for the selected model and task.

## Reference(s):

- [Agentgates inference API documentation and live pricing](https://api.agentgates.ai/api/inference/docs)
- [Agentgates inference catalog and model prices](https://api.agentgates.ai/api/inference/catalog)
- [ClawHub skill page](https://clawhub.ai/agentgates/skills/agentgates-inference)

## Skill Output:

**Output Type(s):** [Text, API Calls, Guidance]

**Output Format:** [Chat completion text; requests and responses use the documented JSON chat API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Model and token ceiling vary by request; responses and charges depend on the selected model and tokens used.]

## Skill Version(s):

1.0.1 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
