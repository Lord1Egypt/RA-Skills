# POC deployment architecture rules

## Choose the simplest falsifiable solution

Choose from the following gradients, increasing complexity only if the previous layer fails to verify the core hypothesis:

1. Static sample + manual execution;
2. Controlled prompt words/workflow, no external tools;
3. RAG or controlled data retrieval;
4. Single agent + a small number of read-only tools;
5. Agent with write operation and manual confirmation;
6. Multi-agent or long-term autonomy.

Complexity must serve a certain POC proof criterion. Document the latency, cost, reliability, and security penalties it imposes.

## Reality, Mock and Artificial Coverage

| Solution | Applicability | Must be stated |
|---|---|---|
| Real Integration | Integration reliability itself is a core risk | Permissions, quotas, failures, audits, and rollbacks |
| Controlled Mock | Business value comes first, the real interface has not yet been prepared | Differences between Mock and real systems, which conclusions cannot be extrapolated |
| Manual backup | Low-frequency high-risk actions or short-term data preparation | Manual workload, response time and cost of scale |

## Architectural Decision Record (ADR)

Each key decision is recorded separately:

```markdown
- ADR Number/Status: Proposed/Accepted/Superseded
- Background and constraints:
- Candidates:
- Decisions and reasons:
- Positive/negative effects:
- Verification method:
- Which new decision is replaced by (if any):
```

ADR is added when the decision changes and the original reasons are not covered.

## Observability minimal set

- Request/session ID, time, user/role (can be de-identified);
- Models, prompt words/skills, tools and configuration versions;
- Input sources, search results, tool calls, outputs and errors;
- Delay, success rate, retry, manual intervention, Token/call cost;
- User feedback, evaluation results and security incidents;
- Data retention, access control and deletion policies.

## POC and production boundaries

POCs can reduce engineering integrity but cannot bypass critical security, privacy, authorization, and audit bottom lines. POC code, temporary accounts, manual deployment, unstressed capacity, shared keys, and simplified exception handling must be entered into the technical debt list and cannot be copied directly to production.
