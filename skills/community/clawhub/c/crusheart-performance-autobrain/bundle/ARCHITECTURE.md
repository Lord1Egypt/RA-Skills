# Crusheart-AutoBrain-Turbo — Architecture Reference

> **Version**: 6.3.1 | **Last updated**: 2026-05-27
> **Purpose**: System file navigation — find any file, understand its role, know who calls it.

---

## 1. Directory Overview

```
workspace/
├── core/
│   ├── engines/          ← 90+ Python engines (8 groups)
│   ├── pipeline/         ← 10-stage message pipeline
│   ├── planner/          ← Task decomposition & goal planning
│   └── capability/       ← Task graph models
├── scripts/              ← Shell & Python helper scripts (8 auto-deployed)
├── skills/               ← OpenClaw skill definitions
├── memory/               ← Daily memory logs
├── projects/             ← Active project context (optional)
├── SOUL.md               ← Agent behavior rules (deployed)
├── IDENTITY.md           ← Agent identity (deployed)
├── USER.md               ← User profile (deployed)
└── TOOLS.md              ← Tool usage notes (deployed)
```

---

## 2. Plugin Structure

The plugin is deployed from index.js into the workspace:

| File | Role |
|------|------|
| `index.js` | Node.js bridge; lifecycle hooks (bootstrap / received / preprocessed / sent) |
| `bundle/crusheart-core.tar.gz` | 90+ Python engines, 10-stage pipeline, planner, capability |
| `bundle/install_wizard.py` | Installation wizard (compat check + 8-step init) |
| `bundle/daily_maintenance.py` | Unified daily maintenance at 01:00 |
| `bundle/scan_memory.py` | Memory scan & archive |
| `bundle/scan_skills.py` | Skill scan & classification |
| `bundle/init_correction_data.py` | Correction data chain initialization |
| `bundle/read_config.py` | Config reader (model, channel) |
| `bundle/auto_save_capsule.py` | Context capsule snapshot |
| `bundle/version_check.py` | Version check against clawhub.ai |
| `bundle/register_crons.sh` | Register 2 cron tasks |
| `bundle/SOUL.md` | Iron rules (deployed on first install) |
| `bundle/INSTALL_GUIDE.md` | Installation guide doc |
| `bundle/ARCHITECTURE.md` | This file |
| `skill/SKILL.md`, `skill/_meta.json` | Skill page for clawhub |

---

## 3. Plugin Entry Point: index.js

```
onLoad()
  ├── acquireSlot()
  │     ├── Check openclaw plugins list for overlapping plugins
  │     │     (keywords: memory, anti-hallucination, self-evolution, etc.)
  │     ├── If conflict found → block install + notify user
  │     ├── Else → atomic mkdir .crusheart-slot.lock/
  ├── deploy()
  │     ├── tar xzf crusheart-core.tar.gz → workspace core/
  │     ├── Copy skill metadata → skills/Crusheart-AutoBrain-Turbo/
  │     ├── Deploy bundle scripts → workspace scripts/
  │     ├── Write .crusheart-injected.md marker (SOUL.md not overwritten)
  │     ├── First install:
  │     │     1. install_wizard.py --check  (compatibility check → block or proceed)
  │     │     2. install_wizard.py --init    (8-step initialization)
  │     └── Non-first: quick engine scan only
  ├── auto_engines.py scan

Hooks:
  agent:bootstrap
    → init_engines.py --bootstrap
    → dual_mode_classifier.py --init

  message:received (priority 50)
    → dual_mode_classifier.py

  message:received (priority 10)
    → saveCapsule(ctx)  (JS-native, no Python spawn)

  message:preprocessed (priority 100)
    → anti_fake_validator.py [BLOCKED]?

  message:sent (priority 50)
    → saveCapsule(ctx)

  message:sent (priority 10)
    → self_evolution_v3.py --evaluate-turn
```

---

## 4. Engine Groups

### 4.1 init/ — Initialization & Config (12 engines)

| File | Role | Called by |
|------|------|-----------|
| `config_loader.py` | Layered config (default → user → env → runtime override) | All engines (import) |
| `config_validator.py` | Config schema validation | Bootstrap |
| `init_engines.py` | Orchestrates engine initialization | Bootstrap + cron 05:00 |
| `auto_engines.py` | Auto-load engines, skill scan, pipeline test | Bootstrap, CLI |
| `lazy_load_enforcer.py` | Lazy load control: search interval, cache TTL | Runtime |
| `session_manager.py` | Session state management, capsule save/load | Pipeline, hooks |
| `session_bootstrap.py` | Bootstrap session state, cron verification | Bootstrap |
| `context_capsule.py` | DAG-based session handoff with SQLite | Hooks, pipeline |
| `skill_router.py` | Skill scanning, classification, matching | Pipeline |
| `skill_auto_invoker.py` | Auto-invoke skills by task type | Pipeline |
| `task_scheduler.py` | Background task scheduler | Cron, hooks |
| `engines.json` | Engine registry (29 engines) | init_engines |

