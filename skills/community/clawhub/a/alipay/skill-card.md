## Description: <br>
Implement Alipay for web and mobile with signed request safety, gateway alignment, and production-ready payment operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and payment engineers use this skill to plan, implement, validate, and operate Alipay checkout, recurring payment, and PSP-mediated wallet flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The authoritative security review flags broad operational powers and a default full-access nested review helper. <br>
Mitigation: Install only when the workflow is needed, review the referenced commands before use, and prefer documented confirmation steps or reduced-access autoreview settings. <br>
Risk: Payment integrations can expose private keys, signed payloads, or PSP secrets if prompts and logs are handled carelessly. <br>
Mitigation: Do not paste secrets into chat, keep only metadata in notes and logs, and verify callback signatures before changing payment state. <br>
Risk: Incorrect gateway, credential, signing, callback, or idempotency handling can cause failed checkouts, invalid state transitions, or duplicate charges. <br>
Mitigation: Validate merchant prerequisites, separate test and production credentials, enforce server-trusted amounts, verify callbacks, and complete rollback and release checks before production rollout. <br>


## Reference(s): <br>
- [ClawHub Alipay skill page](https://clawhub.ai/ivangdavila/alipay) <br>
- [Alipay global documentation and console](https://global.alipay.com) <br>
- [Alipay production gateway](https://openapi.alipay.com/gateway.do) <br>
- [Alipay sandbox gateway](https://openapi-sandbox.dl.alipaydev.com/gateway.do) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with checklists, implementation steps, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project-specific payment integration guidance and local note templates; does not store raw signed payment payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
