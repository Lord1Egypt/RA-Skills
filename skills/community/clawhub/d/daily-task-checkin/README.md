# 日常任务打卡助手

A public-safe OpenClaw skill for task intake, reminder flow, nightly completion checks, and reward or follow-up approval.

Published on ClawHub as `daily-task-checkin@1.0.2`.

## What it does

This skill supports a simple daily task loop:

1. receive a task list from the sender
2. record the task list as provided
3. confirm the start time before reminders
4. send short reminders during the day
5. check completion status at night
6. ask whether a reward or follow-up note is allowed

## Why it exists

It is a reusable template for:

- daily task coordination
- parent-approved or operator-approved reminders
- short reminder-based execution
- public-safe OpenClaw skill examples

## File structure

```text
skills/
  daily-task-checkin/
    SKILL.md
    README.md
    examples/
      sender-example.md
      reminder-example.md
      completion-example.md
    agents/
      openai.yaml
```

`SKILL.md` is the main skill entrypoint. `README.md` is for human readers, `examples/` contains the copyable message flows, and `agents/openai.yaml` provides UI metadata.

## Safety boundaries

Keep this skill public-safe:

- no real names
- no school names
- no group IDs or account IDs
- no private schedules tied to identity
- no sensitive personal or health information

## Where to use it

- OpenClaw local skill library
- community skill examples
- public-safe task workflow demos
- local AI reminder prototypes

## Examples

### Sender example

- Sender: `Today the tasks are desk cleanup, reading, and math review.`
- Assistant: `Recorded as provided. What time should the reminder flow begin today?`

### Reminder example

- Assistant: `It is time to start the task list now. Begin with one short focus block.`
- Assistant: `After that, take a brief break before the next task.`

### Completion example

- Assistant: `The task list appears to be complete. Would you like to allow a reward or follow-up note today?`

For the full example files, see [examples/](./examples/).
