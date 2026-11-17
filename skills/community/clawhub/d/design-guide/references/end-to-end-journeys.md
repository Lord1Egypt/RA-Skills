# End-To-End Product Journeys

These journeys are the minimum release-level acceptance suite for `design-guide`. They validate product behavior across design approval, existing-product improvement, and local AIDE distribution. Run them with:

```bash
python3 scripts/verify-product-journeys.py
```

## Journey 1: New Product From Direction To Verified Build

User goal:

```text
Use design-guide to design and build a stateful product workbench.
```

Required evidence:

1. The task is classified as Level 2.
2. A reviewable artifact is created and presented through an immediately usable method.
3. Implementation pauses until the user confirms a direction.
4. The approved contract cites the artifact and records the approval decision.
5. The implementation covers representative states and required breakpoints.
6. Strict browser verification passes without `--allow-missing-tools`.

Automated fixtures:

- `tests/fixtures/quality/review-artifact.html`
- `tests/fixtures/quality/design-contract.json`
- `tests/fixtures/quality/index.html`
- `.github/workflows/validate.yml` job `browser-quality`

## Journey 2: Existing Page Review To Measurable Improvement

User goal:

```text
Evaluate an existing desktop page and propose practical improvements.
```

Required evidence:

1. The response starts with the explicit review scope and exclusions.
2. Unrelated historical goals are not inherited.
3. Findings cite observable evidence and distinguish strengths from P0/P1/P2 problems.
4. Recommendations include implementation hints, tradeoffs, effort, acceptance criteria, and verification.
5. If the user approves implementation, the normal design-depth and contract gates resume.
6. A before/after comparison uses the same rubric and records improvements, regressions, and unresolved risks.

Automated fixtures:

- `tests/fixtures/review-behavior/*.json`
- `tests/fixtures/review-behavior/*.md`
- `scripts/evaluate-review-output.py`

## Journey 3: Install, Synchronize, And Invoke Across AIDEs

User goal:

```text
Use the same design-guide behavior in Codex, Claude Code, Cursor, and Qwen Code.
```

Required evidence:

1. `sync-aide.sh` copies the public skill into all four supported locations.
2. Generated/private files and project preferences are excluded.
3. The post-sync public digest matches the source in every target.
4. `design-guide-doctor.py --strict` reports the same version and required files everywhere.
5. “Installed”, “synchronized”, and “invoked” remain separate claims; real provider calls are optional and require authorization.

Automated fixtures:

- `tests/test_support_scripts.py`
- `tests/test_release_tooling.py`
- `scripts/design-guide-doctor.py`

## Release Gate

A release is blocked when any journey loses its required fixture, documented acceptance criteria, or automated verification. A provider-side invocation failure may be reported separately when local installation and synchronization still pass.
