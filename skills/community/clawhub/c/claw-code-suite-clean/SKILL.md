---
name: claw-code-suite
description: Python-only integration of Claw Code harness engineering project with OpenClaw. Provides access to 184 tools and 200+ commands for security analysis, code quality, development workflows, and agent orchestration. NO NETWORK ACCESS, NO CREDENTIALS REQUIRED, PURELY OFFLINE.
homepage: https://github.com/instructkr/claw-code
metadata:
  {
    "openclaw":
      {
        "emoji": "🦞",
        "requires": { "bins": ["python3"] },
        "install":
          [
            {
              "id": "verify-python",
              "kind": "exec",
              "command": "python3 --version",
              "label": "Verify Python 3 is available",
            },
          ],
      },
  }
---

# Claw Code Suite (Python-Only Edition)

**Version: 1.0.1** - Clean, security-scanner compliant edition

Pure Python integration of the Claw Code harness engineering project with OpenClaw. This skill provides structured access to **184 tools** and **207 commands** mirrored from the original TypeScript implementation, including security analysis, code quality tools, development workflows, and agent orchestration patterns.

## 🔒 SECURITY & TRANSPARENCY GUARANTEE

This edition has been **audited and verified** to contain:

- ✅ **NO NETWORK ACCESS** - No HTTP clients, no web servers, no external API calls
- ✅ **NO CREDENTIALS REQUIRED** - No API keys, no OAuth, no authentication tokens
- ✅ **NO BACKGROUND DAEMONS** - No persistent processes, no servers binding to ports
- ✅ **NO ARBITRARY CODE EXECUTION** - Strict allowlists for tools and commands only
- ✅ **PURELY OFFLINE OPERATION** - All analysis runs locally on your machine
- ✅ **FULL SOURCE CODE TRANSPARENCY** - All Python code included and inspectable

## Quick Start

Once installed, the skill exposes several high-level commands:

```bash
# Get system overview
./run.sh summary

# List available tools (first 10)
./run.sh tools --limit 10

# List available commands (first 10)
./run.sh commands --limit 10

# Route a prompt to find matching tools/commands
./run.sh route --prompt "analyze bash script for security issues" --limit 5

# Execute a specific tool (e.g., bashSecurity)
./run.sh exec-tool --name bashSecurity --payload "#!/bin/bash\necho test"

# Execute a specific command
./run.sh exec-command --name advisor --prompt "review this code"
```

## Available Capabilities

### Tool Categories

- **Security Analysis**: `bashSecurity`, `powershellSecurity`, etc.
- **Code Quality**: Various code analysis and linting tools
- **Development Workflows**: Build, test, deployment automation
- **Agent Orchestration**: `AgentTool`, `forkSubagent`, `runAgent`, etc.
- **UI Components**: `UI`, `agentDisplay`, `agentColorManager`
- **Memory & State**: `agentMemory`, `agentMemorySnapshot`

### Command Categories

- **Execution Commands**: `exec-command`, `exec-tool`
- **Routing & Discovery**: `route`, `show-command`, `show-tool`
- **Session Management**: `load-session`, `flush-transcript`
- **Runtime Modes**: `remote-mode`, `ssh-mode`, `teleport-mode` (placeholders only)
- **Analysis & Reporting**: `summary`, `manifest`, `parity-audit`

## How It Works

1. **Pure Python Implementation**: The entire skill runs in Python with no external dependencies beyond Python 3.
2. **Harness Wrapper**: The `claw_harness.py` provides a production-grade Python wrapper around the Claw Code clean-room port.
3. **Enhanced Harness**: `claw_harness_enhanced.py` supports expanded command set with positional arguments.
4. **Structured Execution**: All commands run with timeouts, output limits, and structured JSON results.
5. **Safe Sandboxing**: Command and argument allowlists prevent arbitrary code execution.
6. **Local Only**: All operations are performed locally with no network calls.

## Integration Examples

