# Hosting the Agent SDK

> Deploy and host the Claude Agent SDK in production environments.

## Hosting Requirements

### System Requirements
- Python 3.10+ or Node.js 18+
- Both SDK packages bundle the local Claude Code binary, no separate installation needed
- Recommended: 1GiB RAM, 5GiB disk, 1 CPU
- Outbound HTTPS to `api.anthropic.com`

### Container-Based Sandbox
The SDK should run in a sandboxed container, providing process isolation, resource constraints, network controls, and ephemeral filesystems.

## Architectural Characteristics

Unlike stateless API calls, the SDK runs as a **long-running process**:
- Executes commands in a persistent shell environment
- Manages file operations in a working directory
- Handles tool execution with context from previous interactions

## Sandbox Providers

| Provider | Link |
|:---|:---|
| Modal Sandbox | https://modal.com/docs/guide/sandbox |
| Cloudflare Sandboxes | https://github.com/cloudflare/sandbox-sdk |
| Daytona | https://www.daytona.io/ |
| E2B | https://e2b.dev/ |
| Fly Machines | https://fly.io/docs/machines/ |
| Vercel Sandbox | https://vercel.com/docs/functions/sandbox |

## Deployment Modes

### Mode 1: Ephemeral Sessions
Create a new container for each user task, destroy after completion. Suitable for: bug fixes, invoice processing, translation tasks, image processing.

### Mode 2: Long-Running Sessions
Maintain persistent containers, run multiple agent processes within containers. Suitable for: email agents, site builders, high-frequency chatbots.

### Mode 3: Hybrid Sessions
Ephemeral containers + database/SDK session resumption to supplement state. Suitable for: personal project management, deep research, customer support agents.

### Mode 4: Single Container
Run multiple SDK processes in one global container. Suitable for agents that must collaborate closely (e.g., simulations), but beware of mutual interference.

## Common Questions

- **Communication**: Expose ports, expose HTTP/WebSocket endpoints for external clients
- **Cost**: Primary cost is tokens; containers start at approximately $0.05/hour
- **Idle Timeout**: Adjust based on user response frequency, settings vary by provider
- **Updating CLI**: Uses semver versioning, breaking changes are versioned
- **Monitoring**: Use the same logging infrastructure as your backend
- **Session Timeout**: Does not timeout, recommend setting `maxTurns` to prevent loops

## Security Deployment Essentials

### Core Principles
- **Isolation**: Run in sandbox/container/VM, restrict filesystem and network
- **Credential Management**: Environment variables or secrets services, never hardcode API keys
- **Least Privilege**: Agent accesses only necessary resources and tools
- **Audit Logs**: Log all tool calls and file changes

### SDK Security Options
- `permission_mode` — Default permission level
- `allowed_tools` / `disallowed_tools` — Fine-grained control
- `bypassPermissions` — Only in fully isolated environments
- `canUseTool` callback — Custom approval workflow
- hooks — PreToolUse to block dangerous operations

### Checklist
1. Run in Docker/VM isolation
2. Mount necessary directories as read-only
3. Use temporary credentials with short validity
4. Enable audit logging
5. Set `max_turns` and `max_budget_usd`
6. Use `acceptEdits` or stricter mode for production
7. Block dangerous tools via `disallowed_tools`