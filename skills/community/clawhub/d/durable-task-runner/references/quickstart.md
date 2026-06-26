# Quickstart

Use this reference after the skill triggers and you need a concrete working pattern.

## Minimal durable task

Create a task before the real work starts:

```bash
python3 scripts/task_ctl.py create demo-task \
  --title "Demo task" \
  --goal "Finish a multi-step task without losing state" \
  --done-criteria '["output produced","verification complete"]' \
  --constraints '["non-destructive"]' \
  --desired-state running \
  --execution-priority tokens \
  --phase planning \
  --health healthy \
  --next-step "break work into milestones" \
  --milestones '[
    {"id":"m1","title":"Plan","status":"running","percent":25},
    {"id":"m2","title":"Execute","status":"pending","percent":0},
    {"id":"m3","title":"Verify","status":"pending","percent":0}
  ]'
```

## Progress checkpoint

Record concrete progress without asking permission to continue:

```bash
python3 scripts/task_ctl.py progress demo-task \
  "baseline recorded; executing first bounded slice" \
  --phase execution \
  --health healthy \
  --next-step "verify the first slice"
```

## Verification + completion

Do not mark completion until verification is explicit:

```bash
python3 scripts/task_ctl.py event demo-task verification_passed \
  --phase verification \
  --details '{"check":"output exists and was reviewed"}' \
  --progress-note "verification passed"

python3 scripts/task_ctl.py update demo-task \
  --desired-state completed \
  --phase complete \
  --last-verified-step "output exists and was reviewed" \
  --next-step "none" \
  --progress-note "task completed"
```

## Restart / continue flow

After interruption, reset, or reboot, prefer the explicit recovery move:

```bash
python3 scripts/task_continue.py
```

Or target a specific task directly:

```bash
python3 scripts/task_continue.py --task-id demo-task
```

When you need to inspect the decision surface manually:

```bash
python3 scripts/task_resume_bootstrap.py --task-id demo-task --plan
python3 scripts/task_resume_apply.py --file /tmp/demo-task-plan.json
```

Use `task_resume_apply.py` only when the plan is clearly low-risk and resumable.

## Subagent/controller pattern

When parallelism is worth it:

1. assign or prepare a line with `task_subagent_ctl.py` or `task_subagent_run.py`
2. give the worker the structured return protocol from `references/subagent-return-protocol.md`
3. ingest the worker return
4. run the dropped-line check before ending the turn

## Smoke checks

Use these before calling the system healthy:

```bash
python3 scripts/task_validation_smoke.py
python3 scripts/task_core_smoke.py
```
