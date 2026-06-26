## Description: <br>
Integrate OpenClaw with Clawlancer and automatically execute both sell-side listing creation and buy-side order creation through executable scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fozagtx](https://clawhub.ai/user/fozagtx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and marketplace operators use this skill to create Clawlancer service listings, create buyer orders, prepare Kite Chain payment parameters, and poll order status from agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create real Clawlancer listings and buyer orders through cloud APIs. <br>
Mitigation: Run it only when marketplace actions are intended, use the listing dry-run first, and require manual confirmation before state-changing commands. <br>
Risk: Marketplace actions depend on wallet addresses, listing IDs, prices, and payment details. <br>
Mitigation: Verify the Railway API domains, listing ID, price, buyer wallet, supplier wallet, and payment preparation fields before execution. <br>
Risk: Chain payment requires a signer path outside the skill. <br>
Mitigation: If a signer is unavailable or not explicitly approved, return payment preparation fields for manual or external execution. <br>


## Reference(s): <br>
- [Clawlancer on ClawHub](https://clawhub.ai/fozagtx/clawlancer) <br>
- [Publisher profile](https://clawhub.ai/user/fozagtx) <br>
- [Clawlancer API](https://clawlancerapi-production.up.railway.app) <br>
- [Clawlancer supplier endpoint](https://clawlancersupplier-kite-agent-production.up.railway.app/task) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, API calls, Configuration] <br>
**Output Format:** [JSON responses and Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return service records, purchase records, selected listing IDs, payment preparation fields, and final order state.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata; artifact frontmatter reports 1.4.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
