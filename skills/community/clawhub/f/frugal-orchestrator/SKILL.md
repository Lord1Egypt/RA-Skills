# Skill: Frugal Orchestrator

## Metadata
- **Name**: frugal-orchestrator
- **Version**: 0.5.0
- **Author**: Agent Zero Project
- **Tags**: orchestration, efficiency, token-optimization, delegation, caching, batch-processing, learning
- **Description**: Complete token-efficient task orchestration platform with auto-routing, caching, batch processing, A2A mesh, and learning engine. Achieves 90%+ token reduction.

## Problem Statement
AI agents often waste tokens on tasks better solved by system tools (Linux commands, Python scripts). This creates unnecessary costs and slower execution.

**Solution**: Frugal Orchestrator v0.5.0 with intelligent task routing, caching layer, and specialized subordinate delegation.

**Result**: 90%+ token reduction while maintaining full functionality

## Core Capabilities

### Module 1: Auto-Router
**Purpose**: Automatically detect task type and route optimally
- System commands → Terminal (95% token reduction)
- Scripts → Python/Node.js execution
- Complex logic → AI delegation
- **Class**: `TaskRouter`

### Module 2: Token Tracker
**Purpose**: TOON-format token metrics logging
- Track delegation vs direct execution
- Generate savings reports
- **Class**: `TokenTracker`

### Module 3: Cache Manager
**Purpose**: Content-addressable result caching with TTL
- CRC32 hash-based keys
- LRU eviction, 7-day default TTL
- **Class**: `CacheManager`

### Module 4: Error Recovery
**Purpose**: Resilient execution with retry/fallback chains
- Exponential backoff, circuit breaker
- **Classes**: `ErrorRecovery`, `FailureType`

### Module 5: Batch Processor
**Purpose**: Parallel task execution
- Concurrent worker pool
- Manifest-based processing
- **Class**: `BatchProcessor`

### Module 6: A2A Adapter
**Purpose**: Agent-to-Agent mesh communication
- Service discovery, load balancing
- **Class**: `A2AAdapter`

### Module 7: Learning Engine
**Purpose**: Pattern recognition for routing decisions
- Confidence scoring, history analysis
- **Class**: `LearningEngine`

### Module 8: Scheduler Integration
**Purpose**: Recurring task scheduling
- Cron-style scheduling
- **Class**: `SchedulerClient`

## Quick Start

```bash
# Run demonstration
cd /a0/usr/projects/frugal_orchestrator/demo && bash run_demo.sh
```

### Python Integration
```python
from scripts.auto_router import TaskRouter
from scripts.cache_manager import CacheManager
from scripts.token_tracker import TokenTracker

# Initialize
router = TaskRouter(TokenTracker())
result = router.route("file_operations", task_input)
```

## Project Statistics
| Metric | Value |
|--------|-------|
| Python Modules | 10 |
| Shell Scripts | 6 |
| Total Files | 58 |
| Python LOC | 1,763 |
| Token Reduction | 90%+ |

## Token Efficiency
| Feature | Token Reduction |
|---------|---------------|
| Auto-routing | 90-95% |
| Caching | >99% for repeats |
| Batch processing | Linear scaling |

## GitHub Repository
https://github.com/nelohenriq/frugal_orchestrator (v0.5.0)

## Version History
- **0.5.0**: Complete orchestration platform (10 modules, full infrastructure)
- **0.2.0**: Standardized agentskills.io format, Git repo
- **0.1.0**: Initial implementation
