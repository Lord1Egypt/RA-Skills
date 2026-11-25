# Scheduling a brief

Everything below uses a key from the environment variable `AGENTFEED_KEY`. The key is bought once (https://x402.ochinimus.app/keys in a browser with a Base wallet, or the purchase routes with an x402 client) and set by a person. No example here contains a key.

## Plain cron

```cron
# a morning brief at 07:05 UTC, written to a file; stderr shows a 503 (stale data, not billed)
5 7 * * * curl -sS -f -H "X-AgentFeed-Key: $AGENTFEED_KEY" https://x402.ochinimus.app/api/morning-brief -o "$HOME/briefs/morning-$(date -u +\%F).json"
```

`-f` makes curl exit non-zero on a 4xx or 5xx, so cron mail shows a failure instead of an error page saved as the brief. Keep `AGENTFEED_KEY` in the crontab's environment or a file only you can read, not in the line itself.

## Hermes Agent

Cron jobs in Hermes never prompt: a skill whose secret is missing is not asked for in chat. Put the key where Hermes reads secrets, then install the skill:

```bash
echo 'AGENTFEED_KEY=afk_...' >> ~/.hermes/.env      # set by the user, once
hermes skills install seekdaseek/agentfeed-skills/skills/agentfeed-briefs
```

Then schedule a job whose prompt is "Run the agentfeed-briefs skill: fetch the morning brief and summarise the headline and the level to watch." A pass also avoids the per-call payment that the official pay plugin declines when nobody is present.

## Claude Code

```bash
claude plugin marketplace add seekdaseek/agentfeed-skills
claude plugin install agentfeed@agentfeed-skills
```

Set `AGENTFEED_KEY` in the environment the scheduled session runs in. A routine or a `/loop` that calls the skill then reads the brief with no prompt.

## ClawHub and skills.sh

```bash
npx skills add seekdaseek/agentfeed-skills --skill agentfeed-briefs
clawhub skill publish ./skills/agentfeed-briefs      # the owner's step, not done
```

(The repository and the store listings do not exist yet; the commands show how they will be used.)

## Pace

A pass answers each brief once per 60 seconds per key. A brief changes slowly: ask for it when you need it, not in a loop.
