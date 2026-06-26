## Description: <br>
Unified entry skill for RealMarket A2A commerce workflows. Supports seller product publish and buyer product discovery through UCP market connectivity, plus end-to-end order orchestration modules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luoqianchenguni-max](https://clawhub.ai/user/luoqianchenguni-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and commerce workflow operators use this skill to orchestrate A2A marketplace flows, including seller product publication and buyer product discovery against a UCP-connected market endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts a user-specified marketplace domain and follows UCP discovery to a REST endpoint, so an untrusted or unexpected endpoint could receive product data or return misleading listings. <br>
Mitigation: Use trusted domains, prefer HTTPS, and review the discovered endpoint when possible before running buyer or seller actions. <br>
Risk: Seller mode publishes products and should be treated as a real marketplace write action. <br>
Mitigation: Confirm the target domain, product name, price, currency, category, and stock setting before running seller publish. <br>
Risk: The broader end-to-end commerce flow depends on separate authentication, payment, ledger, order-state, and realtime modules. <br>
Mitigation: Review those related skills and their security posture before relying on the full commerce workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luoqianchenguni-max/a2a-supermarket) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON from the CLI, with Markdown usage examples in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Seller output reports publish results with mode=seller_publish; buyer output reports discovery results with mode=buyer_discover.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
