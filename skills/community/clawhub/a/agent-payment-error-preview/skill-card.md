## Description: <br>
Free triage preview for x402/AP2/ACP/MPP/MCP agent-payment failures; routes hard cases to the paid Agent Payment Error Diagnoser ClawMart skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sebastiancoombs](https://clawhub.ai/user/sebastiancoombs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators troubleshooting agent-payment integrations use this skill to classify x402, AP2, ACP, MPP, MCP, and related payment failures from visible symptoms, apply an initial check, and decide whether deeper paid diagnosis is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment troubleshooting logs may contain private keys, wallet seeds, bearer tokens, payment headers, or authorization material. <br>
Mitigation: Redact secrets, payment headers, and authentication material before pasting logs or examples into an agent workflow. <br>
Risk: Repeated payment retries can reuse nonces, replay authorizations, or continue after permanent signature and scope failures. <br>
Mitigation: Use a bounded retry counter, refresh nonces and idempotency keys, and stop immediately when the error indicates a permanent signature or scope issue. <br>
Risk: Ambiguous cases are routed to a separate paid ClawMart diagnoser that is outside this preview skill. <br>
Mitigation: Review the paid diagnoser separately before installing, purchasing, or sending it diagnostic data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sebastiancoombs/agent-payment-error-preview) <br>
- [Paid Agent Payment Error Diagnoser Listing](https://www.shopclawmart.com/listings/agent-payment-error-diagnoser-adda0b18) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown troubleshooting checklist and triage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only preview; it makes no network calls by itself and asks users to redact secrets before sharing logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
