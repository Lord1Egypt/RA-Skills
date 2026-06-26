# Notes for the OpenClaw Auto-Updater Skill

- This workspace skill intentionally replaces legacy Clawdbot/ClawdHub auto-update guidance with OpenClaw-native commands.
- Prefer gentle per-skill updates (`openclaw skills update <slug>`) when repeated `--all` runs are likely to hit ClawHub rate limits.
- Treat automatic OpenClaw core updates as opt-in, because changing the runtime is higher risk than updating skills.
- When the user wants summaries to return to the same conversation, prefer current-session binding over anonymous delivery.
- If a run hits `429 Rate limit exceeded`, say clearly that it is a ClawHub remote rate limit, not a local machine failure.
- If OpenClaw command surfaces change, update the examples in this skill to match local `openclaw ... --help` output.
