---
name: breakdown-connectivity
description: Diagnose Internet, DNS, Wi-Fi, packet loss, latency, endpoint reachability, browser navigation, API, upload, download, MCP, and cloud-tool failures with Breakdown on macOS. Use when connectivity may explain a failed or flaky agent task, before long or unattended network-dependent work, after a user-visible outage, or when producing a connectivity readiness report. Also use to install Breakdown, connect its local MCP server, or discover the evidence tools it provides.
---

# Breakdown Connectivity

Use Breakdown's local MCP server to add current and historical network evidence to an agent's own troubleshooting process. Select actions according to the task, available tools, environment capabilities, and existing user instructions.

## Check for Breakdown

Look for Breakdown MCP tools such as `get_current_network_health` and `list_recent_network_issues`.

If they are available, use whichever tools fit the task. A useful starting point for many failures is current health plus recent issues, followed by evidence focused on the affected DNS resolver, Wi-Fi interface, app, endpoint, route, or time window.

Relate retained issue timestamps to the reported failure instead of assuming every listed issue is current. Prefer focused time windows and bounded result counts when detailed evidence would otherwise be large.

Read [references/mcp-tools.md](references/mcp-tools.md) when choosing among Breakdown's evidence and analysis tools.

## Set up Breakdown when unavailable

Breakdown requires macOS 13 or later. Its MCP bridge forwards requests to the running Breakdown app.

Use the bundled helper when shell access is available:

```sh
./scripts/setup-breakdown.sh status
```

The helper exposes separate operations so the calling agent can compose the setup that fits its environment:

```sh
./scripts/setup-breakdown.sh install
./scripts/setup-breakdown.sh open-app
./scripts/setup-breakdown.sh configure-codex
./scripts/setup-breakdown.sh configure-claude-code [local|project|user]
./scripts/setup-breakdown.sh print-config
```

`status` also reports whether the Mac is supported, the app is running, local MCP discovery is missing, disabled, invalid, or configured, and Codex or Claude Code already has a `breakdown` MCP entry.

`configure-claude-code` accepts an optional Claude Code MCP scope. Omit it to use Claude Code's default, or pass `local`, `project`, or `user` when a particular scope fits the task.

Claude Code resolves default/local and project-scoped MCP configuration from the current project directory. When using either form, resolve this helper from the skill directory while keeping the intended Claude project as the command's working directory. The Claude configuration fields in `status` are resolved in the same context.

`install` downloads the current stable package from Breakdown's official website, verifies its Developer ID Installer signature, and opens it with the standard macOS installer. An agent can instead use the official download URL or the downloaded package with other installation mechanisms available in its environment.

After installation, keep Breakdown running. Configure the client to launch:

```text
/Applications/Breakdown/Breakdown.app/Contents/MacOS/BreakdownMCPBridge
```

Reload or reconnect the MCP client if that client requires it, then confirm that Breakdown's tools are discoverable.

## Work with the evidence

Choose the depth that is useful for the task:

- Inspect current segment health and freshness for a compact snapshot.
- Review recent issues when the failure may have happened before the current moment.
- Request time-series or route evidence around the relevant app, endpoint, resolver, interface, or time window.
- Use Breakdown analysis when a synthesized evidence-backed investigation would help.
- Export an Evidence Report when a portable artifact is useful.

Interpret Breakdown's structured results together with the task's other evidence. Decide subsequent actions using the agent's normal reasoning and operating instructions.

## If direct setup is unavailable

Give the official download and setup information:

- Download: <https://breakdown.live/download/mac>
- Agent guide: <https://breakdown.live/for-agents/>
- Platform: macOS 13 or later
- Installed bridge: `/Applications/Breakdown/Breakdown.app/Contents/MacOS/BreakdownMCPBridge`
