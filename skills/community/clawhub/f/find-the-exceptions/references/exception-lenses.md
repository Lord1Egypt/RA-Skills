# Exception Lenses

Use only lenses relevant to the process.

- Boundaries: exactly equal to threshold, zero, max/min, empty collection.
- Data quality: missing, invalid, stale, duplicate, conflicting, wrong unit.
- Timing: late, early, concurrent, replayed, out-of-order, timeout.
- Authority: absent approver, delegated authority, joint approval, revoked permission.
- Lifecycle: cancel, amend, reopen, retry, rollback, partial completion.
- Scope: jurisdiction, customer category, internal/external, special program.
- Dependency: system unavailable, source missing, API degraded, human non-response.
- Identity: ambiguous match, merged entities, renamed IDs, duplicate identities.
- Conflict: two rules apply, policy vs precedent, old vs new version.

After generating candidates, filter by whether the exception can materially change execution, decision, risk, or outcome.
