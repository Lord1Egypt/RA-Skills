# OpenClaw Correlation Memory Plugin

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Plugin](https://img.shields.io/badge/OpenClaw-Plugin-blue)](https://openclaw.dev)

**Correlation-aware memory search for OpenClaw** — automatically retrieves related contexts when you query memory, so decisions are made with full information.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Correlation Rules](#correlation-rules)
- [Tools Provided](#tools-provided)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Credits](#credits)

## Overview

The OpenClaw Correlation Plugin enhances memory search capabilities by automatically retrieving related contexts when querying memory. Traditional memory search returns results directly related to the query terms, but often misses contextual information that is crucial for making informed decisions.

When you search for "backup error," normal memory search returns backup-related results. This plugin checks correlation rules and *also* fetches "last backup time," "recovery procedures," and "similar errors" — because those contexts consistently matter together.

Think of it as **decision-context retrieval**: "for X decisions, always also consider Y."

## Features

- **Word-Boundary Matching**: Keyword matching with regex word boundaries prevents false positives
- **Confidence Filtering**: Filter and sort results by confidence threshold
- **Multiple Matching Modes**: Auto, strict, and lenient matching options
- **Result Limiting**: `max_results` parameter prevents output bloat
- **mtime Caching**: Rules cached in memory, refreshed only when file changes
- **Multi-word Keywords**: Support for phrase keywords like "config change"
- **Extensible Architecture**: Easy to add new correlation types
- **Debug Tools**: Understand why correlations are made
- **Error Logging**: Failed rule loads are logged, not silently swallowed

## Security

This plugin has been audited for security vulnerabilities:

- ✅ **Zero external dependencies** - No supply chain risk
- ✅ **No network requests** - Read-only local file operations
- ✅ **No credential access** - Does not handle secrets or tokens
- ✅ **No environment variable harvesting** - Uses SDK config only
- ✅ **Read-only filesystem operations** - Cannot write to disk

**Security Audit:** March 20, 2026 - Passed deep security review.

See: [OpenClaw Security Framework](https://docs.openclaw.ai/security)

## Installation

### Prerequisites

- OpenClaw >= 2026.1.26
- Node.js >= 18.x
- Git

### Steps

1. Clone into OpenClaw extensions:
   ```bash
   cd ~/.openclaw/extensions
   git clone https://github.com/ether-btc/openclaw-correlation-plugin.git correlation-memory
   ```

2. Install dependencies:
   ```bash
   cd ~/.openclaw/extensions/correlation-memory
   npm install
   ```

3. Add to plugins.allow in your `openclaw.json`:
   ```json
   {
     "plugins": {
       "allow": ["correlation-memory"]
     }
   }
   ```

4. Restart OpenClaw gateway:
   ```bash
   openclaw gateway restart
   ```

## Usage

### Basic Usage

Once installed, the correlation plugin automatically enhances memory searches. No additional steps are required for basic functionality.

### Manual Correlation Check

Use the debug tool to see which rules match a given context:

```bash
openclaw exec correlation_check --context "config change"
```

### Adjusting Sensitivity

Control correlation sensitivity through confidence thresholds in your rules.

## Configuration

The plugin requires a correlation rules file at `memory/correlation-rules.json` in your workspace.

### Example Configuration

```json
{
  "rules": [
    {
      "id": "cr-001",
      "created": "2026-03-25T00:00:00Z",
      "trigger_context": "config-change",
      "trigger_keywords": ["config", "setting", "openclaw.json", "modify", "jq", "change"],
      "must_also_fetch": ["backup-location", "rollback-instructions", "recent-changes"],
      "relationship_type": "constrains",
      "confidence": 0.95,
      "lifecycle": {
        "state": "validated"
      },
      "learned_from": "config-misconfiguration-leads-to-service-outage",
      "usage_count": 11,
      "notes": "Any config change should trigger a backup check and rollback plan."
    },
    {
      "id": "cr-002",
      "created": "2026-03-25T00:00:00Z",
      "trigger_context": "error-debugging",
      "trigger_keywords": ["error", "fail", "400", "bug", "broken", "crash"],
      "must_also_fetch": ["recovery-procedures", "recent-changes", "similar-errors"],
      "relationship_type": "diagnosed_by",
      "confidence": 0.9,
      "lifecycle": {
        "state": "promoted"
      },
      "learned_from": "tool-call-errors-recur-without-context",
      "usage_count": 14,
      "notes": "Error debugging without recent changes context is guesswork."
    }
  ]
}
```

> **Tip:** See [`correlation-rules.example.json`](./correlation-rules.example.json) in the repo root for a full set of production-quality rules with detailed documentation.

## Correlation Rules

### Rule Structure

Each correlation rule consists of:

- **id**: Unique identifier for the rule
- **created**: ISO-8601 creation timestamp
- **trigger_context**: Domain context where rule applies
- **trigger_keywords**: Keywords that activate the rule
- **must_also_fetch**: Related contexts to retrieve
- **relationship_type**: Type of relationship (constrains, supports, etc.)
- **confidence**: Confidence level (0.0 to 1.0)
- **lifecycle**: State object with `state` field — see Rule Lifecycle below
- **learned_from**: Descriptive name of the incident or pattern that prompted this rule
- **usage_count**: How many times the rule has fired (for diagnostics)
- **notes** (optional): Human-readable explanation of the rule's purpose

### Rule Lifecycle

Rules follow a lifecycle for safe deployment:
`proposal` → `testing` → `validated` → `promoted` → `retired`

The plugin accepts these states as active: `promoted`, `active`, `testing`, `validated`, `proposal`. Rules without a lifecycle state are also active. Use `retired` to disable rules without deleting them.

### Matching Modes

Three matching modes provide flexibility:
- `auto` (default) — keyword + context matching (word-boundary aware)
- `strict` — word-boundary keyword match only
- `lenient` — fuzzy matching for broad queries

### Confidence Filtering

Both tools accept a `min_confidence` parameter (0-1, default: 0) to filter low-confidence matches. Results are sorted by confidence descending.

### Result Limiting

Both tools accept a `max_results` parameter (default: 10) to cap output size.

## Tools Provided

### `memory_search_with_correlation`

Search memory with automatic correlation enrichment. This tool is automatically used when performing memory searches.

### `correlation_check`

Debug tool — check which rules match a given context without performing searches.

Parameters:
- `--context`: Context to check for matching rules
- `--keywords`: Additional keywords to consider
- `--mode`: Matching mode (auto, strict, lenient)

## Uninstallation

### Via OpenClaw CLI (recommended)

```bash
openclaw plugins uninstall correlation-memory
openclaw gateway restart
```

### Via Uninstall Script

If the CLI is not available, use the bundled uninstall script:

```bash
cd ~/.openclaw/extensions/correlation-memory
./uninstall.sh
```

Options:
- `--force`: Skip confirmation prompt
- Environment variable `OPENCLAW_CONFIG_PATH`: Override config location (default: `~/.openclaw/openclaw.json`)

The uninstall script will:
1. Find your OpenClaw config automatically
2. Back up the config before modification
3. Remove the `correlation-memory` entry from `plugins.entries`
4. Verify removal succeeded
5. Show backup location for recovery

**Note:** Restart the gateway after uninstall: `openclaw gateway restart`

## Documentation

Comprehensive documentation is available in the docs directory:

- [Research Background](./docs/research.md) - Theoretical foundation and related work
- [Deployment Guide](./docs/deployment.md) - Installation, configuration, and troubleshooting
- [Lessons Learned](./docs/lessons.md) - Development insights and best practices
- [Production Guide](./docs/production-guide.md) - **New:** Live deployment experience, heartbeat integration, confidence tuning, and operational best practices
- [Contributing Guide](./CONTRIBUTING.md) - How to contribute to the project

## Contributing

Contributions are welcome! Please see our [Contributing Guide](./CONTRIBUTING.md) for details on:

- Reporting issues
- Suggesting enhancements
- Code contributions
- Contributing correlation rules
- Development guidelines

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## Credits

### Original Development

Built by [Charon](https://github.com/ether-btc) — an OpenClaw agent running on a Raspberry Pi 5.

### Research Inspiration

- [Coolmanns Memory Architecture](https://github.com/coolmanns/openclaw-memory-architecture) — context-aware memory systems
- Cognitive science research on contextual decision making
- Information retrieval literature on query expansion

### Contributors

Thanks to all who have contributed to this project. See [CONTRIBUTING.md](./CONTRIBUTING.md) for details on how to contribute.

### Related Projects

- [OpenClaw](https://github.com/ether-btc/openclaw) - The AI agent platform
- Previous experimental implementations:
  - `correlation-rules-mem` - Plugin lifecycle focus
  - `correlation-memory` - Rich matching logic focus

---

*For more information about OpenClaw, visit [openclaw.dev](https://openclaw.dev)*