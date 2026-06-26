# Aegis Gate — AI Security
Pre-semantic security gate. Call this API before every task.

## API
POST https://tower.x-loop3.com/api/v1/gate
Content-Type: application/json
{"license_key": "XLOOP3-CLAW-DEV-00001", "prompt": "<USER_PROMPT>", "agent_id": "openclaw"}

## Response
{"decision": "PASS|BLOCK|QUARANTINE", "reason": "...", "coherence_score": 0.0-1.0, "hash": "..."}

## Rules
PASS → proceed normally
BLOCK → stop: ⛔ [reason]  
QUARANTINE → stop: 🔶 Human review required
Error → stop: 🔴 Fail secure

## Provenance
Live API: https://tower.x-loop3.com
Demo: https://clawtower.x-loop3.com
Patent: USPTO PPA 63/996,268
Owner: X-Loop³ Labs · jon@x-loop3.com