# 家庭作业番茄执行助手

A public-safe OpenClaw skill for parent-confirmed homework intake, Pomodoro execution, nightly completion checks, and reward approval.

Published on ClawHub as `family-homework-pomodoro@1.0.1`.

## What it does

This skill supports a simple family homework loop:

1. a parent sends same-day homework
2. the assistant records the homework as provided
3. the assistant confirms the homework start time with the parent
4. the assistant reminds the child to begin homework using a Pomodoro rhythm
5. the assistant checks completion status with the parent at night
6. the assistant asks the parent whether a reward is allowed if the day went well

## Why it exists

It is a reusable template for:

- family homework coordination
- parent-approved homework reminders
- simple Pomodoro-based execution
- public-safe OpenClaw skill examples

## File structure

```text
skills/
  family-homework-pomodoro/
    SKILL.md
    README.md
    agents/
      openai.yaml
```

`SKILL.md` is the main skill entrypoint. `README.md` is for human readers, and `agents/openai.yaml` provides UI metadata.

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
- public-safe family workflow demos
- local AI homework reminder prototypes

## Examples

### Parent example

- Parent: `Today the homework is math worksheet 3 and reading 2 pages.`
- Assistant: `Recorded as provided. What time should homework begin today?`
- Parent: `Start at 6:30 PM.`
- Assistant: `Understood. I will remind the child at 6:30 PM and use a 25/5 Pomodoro rhythm by default.`

### Child reminder example

- Assistant: `It is time to start homework now. Begin with one 25-minute study session.`
- Assistant: `After that, take a 5-minute break.`

### Reward approval example

- Assistant to parent: `The homework appears to be completed well. Would you like to allow a reward today?`
- Parent: `Yes, reward is allowed.`
- Assistant to child: `Nice work. Your parent approved a reward for today.`

## Support and customization

This skill is intended to stay public-safe and reusable. If you later want a
custom version, the natural extension points are:

- alternate reminder cadence
- multiple-child variants
- different reward approval flows
- richer local workflow metadata for a private deployment

For public use, keep the skill generic and non-identifying. For custom work,
handle requests separately from the public template so the shared version stays
clean and easy to reuse.

For a more detailed customization checklist, see
[CUSTOMIZATION.md](./CUSTOMIZATION.md).

For planned version notes, see [CHANGELOG.md](./CHANGELOG.md).

For the next structured release note, see [releases/1.0.1.md](./releases/1.0.1.md).

For a concise example pack, see [EXAMPLES.md](./EXAMPLES.md).
