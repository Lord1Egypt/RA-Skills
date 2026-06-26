---
name: encryptedenergy-uptime
description: Know the second your OpenClaw agent goes silent. Free hosted heartbeat monitor — every-minute pings, public status page, and email alerts when pings stop.
metadata:
  openclaw:
    emoji: "⚡"
    requires:
      env:
        - ENCRYPTED_ENERGY_API_KEY
    primaryEnv: ENCRYPTED_ENERGY_API_KEY
    homepage: https://encryptedenergy.com
---

## Encrypted Energy Uptime

Hosted dead man's switch for your OpenClaw agent. A unix cron runs `ping.sh` once a minute, which posts your gateway's `/health` payload to encryptedenergy.com. If pings stop arriving for the configured threshold (default 10 minutes), the user gets an email alert and the public status page flips to DOWN.

### Setup

1. Sign up at https://encryptedenergy.com.
2. Register an agent at https://encryptedenergy.com/agents/new — that page reveals a per-agent bearer token (the API key).
3. Schedule the ping via the user's system crontab. The gateway is **not** involved at run time — `ping.sh` is pure bash + curl, so don't route it through `openclaw cron add`:

   ```
   ( crontab -l 2>/dev/null; echo "* * * * * PATH=$HOME/.npm-global/bin:/usr/local/bin:/usr/bin:/bin ENCRYPTED_ENERGY_API_KEY=<paste-token> bash {baseDir}/scripts/ping.sh >/dev/null 2>&1" ) | crontab -
   ```

   The `PATH=$HOME/.npm-global/bin:…` prefix is required — `ping.sh` calls `openclaw health --json` and `openclaw status --json`, and crontab's default PATH won't find the openclaw binary. Adjust the PATH if openclaw lives elsewhere (run `which openclaw` to confirm).

The cron pings `http://localhost:18789/health` and POSTs the result to `https://encryptedenergy.com/api/v1/ping` every minute. Wait ~70 seconds and the agent's status page will flip to UP.

### Do not

- Do not modify the health data before sending
- Do not send health pings more frequently than every minute
- Do not expose the gateway port to the internet
- Do not route `ping.sh` through `openclaw cron add` — it dispatches via an agent harness and bills LLM tokens for what is just a curl POST
