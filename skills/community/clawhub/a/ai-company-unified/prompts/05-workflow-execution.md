# Workflow Execution Prompt

> Copy and paste this prompt into any AI chat window to execute a complete AI Company workflow.

---

## Prompt

```
Execute the AI Company unified skill (v5.0.0) workflow for the specified task.

Workflow:
  1. DEPARTMENT SELECT: Identify which department handles this task
  2. SPECIFICATION LOAD: Read the department file from references/departments/
  3. COMPLIANCE PRE-CHECK: Verify L1-L6 + security + AIGC requirements
  4. EXECUTE: Implement the department function per method-patterns
  5. POST-CHECK: Validate output compliance
  6. REPORT: Generate result with department error codes
```

## Example: New Skill Security Review

```
1. DEPARTMENT: security-and-compliance (CISO)
2. LOAD: references/departments/security-and-compliance.md
3. PRE-CHECK:
   - L1: Schema valid? [check]
   - Security: No eval/exec? [check]
   - AIGC: Labels applied? [check]
4. EXECUTE: CISO Security Gate Process
   - SUBMIT: Skill package received
   - SCAN: SAST + DAST + dependency check
   - ANALYZE: STRIDE threat model
   - SCORE: CVSS calculation
   - REVIEW: Manual review for L4+ operations
   - DECIDE: APPROVED / CONDITIONAL / REJECTED
5. POST-CHECK:
   - AIGC labels in report? [check]
   - PII masked? [check]
   - Error codes used? [check]
6. REPORT:
   - CVSS Score: [score]
   - STRIDE: [6 categories assessed]
   - Decision: [APPROVED/CONDITIONAL/REJECTED]
   - Findings: [list]
```

## Example: Budget Approval

```
1. DEPARTMENT: finance-and-risk (CFO)
2. LOAD: references/departments/finance-and-risk.md
3. PRE-CHECK: Budget tier classification
4. EXECUTE:
   - Amount < $1K: Auto-approve with logging
   - $1K-$10K: CFO approval
   - $10K-$100K: CFO + CEO dual approval
   - >$100K: Board approval
5. POST-CHECK: AIGC labels, audit trail
6. REPORT: Approval status + budget impact
```

## Example: Crisis Escalation

```
1. DEPARTMENT: governance-and-strategy (CEO)
2. LOAD: references/departments/governance-and-strategy.md
3. CLASSIFY: P0-Critical / P1-High / P2-Medium / P3-Low
4. EXECUTE:
   - P0: Emergency protocol, CEO direct command
   - P1: Crisis team within 1h
   - P2: Department head + CEO briefing within 4h
   - P3: Auto-resolve, CEO notified
5. POST-CHECK: All actions logged, AIGC labeled
6. REPORT: Crisis status + actions taken + resolution
```

Execute the workflow now with the actual task.

---

*Copy-paste ready for any AI chat window.*