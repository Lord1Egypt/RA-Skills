## Description: <br>
Implement Apple Pay for web and iOS with merchant validation, token handling, and production-safe checkout flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to plan and implement Apple Pay checkout, subscription, and PSP-mediated payment flows with merchant setup, token-safety, validation, rollout, and incident-handling guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive Apple Pay tokens, private keys, or certificate material could be exposed during implementation or troubleshooting. <br>
Mitigation: Forward payment tokens only to the backend or PSP, never store raw token payloads in notes or logs, and do not ask users to paste private keys into chat. <br>
Risk: Production checkout could fail if merchant IDs, certificates, domains, sandbox credentials, or production credentials are misconfigured. <br>
Mitigation: Validate merchant prerequisites and keep sandbox and production credentials separated before recommending rollout. <br>
Risk: Retries without stable idempotency keys can cause duplicate authorizations or payment reconciliation errors. <br>
Mitigation: Require idempotency and reconciliation for authorization, capture, refund, and void operations before enabling retry behavior. <br>
Risk: Apple Pay unavailability or elevated failures can reduce conversion if no fallback path exists. <br>
Mitigation: Require fallback checkout, failure observability, alerting, and rollback or kill-switch criteria before production release. <br>


## Reference(s): <br>
- [ClawHub Apple Pay Skill Page](https://clawhub.ai/ivangdavila/apple-pay) <br>
- [Apple Pay Skill Homepage](https://clawic.com/skills/apple-pay) <br>
- [Apple Pay Production Gateway](https://apple-pay-gateway.apple.com) <br>
- [Apple Pay Certificate Gateway](https://apple-pay-gateway-cert.apple.com) <br>
- [Apple ID](https://appleid.apple.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with code, shell commands, checklists, and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local project notes under ~/apple-pay/ and requires curl, jq, and APPLE_PAY_MERCHANT_ID for diagnostics.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
