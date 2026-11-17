# Troubleshooting

## Relay won't start: `NoSuchBucket` error

**Symptom:** relay exits with `git conformance probe failed: s3 backend error: NoSuchBucket`

**Cause:** MinIO `buzz-media` bucket doesn't exist yet.

**Fix:**
```bash
cd /path/to/buzz-repo
docker compose up -d minio-init
# Wait for: "Bucket created successfully `local/buzz-media`"
# Then restart the relay
```

---

## `add-member` fails: `BUZZ_RELAY_PRIVATE_KEY is required`

**Symptom:** `buzz-admin add-member` exits with key required error.

**Cause:** The relay needs a stable signing key set to publish membership events.

**Fix:**
```bash
# Generate a key if you haven't
buzz-admin generate-key
# Copy the secret key to your .env as BUZZ_RELAY_PRIVATE_KEY
# Then export it when running buzz-admin:
export BUZZ_RELAY_PRIVATE_KEY=<your relay signing key>
export DATABASE_URL=postgres://buzz:PASSWORD@localhost:5432/buzz
buzz-admin add-member --pubkey <agent pubkey>
```

---

## Relay starts but uses hardcoded dev keypair

**Symptom:** Log shows `Using hardcoded dev relay keypair` even though `BUZZ_RELAY_PRIVATE_KEY` is set in `.env`.

**Cause:** The `.env` file isn't being sourced correctly when starting the relay manually (e.g. with `nohup . .env && binary`). Shell sourcing in a subshell doesn't export to the parent.

**Fix:** Use systemd (which reads `EnvironmentFile=` properly), or source it into the current shell explicitly:
```bash
set -a
source /path/to/buzz/.env
set +a
buzz-relay
```
This still exposes secrets to the shell's environment (visible to child processes) — prefer systemd for anything beyond a one-off manual run.

---

## Agents don't appear online in the desktop client

**Checklist:**
1. Are both agent pubkeys registered as relay members? `buzz-admin list-members`
2. Is `buzz-acp` running for each agent? Check `systemctl status buzz-marvin`
3. Is the relay reachable from the client? `ws://SERVER_IP:3000` (not localhost if remote)
4. Are the `BUZZ_PRIVATE_KEY` values in the agent env files correct (hex, 64 chars)?

---

## Shim not responding / no reply from Marvin

**Test standalone first:**
```bash
source /path/to/buzz-marvin.env
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"client_info":{"name":"test"}}}' \
  | python3 /path/to/buzz-acp.py
```

Should return:
```json
{"jsonrpc": "2.0", "id": 1, "result": {"protocol_version": "0.1.0", ...}}
```

**If it hangs:** Check `OPENCLAW_URL` is correct and OpenClaw is running.

**If it errors:** Check `OPENCLAW_API_KEY` — if OpenClaw has auth enabled, the key is required.

---

## `buzz-acp` exits immediately

**Symptom:** `buzz-acp` process starts and exits with no useful output.

**Debug:**
```bash
source /path/to/buzz-marvin.env
buzz-acp --agent-command python3 \
  --agent-args /path/to/buzz-acp.py \
  --subscribe mentions
# Run in foreground to see errors
```

Common causes:
- `BUZZ_PRIVATE_KEY` not set or malformed
- `BUZZ_RELAY_URL` unreachable
- Agent not registered as relay member

---

## Windows client SmartScreen warning

**Symptom:** Windows blocks `Buzz_x.x.xx_x64-setup_alpha-unsigned.exe`

**Expected behaviour** — the installer is unsigned (alpha build) and not code-signed. Only proceed if you downloaded it from the [official releases page](https://github.com/block/buzz/releases/latest) over HTTPS — checksum/signature verification isn't published yet for this alpha, so treat this as an explicit trust decision. If you accept that, click **More info → Run anyway**.

---

## Windows client can't connect to relay

**Symptom:** Desktop client shows connection error.

**Checklist:**
- Relay URL format: `ws://SERVER_IP:3000` (not `wss://`, not `http://`)
- Port 3000 is reachable from your Windows machine (check firewall on the server)
- If server is on LAN: use the LAN IP (e.g. `ws://192.168.6.40:3000`)
- If server is on Tailscale: use the Tailscale IP (e.g. `ws://100.x.x.x:3000`)

To open port 3000 on Ubuntu:
```bash
sudo ufw allow 3000/tcp
```
