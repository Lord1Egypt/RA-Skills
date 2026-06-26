# QA Coverage Plan Template

This section of the Implementation Plan is written for the QA Engineer. It defines what to test, expected outcomes, and the definition of "done" for each feature. QA should be able to execute a full test pass using only this section and the acceptance criteria from the FE/BE specs.

## ID Convention

All QA items use the prefix `QA-` followed by a sequential number: QA-001, QA-002, etc.

---

## QA-S1: Test Scenarios by Requirement

For each SRS requirement, define test scenarios:

```
QA-001: [Test Scenario Name]
SRS Requirement: [SRS-XXX]
Spec Reference: [FE-XXX / BE-XXX — which spec section defines this behavior]
Type: Happy Path | Edge Case | Error Case | Security | Performance
Priority: P1 (must pass for release) | P2 (should pass) | P3 (nice to have)

Preconditions:
  - [system state required before test — e.g., "user is logged in as admin"]
  - [test data required — e.g., "at least 3 orders exist in the database"]

Steps:
  1. [action]
  2. [action]
  3. [action]

Expected Result:
  - [what should happen — be specific about UI state, API response, DB state]
  - [what should NOT happen — if relevant]

Acceptance Criteria Reference: [FE-AC-XXX / BE-AC-XXX]
```

### Coverage Requirements

Every SRS requirement must have at minimum:
- 1 happy path scenario (normal use, valid inputs, expected outcome)
- 1 error/edge case scenario (invalid input, unauthorized access, boundary condition)

High-complexity requirements (effort 5+ story points) should have:
- 2+ happy path scenarios covering different valid inputs
- 2+ error scenarios covering different failure modes
- 1 boundary/edge case scenario

## QA-S2: Test Categories

Organize test scenarios into these categories:

### Functional Tests
Tests that verify features work as specified. These are the bulk of the test plan.

### Integration Tests
Tests that verify components work together:
- FE calls BE endpoint and correctly handles the response
- BE writes to DB and returns correct data
- Third-party integrations send/receive data correctly

### Authentication & Authorization Tests
Verify access control:
```
QA-AUTH-001: Unauthenticated access to protected endpoint
  Steps: Call [endpoint] without a token
  Expected: 401 response

QA-AUTH-002: Insufficient role access
  Steps: Call [admin endpoint] with a user-role token
  Expected: 403 response

QA-AUTH-003: Expired token
  Steps: Call [endpoint] with an expired token
  Expected: 401 response, clear error message

QA-AUTH-004: Cross-user data access
  Steps: User A tries to access User B's [resource] by ID
  Expected: 403 or 404 (depending on spec — never return the data)
```

### Data Integrity Tests
Verify the database remains consistent:
- Required fields cannot be null
- Unique constraints are enforced
- Foreign key relationships are maintained
- Cascade deletes work as specified
- Concurrent operations don't corrupt data (where applicable)

### UI State Tests
Verify all component states render correctly:
- Loading state displays properly
- Empty state displays when no data exists
- Error state displays on API failure
- Data renders correctly in normal state
- Forms validate correctly on submit

## QA-S3: Manual vs. Automated Testing

Specify which tests should be manual and which should be automated:

```
Automated (run on every PR):
  - All API endpoint tests (status codes, response shapes, validation errors)
  - Authentication/authorization tests
  - Data integrity tests
  - Unit tests for business logic

Manual (run before release):
  - Full user flow walkthroughs
  - Visual/layout verification across breakpoints
  - Accessibility spot checks
  - Edge cases that require complex state setup
  - Third-party integration verification
```

Adjust this split based on project maturity and tooling availability.

## QA-S4: Test Data Requirements

Define what test data QA needs:

```
Users:
  - Admin account: [email/password — use test credentials]
  - Standard user account: [email/password]
  - User with no data (empty state testing)
  - User with large data set (pagination testing)

[Resource]:
  - Minimum: [N] records for list/pagination testing
  - Edge cases: [record with max-length fields, record with special characters, etc.]
  - Relationships: [records that reference each other for FK/cascade testing]
```

Note whether test data should be seeded automatically or created manually during testing.

## QA-S5: Definition of Done

A feature is considered "done" when:

1. All P1 test scenarios for the feature pass
2. All P2 test scenarios pass (or failures are documented and accepted by PM)
3. No critical or high-severity bugs remain open against the feature
4. The feature matches the acceptance criteria in the FE/BE spec
5. Code has been reviewed (PR approved)
6. No regressions introduced in existing features (regression test pass)

## QA-S6: Bug Report Format

When QA finds a bug, report it in this format:

```
Title: [Short, descriptive — what's wrong, not what was expected]
Severity: Critical | High | Medium | Low
SRS Requirement: [SRS-XXX]
Spec Reference: [FE-XXX / BE-XXX]
Environment: [browser, OS, or API client]

Steps to Reproduce:
  1. [exact steps]
  2. [exact steps]
  3. [exact steps]

Expected: [what should happen per the spec]
Actual: [what actually happens]
Evidence: [screenshot, error log, network trace]

Notes: [any additional context — does it happen consistently? Only on certain data?]
```

Severity guide:
- **Critical:** Feature is completely broken, data loss, security vulnerability. Blocks release.
- **High:** Feature partially broken, workaround exists but is unacceptable. Should block release.
- **Medium:** Feature works but with noticeable issues. Fix before release if time permits.
- **Low:** Cosmetic, minor UX issue. Can be deferred to next cycle.

## QA-S7: PR Review Checklist

When QA reviews a PR before merge:

```
[ ] Code changes match the spec section referenced in the PR description
[ ] No unrelated changes included (scope creep in the PR)
[ ] Error handling is implemented per the cross-cutting concerns spec
[ ] No hardcoded values that should be configurable
[ ] No console.log / debug statements left in production code
[ ] Tests are included for new functionality
[ ] Existing tests still pass
[ ] Acceptance criteria from the spec are met
```

If QA and the dev disagree on a PR issue, escalate to the Project Engineer. The engineer reviews against the Implementation Plan and makes the call.
