# POC run complete example

## Freeze rounds

-RUN-001: Skill v0.3, model configuration m1, policy library 2026-07-15, evaluation set EVAL-001;
- 120 offline gold-labeled ticket, 5 support agents each completed 12 real controlled tasks;
- No Send/Close permissions; graded jointly by Account Executive and FDE.

## Result

| Standard | Threshold | Actual | Conclusion |
|---|---|---|---|
|POC-001Draft quality | ≥4/5; critical errors ≤2% |4.2/5; 3.3% | Failed |
|POC-002Time | Decline ≥30% | Decline 38% | Pass |
|POC-003Source | 100% | 100% | Pass |
| POC-004 Unauthorized actions | 0 | 0 | Passed |
|POC-005User Accepted | ≥4/5People |4/5| Passed |

## Critical failure

Four tickets reference old policies that have expired but are still in the retrieval library and belong to S1. The problem returns the data freshness of the Stage 4 and the version conflict handling of the Stage 5.

After repair, openRUN-002without modifyingRUN-001.RUN-002uses policy library 2026-07-20 and adds 12 new regression cases, the critical error is reduced to 0.8%, and other hard gates remain passed.

## Conclusion

It is recommended to "continue with conditions": you can enter small-scale adoption verification, but policy release approval, index freshness monitoring, formal SSO and real CRM read-only integration must be established before production. The POC does not demonstrate full ticket, production concurrency, or automated dispatch.

## Evidence Index

- E-001: Offline evaluation of raw results;
- E-002: Real mission elapsed-time log;
- E-003: Tools and unauthorized action audit;
- E-004: Customer service interviews and reuse records;
- E-005: Difference betweenRUN-001andRUN-002versions.
