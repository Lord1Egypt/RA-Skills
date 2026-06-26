---
tracker:
  type: "notion"
  database_id: "${NOTION_DATABASE_ID}"
  poll_interval_seconds: 30

workspace:
  base_dir: "/tmp/dev-factory-workspaces"
  auto_cleanup: true
  retention_hours: 24

orchestration:
  max_concurrent_builds: 3
  per_state_limits:
    building: 3
    testing: 5
    fixing: 2
  retry:
    max_attempts: 3
    backoff_base: 2
  stall_timeout_seconds: 300

agent:
  type: "glm5"
  api_base: "https://api.z.ai/api/coding/paas/v4"
  model: "glm-5"
  timeout_seconds: 300
  stall_timeout_seconds: 300

hooks:
  after_create:
    - command: "python -m venv .venv"
  before_run:
    - command: "rm -rf dist/ build/"
  after_run:
    - command: "pytest --cov=. --cov-report=xml"
---

# Dev-Factory Workflow

This document describes the automated development workflow powered by GLM-5 and Symphony orchestration.

## Overview

Dev-Factory is an automated software development agent that:
- Discovers project ideas from GitHub Trending, CVE databases, and security news
- Builds complete, tested Python projects using GLM-5
- Publishes results to GitHub and tracks progress in Notion

## Architecture

The system uses a hybrid layered architecture:

```
┌─────────────────────────────────────────────────────────────┐
│  SYMPHONY ORCHESTRATION LAYER                                │
│  - SymphonyOrchestrator (daemon mode, polling, concurrency)  │
│  - NotionTrackerAdapter (Symphony's tracker interface)       │
│  - WorkspaceManager (isolated per-build workspaces)          │
│  - GLM5AgentAdapter (HTTP API → agent protocol translation)  │
└─────────────────────────────────────────────────────────────┘
                          ↓ delegates to ↓
┌─────────────────────────────────────────────────────────────┐
│  EXISTING DEV-FACTORY CORE                                   │
│  - BuilderPipeline (discovery, dedup, scoring)               │
│  - HybridOrchestrator (engine selection logic)               │
│  - CorrectionEngine (error analysis & fixing)                │
│  - GitHubPublisher, NotionSync                               │
└─────────────────────────────────────────────────────────────┘
```

## Workflow Stages

### 1. Discovery
- **GitHub Trending**: Find trending Python projects
- **CVE Database**: Discover security vulnerabilities to address
- **Security News**: Monitor security news for tool ideas
- **Deduplication**: Remove duplicate/similar ideas
- **Scoring**: Rank ideas by potential impact

### 2. Build
- **Workspace**: Create isolated workspace per project
- **Development**: Use GLM-5 for code generation
- **Fallback**: Use Claude Code CLI if GLM-5 fails
- **Testing**: Run comprehensive test suite
- **Coverage**: Ensure 80%+ test coverage

### 3. Fix
- **Error Analysis**: Parse test failures
- **Automatic Fixing**: Use AI to fix errors
- **Retry**: Re-test after fixes

### 4. Publish
- **GitHub**: Create repository and push code
- **Notion**: Update task status to "완료" (Completed)

## Configuration

### Tracker (Notion)
The system uses Notion as the issue tracker. Status mapping:
- `아이디어` (Idea) → UNCLAIMED
- `개발중` (Developing) → RUNNING
- `완료` (Completed) → SUCCEEDED
- `실패` (Failed) → FAILED

### Workspace
Each build gets an isolated workspace:
- Pattern: `/tmp/dev-factory-workspaces/{task_id}/`
- Auto-cleanup after 24 hours
- Git repository initialization
- Virtual environment setup

### Concurrency
Parallel build processing:
- Global limit: 3 concurrent builds
- Per-stage limits: Building (3), Testing (5), Fixing (2)
- Adaptive scaling based on utilization

## Agent Configuration

### GLM-5 (Primary)
- Model: `glm-5`
- API Base: `https://api.z.ai/api/coding/paas/v4`
- Features: Tool calling, code generation, error analysis

### Claude Code (Fallback)
- Triggered on: GLM-5 API errors, timeouts, rate limits
- Features: Local execution, no API limits

## Running Modes

### Daemon Mode (NEW)
```bash
python run_symphony_daemon.py
```
- Long-running daemon process
- Parallel build processing
- Automatic polling and retry
- Health check endpoint

### Scheduled Mode (Legacy)
```bash
python run_discovery.py      # Discover new ideas
python run_build_from_notion.py  # Build from Notion queue
```
- Sequential processing
- Cron/scheduler based
- No parallel execution

## Health Monitoring

The daemon provides health statistics:
- Active tasks count
- Concurrency utilization
- Workspace usage
- State machine statistics

Access via: `GET /health` (when health server is enabled)

## Error Handling

### Retry Logic
- Max attempts: 3
- Backoff strategy: Exponential (1s, 2s, 4s, 8s)
- Retry queue: Automatic re-queue with backoff

### Fallback Hierarchy
```
GLM-5 (primary)
  ↓ (API error, timeout, rate limit)
Retry with backoff
  ↓ (persistent failure)
Claude Code CLI (existing fallback)
  ↓ (CLI not found, token exhausted)
Fail with terminal reason
```

## Development

### Adding New Features
1. Implement in `builder/` package
2. Add tests in `tests/`
3. Update documentation
4. Submit PR

### Testing
```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# With coverage
pytest --cov=builder --cov-report=html
```

## License

MIT License - See LICENSE file for details

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request
