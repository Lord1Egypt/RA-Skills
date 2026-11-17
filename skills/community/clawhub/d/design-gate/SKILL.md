---
name: design-gate
version: 1.0.0
description: A design gate checker for architecture validation, feasibility analysis, and impact scope assessment.
author: Terr123123
license: MIT
tags: [design, gate, architecture, feasibility, impact]
---

# Design Gate Skill

## Overview

A generic design gate checker that validates architecture reasonableness, technical feasibility, and impact scope assessment for a design before implementation proceeds.

## Key Features

- **Architecture Validation**: Checks components, responsibilities, interfaces, dependencies, and structure.
- **Feasibility Analysis**: Validates tech stack (language, framework, database, external deps).
- **Impact Scope Assessment**: Validates affected modules, breaking changes, migration needs, and risk level.
- **Composite Gate**: Runs all checks together and produces an overall pass/fail decision.
- **Score-based**: Each check returns a 0-100 score with details and issues; configurable pass threshold.
- **Persistence**: All models serialize to/from JSON for storage and reload.

## Use Cases

- Design phase gate review before development.
- Architecture review for new features or refactors.
- Migration risk assessment.
- Standardizing design documentation completeness.

## Installation

```bash
clawhub install design-gate
```

## Usage

### Basic Usage

```python
from src import DesignGate, Design, Component, TechStack, ImpactScope

gate = DesignGate()

design = Design(
    title="User Service",
    description="User management microservice",
    components=[
        Component("UserController", "Handle HTTP", ["GET", "POST"]),
        Component("UserRepo", "Persist users", ["save", "find"]),
    ],
    dependencies=["auth-service"],
    tech_stack=TechStack("python", "django", "postgres", ["redis"]),
    impact_scope=ImpactScope(["user-module"], False, False, "medium"),
)

results = gate.run_all_checks(design)
print(gate.overall_pass(results))  # True if all checks pass
```

### Individual Checks

```python
arch_result = gate.check_architecture(design)
feasibility_result = gate.check_feasibility(design.tech_stack)
impact_result = gate.check_impact_scope(design.impact_scope)
```

### Custom Threshold

```python
strict_gate = DesignGate(pass_threshold=80.0)
```

## API Reference

- `check_architecture(design: Design) -> GateResult`
- `check_feasibility(tech_stack: TechStack) -> GateResult`
- `check_impact_scope(impact: ImpactScope) -> GateResult`
- `run_all_checks(design: Design) -> List[GateResult]`
- `overall_pass(results: List[GateResult]) -> bool`

### Models

- `Design`: title, description, components, dependencies, tech_stack, impact_scope
- `Component`: name, responsibility, interfaces
- `TechStack`: language, framework, database, external_deps
- `ImpactScope`: affected_modules, breaking_changes, migration_needed, risk_level
- `GateResult`: check_name, passed, score, message, details

## Tests

80 comprehensive tests covering unit, integration, and end-to-end scenarios.

```bash
cd d:\openclaw-skills\quality-stack\design-gate
python -m pytest tests/ -v --tb=short
```

## License

MIT License - free for personal and commercial use.
