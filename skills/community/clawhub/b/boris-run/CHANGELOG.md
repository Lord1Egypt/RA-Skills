# Changelog

All notable changes to the Boris Workflow skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-18

### Added
- Initial release of Boris Workflow skill
- Parallel agent task runner implementing the Boris Cherny pattern
- Support for 1-20 simultaneous agents with work-stealing pattern
- 3-phase workflow: Distribution → Execution → Verification
- Configurable retry strategies (none, linear, exponential)
- Real-time progress tracking with compact and verbose modes
- Optional verification agent for quality assurance
- Organized artifact management with cleanup policies
- YAML-based configuration with hierarchy support
- Environment variable configuration support
- Command-line interface with comprehensive options
- Web UI with modern dark theme and real-time updates
- Server-Sent Events (SSE) for live workflow status
- FastAPI-based backend for Web UI
- Mobile-responsive frontend with Tailwind CSS
- Comprehensive test suite with mock mode
- Full documentation in SKILL.md

### Features

#### Core Workflow Engine
- `boris-run` CLI for executing parallel workflows
- Task queue with work-stealing distribution
- Automatic agent lifecycle management
- Per-task timeout and retry handling
- Structured JSON output for all results

#### Configuration System
- Hierarchical config resolution (CLI → env → project → user → defaults)
- YAML configuration files
- Environment variable prefix: `BORIS_*`
- Runtime config validation

#### Artifact Management
- Timestamped workflow directories
- Per-task artifact organization
- Configurable naming patterns
- Cleanup policies: keep_all, keep_last_N, age_based

#### Progress Reporting
- Compact progress bar mode
- Verbose logging mode
- Real-time status updates
- Per-task duration tracking

#### Retry Handler
- Configurable max attempts
- Multiple backoff strategies
- Exponential backoff with jitter option
- Per-error-type retry rules

#### Web UI
- FastAPI backend with REST API
- Vanilla JavaScript frontend
- Tailwind CSS styling
- Real-time updates via SSE
- Task management interface
- Configuration export to YAML
- Results viewer and downloader

### API Endpoints (Web UI)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/workflows` | GET | List all workflows |
| `/api/workflows` | POST | Create new workflow |
| `/api/workflows/{id}/status` | GET | Get workflow status |
| `/api/workflows/{id}/stream` | GET | SSE status stream |
| `/api/workflows/{id}/results` | GET | Get workflow results |
| `/api/workflows/{id}/cancel` | POST | Cancel workflow |
| `/api/config` | GET | Get configuration |
| `/api/config` | POST | Save configuration |
| `/api/export` | GET | Export config as YAML |
| `/api/models` | GET | List available models |

### File Structure

```
boris-workflow/
├── bin/
│   └── boris-run              # Main CLI executable
├── lib/
│   ├── __init__.py
│   ├── agent_worker.py        # Agent worker implementation
│   ├── artifact_manager.py    # Artifact directory management
│   ├── config.py              # Configuration loading
│   ├── openclaw_bridge.py     # OpenClaw integration
│   ├── progress.py            # Progress reporting
│   └── retry_handler.py       # Retry logic
├── webui/
│   ├── server/
│   │   ├── main.py            # FastAPI application
│   │   └── bridge.py          # CLI bridge
│   ├── static/
│   │   ├── index.html         # Web UI HTML
│   │   ├── app.js             # Frontend JavaScript
│   │   └── styles.css         # Custom styles
│   ├── start.sh               # Web UI startup script
│   └── requirements.txt       # Web UI dependencies
├── tests/                     # Test suite
├── SKILL.md                   # Skill documentation
├── pyproject.toml             # Python package config
└── requirements.txt           # Core dependencies
```

### Dependencies

#### Required
- Python >= 3.9
- pyyaml >= 6.0
- requests >= 2.28.0

#### Optional (for Web UI)
- fastapi >= 0.100.0
- uvicorn[standard] >= 0.23.0
- pydantic >= 2.0.0
- python-multipart >= 0.0.6

### Documentation

- Comprehensive SKILL.md with full usage guide
- CLI help with `--help` flag
- Inline code documentation
- Configuration examples
- Troubleshooting guide

## [Unreleased]

### Planned for 1.1.0
- Task dependency chains (sequential tasks within parallel workflow)
- Plugin system for custom task types
- Integration with external task queues (Redis, RabbitMQ)
- Workflow templates and presets
- Enhanced metrics and analytics
- Web UI authentication

### Planned for 2.0.0
- Distributed execution across multiple machines
- Kubernetes operator for cloud deployment
- Webhook notifications
- Advanced scheduling (cron workflows)
- Workflow visualizer with graph view

---

## Release Notes Format

Each release includes:
- **Added** - New features
- **Changed** - Changes to existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Bug fixes
- **Security** - Security-related changes

## Migration Guides

### Upgrading to 1.0.0

This is the initial release. No migration needed.
