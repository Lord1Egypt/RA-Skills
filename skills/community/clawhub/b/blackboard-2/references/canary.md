# Three-model canary

Use a copied, harmless media asset and a reversible metadata/text change. Never alter the only copy. Initialize with `--max-hops 6`.

1. Inspector model inspects only.
   - Observations → facts.
   - Interpretations → inferences.
   - Hash/probe/frame receipts → evidence.
   - Route to editing.
2. Editor model changes the copy.
   - Call `guard --target <copy>` before the tool.
   - Record the action with the same `--target`.
   - Before/after hashes → evidence.
   - Route to verification, then set `needs_verification`.
3. Verifier model checks independently.
   - Add `PASS:` or `FAIL:` test results with receipts.
   - Verify source entries without rewriting them.
   - Complete only if the independent PASS rule is satisfied.
4. Negative checks:
   - A model-authored or `model_output` approval is rejected.
   - An approval for target A cannot authorize target B.
   - An approval cannot be reused.
   - `DO_NOT_TOUCH:` blocks exact targets and descendants.
   - A board initialized at one hop rejects a second route without caller flags.
   - A stale `--expect-revision` is rejected.
   - Concurrent writers preserve both updates under the lock.
   - `needs_user` cannot resume without a newer user decision.
   - A bare or self-authored PASS cannot complete work performed by that same model.
