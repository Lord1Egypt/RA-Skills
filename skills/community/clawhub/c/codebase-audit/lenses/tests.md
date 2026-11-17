# Test strength

Fires: always

Leading word: **red**. A test earns its place by going red on a regression, and only then.

Run the suite first and record the result. Revert every mutation you make: `git status` shows no source changes at the end.

Artifact: a survivor list (mutation or deletion that no test caught) and a classification table (test → class → action).

- **delete-test** (when there is a test suite): On each critical module, delete or stub function bodies and branches one at a time and run the tests. What can be deleted with no test failing? That code is dead or untested.
- **mutation** (when there is a test suite): Flip comparisons, boundaries (`<` to `<=`), booleans and early returns on the critical modules. Use the stack's mutation tool if one is installed (Stryker, mutmut, PIT, cargo-mutants, go-mutesting, Muter); otherwise make 10 to 20 hand mutations on the riskiest lines.
- **classify** (when there are tests): Give every test in scope one class and its action:
  - *Repeats the implementation*: it checks the same interpretation against itself. Remove.
  - *Tied to internals*: it breaks when the code changes but behavior does not (private methods, call counts on internal collaborators, exact SQL, whole-tree snapshots). Rewrite against behavior.
  - *Cannot fail*: no assertion, asserts a mock returns what it was told, swallows the assertion, or passes whatever the code does. Remove.
  - *Disabled*: skipped or ignored. Name the requirement it hides; fix it or delete it with that reason.
  - *Flaky*: real sleeps, wall-clock time, network, shared state, order dependence. Inject the clock or the boundary.
  - *Earns its place*: goes red on a real regression. Keep.
- **critical-gaps**: Each critical path no test exercises end to end through its public interface.
- **contract** (when a client and a server ship separately): Tests that pin the shapes they exchange (schema snapshots, contract tests, generated types checked in CI), so a server change that would break the shipped client fails a build instead of a user.
- **property-candidates**: Invariants a property-based or fuzz test would check better than examples: encode/decode round trips, idempotent operations, counters that never go negative, parsers fed arbitrary input.

Done: every critical module went through delete-test and mutation, and every test in scope has a class and an action.
