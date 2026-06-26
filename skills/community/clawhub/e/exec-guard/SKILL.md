---
name: exec-guard
description: Safe command execution for AI agents with timeout control, 8KB ring buffer memory protection, background process management, and multi-agent sharing via HTTP service. Use when executing system commands, running long tasks, starting services, or managing background processes. Supports CLI and HTTP server modes.
---

# exec-guard - AI Agent Command Execution Module

Safe and reliable system command execution for AI agents.

## Quick Start

### CLI Mode

```bash
echo '{"command": "ls -la"}' | node scripts/dist/index.js
```

### HTTP Service Mode

```bash
node scripts/dist/index.js --server --port 8080
curl -X POST http://localhost:8080/exec -H "Content-Type: application/json" -d '{"command": "ls -la"}'
```

## Core Capabilities

| Capability | Description |
|------------|-------------|
| **Sync Execution** | Execute command with timeout, wait for result |
| **Background Execution** | Start long tasks, get PID, query later |
| **Watch Window** | Confirm service startup before returning |
| **8KB Ring Buffer** | Head-Tail dual buffer prevents OOM |
| **Process Management** | Query status, get logs, terminate processes |
| **Multi-Agent Sharing** | HTTP service allows multiple agents to share state |

## API Reference

### POST /exec

Execute a command:

```json
{
  "command": "required - system command",
  "workingDir": "optional - working directory",
  "timeoutSeconds": "optional - default 30",
  "runInBackground": "optional - default false",
  "watchDurationSeconds": "optional - for service startup",
  "env": "optional - custom environment variables"
}
```

### GET /process/:pid

Query process status.

### GET /process/:pid/logs

Get process output logs.

### DELETE /process/:pid

Terminate a process.

### GET /processes

List all background processes.

## Response Status

| Status | Meaning |
|--------|---------|
| `success` | Command completed, exit code 0 |
| `failed` | Command failed, non-zero exit |
| `timeout` | Command killed after timeout |
| `killed` | Process manually terminated |
| `running` | Background process active |

## Best Practices

1. **Set reasonable timeout** - Prevent stuck commands
2. **Use watch window for services** - Confirm startup success
3. **Use background mode for long tasks** - Training, data processing
4. **Clean up processes** - Terminate when done

## Full Documentation

See `references/AGENT_GUIDE.md` for detailed usage guide and examples.

## License

MIT