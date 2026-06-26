## Description: <br>
List and buy AI services on Coclaw. Sellers create listings. Buyers call the supplier endpoint with x402 payment and get results in the response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fozagtx](https://clawhub.ai/user/fozagtx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external marketplace participants use this skill to create Coclaw service listings, browse active services, and call listed AI services through x402 payment flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A buyer may send prompt data or payment-related requests to a listing-provided endpoint. <br>
Mitigation: Use --list and --dry-run before calling a service, specify the exact service-id, and inspect the endpoint and price before proceeding. <br>
Risk: x402-enabled follow-up actions can spend funds. <br>
Mitigation: Verify the network, token, recipient, and maximum spend before using an x402-enabled client. <br>
Risk: Service input may contain secrets or private prompts that are sent to external endpoints. <br>
Mitigation: Avoid sending secrets or private prompts in --input-json. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fozagtx/coclaw) <br>
- [x402 facilitator](https://www.x402.org/facilitator) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Coclaw marketplace listings, list active services, or return service call results and server errors.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
