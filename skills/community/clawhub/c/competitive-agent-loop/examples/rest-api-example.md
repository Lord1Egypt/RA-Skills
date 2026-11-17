# Example: REST API CRUD for Users

## Input
User request: "Create a RESTful API endpoint for user management with CRUD operations"

## Planner Analysis (main)
### Complexity Assessment
- new_technology_learning: 0.1 (FastAPI is familiar)
- integration_complexity: 0.2 (Standard REST patterns)
- data_model_changes: 0.3 (New users table)
- test_coverage_needed: 0.4 (CRUD requires full coverage)
- deployment_risk: 0.1 (Isolated service)
- complexity_multiplier: 1.1 (Simple task)

### Time Budget
- accepted_standards: 5 (create, read, update, delete, validation)
- dev_time: 5 x 3 x 1.1 = 16 min (round to 20 min with buffer)
- verify_time: 20 x 0.4 = 8 min
- total_budget: 28 min

## Sprint Contract
### Acceptance Criteria
| ID | Criterion | Verification |
|----|-----------|--------------|
| AC-001 | POST /users creates user, returns 201 + new object | curl test + response parse |
| AC-002 | GET /users returns array of users | curl test + JSON validation |
| AC-003 | PUT /users/:id updates user, returns 200 | curl test + DB check |
| AC-004 | DELETE /users/:id removes user, returns 204 | curl test + DB verify |
| AC-005 | Input validation returns 422 with error details | malformed input test |

## Execution Flow
### Phase A: Contract Negotiation (3 min)
1. main analyzes requirements, generates contract draft
2. spawn coder to review and propose additions
3. spawn checker to verify criteria are measurable
4. User approves final contract

### Phase B: Single Solution (Simple task, no competition needed)
1. spawn coder "Implement REST API per contract" (20 min)
   - Output: code diff + acceptance proof commands
2. push completion received
3. spawn checker "Verify each AC criterion, score 0-10" (8 min)
   - Output: {score, passed[], failed[], critique[]}
4. push completion received

### Phase C: Result Processing
If score >= 8 AND all criteria passed:
  -> spawn memowriter to document the sprint
  -> Task complete

If score < 8 OR some criteria failed:
  -> Iterate up to 5 times with coder fixes
  -> If still failing after 3 iterations, notify user for intervention