### Security Analysis
```bash
# Analyze a bash script
./run.sh exec-tool --name bashSecurity --payload "$(cat script.sh)"

# Analyze PowerShell
./run.sh exec-tool --name powershellSecurity --payload "$(cat script.ps1)"
```

### Code Review
```bash
# Route a code review request
./run.sh route --prompt "review this Python function for bugs" --limit 5

# Use the advisor command
./run.sh exec-command --name advisor --prompt "Review this API endpoint for security issues"
```

### Agent Orchestration
```bash
# Start an agent session (simulated locally)
./run.sh exec-tool --name runAgent --payload "Explore the current directory structure"

# Fork a subagent for specific task
./run.sh exec-tool --name forkSubagent --payload "Write unit tests for module X"
```

## Configuration

Environment variables (optional):

- `CLAW_CODE_WORKSPACE`: Path to claw-code repository (default: `./claw-code`)
- `CLAW_CODE_TIMEOUT_SEC`: Command timeout in seconds (default: 120)
- `CLAW_CODE_MAX_OUTPUT_CHARS`: Maximum output length (default: 25000)
- `CLAW_CODE_EVENT_LOG`: Path to event log file

## Skill Structure

```
claw-code-suite/
├── SKILL.md                    # This file
├── run.sh                      # Main entry point
├── claw_harness.py             # Original production harness wrapper (6 commands)
├── claw_harness_enhanced.py    # Enhanced harness with full command set
├── claw_wrapper.py             # Python adapter
├── scripts/
│   └── claw_wrapper.py         # Core Python wrapper
├── claw-code/                  # Claw Code Python port (full, clean)
│   ├── src/                    # Python source code (184 tools, 207 commands)
│   ├── tests/                  # Test suite
│   └── telemetry/              # Event logging
├── capability_index.json       # Tool/command inventory
└── package.json                # Node.js metadata
```

## Security Verification

To verify this skill contains no network code:

```bash
# Check for network imports in Python code
find . -name "*.py" -exec grep -l "requests\|http\.client\|urllib\|socket" {} \;

# Check for Rust/Cargo files (should be none)
find . -name "*.rs" -o -name "Cargo.*" -o -name "*.toml"

# Check for server/binding code
find . -name "*.py" -exec grep -l "server\|bind\|listen\|port" {} \;
```

## Changelog

### v1.0.1 (2026-04-06)
- **SECURITY FIX**: Removed entire Rust workspace (api/, server/, runtime/, etc.)
- **TRANSPARENCY**: Updated documentation to accurately reflect Python-only nature
- **VERIFICATION**: All network/server/AI provider code removed
- **COMPLIANCE**: Now passes ClawHub security scanner without flags
- **FUNCTIONALITY**: All 184 tools and 207 commands remain fully functional

### v1.0.0 (2026-04-01)
- Initial release with full Claw Code Python port
- Included Rust workspace (removed in v1.0.1 for security)

## Advanced Usage

### Direct Python API
```python
import sys
sys.path.append(".")
from claw_harness_enhanced import claw_invoke, claw_exec_tool
import asyncio

async def main():
    result = await claw_exec_tool("bashSecurity", "#!/bin/bash\necho test")
    print(result)

asyncio.run(main())
```

### Using Enhanced Harness Directly
```bash
python3 -c "
import asyncio
from claw_harness_enhanced import claw_route
result = asyncio.run(claw_route('security audit', 3))
print(result)
"
```

## Development

The skill is built on the Claw Code Python port, which mirrors 184 tools and 207 commands from the original TypeScript implementation. The port maintains parity with the original while providing a clean Python API.

To extend or modify:
1. Edit `claw_harness_enhanced.py` to expose additional commands from `src/main.py`
2. Update `COMMAND_DEFS` in the harness
3. Test with `./run.sh --summary` to verify functionality

## License

Claw Code is licensed under its original terms. This integration skill is provided as-is for OpenClaw users.

## Support

- GitHub: https://github.com/instructkr/claw-code
- OpenClaw Discord: https://discord.com/invite/clawd
- ClawHub: https://clawhub.ai