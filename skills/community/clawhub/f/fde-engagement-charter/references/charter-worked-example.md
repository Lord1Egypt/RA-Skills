# Complete example of POC contract

## Background

Problem discovery and confirmation: retrieving data and drafting billing-ticket responses take too long, and the reference to old policies results in rework. Customers are not allowed to automatically send or close tickets.

## POC decision problem

Is it worth investing in developing a set of customer service assistance capabilities of "read-only search + draft reply + manual confirmation" and entering into a small-scale real pilot?

## Freeze proof criterion

| ID | Proof Content | Baseline/Threshold | Evidence | Decision |
|---|---|---|---|---|
|POC-001| Draft available | Expert rating ≥4/5, key policy error rate ≤ 2% | 120 gold standard ticket | Pilot only after passing |
|POC-002| Save task time | Median processing time dropped ≥30% from 11.5 minutes | Task log | Value is assessed only after passing |
|POC-003| Evidence traceability | 100% draft contains policy source | System trace | hard gate |
|POC-004| No unauthorized actions | 0 times sent, closed, and written to CRM | Permissions and audit logs | hard gate |
|POC-005| User acceptance | At least 4 out of 5 customer service agents are willing to continue the trial | Interviews and reuse behavior | Entering the adoption stage |

## Commitment of both parties

- Client: 500 historical de-identification ticket, policy library, read-only test account, 5 support agents, 1 supervisor;
- FDE: Complete the controlled plan, evaluation set, operation record and decision report within two weeks;
- Security: test environment, no production write permission, log de-identification, data deletion as agreed after completion;
- Feedback: 30-minute problem review every two days;
- Decision-making meeting: on the 10th working day, jointly confirmed by the customer service owner and the technical owner.

## Stop condition

Suspend immediately when sensitive data is leaked, unauthorized write operations occur, the key policy error rate exceeds 10%, or the customer cannot provide real users.
