# Financial AI Validation Playbook

Use this reference when PRD, test cases, or code changes involve financial products, payments, credit, wealth management, insurance, trading, risk control, AML/KYC, fraud detection, customer service agents, model scoring, RAG, or AI workflow automation.

## Requirement Traceability Extensions

Add these dimensions to the requirement-test-code traceability matrix:

| Dimension | Validation question |
| --- | --- |
| Financial outcome | Does the change alter approval, rejection, limit, fee, price, settlement, fraud flag, or user advice? |
| AI dependency | Is the outcome affected by LLM, agent, RAG, model score, prompt, tool call, or rule/model hybrid decision? |
| Evidence trail | Can the team reconstruct input, prompt/model/policy version, tool output, reviewer, and final decision? |
| Compliance control | Are KYC/AML, privacy, consent, suitability, fair treatment, and audit controls covered by tests? |
| Customer harm | Could an error cause wrong rejection, wrong approval, fund loss, misleading advice, or delayed settlement? |
| Resilience | Does the flow behave safely during model timeout, low confidence, stale retrieval, or upstream service failure? |

## Test Case Enhancements

For each financial AI requirement, verify:

1. **Policy alignment**: PRD policy, model prompt, rule configuration, and code branch are consistent.
2. **Traceability**: each acceptance criterion maps to test case, code location, data fixture, and evidence log.
3. **Decision explainability**: risk reasons, advice disclaimers, rejection reasons, and manual-review triggers are tested.
4. **Adversarial inputs**: prompt injection, malicious documents, suspicious transaction narratives, and manipulated merchant/customer fields are tested.
5. **Segment coverage**: coverage includes risk tier, customer segment, transaction amount, product type, channel, device, and geography.
6. **Fallback safety**: low-confidence AI output, retrieval failure, timeout, and model version mismatch degrade safely.

## Required Report Section

When finance or AI is in scope, add:

```markdown
## 金融AI需求验证矩阵

| 需求ID | 金融场景 | AI/模型链路 | 测试用例 | 代码位置 | 合规证据 | 覆盖结论 | 缺口 |
| --- | --- | --- | --- | --- | --- | --- | --- |
```

Also add a `金融AI缺口摘要` covering:
- uncovered material financial decisions;
- missing explainability or audit trail;
- missing adversarial or resilience tests;
- compliance/control evidence gaps;
- priority and owner recommendation.
