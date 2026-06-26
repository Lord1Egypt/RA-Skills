## Description: <br>
Retail complaint and after-sales handler for digital employees that classifies complaints, generates empathetic responses, routes escalations, and manages return, exchange, and refund requests according to configured policy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangwei-frank](https://clawhub.ai/user/fangwei-frank) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Customer-support teams and digital retail employees use this skill to classify dissatisfied customer messages, respond empathetically, apply configured return or refund policy, and escalate high-risk complaints to human staff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Refund, legal, media, regulator, or other high-stakes complaint handling can require business judgment beyond a template. <br>
Mitigation: Keep human review and escalation active for refunds, legal threats, media complaints, regulator references, repeat contacts, and abusive or threatening cases. <br>
Risk: Trigger phrases and escalation levels may not match every retailer's policies, language mix, or complaint taxonomy. <br>
Mitigation: Review and adapt the trigger phrases, policy entries, and permission thresholds before deployment. <br>
Risk: The skill depends on external policy and permission configuration that is not included in the artifact. <br>
Mitigation: Verify policy_entries and permissions_config are present, current, and approved by the business owner before relying on automated responses. <br>


## Reference(s): <br>
- [Complaint Classification Guide](references/classification-guide.md) <br>
- [Complaint Response Templates](references/response-templates.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/fangwei-frank/complaint-handler) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance with response templates and escalation instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual Chinese and English trigger phrases; depends on configured policy entries and permissions configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
