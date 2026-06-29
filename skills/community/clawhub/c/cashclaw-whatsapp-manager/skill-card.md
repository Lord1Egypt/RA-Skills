## Description: <br>
Sets up and manages WhatsApp Business accounts including auto-response systems, client communication workflows, FAQ templates, and broadcast campaigns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andreataide86](https://clawhub.ai/user/andreataide86) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators and service providers use this skill to set up and manage WhatsApp Business communication workflows for clients, including profile setup, automated replies, FAQ templates, quick replies, and broadcast campaign plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad keyword triggers can send an irrelevant canned response in a real customer conversation. <br>
Mitigation: Test auto-response triggers with representative conversation examples and narrow broad triggers such as 'where', 'help', and '1' or require menu state before deployment. <br>
Risk: Broadcast campaigns can create compliance or customer-trust issues if sent to the wrong audience or without opt-out handling. <br>
Mitigation: Use opted-in contact lists, include an opt-out instruction such as 'Reply STOP to unsubscribe', and limit repeated broadcasts to the same contact. <br>
Risk: Installing the companion npm package introduces supply-chain risk outside the Markdown artifact. <br>
Mitigation: Review the npm package before installation and test the `cashclaw` commands in a controlled environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/andreataide86/skills/cashclaw-whatsapp-manager) <br>
- [Publisher Profile](https://clawhub.ai/user/andreataide86) <br>
- [CashClaw npm package](https://www.npmjs.com/package/cashclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML, JSON, and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces client-ready WhatsApp Business setup notes, templates, campaign plans, FAQ structures, and operational recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
