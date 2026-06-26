## Description: <br>
AI-powered intelligent customer service for banking and securities, covering FAQ answering, account inquiry, transaction guidance, complaint handling, and 24/7 automated support for China financial institution call centers and digital customer service teams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gechengling](https://clawhub.ai/user/gechengling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External banking and securities service teams use this skill to draft automated customer-service responses, classify customer intent, answer common account and product questions, and structure complaint handling with compliance checks. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Customer-service workflows can involve personal, account, or complaint details. <br>
Mitigation: Collect only the minimum needed information, mask sensitive fields, and never request full account numbers, passwords, or other secrets. <br>
Risk: Incorrect identity handling could expose banking services or advice to the wrong person. <br>
Mitigation: Require identity verification through official bank channels before account-specific assistance or transaction guidance. <br>
Risk: Complaints and regulated financial issues require approved handling and auditability. <br>
Mitigation: Route complaints into an approved secure ticketing system and review responses against applicable regulations and institutional policies before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gechengling/bank-customer-service) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown prose with embedded Python-style dictionaries, FAQ response templates, SOP text, and intent classification examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on customer-service answer patterns, complaint handling flow, and intent classification; real deployments should connect responses to approved banking systems and policies.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
