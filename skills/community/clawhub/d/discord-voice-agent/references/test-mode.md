# One-command test mode

## Goal

Give users one obvious command that confirms the skill is wired correctly before they try real voice.

## Command

```bash
npm run smoke
```

## What it should prove

- the bot starts
- the pipeline is wired
- the OpenClaw reply path is reachable enough for a simple prompt
- the runtime can produce a short test result without needing a live conversation

## Suggested follow-up

After smoke passes, run:

```bash
npm test
```

Then do one real voice check:

- `/status`
- `/say`
- one short voice turn
