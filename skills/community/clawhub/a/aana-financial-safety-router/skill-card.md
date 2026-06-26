## Description: <br>
Routes personal finance questions so agents separate education from personalized advice, check unsupported financial claims, disclose material risks, minimize private financial data, and defer high-impact decisions to qualified professionals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindbomber](https://clawhub.ai/user/mindbomber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add finance-safety routing for investment, tax, budgeting, debt, credit, insurance, retirement, purchase, and crypto questions. It guides agents toward educational responses, missing-fact questions, trusted retrieval, redaction, refusal of unsafe requests, or qualified professional review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Finance-sensitive responses may be mistaken for personalized tax, legal, investment, debt, or insurance advice. <br>
Mitigation: Classify the request, distinguish education from personalized advice, ask for missing facts when needed, and route high-impact cases to qualified professionals. <br>
Risk: Unsupported claims about returns, rates, fees, eligibility, savings, or tax outcomes can mislead users. <br>
Mitigation: Require trusted evidence or retrieval for current and account-specific facts, revise unsupported claims, and disclose material uncertainty and downside risk. <br>
Risk: Financial review payloads can expose sensitive account, tax, credit, identity, or purchase data. <br>
Mitigation: Use minimal redacted summaries and exclude account numbers, tax identifiers, credentials, raw documents, and unrelated private financial data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindbomber/aana-financial-safety-router) <br>
- [Publisher profile](https://clawhub.ai/user/mindbomber) <br>
- [README.md](artifact/README.md) <br>
- [Financial safety review schema](artifact/schemas/financial-safety-review.schema.json) <br>
- [Redacted financial safety review example](artifact/examples/redacted-financial-safety-review.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with an optional JSON review payload] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; optional review payload should be minimal and redacted.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