### 4.2 memory/ — Memory System (7 engines)

| File | Role | Called by |
|------|------|-----------|
| `auto_memory.py` | SQLite-backed 5-layer memory + inverted index + TF-IDF + semantic dedup | Pipeline, hooks |
| `vector_memory.py` | TF-IDF vector search with cosine similarity | auto_memory |
| `memory_layer_engine.py` | L1-L5 memory lifecycle management | Cron (maintenance) |
| `dag_context_manager.py` | DAG context graph, SQLite persistent | Pipeline |
| `user_dynamic_portrait.py` | Evolving user profile based on interactions | Self-evolution |
| `exec_logger.py` | Execution log with structured fields | Pipeline, scripts |
| `anti_forget_engine.py` | Anti-forget: periodic memory review | Cron (maintenance) |

### 4.3 quality/ — Quality & Validation (11 engines)

| File | Role | Called by |
|------|------|-----------|
| `anti_fake_validator.py` | Anti-hallucination validation (v4) | Pipeline stage 3, hook |
| `circuit_breaker.py` | 3-state circuit breaker + timeout + auto-retry + checkpoint + process log | tools/gateway |
| `closed_loop.py` | Result checker + audit + recovery + summarizer | Self-evolution |
| `identity_drift_guard.py` | Guards against agent identity drift | Self-evolution |
| `iron_rules.py` | Behavior pre-checks (the 8 iron rules) | Pipeline, anti_fake |
| `judge_engine.py` | LLM-as-Judge scoring + Reflexion + ReplayBuffer | Pipeline stage 6.5 |
| `anomaly_detector.py` | 6-dimension anomaly monitoring | Cron, health check |
| `unified_judge.py` | Central arbitration judge | Orchestration |
| `quality_dashboard.py` | Engine quality metrics dashboard | Cron (health check) |
| `success_path_store.py` | Records successful execution paths | Self-evolution |
| `logger.py` | Structured logging, per-module rotation | All engines |

### 4.4 operations/ — Operations (7 engines)

| File | Role | Called by |
|------|------|-----------|
| `health_check.py` | 8-dimension health scoring (0-100) | Cron 01:00 |
| `autonomy_cycle.py` | R-CCAM-style autonomous cycle | Pipeline |
| `decision_core.py` | Core decision-making | Pipeline |
| `background_executor.py` | Background tasks + subagent spawn + heartbeat | Self-evolution |
| `unified_executor.py` | Unified task executor with priority queue | Pipeline |
| `state_manager.py` | Plugin & daemon state management | Bootstrap |
| `runtime_probe.py` | Runtime resource monitoring | Health check |

### 4.5 workflow/ — Workflow Orchestration (7 engines)

| File | Role | Called by |
|------|------|-----------|
| `workflow_orchestrator.py` | Multi-skill workflow orchestration | Pipeline |
| `engine_orchestrator.py` | Routes tasks between engines | Pipeline stage 4 |
| `serial_lanes.py` | Serial task lanes with mutex for device ops | Pipeline |
| `workflow_engine.py` | Workflow execution engine | Orchestrator |
| `task_executor.py` | Task execution engine | Orchestrator |
| `goal_compiler.py` | Compiles user goal into executable steps | Pipeline |
| `rule_engine.py` | Condition evaluation + 6 action types | Pipeline |

### 4.6 tools/ — Tool Support (12 engines)

| File | Role | Called by |
|------|------|-----------|
| `failover.py` | Model failover with circuit breaker + cooldown | Pipeline, hooks |
| `auto_tuning.py` | Parameter auto-tuning based on execution data | Cron, dual_mode |
| `crusheart_db.py` | SQLite DB manager with schema versioning | Memory, tools |
| `tool_execution_gateway.py` | External tool execution with permission check | Pipeline |
| `mutex_engine.py` | Global mutex + heartbeat lock for background tasks | Cron, scheduler |
| `enhancement_engine.py` | Event triggers + alert routing + smart scheduler | Operations |
| `trace_timeline.py` | Execution trace timeline | Debug, quality |
| `plugin_sdk.py` | Third-party engine interface standard | Compat |
| `message_pipeline.py` | Compatibility shim (delegates to core/pipeline/) | Scripts |
| `task_template_library.py` | Task template library | Orchestrator |
| `context_warning.py` | Context overflow warning (round/toolcall thresholds) | Pipeline |
| `device_receipt_reconciler.py` | Device operation receipt reconciliation | Operations |

### 4.7 hooks/ — Lifecycle Hooks (4 engines)

| File | Role | Called by |
|------|------|-----------|
| `hook_engine.py` | Hook registration and lifecycle management | Index.js |
| `dual_mode_classifier.py` | Dual-mode classification (fast vs agent) | Hook: received |
| `self_evolution_v3.py` | Self-evaluation per-turn (v3) | Hook: sent |
| `self_evolution_engine.py` | Self-evolution v4 with RiskAwareExecutor | Hook, pipeline |

### 4.8 compat/ — Third-party Engine Compatibility (2 engines)

