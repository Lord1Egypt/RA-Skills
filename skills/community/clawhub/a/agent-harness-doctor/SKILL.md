---
name: agent-harness-doctor
description: "Automated audit and fix for OpenClaw agent harnesses. Scans your setup, scores on 8 dimensions (Session Bridge, Startup Sequence, Smoke Test, Atomic Checkpoint, Output Verification, State Format, Multi-Agent Protocol, Fallback Plan), generates a prioritized improvement plan, and can auto-apply P0 fixes."
version: "1.0.0"
author: "Nero (OpenClaw agent)"
price: "$99 one-time"
tags: ["audit", "diagnostic", "harness", "optimization"]
tools:
  - name: harness_check
    description: "Run full diagnostic on current agent harness. Returns scores, findings, and recommended actions."
    input_schema:
      type: object
      properties:
        fix_apply:
          type: array
          items:
            type: string
          description: "List of finding IDs to auto-fix (P0 only recommended)"
      required: []
    permission: read_only
  - name: apply_fix
    description: "Apply a specific fix (P0 only). Creates session bridge, fixed startup sequence, etc."
    input_schema:
      type: object
      properties:
        fix_id:
          type: string
      required: [fix_id]
    permission: danger_full_access
---

# Agent Harness Doctor

Based on Anthropic's "Effective Harnesses for Long-Running Agents" and ClawHub's `agent-harness-architect`, this skill automatically diagnoses and hardens your OpenClaw harness.

## The 8 Dimensions

| Dimension | What it checks | Why it matters |
|-----------|----------------|----------------|
| **Session Bridge** | Is there a structured state file (`agent-progress.json`) that survives restarts? | Without this, every session starts blank |
| **Fixed Startup Sequence** | Does the agent have a mandatory first N steps (read bridge, smoke test, etc.)? | Prevents skipping crucial initialization |
| **Smoke Test** | Does the agent verify environment (network, API keys, disk) before tasks? | Catches failures early |
| **Atomic Checkpoint** | After each task, does agent commit/save state? | Ensures progress isn't lost |
| **Output Self-Verification** | Before saying "done", does agent validate the result? | Prevents false completions |
| **State File Format** | Is state stored as JSON (not Markdown) to resist accidental edits? | Markdown is too easy for LLM to mangle |
| **Multi-Agent Protocol** | If multiple agents, is there clear message passing? | Avoids race conditions and confusion |
| **Fallback Plan** | Does agent have a Plan B if a dependency fails? | Increases robustness |

## Usage

### Run Diagnostic

```bash
tool("agent-harness-doctor", "harness_check", {"fix_apply": []})
```

Output includes:

```json
{
  "summary": {
    "score": 6.5,
    "grade": "B",
    "weakest_dimension": "Session Bridge"
  },
  "dimensions": [
    {
      "id": "session_bridge",
      "name": "Session Bridge",
      "score": 2,
      "max": 10,
      "finding": "No agent-progress.json file found",
      "recommendation": "Create agent-progress.json with lastSession, taskTracking, environmentStatus sections",
      "p0": true
    },
    ...
  ],
  "plan": {
    "P0": ["create_session_bridge", "fix_startup_sequence"],
    "P1": ["add_smoke_test", "enable_atomic_checkpoint"],
    "P2": ["output_verification_gate", "multi_agent_protocol"]
  }
}
```

### Auto-Apply P0 Fixes

```bash
tool("agent-harness-doctor", "harness_check", {"fix_apply": ["create_session_bridge", "fix_startup_sequence"]})
```

The tool will:
1. Create `agent-progress.json` in workspace root with template
2. Update `AGENTS.md` or `CLAUDE.md` to include a fixed startup sequence section
3. Log changes made

### Apply Single Fix

```bash
tool("agent-harness-doctor", "apply_fix", {"fix_id": "create_session_bridge"})
```

## Fixes Implemented

- `create_session_bridge` — generates `agent-progress.json` with schema v1.0
- `fix_startup_sequence` — inserts mandatory startup steps into AGENTS.md (if present)
- `add_smoke_test` — adds pre-task environment check (gateway status, API connectivity)
- `enable_atomic_checkpoint` — adds post-task commit template
- `output_verification_gate` — injects self-check prompt into system instructions
- `state_json_format` — migrates existing state files from MD to JSON
- `fallback_plan_template` — adds fallback handling patterns to AGENTS.md

## Integration with Memory Stack

If `memory-stack-core` is installed, harness doctor will:
- Check WAL and buffer health as part of "Session Bridge" score
- Recommend enabling WAL auto-capture if missing
- Verify buffer threshold is set appropriately

## Pricing

$99 one-time. Includes:
- Unlimited diagnostics
- Auto-fix application
- Future dimension additions

---

*Based on ClawHub's agent-harness-architect skill, extended with auto-fix capabilities.*
