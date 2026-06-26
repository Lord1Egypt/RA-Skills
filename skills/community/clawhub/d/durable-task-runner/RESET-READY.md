# RESET-READY.md

Project: durable-task-runner

## Reset-safe checkpoint

Current bootstrap task:
- `state/tasks/durable-task-runner-bootstrap.json`
- phase: `prototype-validation`
- milestone: `m9` running (~55%)
- next step: `add repeatable smoke script, then judge whether prototype validation is complete`

Validation task created and preserved:
- `state/tasks/validation-durable-flow.json`
- proves non-bootstrap restart/apply flow on a separate durable task

## First move after reset

Inside `shared/durable-task-runner`:

```bash
python3 scripts/task_resume_bootstrap.py --task-id durable-task-runner-bootstrap --plan
```

If the output is clean/resumable, apply it with:

```bash
python3 scripts/task_resume_bootstrap.py --task-id durable-task-runner-bootstrap --plan > /tmp/dtr-bootstrap-plan.json
python3 scripts/task_resume_apply.py --file /tmp/dtr-bootstrap-plan.json
```

## Expected immediate follow-up work

1. Re-run validation via `python3 scripts/task_validation_smoke.py`
2. Decide whether milestone 9 is complete or whether one meaningful gap still remains
3. Keep the next gap small and evidence-driven if one shows up

## Notes

- Resume/bootstrap low-risk flow is implemented and validated.
- Non-bootstrap validation already passed once on `validation-durable-flow`.
- Do not overcomplicate the next step; the point is repeatability and honest validation, not a new subsystem.
