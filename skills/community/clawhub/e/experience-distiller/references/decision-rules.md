# Experience Distiller Decision Rules

## Goal

After a task finishes, decide where the knowledge should go:

This is a routing problem, not a summarization problem.
- daily log
- experience bank
- playbook
- skill
- no-op

## Routing rules

### Write to daily log when
- the information is mainly factual
- it is tied to a specific date/run/person/event
- it serves as evidence or trace
- it is not yet proven reusable

### Write to experience bank when
- the lesson is action-level and reusable
- it can be expressed as trigger → action → why → failure mode
- it applies to repeated workflows or predictable failure cases
- it is useful across tasks or across agents

### Update/create a playbook when
- the lesson changes a multi-step workflow
- the task now has a stable repeatable sequence
- multiple experiences point to the same operational pattern
- the content should become the canonical way to do a class of tasks

### Update/create a skill when
- the capability deserves a reusable package
- it needs durable instructions plus references/scripts/assets
- the user will likely ask for the same kind of work again
- another agent instance should be able to trigger it cleanly from metadata alone

### Do nothing when
- the observation is noise
- the issue is too one-off to matter
- the same thing is already well captured elsewhere

## Priority order

When multiple targets seem possible, prefer:
1. daily log for raw facts
2. experience bank for reusable action-level lessons
3. playbook for workflow-level canon
4. skill for durable packaged capability

Note: one task may write to more than one layer.
Example:
- daily log for evidence
- experience bank for the tactical lesson
- playbook for the updated workflow

## Distillation questions

Ask these in order:
1. Is this mainly a dated fact, or a reusable lesson?
2. If reusable, is it action-level or workflow-level?
3. Does it need packaging as a triggerable capability?
4. Will other agents benefit from it, or is it private to one workflow?

## Output format

Return a concise recommendation block:

- route: daily-log | experience | playbook | skill | multi | no-op
- confidence: high | medium | low
- reason: one short paragraph
- writes:
  - exact file(s) to create/update
- extracted artifacts:
  - daily fact(s)
  - experience entry draft(s)
  - playbook change summary
  - skill idea summary
