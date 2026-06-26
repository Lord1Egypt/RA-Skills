# FeedTo OpenClaw Skill

FeedTo now uses a persistent outbound realtime listener on the OpenClaw side.

## Setup

1. Install the FeedTo browser extension and sign in at <https://feedto.ai>.
2. In OpenClaw, run:
   ```bash
   clawhub install feedto
   ```
3. Paste your FeedTo API key when OpenClaw prompts for `FEEDTO_API_KEY`.
4. If needed, restart once:
   ```bash
   openclaw gateway restart
   ```

Get your API key at <https://feedto.ai/settings>.

## Transport

- Primary path: Supabase Realtime broadcast over an outbound websocket
- Local delivery: the listener writes feeds into a local inbox that the skill cron drains into chat
- Fallback: if realtime is unavailable, the listener backfills from `/api/feeds/pending`

## Debugging

```bash
# foreground listener
node scripts/realtime.mjs

# drain the local inbox
bash scripts/poll.sh

# inspect listener health, queue depth, and last error
bash scripts/poll.sh --status
```

Optional envs:
- `FEEDTO_DISABLE_REALTIME=1` forces polling fallback
- `FEEDTO_STATE_DIR=/path/to/state` overrides the local state directory
- `FEEDTO_HTTP_TIMEOUT_MS=15000` overrides request timeout for session/fallback calls
- `FEEDTO_MAX_LOG_BYTES=1048576` caps daemon log growth before local trimming
