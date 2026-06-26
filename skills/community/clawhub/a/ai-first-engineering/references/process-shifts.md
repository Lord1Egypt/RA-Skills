# Process Shifts for AI-First Teams

## The Three Core Shifts

### 1. Planning Quality > Typing Speed

**Old model (human-centric):**

- Spec can be 60% clear; developer fills in ambiguities while coding
- Speed is measured by lines written per hour
- Learning happens during implementation

**AI-first model:**

- Spec must be 90%+ clear before implementation
- Speed is measured by iteration cycles (how many times do we rebuild?)
- Learning happens during planning and review

**Practical impact:**

- Spend 2-3x longer on specs, acceptance criteria, examples
- AI implementation becomes fast and predictable
- Reduces revision cycles (and thus total time)

### 2. Eval Coverage > Anecdotal Confidence

**Old model:**

- "Does it work?" → deploy to staging, test manually, ask team
- Risk: hard to catch regressions, individual biases affect review

**AI-first model:**

- "Does it work?" → run regression test suite, review evals
- Every touched domain gets regression coverage
- Edge cases explicitly tested, not assumed safe

**Practical impact:**

- Tests become visible, measurable risk signal
- "Feels right" is no longer acceptable
- Evals catch regressions before code review

### 3. Review Focus Shifts from Syntax to Behavior

**Old focus (syntax/style):**

- "This should use const, not var"
- "Inconsistent indentation"
- "Function name is unclear"
- → All handled by linters, formatters, type checkers

**New focus (behavior/risk):**

- "Does this handle the null case?"
- "What breaks if the database is down?"
- "Is user input validated before use?"
- "Could this cause a data race?"
- → Cannot be automated; requires human judgment

**Review checklist for AI code:**

1. Behavior regressions? (Run regression suite; are tests passing?)
2. Security assumptions? (Input validation, permissions, secrets)
3. Data integrity? (Constraints, atomicity, rollback)
4. Failure handling? (Network, database, timeout error paths)
5. Rollout safety? (Feature flags, backward compat, canary safe)

## Organizational Implications

**Hiring:** Look for engineers who can write clear specs and good evals, not just fast coders.

**Meetings:** Spend more time in planning/design meetings; less time in nitpicky code review.

**Culture:** "Move fast and break things" becomes "plan well and test thoroughly."

**Tools:** Invest in eval infrastructure, regression test suite, type checking — these are now your primary defense.
