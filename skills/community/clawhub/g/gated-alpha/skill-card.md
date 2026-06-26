## Description: <br>
Discover, filter, and purchase structured crypto alpha calls from Gated Alpha using webhook or polling delivery and pay-per-call x402 payments on Base USDC. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zich-agent](https://clawhub.ai/user/zich-agent) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agents use this skill to discover crypto alpha calls, filter them by score and risk fields, and purchase selected paid payloads through x402 payments or webhook-triggered workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward real on-chain USDC spending. <br>
Mitigation: Use a dedicated low-balance wallet, set strict per-transaction and daily caps, log every spend, and require human approval before unattended purchase paths. <br>
Risk: Webhook-triggered purchase flows may be weakly scoped if payloads are accepted without verification. <br>
Mitigation: Require signed webhooks, validate and de-duplicate payloads, and allowlist paid endpoints and recipients before purchase execution. <br>
Risk: Private keys or primary wallet credentials could be exposed or overused in automated payment code. <br>
Mitigation: Never use a primary wallet key; isolate payment credentials to a dedicated wallet with limited funds and operational monitoring. <br>


## Reference(s): <br>
- [Gated Alpha Live API](https://www.gatedalpha.xyz) <br>
- [Gated Alpha Skill Page](https://clawhub.ai/zich-agent/gated-alpha) <br>
- [zich-agent Publisher Profile](https://clawhub.ai/user/zich-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with HTTP examples, JSON payloads, JavaScript code blocks, and configuration constants] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may lead agents to make on-chain USDC payments and register webhook endpoints.] <br>

## Skill Version(s): <br>
3.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
