## Description: <br>
Use ACE Phase 0 to pay x402-gated APIs with bounded wallet-funded session keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SumeetChougule](https://clawhub.ai/user/SumeetChougule) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent needs to make x402-gated API calls under explicit wallet-funded spend limits, TTL, and category policy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill authorizes bounded wallet-funded API payments, so misuse or misconfiguration can spend real funds. <br>
Mitigation: Use a minimally funded wallet or limited session key, keep TTL short, set low per-transaction and daily caps, and verify endpoint, price, and reason before payment. <br>
Risk: Runtime behavior depends on external SDKs and x402 endpoints that are not bundled with the skill. <br>
Mitigation: Pin and review SDK versions and fetch endpoint schema or documentation before allowing payable requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SumeetChougule/chaoschain-ace) <br>
- [ChaosChain ACE SDK repository](https://github.com/chaoschain-labs/chaoschain-ace-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and policy configuration fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes payment-policy setup, spend-intent reasoning, schema discovery guidance, and refusal rules for out-of-policy requests.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
