# Test Cases Prompt

> Copy and paste this prompt into any AI chat window to generate test cases for the AI Company skill.

---

## Prompt

```
Generate comprehensive test cases for the AI Company unified skill (v1.1.0).
Cover all 16 departments and shared infrastructure.
```

## Code Template Tests

| ID | Template | Test | Expected |
|----|----------|------|----------|
| TC-TPL-01 | validate_input_schema | Valid schema | True |
| TC-TPL-02 | validate_input_schema | Invalid data | False |
| TC-TPL-03 | sanitize_user_query | "; rm -rf /" | Shell chars stripped |
| TC-TPL-04 | execute_safe_command | timeout=2, sleep 60 | Timeout error |
| TC-TPL-05 | format_output_json | Any content | ai_generated: true |
| TC-TPL-06 | retry_with_backoff | Fail twice, succeed | Returns on 3rd try |
| TC-TPL-07 | read_reference_file | /etc/passwd | None (blocked) |
| TC-TPL-08 | generate_trace_id | 10K IDs | All unique |
| TC-TPL-09 | check_rate_limit | 11 req/60s, limit=10 | 11th returns False |
| TC-TPL-10 | mask_sensitive_data | Email + IP | [EMAIL] + [IP] |

## Department Tests

| ID | Department | Test | Expected |
|----|-----------|------|----------|
| TC-GOV-01 | CEO | Crisis P0 escalation | Emergency protocol activated |
| TC-GOV-02 | COO | SLA breach detection | Breach protocol triggered |
| TC-GOV-03 | HQ | P0 message routing | <100ms delivery |
| TC-FIN-01 | CFO | Budget >$100K request | Board approval required |
| TC-FIN-02 | CRO | Circuit breaker L3 | Operations halted |
| TC-TEC-01 | CTO | Agent L5 operation | CEO sign-off required |
| TC-PLT-01 | Framework | L1 schema violation | FW_001 error |
| TC-SEC-01 | CISO | STRIDE missing category | Review incomplete |
| TC-SEC-02 | CLO | AIGC content unlabeled | CLO_005 error |
| TC-PEO-01 | CHO | Agent decommission | Knowledge extracted |
| TC-MKT-01 | CMO | RICE score >= 3.5 | Proposal proceeds |
| TC-QOP-01 | CQO | G3 CVSS >= 7.0 | REJECTED |
| TC-QOP-02 | PMGR | P0 task assigned | Drop everything |
| TC-INT-01 | Intel | P1 event detected | HQ notified within 1h |
| TC-INF-01 | Information | GPS unavailable | IP fallback |
| TC-TRN-01 | Translator | Legal translation | Human review required |

## AIGC Labeling Tests

| ID | Test | Expected |
|----|------|----------|
| TC-AIGC-01 | Output with explicit label | PASS |
| TC-AIGC-02 | JSON with ai_generated: true | PASS |
| TC-AIGC-03 | Output with no AI disclosure | FW_010 error |

---

*Copy-paste ready for any AI chat window.*