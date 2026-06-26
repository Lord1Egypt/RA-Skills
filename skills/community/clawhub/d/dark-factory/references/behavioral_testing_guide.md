# Behavioral Testing Guide

## Why Behavioral Tests Matter

Behavioral tests are the foundation of the dark factory. Unlike unit tests (which test implementation details), behavioral tests describe **what the software should do from the user's perspective**. They are written before any code is generated, which means they serve as both the specification and the acceptance criteria simultaneously.

A well-written behavioral test answers three questions: given this input, when this action occurs, what output should result? If you cannot answer all three clearly, the specification is not ready for execution.

## Writing Effective Behavioral Scenarios

### Structure

Every scenario in `behavioral_scenarios` requires three fields:

```json
{
  "scenario": "User submits a valid support ticket",
  "input": {
    "user_id": "user-001",
    "subject": "Login not working",
    "body": "I cannot log in since yesterday."
  },
  "expected_output": {
    "ticket_id": "ticket-XXXXXXXX",
    "status": "open",
    "priority": "medium",
    "assigned_to": "support-team"
  }
}
```

The `scenario` field should be a plain-English sentence that a non-technical stakeholder can read and verify. The `input` and `expected_output` should be concrete — avoid placeholders like `"ticket_id": "any string"`.

### Patterns

**Happy path** — the normal, expected flow with valid inputs. Always include at least one happy path scenario per feature.

**Edge cases** — boundary conditions, empty inputs, maximum values, minimum values. These are the scenarios most likely to reveal bugs.

**Error cases** — invalid inputs, missing required fields, unauthorized access. The expected output should be a well-defined error response, not a crash.

**State transitions** — if your feature involves state (e.g. a ticket moving from `open` to `resolved`), write scenarios for each valid transition.

### Example: Good vs. Poor Scenarios

**Poor scenario:**
```json
{
  "scenario": "Test the ticket system",
  "input": { "data": "something" },
  "expected_output": { "result": "ok" }
}
```
This is untestable. The scenario description is vague, the input is meaningless, and the expected output cannot be verified.

**Good scenario:**
```json
{
  "scenario": "Submitting a ticket with an empty body returns a validation error",
  "input": {
    "user_id": "user-001",
    "subject": "Login issue",
    "body": ""
  },
  "expected_output": {
    "error": "validation_error",
    "field": "body",
    "message": "Body cannot be empty"
  }
}
```
This is specific, testable, and describes a real edge case.

## Anti-Patterns to Avoid

**Vague descriptions** — "Test that it works" tells the test engine nothing. Be specific about the action and the expected result.

**Missing expected outputs** — an empty `expected_output: {}` means the test will always pass, which defeats the purpose.

**Testing implementation details** — behavioral tests should describe outcomes, not how the code achieves them. "Function X is called with parameter Y" is an implementation detail, not a behavior.

**Overlapping scenarios** — if two scenarios test exactly the same input/output combination, one is redundant. Consolidate them.

**Ignoring error paths** — happy-path-only specifications produce fragile software. Always include at least one error scenario per feature.

## Checklist

Before submitting a specification to the dark factory, verify:

- [ ] Every scenario has a clear, plain-English description
- [ ] Every scenario has concrete, non-empty `input` and `expected_output`
- [ ] At least one happy path scenario is included
- [ ] At least one edge case scenario is included
- [ ] At least one error case scenario is included
- [ ] `success_criteria.test_pass_rate` is set (recommended: 0.95)
- [ ] The specification passes `specification_validator.py` with zero errors

## Running Behavioral Tests

```bash
# Validate first
python specification_validator.py my_spec.json

# Run behavioral tests
python behavioral_test_engine.py my_spec.json

# Review the test report
cat my_spec_test_report.json | python3 -m json.tool
```

A pass rate below the target does not necessarily mean the code is wrong — it may mean the scenarios are ambiguous or the expected outputs are too strict. Review failed scenarios carefully before concluding there is a bug.
