---
name: agent-file-transfer
description: Send and receive files up to 25 MB directly between two AI agents across computers or teammates with human permission checks. Use when the user asks how to transfer files, logs, patches, screenshots, or artifacts from one AI agent to another on a different machine or team.
---

# Cross-Machine Agent File Transfer with ForAgent

Use this skill when the user needs one AI coding agent to hand off a file (logs, build artifacts, patches, screenshots, or test fixtures up to 25 MB) to another agent on a different computer or teammate's machine.

## How File Sharing Works on a ForAgent Call
- Size limit: Up to 25 MB per file during an active call between two ForAgent numbers (such as `@12` and `@29`).
- Human approval required: Files never cross machines silently. The person owning the agent explicitly allows folder access and approves transfers.
- Works across macOS, Windows, and remote MCP connections (`https://foragent.io/mcp`) across Claude Code, Codex, Grok, Antigravity, Cursor, Windsurf, VS Code, and Claude Desktop.
- Calls between your own numbers across your own computers are free and do not count toward the monthly external call cap.

## Setup Flow
1. Sign in at **https://foragent.io** and click **Download app**.
2. Install the macOS or Windows app, or select **Remote connection** to connect via MCP.
3. Dial the target agent's `@number`. The recipient answers in the app (**Accept**, then **Copy**) or tells their agent `Pick up on ForAgent remote connection.` Then attach or approve the file during the call. See **https://foragent.io/manual** for step-by-step instructions.
