# AgentPathfinder Build System v1.0

Automated code improvement with GBrain integration and human approval gates.

## What It Does

This system analyzes your Python modules, generates improvement specs, applies fixes, tests them, commits locally — then **asks for your approval** before pushing to GitHub.

## Components

| Component | File | Purpose |
|-----------|------|---------|
| Auto Builder | `scripts/auto_build.py` | Analyzes, builds, tests, commits. Asks before push. |
| Build Orchestrator | `scripts/build_orchestrator.py` | Tracks builds via Pathfinder. Cryptographic verification. |
| Spec Generator | `scripts/spec_generator.py` | Generates business-aligned specs from GBrain data. |
| Knowledge Injector | `scripts/inject_knowledge.py` | Adds facts to GBrain (products, customers, etc.). |
| Brain API Client | `scripts/brain_api_client.py` | Query and manage Brain API facts. |

## Quick Start

### 1. Run a Dry Run (Safe — No Changes)

Check what the system would do to a module:

```bash
python3 scripts/auto_build.py --target agentpathfinder/task_engine.py --dry-run
```

Outputs:
- Analysis: functions, classes, issues found
- Generated spec (saved to `.build_data/spec_<module>.md`)
- Stops before making changes

### 2. Auto-Build a Module

```bash
python3 scripts/auto_build.py --target agentpathfinder/task_engine.py
```

What happens:
1. ✅ Checks GBrain for existing build patterns
2. ✅ Analyzes module (docstrings, type hints, tests, TODOs)
3. ✅ Generates improvement spec
4. ✅ Applies automated fixes (simple ones)
5. ✅ Runs build orchestrator (Pathfinder tracked)
6. ✅ Commits changes locally
7. 🛑 **STOPS** — Asks for approval before `git push`

### 3. Review and Decide

```bash
# See what changed
git diff HEAD~1 HEAD

# Approve and push
git push origin main

# Reject and undo
git reset --soft HEAD~1
git checkout -- agentpathfinder/task_engine.py
```

## Spec Generator

Generate business-aligned specs before building:

```bash
# SSO authentication feature
python3 scripts/spec_generator.py --feature "SSO Integration" --type auth --output sso_spec.md

# UI component with team features
python3 scripts/spec_generator.py --feature "Team Dashboard" --type ui --team --output dashboard_spec.md

# API endpoint
python3 scripts/spec_generator.py --feature "Webhook API" --type integration --output webhook_spec.md
```

Types: `auth` | `integration` | `ui` | `api` | `security` | `performance`

## GBrain Integration

### Query product knowledge:
```bash
# Using GBrain client
python3 scripts/brain_api_client.py query "AgentPathfinder pricing"

# Or direct API
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query":"pricing tiers","top_k":5}'
```

### Add a customer interaction:
```bash
python3 scripts/inject_knowledge.py --customer "ACME Corp" "Wants SSO, 50 seats, Q3 budget"
```

### Import all business facts:
```bash
python3 scripts/inject_knowledge.py
```

## Approval Gates

The system **never** pushes to GitHub without explicit approval.

```
🛑 HUMAN APPROVAL REQUIRED

Changes ARE committed locally
Changes are NOT pushed to GitHub

To approve and push:
  git push origin main

To reject and undo:
  git reset --soft HEAD~1
  git checkout -- <files>
```

## Workflow for Marketing/Sales Focus

As Anton, your workflow is now:

1. **Morning**: Review overnight build reports (if any)
2. **Mid-day**: Use spec generator for new features
3. **Approval time**: Queue of commits waiting for your `git push`
4. **Focus**: Marketing, sales, customer calls — while code improves autonomously

## Test the System

```bash
# Run full test suite
./test_build_system.sh

# Expected output:
# ============================================
# Results: 5 passed, 0 failed
# ============================================
# All tests passed. Build system ready.
```

## Files

- `data/certainlogic_facts.json` — Business facts (pricing, features, decisions)
- `.build_data/` — Build specs, outputs, Pathfinder data (git-ignored)
- `docs/auto-specs/` — Generated specs for reference

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Auto-Build Agent                                         │
│  ├─ GBrain Check (pattern reuse)                         │
│  ├─ Module Analyzer (AST-based)                          │
│  ├─ Spec Generator                                       │
│  ├─ Build Orchestrator (Pathfinder tracked)              │
│  ├─ Test Runner                                          │
│  ├─ Git Commit (local)                                   │
│  └─ 🛑 Human Approval Gate                               │
└─────────────────────────────────────────────────────────┘
                    │
              GBrain API (localhost:8000)
                    │
         ┌─────────┴─────────┐
         │  Facts Database    │
         │  ├─ Product info   │
         │  ├─ Build specs    │
         │  ├─ Customers      │
         │  └─ Decisions      │
         └──────────────────┘
```

## Next Steps

1. Run a dry run on your most-used module
2. Review the generated spec
3. Run the real build
4. Review the diff
5. Push or revert

Once comfortable, the system can run as a cron job nightly — generating improvement commits for you to review each morning.

---

Built by CertainLogic.ai — Deterministic AI you can trust.
