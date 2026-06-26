# Eval-First Loop Patterns

## The Core Loop

1. **Define evals** (before implementation)
   - Capability eval: "Can the system do the required task?"
   - Regression eval: "Does existing functionality still work?"

2. **Establish baseline** (run evals, capture failure signatures)
   - Record which tests pass, which fail
   - Document error patterns, edge cases that break
   - This is your benchmark

3. **Execute implementation** (code, test, debug)
   - Keep evals running during development
   - Treat failing evals as blocking issues

4. **Re-run evals post-implementation** (measure improvement)
   - Compare against baseline
   - Confirm regressions were avoided
   - Document any new failure patterns discovered

## Why It Matters

Eval-first execution prevents the "we think it works" trap. Evals force clarity:
- What does done look like?
- What could break?
- Are we actually measuring what we intended?

Without evals, code review becomes purely subjective. With evals, review can focus on deeper concerns: invariants, security, coupling, error boundaries.

## Example: Adding a Webhook Handler

**Capability eval:**
```python
def test_webhook_handler_processes_valid_event():
    handler = WebhookHandler()
    event = create_test_event(type="user.created", data={"id": 123})
    result = handler.process(event)
    assert result.success == True
    assert result.event_id == event.id
```

**Regression eval:**
```python
def test_existing_routes_still_work():
    # Verify /api/v1/users still responds
    # Verify /api/v1/billing still calculates correctly
    # etc.
```

**After implementation:** Both pass, regression tests still pass, new edge cases discovered and added to regression set.

## Anti-Pattern: "We'll test in staging"

Don't wait. Evals catch issues in seconds, not after deployment.
