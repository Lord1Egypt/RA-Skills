#!/usr/bin/env bash
# NOTE: On CIFS/SMB mounts, run with: bash scaffold.sh
# Sets up debugging utilities: structured logging, VS Code launch configs, debug helper scripts

set -euo pipefail

PROJECT_DIR="${1:-.}"
echo "Setting up debug utilities in: $PROJECT_DIR"

# Detect project type
LANG="unknown"
if [ -f "$PROJECT_DIR/package.json" ]; then
  LANG="node"
elif [ -f "$PROJECT_DIR/pyproject.toml" ] || [ -f "$PROJECT_DIR/requirements.txt" ] || [ -f "$PROJECT_DIR/setup.py" ]; then
  LANG="python"
fi

echo "Detected project type: $LANG"

# ── Create .vscode directory ──────────────────────────────────────────

mkdir -p "$PROJECT_DIR/.vscode"

# ── VS Code launch.json ──────────────────────────────────────────────

if [ "$LANG" = "node" ]; then
  cat > "$PROJECT_DIR/.vscode/launch.json" << 'LAUNCHEOF'
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Current File",
      "type": "node",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "skipFiles": ["<node_internals>/**", "node_modules/**"]
    },
    {
      "name": "Debug Tests (Jest)",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/node_modules/.bin/jest",
      "args": ["--runInBand", "--no-coverage", "${relativeFile}"],
      "console": "integratedTerminal",
      "skipFiles": ["<node_internals>/**"]
    },
    {
      "name": "Debug Tests (Vitest)",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/node_modules/.bin/vitest",
      "args": ["run", "--no-coverage", "${relativeFile}"],
      "console": "integratedTerminal",
      "skipFiles": ["<node_internals>/**"]
    },
    {
      "name": "Attach to Process",
      "type": "node",
      "request": "attach",
      "port": 9229,
      "skipFiles": ["<node_internals>/**", "node_modules/**"]
    }
  ]
}
LAUNCHEOF

elif [ "$LANG" = "python" ]; then
  cat > "$PROJECT_DIR/.vscode/launch.json" << 'LAUNCHEOF'
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Current File",
      "type": "debugpy",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "justMyCode": true
    },
    {
      "name": "Debug FastAPI",
      "type": "debugpy",
      "request": "launch",
      "module": "uvicorn",
      "args": ["app.main:app", "--reload", "--port", "8000"],
      "console": "integratedTerminal",
      "justMyCode": true
    },
    {
      "name": "Debug pytest",
      "type": "debugpy",
      "request": "launch",
      "module": "pytest",
      "args": ["-xvs", "${relativeFile}"],
      "console": "integratedTerminal",
      "justMyCode": true
    },
    {
      "name": "Attach to Remote",
      "type": "debugpy",
      "request": "attach",
      "connect": { "host": "localhost", "port": 5678 },
      "justMyCode": true
    }
  ]
}
LAUNCHEOF

else
  cat > "$PROJECT_DIR/.vscode/launch.json" << 'LAUNCHEOF'
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Current File (Node)",
      "type": "node",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "skipFiles": ["<node_internals>/**"]
    },
    {
      "name": "Debug Current File (Python)",
      "type": "debugpy",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "justMyCode": true
    }
  ]
}
LAUNCHEOF
fi

echo "  Created .vscode/launch.json ($LANG configs)"

# ── VS Code settings.json (debug-friendly) ──────────────────────────

if [ ! -f "$PROJECT_DIR/.vscode/settings.json" ]; then
  cat > "$PROJECT_DIR/.vscode/settings.json" << 'SETEOF'
{
  "debug.console.fontSize": 14,
  "debug.inlineValues": "on",
  "debug.showBreakpointsInOverviewRuler": true,
  "debug.toolBarLocation": "docked"
}
SETEOF
  echo "  Created .vscode/settings.json"
else
  echo "  Skipped .vscode/settings.json (already exists)"
fi

# ── Create scripts directory ─────────────────────────────────────────

mkdir -p "$PROJECT_DIR/scripts"

# ── Debug helper: structured logging setup ───────────────────────────

if [ "$LANG" = "node" ]; then
  cat > "$PROJECT_DIR/scripts/debug-logger.ts" << 'LOGEOF'
/**
 * Structured debug logger with context and levels.
 * Usage:
 *   import { logger } from './scripts/debug-logger';
 *   logger.info('User logged in', { userId: 123 });
 *   logger.error('Failed to fetch', { url, status });
 */

type LogLevel = 'debug' | 'info' | 'warn' | 'error';

const LEVELS: Record<LogLevel, number> = {
  debug: 0,
  info: 1,
  warn: 2,
  error: 3,
};

const currentLevel: LogLevel = (process.env.LOG_LEVEL as LogLevel) || 'info';

function log(level: LogLevel, message: string, context?: Record<string, unknown>): void {
  if (LEVELS[level] < LEVELS[currentLevel]) return;

  const entry = {
    timestamp: new Date().toISOString(),
    level: level.toUpperCase(),
    message,
    ...context,
  };

  const output = JSON.stringify(entry);

  switch (level) {
    case 'error': console.error(output); break;
    case 'warn':  console.warn(output);  break;
    default:      console.log(output);   break;
  }
}

