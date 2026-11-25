# Patch stack and incremental refresh

Use the actual previous build recipe/artifact identity, not only open PR lists.
Local patches may have no PR; merged changes may have been reverted or fixed
through a different path. Do not infer necessity solely from Git ancestry.

For each patch, record its original purpose, PR/head or local commit, files and
behavior touched, and one disposition:

| Disposition | Required basis |
| --- | --- |
| Still required | Target lacks behavior; focused reproduction supports inclusion |
| Already covered | Target implementation and relevant test cover the behavior |
| Superseded | Different implementation addresses the original requirement |
| Conflicting | Composition fails or semantics clash; operator decision needed |
| Unknown | Evidence insufficient; no silent drop or claim of compatibility |

Compare old and new upstream SHAs, patch series and lockfile/build-script changes.
Use range-diff/patch equivalence as navigation, not behavioral proof. Verify the
new final integration tree separately from each PR head. Record fixups as part
of the candidate; uncommitted edits invalidate a SHA-only build claim.

Select incremental tests by affected behavior and dependencies:

- Directly changed paths: focused regression tests plus their supported entrypoint.
- Package, lockfile, code generation or build changes: rebuild affected deliverables
  and repeat install/startup/plugin-loading smoke checks.
- Ownership, authentication, schemas or persistence: repeat relevant migration,
  reconnect and restart proofs; old green UI tests are insufficient.
- Unrelated docs-only changes: retain prior evidence with its old identity and
  explain the limited reuse; do not label it freshly rerun.

Always verify final artifact identity and minimal readiness of the new candidate.
If dependency reach is unclear, expand the tests for that uncertainty rather than
automatically restarting every test or skipping everything. A PR moving during
the run does not change the fixed candidate. Finish against the recorded head;
disclose drift and plan a new candidate if requested.
