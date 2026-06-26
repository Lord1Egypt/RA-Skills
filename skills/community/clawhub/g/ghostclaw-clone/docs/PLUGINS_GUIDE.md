# Developer Guide: External Ghostclaw Plugins (v0.1.6)

This document details the method for creating and installing external plugins (adapters) to extend Ghostclaw's architectural analysis capabilities.

## 1. Plugin Types

Ghostclaw supports three types of adapters:

1. **MetricAdapter**: For external analysis tools (e.g., linters, security scanners, custom AST logic).
2. **StorageAdapter**: For custom vibe history persistence (e.g., Redis, PostgreSQL).
3. **TargetAdapter**: For routing reports to external systems (e.g., Slack, Webhooks, CI dashboards).

## 2. Implementation Method

### Step 1: Scaffold a Template

Use the CLI to generate a boilerplate adapter for your project:

```bash
ghostclaw plugins scaffold my-custom-metric
```

### Step 2: Building from Scratch

Ghostclaw uses the `pluggy` hook system and `abc` (Abstract Base Classes) to ensure plugins are both flexible and type-safe. To build a plugin from scratch, follow the pattern for your specific plugin type.

#### Architecture Alignment

1. **Discovery**: `PluginRegistry` scans `.ghostclaw/plugins/` for subclasses of `BaseAdapter`.
2. **Lifecycle**: `GhostAgent` triggers plugins via event hooks (`INIT`, `PRE_ANALYZE`, `SYNTHESIS_CHUNK`, etc.).
3. **Concurrency**: All adapter methods (`analyze`, `emit`, `save_report`) are **asynchronous**.

---

### Type 1: MetricAdapter (Analysis Engine)

Used to add new scanning capabilities or integrate third-party tools.

```python
from typing import Dict, List, Any
from ghostclaw.core.adapters.base import MetricAdapter, AdapterMetadata

class SecurityScanner(MetricAdapter):
    def get_metadata(self) -> AdapterMetadata:
        return AdapterMetadata(
            name="sec-scan",
            version="1.0.0",
            description="Checks for hardcoded secrets.",
            author="Ghost Team"
        )

    async def is_available(self) -> bool:
        return True # Add 'bin/sh' check here if needed

    async def analyze(self, root: str, files: List[str]) -> Dict[str, Any]:
        return {
            "issues": ["Found potential secret in config.py:12"],
            "architectural_ghosts": [],
            "red_flags": ["Critical: Hardcoded Key"]
        }
```

### Type 2: StorageAdapter (Persistence)

Used to change where vibe history and reports are saved.

```python
from typing import List, Any
from ghostclaw.core.adapters.base import StorageAdapter, AdapterMetadata

class RedisStorage(StorageAdapter):
    def get_metadata(self) -> AdapterMetadata:
        return AdapterMetadata(name="redis-store", version="0.1.0", description="Redis backend.")

    async def is_available(self) -> bool:
        return True # Check redis connection

    async def save_report(self, report: Any) -> str:
        # report is an ArchitectureReport or Dict
        report_id = report.get("metadata", {}).get("fingerprint", "unknown")
        # Logic to save to Redis...
        return report_id

    async def get_history(self, limit: int = 10) -> List[Any]:
        return [] # Retrieve from Redis...
```

### Type 3: TargetAdapter (Reporting/Webhooks)

Used to route analysis events to external services (Slack, Discord, internal dashboards).

```python
from typing import Any
from ghostclaw.core.adapters.base import TargetAdapter, AdapterMetadata

class SlackNotifier(TargetAdapter):
    def get_metadata(self) -> AdapterMetadata:
        return AdapterMetadata(name="slack", version="1.0.0", description="Pings Slack on completion.")

    async def is_available(self) -> bool:
        return True # Check SLACK_WEBHOOK_URL env

    async def emit(self, event_type: str, data: Any) -> None:
        if event_type == "POST_SYNTHESIS":
            score = data.get("report", {}).get("vibe_score")
            print(f"DEBUG: Pinging Slack with score {score}")
```

---

## 3. Installation & Verification

### Installation

1. Create `.ghostclaw/plugins/` in your repository.
2. Place your `.py` file(s) inside.
3. Or use: `ghostclaw plugins add ./my_plugin.py`

### Verification

Run the following to see your custom adapters in the **"External"** category:

```bash
ghostclaw plugins list
```

---

*Ghostclaw v0.1.6 - Decoupled. Modular. Extensible.*
