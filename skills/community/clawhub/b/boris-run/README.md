# Boris Workflow for OpenClaw

> Parallel agent task runner implementing the Boris Cherny multi-agent pattern

[![OpenClaw](https://img.shields.io/badge/OpenClaw-Compatible-blue)](https://openclaw.dev)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## Overview

Boris Workflow is a powerful parallel execution engine for OpenClaw that enables you to run multiple independent tasks across multiple AI agents simultaneously. Inspired by Boris Cherny's approach to multi-agent orchestration, it provides automatic progress tracking, configurable error retry, and organized artifact management.

### What It Does

The Boris Workflow implements a **3-phase parallel execution pattern**:

1. **Phase 1: Distribution** — Tasks are queued and distributed to available agents
2. **Phase 2: Execution** — Agents pull work from the queue (work-stealing pattern)
3. **Phase 3: Verification** — Optional verification agent reviews all results

```
┌─────────────────────────────────────────────────────────────┐
│                      ORCHESTRATOR                           │
│                    (boris-run CLI)                          │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  AGENT 1     │    │  AGENT 2     │    │  AGENT N     │
│ (Task A)     │    │ (Task B)     │    │ (Task C)     │
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           ▼
              ┌────────────────────┐
              │  RESULT COLLECTOR  │
              └────────────────────┘
```

## Key Features

### 🚀 Parallel Execution
- Spawn 1-20 agents working simultaneously
- Work-stealing pattern ensures no idle agents
- Automatic load balancing across varying task durations

### 🔄 Intelligent Retry
- Configurable retry strategies: none, linear, exponential
- Per-task timeout handling
- Automatic failure recovery

### 📊 Progress Tracking
- Real-time progress updates
- Compact progress bar or verbose logging modes
- Per-task status monitoring

### ✅ Verification Layer
- Optional verification agent reviews all results
- Quality assessment and error detection
- Verification reports in structured JSON

### 🎨 Web UI (Optional)
- Modern dark-themed interface
- Real-time status via Server-Sent Events
- Drag-and-drop task management
- Configuration export as YAML

### 📁 Organized Artifacts
- Automatic directory structure per workflow
- Timestamped artifact naming
- Cleanup policies (keep_all, keep_last_N, age_based)

## Quick Start

```bash
# Install dependencies
cd ~/.openclaw/workspace/skills/boris-workflow
pip install -r requirements.txt

# Run 3 tasks with 3 agents
./bin/boris-run --tasks "research|analyze|write"

# Run 10 tasks with 5 agents
./bin/boris-run --tasks "t1|t2|t3|t4|t5|t6|t7|t8|t9|t10" --agents 5

# With verification step
./bin/boris-run --tasks "code|test|review" --verify

# Dry run to preview
./bin/boris-run --tasks "build|deploy" --dry-run
```

## Web Interface

Boris Workflow includes a modern web UI for visual workflow management:

```bash
# Start the Web UI
cd ~/.openclaw/workspace/skills/boris-workflow/webui
./start.sh
```

Open http://localhost:8080 in your browser.

### Web UI Features

- **Dynamic Task Management** — Add, remove, and reorder workflow tasks with an intuitive interface
- **Agent Configuration** — Adjust agent count (1-20) and select AI models from a dropdown
- **Real-time Status** — Live progress updates via Server-Sent Events (SSE)
- **Results Viewer** — View and download workflow results in JSON format
- **Configuration Management** — Save settings and export as YAML
- **Modern Dark UI** — Clean interface built with Tailwind CSS
- **Mobile Responsive** — Works seamlessly on all screen sizes

### Web UI Screenshots

```
┌─────────────────────────────────────────────────────────────┐
│  🚀 Boris Workflow                              [Settings]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Workflow Name: batch-analysis                              │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Tasks                    │  Agents: [ 3 ▼]          │   │
│  │ ──────────────────────── │  Model: [kimi-coding ▼]  │   │
│  │ □ Research market trends │  Timeout: [300s ▼]       │   │
│  │ □ Analyze competitors    │  Retries: [2 ▼]          │   │
│  │ □ Write summary report   │                          │   │
│  │ □ + Add Task             │  [✓] Enable Verification │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [Start Workflow]          [Dry Run]          [Export YAML] │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Progress                                            │   │
│  │ ████████░░░░░░░░░░ 8/10 tasks complete (80%)       │   │
│  │                                                     │   │
│  │ task_0_research     ✅ Complete    2m 14s          │   │
│  │ task_1_analyze      ✅ Complete    1m 52s          │   │
│  │ task_2_write        🔄 Running     0m 45s          │   │
│  │ task_3_verify       ⏳ Pending     --              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Requirements

### System Requirements
- **OpenClaw**: Installed and configured
- **Python**: 3.9 or higher
- **OS**: Linux, macOS, or WSL on Windows
- **Memory**: 4GB RAM minimum (8GB recommended for multiple agents)
- **Disk**: 100MB for installation, variable for artifacts

### Python Dependencies
```
pyyaml>=6.0
requests>=2.28.0
```

### Optional Dependencies (for Web UI)
```
fastapi>=0.100.0
uvicorn[standard]>=0.23.0
pydantic>=2.0.0
python-multipart>=0.0.6
```

## Configuration

### Configuration Hierarchy

Config values are resolved in priority order (highest to lowest):
1. CLI arguments
2. Environment variables (`BORIS_*`)
3. Project config (`./.boris/config.yaml`)
4. User config (`~/.boris/config.yaml`)
5. System defaults

### Example Config File

```yaml
# ~/.boris/config.yaml

# Agent defaults
agents:
  default_count: 3
  max_count: 20
  timeout_seconds: 300
  model: "kimi-coding/k2p5"

# Retry configuration
retry:
  max_attempts: 2
  backoff_strategy: "exponential"
  initial_delay_ms: 1000
  max_delay_ms: 30000

# Output and artifacts
output:
  base_dir: "~/.boris/artifacts"
  naming_pattern: "{workflow_name}_{timestamp}_{task_id}"
  cleanup_policy: "keep_last_10"

# Verification settings
verification:
  enabled: false
  verifier_model: "kimi-coding/k2p5"
  auto_retry_failed: true

# Logging
logging:
  level: "info"
  format: "text"
```

## CLI Reference

```
Usage: boris-run [OPTIONS]

Required:
  -t, --tasks TEXT          Tasks to run, pipe-separated
  
Optional:
  -a, --agents INTEGER      Number of agents (default: 3, max: 20)
  -n, --name TEXT          Workflow name
  -c, --config PATH        Config file path
  -o, --output PATH        Artifacts directory
  -r, --retries INTEGER    Max retries per task
  -T, --timeout INTEGER    Timeout per agent (seconds)
  --verify                 Enable verification step
  --dry-run                Preview without execution
  --mock                   Use mock bridge for testing
  -v, --verbose            Verbose logging
  -q, --quiet              Suppress progress output
  --version                Show version
  -h, --help               Show help
```

## Use Cases

- **Batch Content Processing** — Generate 10 blog posts simultaneously
- **Multi-Source Research** — Research 5 topics in parallel
- **Code Review at Scale** — Review 20 files with 5 agents
- **Data Analysis Pipeline** — Process multiple datasets concurrently
- **Test Suite Execution** — Run independent test files in parallel

## License

MIT License - OpenClaw Community

## Author

Created by Goli / mukston for the OpenClaw ecosystem.
