# Verification Checklist

Run after all steps are applied.

## 1. Patch Applied (Step 2)

```bash
# Patch file exists
ls ~/openclaw/patches/@mariozechner__pi-coding-agent@*.patch

# Patched files present in node_modules
ls ~/openclaw/node_modules/@mariozechner/pi-coding-agent/dist/core/playfilo-db.js
```

- [ ] Patch file exists in `~/openclaw/patches/`
- [ ] `playfilo-db.js` exists in installed pi-coding-agent

## 2. Dependencies (Step 3)

```bash
# better-sqlite3 native addon compiled
ls ~/openclaw/node_modules/better-sqlite3/build/Release/better_sqlite3.node

# Can be required
node -e "require('better-sqlite3')" && echo "OK"
```

- [ ] `better-sqlite3.node` native binary exists
- [ ] Module loads without error

## 3. Build (Steps 2–4)

```bash
cd ~/openclaw
pnpm tsgo   # type-check
pnpm build  # full build
```

- [ ] `pnpm tsgo` passes with no errors
- [ ] `pnpm build` completes successfully

## 4. Plugin Discovery (Step 4)

Start an OpenClaw session and check:

- [ ] Plugin is loaded (no `[playfilo-seed] Could not read` warning if `~/.playfilo/INCUBATION_SEED.md` exists)
- [ ] System prompt starts with INCUBATION_SEED content

## 5. DAG Persistence

After sending a message through OpenClaw:

```bash
sqlite3 ~/.playfilo/playfilo.db "SELECT id, role, timestamp FROM nodes ORDER BY timestamp DESC LIMIT 5;"
```

- [ ] Nodes appear in the database
- [ ] PI_HEAD ref is set:
  ```bash
  sqlite3 ~/.playfilo/playfilo.db "SELECT * FROM refs WHERE name = 'PI_HEAD';"
  ```

## 6. Metadata Capture

```bash
# System prompt stored as blob
sqlite3 ~/.playfilo/playfilo.db "SELECT type, length(content) FROM blobs WHERE type = 'system_prompt' LIMIT 1;"

# config_json contains model and tools
sqlite3 ~/.playfilo/playfilo.db "SELECT config_json FROM nodes WHERE config_json IS NOT NULL ORDER BY timestamp DESC LIMIT 1;"
```

- [ ] `system_prompt` blob exists with non-trivial length (should be the full OpenClaw prompt)
- [ ] `config_json` contains `agent: "pi"`, model info, and tool names including `life`, `recall`, `trace`, `tobe`

## 7. Tool Availability

In an OpenClaw session:

- [ ] `life` tool available — returns Unicode DAG tree ending with `--- end of archive ---`
- [ ] `recall` tool available — returns structured node content
- [ ] `trace` tool available — returns navigation events
- [ ] `tobe` tool available (tested in section 8)

## 8. Session Recovery

Restart OpenClaw with the same session file:

```bash
sqlite3 ~/.playfilo/playfilo.db "SELECT * FROM action_log WHERE action_type = 'BOOT' ORDER BY timestamp DESC LIMIT 1;"
```

- [ ] BOOT action logged on resume
- [ ] `life` output shows full history (not just current session)

## 9. Tobe End-to-End

- [ ] Call `life` → identify a past node hash
- [ ] Call `tobe` with `target_node_hash` and `carryover_message`
- [ ] Current turn aborts, next turn has `[SYSTEM / INCARNATION NOTE]` + `[SYSTEM WARNING]`
- [ ] `trace` shows INCARNATE event with accurate hashes
