# Quick Start / 快速开始

## One-Command Smoke Test

```bash
# From the critical-debater-suite directory:

# 1. Initialize a test workspace
bash scripts/init-workspace.sh /tmp/test-debate "Should central banks adopt digital currencies?" 3

# 2. Verify workspace was created
ls -la /tmp/test-debate/
# Expected: config.json, evidence/, claims/, rounds/, reports/, logs/

# 3. Verify config
cat /tmp/test-debate/config.json | jq .
# Expected: topic, round_count=3, status=initialized

# 4. Verify round directories
ls /tmp/test-debate/rounds/
# Expected: round_1/ round_2/ round_3/

# 5. Verify empty stores
cat /tmp/test-debate/evidence/evidence_store.json
# Expected: []

# 6. Verify audit trail
cat /tmp/test-debate/logs/audit_trail.jsonl
# Expected: {"timestamp":"...","action":"workspace_initialized",...}

# 7. Test JSON validation
bash scripts/validate-json.sh /tmp/test-debate/config.json config
# Expected: OK: /tmp/test-debate/config.json validates against config

# 8. Test hash script
bash scripts/hash-snippet.sh "test snippet"
# Expected: SHA-256 hash string

# 9. Cleanup
rm -rf /tmp/test-debate
```

## Full Debate (via Claude Code)

```
debate "Should central banks adopt digital currencies?" --rounds 3 --depth standard
```

This triggers the full orchestration flow:
1. Workspace initialization
2. Broad evidence search (5 queries for standard depth)
3. 3 rounds of Pro/Con debate with Judge audit
4. Final bilingual report generation

## Full Debate (via Python Orchestrator)

```bash
# Initialize workspace first
bash scripts/init-workspace.sh ./debates/cbdc-test "Should central banks adopt digital currencies?" 3

# Run orchestrator
python3 scripts/debate_orchestrator_generic.py ./debates/cbdc-test "Should central banks adopt digital currencies?" 3
```

## Red Team Mode

```
red team this: "Our company should migrate all services to Kubernetes"
```

In red team mode:
- Con = Red Team (identifies risks)
- Pro = Blue Team (proposes mitigations)
