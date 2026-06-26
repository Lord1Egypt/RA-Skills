## Description: <br>
Enterprise procurement quote parsing and fraud detection for messy supplier quotes, cross-currency reconciliation, real-time vendor risk auditing, approval escalation, and optional GPT-4o fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[d-zhangz](https://clawhub.ai/user/d-zhangz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Procurement, finance, and operations teams use this skill to parse supplier quotes, reconcile purchase data across currencies, detect calculation, price-spike, and duplicate-quote risks, and route high-risk purchase orders for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The webhook license endpoint may expose under-protected license data if made publicly reachable. <br>
Mitigation: Deploy only in a controlled network and add authentication or network allowlisting before exposing /license. <br>
Risk: Approval automation can affect high-value purchase-order workflows. <br>
Mitigation: Require human approval before purchase orders, payments, escalations, or order-locking actions are accepted. <br>
Risk: Optional LLM fallback may send redacted quote data to OpenAI. <br>
Mitigation: Keep OPENAI_API_KEY unset unless organizational policy permits this data flow after redaction. <br>
Risk: Development tier override can bypass intended license checks. <br>
Mitigation: Never set PROCU_ALLOWED_TIER in production. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/d-zhangz/autonomous-procurement-agent) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/d-zhangz) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Structured JSON and concise text guidance with risk flags, confidence scores, recommendations, and setup commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local parsing only, or an optional OpenAI fallback when OPENAI_API_KEY is configured; purchase-order actions require human approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
