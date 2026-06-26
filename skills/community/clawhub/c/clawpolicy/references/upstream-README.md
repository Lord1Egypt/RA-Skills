# ClawPolicy

> Explainable autonomous execution policy engine for low-touch, auditable agent execution

**English (Primary)** | **[Chinese (Simplified)](README.zh-CN.md)**

## 3.0.1 Highlights

- Policy lifecycle: `hint -> candidate -> confirmed -> suspended -> archived`
- Canonical local storage: `.clawpolicy/policy/`
- Policy-first supervision CLI: `clawpolicy policy ...`
- Stable Python API for confirmation, policy storage, and Markdown conversion/export
- Optional Phase 3 extras remain available through `clawpolicy[phase3]`

## Installation

### PyPI

```bash
python3 -m pip install clawpolicy
```

Optional Phase 3 extras:

```bash
python3 -m pip install "clawpolicy[phase3]"
```

### Source checkout

```bash
git clone https://github.com/DZMing/clawpolicy.git
cd clawpolicy
python3 -m pip install -e ".[dev]"
```

## CLI Entry Points

- `clawpolicy`: primary console entry point
- `python -m clawpolicy`: module entry point

Initialize policy memory and inspect the current lifecycle state:

```bash
clawpolicy init
clawpolicy analyze
clawpolicy policy status
clawpolicy policy recent
```

`init` provisions:

- `.clawpolicy/policy/rules.json`
- `.clawpolicy/policy/playbooks.json`
- `.clawpolicy/policy/policy_events.jsonl`
- `.clawpolicy/USER.md`
- `.clawpolicy/SOUL.md`
- `.clawpolicy/AGENTS.md`

Low-frequency supervision commands:

```bash
clawpolicy policy status
clawpolicy policy recent
clawpolicy policy risky
clawpolicy policy suspended
python -m clawpolicy policy status
```

## Public Python API

The `clawpolicy` package exposes the supported policy-facing surface:

```python
from clawpolicy import (
    ConfirmationAPI,
    PolicyEvent,
    PolicyStore,
    Playbook,
    Rule,
    MarkdownToPolicyConverter,
    PolicyToMarkdownExporter,
    create_api,
)
```

- `ConfirmationAPI` / `create_api`: runtime confirmation and feedback loop integration
- `PolicyStore`: canonical policy asset persistence
- `Rule`, `Playbook`, `PolicyEvent`: public policy models
- `MarkdownToPolicyConverter`: convert Markdown memory into policy assets
- `PolicyToMarkdownExporter`: export canonical policy assets back to Markdown

## Verification

```bash
python3 -m pytest tests/ -v
python3 scripts/check_docs_consistency.py
python3 -m ruff check lib tests scripts
python3 -m clawpolicy policy status
clawpolicy policy status
```

## Core Modules

- `lib/policy_models.py`: canonical `Rule`, `Playbook`, and `PolicyEvent` models
- `lib/policy_store.py`: canonical `PolicyStore` and policy asset persistence
- `lib/policy_resolution.py`: scope inference and precedence resolution
- `lib/confirmation.py`: runtime truth loop, event recording, and feedback application
- `lib/promotion.py`: promotion gates for `candidate -> confirmed`
- `lib/demotion.py`: suspension, reactivation, and archive gates
- `lib/learner.py`: weak-hint derivation and strong-evidence aggregation
- `lib/api.py`: stable confirmation API surface
- `lib/cli.py`: initialization, status, supervision, export, and inspection commands
- `lib/environment.py`: interaction environment
  - `State`: State data class (17 dimensions)
  - `Action`: Action data class (11 dimensions)
- `lib/contracts.py`: single source of truth for state and action dimensions

## Optional Phase 3 Modules

- `lib/distributed_trainer.py`
- `lib/hyperparameter_tuner.py`
- `lib/monitoring.py`
- `lib/performance_optimizer.py`

## Test Coverage

- **Total Tests**: 183
- **Local Validation**: `python3 -m pytest tests/ -v`
- **Coverage Areas**: policy lifecycle promotion and suspension, scope precedence, public surface hard cut, canonical policy storage, CLI supervision, confirmation policy, RL core, optional Phase 3 modules, and docs/contract drift guards

## Release and Versioning

- Versioning: SemVer
- Current release line: `3.x`
- Release runbook: `RELEASING.md` / `RELEASING.zh-CN.md`
- Changelog: `CHANGELOG.md`

## Documentation

- Architecture: `docs/architecture.md`
- Reward model: `docs/reward-model.md`
- Configuration: `docs/configuration.md`
- Optional dependencies: `docs/phase3-optional-deps.md`
- Contributing: `CONTRIBUTING.md`
- Security: `SECURITY.md`
- Support: `SUPPORT.md`

## License

MIT
