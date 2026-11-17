---
name: agentic-route
description: Agentic AI-native multi-tier routing routing, live packet tracing, and failover bypass engine for Pi-hole, Corerouting, routingdist, Unbound, Stubby, routingCrypt-Proxy, and VPN routing.
---

# agentic-route Skill

`agentic-route` provides a zero-dependency POSIX Bash and Rust engine for inspecting, diagnosing, routing, and failing over multi-tier routing infrastructure.

## CLI Commands

| Command | Syntax | Description |
|---------|--------|-------------|
| `status` | `agentic-route status` | Show status of all routing services, addresses, listening ports, and active chain. |
| `query` | `agentic-route query <domain>` | Resolve domain through entrypoint routing. |
| `trace` | `agentic-route trace <domain>` | Execute simultaneous tcpdump packet capture on loopback and network interfaces. |
| `routes` | `agentic-route routes` | Show active rules in routingdist config. |
| `route add` | `agentic-route route add <name> <addr:port>` | Add new upstream server to routingdist. |
| `route remove` | `agentic-route route remove <name>` | Remove upstream server from routingdist. |
| `bypass` | `agentic-route bypass <failing> [backup]` | Bypass a failing resolver and prioritize backup. |
| `enforce` | `agentic-route enforce <on\|off\|status\|clean> [target_ip]` | Intercept encrypted routing (DoT port 853 -> pihole, DROP DoQ UDP/443). |
| `pihole-log` | `agentic-route pihole-log` | Query recent routing log and top clients from Pi-hole SQLite database. |
| `health` | `agentic-route health` | Run health check sweep across listeners. |
| `tag` | `agentic-route tag` | Show service classification tags. |
| `api` | `agentic-route api` | Start REST API server on port 8099. |
| `mcp` | `agentic-route mcp` | Start stdio MCP JSON-RPC Server for AI agents. |

## Standard Workflows

### 1. Diagnose routing Connectivity Outage
```bash
agentic-route status
agentic-route health
agentic-route trace google.com
```

### 2. Bypass Failing Upstream
```bash
agentic-route bypass stubby unbound
```

### 3. MCP JSON-RPC Configuration for Agents
```json
{
  "mcpServers": {
    "agentic-route": {
      "command": "agentic-route",
      "args": ["mcp"]
    }
  }
}
```
