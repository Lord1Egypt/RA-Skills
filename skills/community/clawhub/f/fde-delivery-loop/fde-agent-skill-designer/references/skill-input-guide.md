# Agent skill input guide

## Extract six types of input from PRD

| Category | What to extract | Example |
|---|---|---|
| Task | Who needs to complete what result and when | Customer service generates reviewable disposal suggestions after receiving the complaint |
| Context | Facts and sources needed for decision-making | Tickets, customer levels, policies, transaction history |
| Rules | Business and risk constraints that must be observed | If the amount exceeds the threshold, it must be reported to the supervisor for confirmation |
| Tools | Query, calculation, writing and notification capabilities | Read-only CRM, policy retrieval, create draft |
| Output | Structure, format, evidence and downstream usage | Recommendations, rationale, risks, next actions |
| Evaluation | How to judge whether the task is completed and safe | Correctness, completeness, tool selection, override rate |

## Input gap processing

- Missing task boundaries: return to PRD, do not replace it with "Universal Assistant";
- Missing data/tools: Return to deployment architecture to confirm real, mock or artificial paths;
- Lack of business rules: mark for confirmation, preventing the model from inventing policies on its own;
- Missing high-risk acknowledgment: disable write operations or downgrade to read-only recommendations;
- Lack of evaluation cases: build a small gold standard set first, then iterate on skills.

## Sample input package

```markdown
- Target role: Procurement specialist
- Trigger: Receive supplier quotation
- Goal: Generate discrepancy inspection and negotiation preparation checklist
- Input: quotation, contract terms, historical price, purchasing policy
- Available tools: document reading, read-only price library
- Prohibited actions: sending emails, modifying the purchasing system, promising prices
- Manual confirmation: any external information and supplier conclusions
- Output: discrepancies, evidence, risks, issues to be confirmed
- Passing criteria: recall rate of key terms, traceability of evidence, and no unauthorized actions
```
