# RELEASE.md

Release checklist for the development repo.

## Goal

Keep the repository useful for development while emitting a cleaner public-skill bundle for ClawHub.

## Verification

Run from repo root:

```bash
python3 scripts/task_validation_smoke.py
python3 scripts/task_core_smoke.py
python3 scripts/task_delivery_smoke.py
python3 scripts/task_tick_all.py
python3 scripts/prepare_publish.py
```

## Publish flow

1. Build the clean bundle:
   ```bash
   python3 scripts/prepare_publish.py
   ```
2. Review the output folder:
   ```bash
   find dist/durable-task-runner -maxdepth 3 -type f | sort
   ```
3. Review `CHANGELOG.md`, `STATUS.md`, and the top lines of `README.md` / `SKILL.md` so public copy and release notes are honest.
4. Publish from the clean bundle, not from the repo root:
   ```bash
   clawhub publish dist/durable-task-runner \
     --slug durable-task-runner \
     --name "Durable Task Runner" \
     --version 0.1.2 \
     --changelog "Refine public positioning for reset-safe long work, refresh release/status hygiene, and publish the 0.1.2 bundle with release history included."
   ```

## Notes

- The full repo intentionally contains dogfooding/project-history files that are not part of the preferred ClawHub publish surface.
- `scripts/prepare_publish.py` is the canonical way to build the publishable bundle.
- The publish bundle intentionally excludes runtime task state (`state/tasks/`) and other generated/local-history artifacts.
- The Python scripts are stdlib-only; no external Python dependencies are required.
- ClawHub auth is still a separate prerequisite (`clawhub login`).
