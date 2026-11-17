# Design Gate Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![ClawHub](https://img.shields.io/badge/ClawHub-v1.0.0-blue.svg)](https://clawhub.ai/skills/design-gate)
[![Tests](https://img.shields.io/badge/Tests-80%20passed-green.svg)](tests/)

A generic design gate checker that validates architecture reasonableness, technical feasibility, and impact scope assessment.

## Features

- Architecture validation (components, responsibilities, interfaces, dependencies)
- Feasibility analysis (language, framework, database, external deps)
- Impact scope assessment (affected modules, breaking changes, migration, risk)
- Composite gate with overall pass/fail decision
- Score-based checks (0-100) with configurable threshold
- JSON serialization for persistence

## Installation

```bash
clawhub install design-gate
```

## Quick Start

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
print(gate.overall_pass(results))
```

## Tests

80 comprehensive tests covering unit, integration, and end-to-end scenarios.

```bash
python -m pytest tests/ -v --tb=short
```

## License

MIT License - free for personal and commercial use.

## Author

Terr123123
