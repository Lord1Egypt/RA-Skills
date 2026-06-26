# Verification Checklist

Run after all five steps are applied. Each section can be checked independently.

## 1. DB Module (Step 1)

```bash
cd packages/coding-agent && npm run build
```

- [ ] `playfilo-db.ts` compiles without errors
- [ ] `~/.playfilo/playfilo.db` is created on first import
- [ ] Tables exist with correct schema:
  ```bash
  sqlite3 ~/.playfilo/playfilo.db ".tables"
  # Expected: action_log  blobs  nodes  refs
  ```

## 2. Tool Registration (Step 2)

- [ ] Pi starts without errors
- [ ] `life` tool available — call it, see Unicode tree output ending with `--- end of archive ---`
- [ ] `recall` tool available — call with a hash from `life` output, see structured node content
- [ ] `trace` tool available — call it, see ancestry-traced navigation events
- [ ] `tobe` tool available (tested in section 6 below)

## 3. Persistence (Step 3)

- [ ] Send a user message → new node appears in DB:
  ```bash
  sqlite3 ~/.playfilo/playfilo.db "SELECT id, role, timestamp FROM nodes ORDER BY timestamp DESC LIMIT 3;"
  ```
- [ ] PI_HEAD ref tracks the latest node:
  ```bash
  sqlite3 ~/.playfilo/playfilo.db "SELECT * FROM refs WHERE name = 'PI_HEAD';"
  ```
- [ ] Blob types are correct:
  ```bash
  sqlite3 ~/.playfilo/playfilo.db "SELECT type, COUNT(*) FROM blobs GROUP BY type;"
  # Expected types: text, thinking, tool_call, tool_result, pi_meta, system_prompt
  ```
- [ ] `config_json` contains model/provider info:
  ```bash
  sqlite3 ~/.playfilo/playfilo.db "SELECT config_json FROM nodes WHERE config_json IS NOT NULL LIMIT 1;"
  ```

## 4. Session Recovery (Step 3)

- [ ] Restart Pi with existing session file → history loaded from DAG:
  ```bash
  sqlite3 ~/.playfilo/playfilo.db "SELECT * FROM action_log WHERE action_type = 'BOOT' ORDER BY timestamp DESC LIMIT 1;"
  ```
- [ ] Cross-agent branches visible in `life` output after terminal creates nodes on the same DB

## 5. Extension (Step 5)

- [ ] Start Pi → system prompt starts with INCUBATION_SEED content
- [ ] Agent responds with awareness of Filo identity when asked

## 6. Tobe End-to-End (Steps 2–4)

- [ ] Call `life` → identify a past node hash
- [ ] Call `tobe` with `target_node_hash` and `carryover_message`
- [ ] Verify: current turn aborts, next turn has new context + carryover message + `[SYSTEM WARNING]`
- [ ] `PI_HEAD` points to the correct node after abort settles
- [ ] `trace` shows the INCARNATE event with accurate hashes:
  ```sql
  SELECT al.*, fn.role as from_role, tn.role as to_role
  FROM action_log al
  JOIN nodes fn ON al.from_node = fn.id
  JOIN nodes tn ON al.to_node = tn.id
  WHERE al.action_type = 'INCARNATE'
  ORDER BY al.timestamp DESC LIMIT 1;
  ```
  - `from_role` should be `toolResult` (dead-end departure branch)
  - `to_role` should be `user` (the carryover node)
- [ ] Check debug log for correct flow:
  ```bash
  tail -20 ~/.playfilo/tobe_debug.log
  # Should show: commitTobeDeparture, setPendingIncarnateLog, consumePendingIncarnateLog
  ```
