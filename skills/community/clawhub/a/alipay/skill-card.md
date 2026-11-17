## Description:

Implement Alipay for web and mobile with signed request safety, gateway alignment, and production-ready payment operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to plan and implement Alipay checkout, subscription, PSP-mediated, validation, launch, and incident-response workflows for web and mobile payment integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment integration guidance can affect production charges, refunds, and rollout decisions.

Mitigation: Review payment, refund, and rollout changes before applying them, and keep production rollout gated on validation evidence.

Risk: Private keys, PSP secrets, or raw signed payloads could be exposed if shared in chat or stored in notes.

Mitigation: Do not paste secrets into chat, and store only short local notes, metadata, validation outcomes, and failure signatures.

Risk: Incorrect gateway, credential, callback, or idempotency handling can cause failed, fraudulent, or duplicate payment state transitions.

Mitigation: Use test mode until validation is complete, verify callback signatures, separate test and production credentials, and validate retry behavior with stable idempotency keys.

## Reference(s):

- [ClawHub Alipay Skill](https://clawhub.ai/ivangdavila/skills/alipay)
- [Skill Homepage](https://clawic.com/skills/alipay)
- [Alipay Global](https://global.alipay.com)
- [Alipay Production Gateway](https://openapi.alipay.com/gateway.do)
- [Alipay Sandbox Gateway](https://openapi-sandbox.dl.alipaydev.com/gateway.do)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with checklists, implementation notes, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local project notes under ~/alipay/ when the user approves setup.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
