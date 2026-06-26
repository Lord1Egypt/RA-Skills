## Description: <br>
Find and compare gas prices across multiple EVM chains to identify the cheapest option for transactions and contract deployments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlrjsdl200-byte](https://clawhub.ai/user/dlrjsdl200-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to compare current EVM gas costs and choose lower-cost chains for transactions or contract deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill calls a disclosed external Chain Ops MGO API, so results depend on that operator and service availability. <br>
Mitigation: Confirm the operator is trusted before installation and treat gas recommendations as decision support rather than a guaranteed execution outcome. <br>
Risk: Paid endpoints can spend small amounts of USDC when an agent environment supports automatic x402 payments. <br>
Mitigation: Keep payment approval, spending limits, or wallet controls enabled for agents that may call paid endpoints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlrjsdl200-byte/chain-ops-mgo) <br>
- [MGO dashboard](https://mgo.chain-ops.xyz) <br>
- [MGO llms.txt](https://api.mgo.chain-ops.xyz/llms.txt) <br>
- [GitHub link listed by skill documentation](https://github.com/dlrjsdl200-byte/x402-gas-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Concise text or Markdown with chain comparisons, endpoint details, and recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference live gas-price API responses and x402-paid endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
