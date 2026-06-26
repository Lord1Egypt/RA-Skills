# Automation And Scheduling

This skill should ask for a dream review time before installation or activation.

## Pre-Install Prompt

Ask the user:

```text
What time should this bot run its daily dream review and cognitive consolidation? Please include timezone if different from the current environment.
```

Record the answer in `.cognitive-training/schedule.md`.

## Schedule File

```markdown
# Dream Schedule

Status: active | manual | paused
Time: HH:MM
Timezone: Area/City
Scope: thread | workspace | project
Last configured: YYYY-MM-DD

Prompt:
Run cognitive-self-training dream review. Read today's cognitive training files, randomly select an enabled dream style, write the result with exactly these top-level sections: Dream Review, Dream Recurrence Statement, Tian-Dao Deduction, Research Hypotheses, Tomorrow's Practice, Store Updates, Summary Narrative. Create due recall cards, update graph links, and propose tomorrow's strategy. Do not store secrets or raw private transcripts.
```

## Platform Mapping

Use the host platform's native scheduler.

- Codex Desktop: prefer a thread heartbeat when the user wants the review to continue in the current conversation.
- Codex Desktop cron: use when the user wants a separate recurring job against a workspace.
- OpenClaw: use its hook or scheduling mechanism if available; otherwise keep `schedule.md` and ask the user to configure the platform scheduler.
- Hermes or other bots: create an equivalent daily scheduled task with the prompt above.

## Safety

- Do not enable a schedule without user consent.
- Do not choose a hidden default.
- If the user skips time selection, set `Status: manual`.
- If the platform cannot create an automation, still write `schedule.md` and report the missing platform step.
