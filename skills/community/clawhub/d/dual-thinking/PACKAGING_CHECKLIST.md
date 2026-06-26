# Packaging Checklist

Before setting `PUBLISH_STATUS: Packaged`, confirm the archive includes:
- `SKILL.md`
- `CHANGELOG.md`
- `GOVERNANCE.md`
- `references/modes.md`
- `references/runtime-contract.md`
- `references/skill-review-mode.md`
- `references/skill-classes.md`
- `references/round-output-contract.md`
- `references/failure-handling.md`
- `references/patch-discipline.md`
- `references/convergence-rules.md`
- `references/weak-model-guide.md`
- `references/validator-schema.md`
- `references/examples.md`
- `references/reference-freeze.md`
- `references/reference-scenarios.md`
- `references/reference-release-checklist.md`
- `references/change-policy.md`
- `references/self-evolution-lens.md`
- `references/harvest-doctrine.md`
- `references/verification-evidence.md`
- `references/reference-test-log.md`
- `references/backlog-next-line.md`
- `tests/test_round_flow.sh`
- `tests/test_weak_model_shortcut.sh`
- `tests/test_reference_alignment.sh`
- `tests/test_multi_alternation.sh`
- `tests/test_rollback_on_validation_failure.sh`
- `tests/test_self_evolution_alignment.sh`
- `tests/fixtures/sample-round-block.txt`
- `tests/fixtures/weak-model-shortcut-round.txt`
- `tests/README.md`

Release checks:
- `python3 skills/skill-creator-canonical/scripts/quick_validate.py skills/dual-thinking`
- `python3 skills/skill-creator-canonical/scripts/validate_weak_models.py skills/dual-thinking`
- `bash skills/dual-thinking/tests/test_round_flow.sh skills/dual-thinking/tests/fixtures/sample-round-block.txt`
- `bash skills/dual-thinking/tests/test_weak_model_shortcut.sh`
- `bash skills/dual-thinking/tests/test_reference_alignment.sh`
- `bash skills/dual-thinking/tests/test_multi_alternation.sh`
- `bash skills/dual-thinking/tests/test_rollback_on_validation_failure.sh`
- `bash skills/dual-thinking/tests/test_self_evolution_alignment.sh`
- `test -s skills/dual-thinking/PACKAGING_CHECKLIST.md`
- `test -f skills/dual-thinking/.clawhubignore`
- `test -f skills/dual-thinking/CHANGELOG.md`
- `test -f skills/dual-thinking/GOVERNANCE.md`
- `node -e "const {listTextFiles}=require('/home/irtual/.npm-global/lib/node_modules/clawhub/dist/skills.js'); listTextFiles('/home/irtual/.openclaw/workspace/skills/dual-thinking').then(files=>{const hasReview=files.some(f=>f.relPath.startsWith('review/')); console.log(hasReview ? 'REVIEW_INCLUDED' : 'REVIEW_EXCLUDED'); process.exit(hasReview ? 1 : 0);});"`

Reference line checklist:
- active version target for this release step: `8.5.24`
- `SKILL.md` classified honestly as the active `reference-candidate`, `reference-verified`, or `reference-release` line for the current release step
- `GOVERNANCE.md` present for non-runtime policy/governance detail
- `references/round-output-contract.md` synced
- `references/validator-schema.md` synced
- `references/runtime-contract.md`, `references/self-evolution-lens.md`, `references/failure-handling.md`, `references/reference-scenarios.md`, `references/reference-release-checklist.md`, `references/verification-evidence.md`, and `references/reference-test-log.md` synced to the live inline current-date trend-grounding lock family
- required scenario tests recorded in `references/verification-evidence.md` and `references/reference-test-log.md`
- release/evidence/test surfaces explicitly cover `BLOCKED_STATE: current-date-trend-not-grounded`, the current-date trend-grounding recovery branch, the round-1 / round-2 internet-assisted minimum floor for in-scope current-date-sensitive work, and the self-evolution live-public-evidence requirement
- version strategy explicitly distinguishes the frozen `v8.5.9 reference-release` baseline from the active `v8.5.24` candidate/release line