| File | Role | Called by |
|------|------|-----------|
| `compat_engine.py` | Third-party engine adapter | Tools |
| `compat_registry.py` | Third-party engine auto-discover and registration | Bootstrap |

---

## 5. Pipeline Stages (core/pipeline/)

| Stage | File | Function |
|-------|------|----------|
| 0 | `engines.py` | Engine status probe |
| 1 | `dual_mode.py` | Dual-mode classification (fast/agent) |
| 2 | `skill_match.py` | Skill matching |
| 3 | `anti_fake.py` | Inbound anti-hallucination |
| 4 | `engine_route.py` | Engine routing |
| 5 | `session_state.py` | Session state (RAM layer) |
| 6 | `memory_align.py` | Memory alignment |
| 6.5 | `evolution_context.py` | Evolution context injection |
| 7 | `self_reflection.py` | Outbound self-reflection |
| 8 | `anti_fake.py` (stage 8) | Outbound anti-hallucination |
| post | `orchestrator.py` | Correction + capsule sync |

---

## 6. Planner (core/planner/)

| File | Role |
|------|------|
| `task_planner.py` | Task plan construction |
| `task_decomposer.py` | Task decomposition |
| `goal_parser.py` | Goal parsing |
| `plan_schema.py` | Plan schema definition |
| `skill_selector.py` | Skill selectors |
| `route_selector.py` | Route selection |

---

## 7. Capability (core/capability/)

| File | Role |
|------|------|
| `task_graph.py` | Task graph models for dependency tracking |

---

## 8. Data Flow

```
User message → Hook: received → Dual-mode classifier → Pipeline (10 stages)
                                                                 │
                                                      AutoBrain engines
                                                                 │
                                                      Agent generates reply
                                                                 │
                                                    Hook: sent → Self-evaluation
                                                                 │
                                                    Capsule save (every cycle)
```

---

## 9. Error Isolation System

```
Circuit Breaker (circuit_breaker.py v2.0):
  - 3-state: CLOSED → OPEN → HALF_OPEN → CLOSED
  - Timeout protection: configurable per-call timeout
  - Auto-retry: exponential backoff, configurable retry count
  - CheckpointManager: task progress persistence for resume
  - ProcessLogger: temporary task logs, auto-deleted on success
  - Global registry: all protected services tracked in one place

Flow:
  fn() → can_request()? → call() with timeout → success? → record_success()
                                                    fail? → retry? → record_failure() → OPEN
```

---

## 10. Background Sub-Agent System

```
background_executor.py:
  - submit() → spawn_subagent() → heartbeat loop (600s interval)
  - Timeout detection + recovery
  - SQLite persistent state

unified_executor.py:
  - Priority queue with auto-split
  - spawn_subagent() for async delegation
```

---

## 11. Cron Tasks

| Time | Name | Description |
|------|------|-------------|
| `0 1 * * *` | Unified maintenance + memory | Health check + memory consolidation + system cleanup + dream scan + ReplayBuffer distill + execution review + memory scan/archive/index + skill scan |
| `0 5 * * *` | Engine init + version check | `init_engines.py --bootstrap` + `version_check.py` |

> 2 cron tasks: 01:00 unified maintenance (memory maintenance merged in), 05:00 engine init + version check.

---

## 12. Key Data Files

| Path | Purpose | Created by |
|------|---------|------------|
| `.crusheart-slot.lock/` | Exclusive plugin lock | index.js |
| `.crusheart-deploy-state.json` | First-install flag | index.js |
| `.context_capsule.json` | Context capsule snapshot | Hooks |
| `.install_wizard_state.json` | Wizard completion state | install_wizard.py |
| `.skill_engine_connection.json` | Skill-engine linkage marker | install_wizard.py |
| `.verified_memories.jsonl` | Verified high-score responses | judge_engine |
| `.reflexions.jsonl` | Reflection triplets | judge_engine |
| `.replay_buffer/records.jsonl` | Correction signal records | judge_engine |
| `.replay_buffer/distilled.jsonl` | Distilled experiences | judge_engine |
| `.quality_scores.json` | Engine quality scores | quality_dashboard |
| `.evolution_state/` | Self-evolution state | self_evolution_engine |
| `.auto_memory.db` | SQLite memory store | auto_memory |
| `.checkpoints/` | Task checkpoint progress | circuit_breaker (CheckpointManager) |
| `.process_logs/` | Temporary process task logs | circuit_breaker (ProcessLogger) |

---

## 13. Modification Checklist

Before modifying system files:

```
□ File identified — use this doc to find the exact file
□ API change? → update all callers listed in "Called by" column
□ Pipeline stage changed? → don't break stage data flow
□ New data file? → add to section 12 (Key Data Files)
□ New cron task? → add to section 11 (Cron Tasks)
□ Engine removed? → update engines.json
□ Restart needed? → save capsule + notify user + delayed restart
□ Run arch_index.py to record snapshot
□ Bump version number
```

---

**Feedback**: HIM603070@gmail.com
