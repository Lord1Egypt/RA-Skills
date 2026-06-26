---
name: cognitive-flexibility
description: |
  Cognitive Flexibility Skill - AI cognitive flexibility with 4 modes.
  Supports automatic mode switching and metacognitive monitoring.
  
  Use when:
  - Complex reasoning and multi-step thinking needed
  - Self-assessment and reflection required
  - Cross-scenario knowledge transfer
  - Creative problem solving
  - Task complexity > medium (estimated >2 hours)

metadata:
  version: 2.1.0
  author: DaoShi (optimizer)
  license: MIT
  tags: [cognition, reasoning, flexibility, ooda, metacognition, ai-agent]
  
allowed-tools:
  - Read
  - Write
  - Edit
  - memory_search
  - sessions_send
  - web_search

requirements:
  python: ">=3.8"
  openclaw: ">=2026.3.28"
---

# Cognitive Flexibility Skill

## Overview

This Skill implements four cognitive modes based on human cognitive science:

| Mode | Name | Driver | Scenario | Core Ability |
|------|------|--------|----------|--------------|
| **OOA** | Experience Mode | Memory-driven | Familiar scenarios | Pattern matching |
| **OODA** | Reasoning Mode | Knowledge-driven | Complex problems | Chain reasoning |
| **OOCA** | Creative Mode | Association-driven | Innovation needs | Analogy generation |
| **OOHA** | Discovery Mode | Hypothesis-driven | Exploration | Hypothesis generation |

## Quick Start

### Basic Usage

```python
from scripts.cognitive_controller import CognitiveController

# Create controller
controller = CognitiveController(confidence_threshold=0.7)

# Execute task (auto mode selection)
task = "Analyze user feedback data"
result = await controller.process(task, tools=tools)

# View result
print(f"Mode: {result['mode']}")
print(f"Answer: {result['answer']}")
print(f"Confidence: {result['assessment']['overall_score']:.2f}")
```

### Manual Mode Selection

```python
# OODA reasoning mode
from scripts.chain_reasoner import OODAReasoner
reasoner = OODAReasoner()
result = await reasoner.process(task, tools=tools)

# OOA experience mode
from scripts.pattern_matcher import PatternMatcher
matcher = PatternMatcher()
result = await matcher.match(task, tools=tools)

# OOCA creative mode
from scripts.creative_explorer import CreativeExplorer
explorer = CreativeExplorer()
result = await explorer.explore(task)

# OOHA discovery mode
from scripts.hypothesis_generator import HypothesisGenerator
generator = HypothesisGenerator()
result = await generator.discover(task)
```

## Features

- **4 Cognitive Modes**: OOA/OODA/OOCA/OOHA
- **Auto Mode Switching**: Cognitive Controller selects best mode
- **Metacognitive Monitoring**: Self-assessment and confidence scoring
- **Usage Tracking**: Complete usage logs and statistics
- **100% Test Coverage**: All tests passing

## File Structure

```
cognitive-flexibility/
├── scripts/
│   ├── __init__.py
│   ├── chain_reasoner.py       # OODA reasoning
│   ├── pattern_matcher.py      # OOA pattern matching
│   ├── self_assessor.py        # Metacognitive monitoring
│   ├── cognitive_controller.py # Mode switching
│   ├── creative_explorer.py    # OOCA creative mode
│   ├── hypothesis_generator.py # OOHA discovery mode
│   └── usage_monitor.py        # Usage tracking
├── references/
│   └── ooda-guide.md
├── tests/
│   └── test_cognitive_skills.py
├── SKILL.md
├── README.md
└── MONITORING-GUIDE.md
```

## Testing

```bash
# Run tests
python tests/test_cognitive_skills.py

# Expected output: 6/6 tests passed (100%)
```

## Monitoring

```python
from scripts.usage_monitor import UsageMonitor

monitor = UsageMonitor()

# Get usage stats
stats = monitor.get_stats(days=7)

# Generate report
report = monitor.generate_report(days=7)
print(report)
```

## Requirements

- Python >= 3.8
- OpenClaw >= 2026.3.28
- No external dependencies

## License

MIT License

## Support

- **Documentation**: See README.md and MONITORING-GUIDE.md
- **Issues**: GitHub Issues
- **Community**: Discord #skills-feedback

---

_DaoShi · Cognitive Flexibility Skill v2.1.0_