export const logger = {
  debug: (msg: string, ctx?: Record<string, unknown>) => log('debug', msg, ctx),
  info:  (msg: string, ctx?: Record<string, unknown>) => log('info', msg, ctx),
  warn:  (msg: string, ctx?: Record<string, unknown>) => log('warn', msg, ctx),
  error: (msg: string, ctx?: Record<string, unknown>) => log('error', msg, ctx),
};
LOGEOF
  echo "  Created scripts/debug-logger.ts"

elif [ "$LANG" = "python" ]; then
  cat > "$PROJECT_DIR/scripts/debug_logger.py" << 'LOGEOF'
"""
Structured debug logger with context and levels.
Usage:
    from scripts.debug_logger import logger
    logger.info("User logged in", user_id=123)
    logger.error("Failed to fetch", url=url, status=status)
"""

import json
import logging
import sys
from datetime import datetime, timezone


class StructuredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        # Merge extra context
        if hasattr(record, "context") and isinstance(record.context, dict):
            entry.update(record.context)
        if record.exc_info and record.exc_info[1]:
            entry["exception"] = str(record.exc_info[1])
        return json.dumps(entry)


def get_logger(name: str = "app") -> logging.Logger:
    log = logging.getLogger(name)
    if not log.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(StructuredFormatter())
        log.addHandler(handler)
        log.setLevel(logging.DEBUG)
    return log


logger = get_logger()
LOGEOF
  echo "  Created scripts/debug_logger.py"
fi

# ── Debug helper: quick bisect script ────────────────────────────────

cat > "$PROJECT_DIR/scripts/bisect-test.sh" << 'BISEOF'
#!/usr/bin/env bash
# Quick git bisect helper.
# Usage:
#   git bisect start HEAD <last-known-good-commit>
#   git bisect run bash scripts/bisect-test.sh
#
# Edit the TEST_COMMAND below to match your test.

set -euo pipefail

# ── EDIT THIS: the command that should pass ──
TEST_COMMAND="npm test"
# TEST_COMMAND="python -m pytest tests/test_specific.py -x"
# TEST_COMMAND="cargo test specific_test"

echo "=== Bisect test at $(git rev-parse --short HEAD) ==="

if $TEST_COMMAND; then
  echo "PASS — this commit is good"
  exit 0   # good
else
  echo "FAIL — this commit is bad"
  exit 1   # bad
fi
BISEOF
echo "  Created scripts/bisect-test.sh"

# ── Debug helper: timing/profiling wrapper ───────────────────────────

cat > "$PROJECT_DIR/scripts/time-request.sh" << 'TIMEEOF'
#!/usr/bin/env bash
# Time an HTTP request with detailed breakdown.
# Usage: bash scripts/time-request.sh https://localhost:3000/api/health

set -euo pipefail

URL="${1:?Usage: bash scripts/time-request.sh <URL>}"

echo "Timing request to: $URL"
echo ""

curl -o /dev/null -s -w "\
  DNS Lookup:    %{time_namelookup}s\n\
  TCP Connect:   %{time_connect}s\n\
  TLS Handshake: %{time_appconnect}s\n\
  Start Transfer:%{time_starttransfer}s (TTFB)\n\
  Total:         %{time_total}s\n\
  \n\
  HTTP Code:     %{http_code}\n\
  Download Size: %{size_download} bytes\n" "$URL"
TIMEEOF
echo "  Created scripts/time-request.sh"

# ── .env.debug template ─────────────────────────────────────────────

if [ ! -f "$PROJECT_DIR/.env.debug" ]; then
  cat > "$PROJECT_DIR/.env.debug" << 'ENVEOF'
# Debug environment variables — source before debugging
# Usage: source .env.debug && node app.js

# Logging
LOG_LEVEL=debug

# Node.js
NODE_OPTIONS="--enable-source-maps"
# NODE_OPTIONS="--inspect"
# NODE_OPTIONS="--inspect-brk"

# Python
# PYTHONDONTWRITEBYTECODE=1
# PYTHONUNBUFFERED=1
ENVEOF
  echo "  Created .env.debug"
else
  echo "  Skipped .env.debug (already exists)"
fi

# ── Summary ──────────────────────────────────────────────────────────

echo ""
echo "Debug utilities set up successfully!"
echo ""
echo "Files created:"
echo "  .vscode/launch.json    — debugger launch configurations"
echo "  .vscode/settings.json  — debug-friendly editor settings"
if [ "$LANG" = "node" ]; then
  echo "  scripts/debug-logger.ts — structured JSON logger"
elif [ "$LANG" = "python" ]; then
  echo "  scripts/debug_logger.py — structured JSON logger"
fi
echo "  scripts/bisect-test.sh  — git bisect test runner"
echo "  scripts/time-request.sh — HTTP request timing"
echo "  .env.debug              — debug environment variables"
echo ""
echo "Quick start:"
echo "  1. Open the project in VS Code"
echo "  2. Press F5 to start debugging with the launch config"
echo "  3. Set breakpoints by clicking the gutter"
