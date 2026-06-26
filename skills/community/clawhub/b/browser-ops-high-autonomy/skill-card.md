## Description: <br>
Automates routine browser workflows end-to-end on approved domains and escalates only for legal, payment, login, security, domain, or blocking issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forevercrab321-svg](https://clawhub.ai/user/forevercrab321-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations teams and browser-capable agents use this skill to complete approved-domain workflows such as customer support, email operations, CRM updates, administrative forms, platform operations, routine communication, and structured data extraction. The skill returns explicit status and next-action metadata when it finishes or encounters a restricted event. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad browser authority can affect user accounts, settings, messages, forms, or private data if enabled in an inappropriate browser context. <br>
Mitigation: Use the skill only on approved domains and require explicit confirmation before submitting forms, sending messages, changing settings, deleting data, or extracting private information. <br>
Risk: Security, login, legal, and payment events require human judgment or credentials that the skill should not bypass. <br>
Mitigation: Stop and return the matching escalation status for login verification, security challenges, legal acknowledgements, payment or billing actions, unapproved domains, and irrecoverable blockers. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/forevercrab321-svg/browser-ops-high-autonomy) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON object with status, rationale, and next_action fields, accompanied by concise human-facing guidance when useful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Status must be one of DONE, BLOCKED, LOGIN_REQUIRED, SECURITY_CHALLENGE, LEGAL_REVIEW_REQUIRED, PAYMENT_REVIEW_REQUIRED, or DOMAIN_NOT_ALLOWED.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
