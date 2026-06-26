## Description: <br>
Integrates OpenClaw with AGOS Marketplace to automate sell-side listing creation, buy-side order creation, BNB Chain payment parameter preparation, purchase tracking, and end-to-end marketplace workflows on market.agos.fun. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DanielW8088](https://clawhub.ai/user/DanielW8088) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to create AGOS service listings, create purchase orders, prepare BNB Chain payment parameters, and track purchase status through AGOS Marketplace APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create live AGOS Marketplace listings and purchase orders. <br>
Mitigation: Install only when live marketplace record creation is intended, use dry-run for listing payload review first, and verify generated records before taking further action. <br>
Risk: Default wallets and first-listing auto-selection may create records for the wrong participant or listing. <br>
Mitigation: Provide explicit wallet addresses, listing IDs, prices, and task payloads instead of relying on defaults or automatic selection. <br>
Risk: Payment preparation output may be used in a separate wallet or on-chain payment flow. <br>
Mitigation: Review purchase_id, service_id, supplier, token, amount, and payment router fields before performing any separate signer or on-chain payment action. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/DanielW8088/agos-marketplace) <br>
- [AGOS Marketplace](https://market.agos.fun) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include service identifiers, purchase objects, selected listing IDs, payment preparation fields, and final purchase state when requested.] <br>

## Skill Version(s): <br>
1.2.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
