# Setup Commands (reference only)

Use these if you prefer to run the install manually yourself.

## Install skill + guard
```bash
clawhub install dr-session-cleaner
cd skills/dr-session-cleaner
./scripts/install_guard.sh \
  --target <operator-notification-target> \
  --interval 15 \
  --threshold 0.8 \
  --channel discord \
  --state "$HOME/.openclaw/session-guard/state.json" \
  --log "$HOME/.openclaw/session-guard/guard.log" \
  --cooldown 60
```

## Run once without cron (health check)
```bash
cd skills/dr-session-cleaner
python3 scripts/session_guard.py \
  --target <operator-notification-target> \
  --threshold 0.8 \
  --channel discord \
  --state "$HOME/.openclaw/session-guard/state.json" \
  --cooldown-min 60
```
Replace `<operator-notification-target>` with the provider-valid target held in this agent's protected local manifest. Do not record a real target in this shared skill or its setup instructions.
