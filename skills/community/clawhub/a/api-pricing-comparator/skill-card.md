## Description: <br>
Compare AI API or model pricing across providers and produce a structured summary for product pages, blog posts, or buyer guides. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xujfcn](https://clawhub.ai/user/xujfcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product marketers, and buyer-guide authors use this skill to normalize AI model or API pricing, compare raw cost with practical value, and produce structured recommendations for product pages, articles, or vendor-selection workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the optional Crazyrouter example could send API requests to an external endpoint with the configured API key. <br>
Mitigation: Confirm the intended endpoint before use and use a dedicated, limited API key. <br>
Risk: Pricing comparisons can become misleading when source prices are stale, missing, or measured in incompatible billing units. <br>
Mitigation: Verify current source prices, state workload assumptions, keep non-token units explicit, and mark missing values as unavailable. <br>


## Reference(s): <br>
- [Pricing Normalization Rules](references/pricing-normalization.md) <br>
- [Example Inputs and Use Cases](references/example-inputs.md) <br>
- [Crazyrouter Homepage](https://crazyrouter.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with normalized pricing tables and recommendation sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses explicit assumptions, marks unavailable values, and separates raw unit price from platform value.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
