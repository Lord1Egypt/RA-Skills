## Description: <br>
Autonomous Commerce enables agents to execute budget-limited physical e-commerce purchases with escrow protection, saved-account guardrails, and cryptographic proof. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pandeyaby](https://clawhub.ai/user/pandeyaby) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent developers use this skill when a user has explicit purchase intent, a budget, saved payment and delivery details, and escrow or payment confirmation for a physical retail order. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real orders using saved account, payment, wallet, and escrow authority. <br>
Mitigation: Install only after careful review; use a dedicated shopping account, isolated browser profile, low-limit payment method, low-balance wallet, strict merchant and budget limits, and manual approval immediately before checkout. <br>
Risk: Consent, proof, storage, and network boundaries may not be consistently enforced by the artifact. <br>
Mitigation: Require explicit user approval for each checkout, restrict allowed merchant domains, enforce budget limits outside the skill, and review proof before escrow release. <br>
Risk: Saved sessions, screenshots, and proof files may contain purchase or account data. <br>
Mitigation: Delete saved sessions, screenshots, and proof files after use, and redact personal information before sharing evidence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pandeyaby/autonomous-commerce) <br>
- [Public purchase proof post](https://moltbook.com/post/8cc8ee6b-8ce5-40d8-81e9-abf5a33d7619) <br>
- [ClawPay escrow integration post](https://moltbook.com/post/86ffca5e-c57b-497d-883d-688c29d6cf88) <br>
- [OpenAI Skills shell tips](https://developers.openai.com/blog/skills-shell-tips) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JavaScript examples and purchase-confirmation templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Completed purchases return order details, total amount, delivery estimate, escrow status, proof hash, and a local screenshot path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
