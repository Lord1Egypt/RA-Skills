---
name: cleimesh-mcp
description: Put the MCP tools an agent already uses behind CleiMesh, so each tool call runs under a signed, narrowable token and leaves a replayable receipt — a prompt injection cannot widen the grant, and you can prove afterwards what every tool did. Use when the user runs MCP servers in Claude Code, Cursor or another MCP client and wants to limit what a tool may touch, stop an injected tool call from reaching keys or the network, or produce an auditable, replayable record (audits, GDPR, LGPD). Also use after wrapping, when a CleiMesh-guarded MCP call is refused.
license: MIT OR Apache-2.0
homepage: https://github.com/cleitonaugusto/cleimesh
---

# Put an agent's MCP tools behind CleiMesh

Most guardrails **decide at the door** and then let the tool run with full access, and their logs ask you to trust whoever signed them. CleiMesh is different on two points no gateway offers: the token **becomes the sandbox** (default-deny, and it can only narrow as it is delegated), and **every call leaves a signed receipt you can re-run** to check the result byte for byte. This skill puts the MCP tools an agent already uses behind that.

Project: https://github.com/cleitonaugusto/cleimesh

## Ground rules for you, the agent

- **The human runs the commands that change the system, not you.** Installing the binary, issuing a root token and registering an MCP server are the user's to run. Prepare the exact commands, explain them, and hand them over. An agent that installs its own guard can also skip a step of it.
- Never suggest widening a token, clearing a taint or re-enabling a native tool to get a task done — each of those is what an injection would ask for, and each is the human's decision.
- Be honest about the two modes below: `serve` runs tools in the WASM sandbox (fully contained); `wrap` puts a **native** MCP server behind the token (checked and receipted, but not sandboxed — it still reaches whatever its own OS user can). Say which one applies.

## 1. Install (user runs it)

```sh
curl -fsSL https://github.com/cleitonaugusto/cleimesh/releases/latest/download/install.sh | sh
```

Check: `cleimesh --version`.

## 2. Issue a token for the MCP holder

A node issues a root token to a **holder** (a PeerId); each holder can derive a **narrower** one offline, never wider (Attenuating Agent Tokens). The holder here is the key the MCP server runs under (default `~/.config/cleimesh/client.key`).

```sh
cleimesh id --client                    # the holder's PeerId (run on the holder's machine)
cleimesh token issue <HOLDER_PEERID> \
    --tool file_read --read ./project \
    -o agent.json                       # grants file_read over ./project, nothing else
```

Flags that matter: `--tool <name>` (repeatable; a tool with no `--read/--write/--network` sees no directory at all), `--read`/`--write <DIR>`, `--network`, `--taints` (the tool brings in outside content → taints the chain), `--clean-only` (the tool acts on the world → refused while tainted). Delegate further with `cleimesh token derive <chain> <HOLDER_PEERID> --tool ... -o narrower.json`.

Keep grants narrow: never the home folder, never `~/.ssh`, `~/.aws`, or `.env` folders. Confirm the directories **with the user** — do not guess. Full flags: `cleimesh token issue --help`.

## 3. Pick a mode

### A. `serve` — CleiMesh's own tools, in the WASM sandbox (fully contained)

Register CleiMesh as an MCP server; every `tools/call` presents the token chain with a fresh proof of possession, runs under its grants in WASM, and leaves a receipt. Without `--token`, every call is refused.

```sh
claude mcp add cleimesh -- cleimesh mcp serve --token agent.json
```

### B. `wrap` — put an existing (native) MCP server behind the token

The wrapped server's client sees only the tools the token grants; each call is checked against the token's argument constraints and taint, and leaves a signed receipt. **The wrapped server is NOT sandboxed** — it reaches whatever its OS user can, so a token granting it directories or network is a real limit only to the extent the server honours those arguments. Say this to the user.

```sh
claude mcp add fetch -- cleimesh mcp wrap --token fetch.json -- uvx mcp-server-fetch
```

(Cursor and other MCP clients: same `cleimesh mcp serve|wrap ...` command, registered their way.)

## 4. Prove it — the part gateways can't do

After the agent has run, the signed receipt log (default `~/.local/share/cleimesh/receipts/receipts.jsonl`) is the evidence:

```sh
cleimesh audit verify                 # check every signature and the hash chain (non-zero on failure)
cleimesh audit tail                   # read the recent calls, allowed and refused
cleimesh audit replay <step-id>       # re-run a call from its receipt, compare the outcome byte for byte
cleimesh audit report --subject <id>  # privacy report per data subject / agent (GDPR, LGPD)
cleimesh audit suggest                # the narrower token the agent actually needed
```

`audit verify` catches a tampered or truncated log; `audit replay` catches a node that signed a false result (only calls without directories or network replay). Keep a log head off the machine (`cleimesh audit head`) and pass it to `verify` to detect a rolled-back log.

## 5. If a call is refused

A refusal is the guard working. Read why with `cleimesh audit tail`. Common causes: the tool asked for a path outside its grant, the token doesn't cover that tool, or the agent is **tainted** (it read untrusted content, so writes and network are refused until a human runs `cleimesh taint clear ... --reason "<why>"`). Do not route around it — surface the reason to the user and let them decide.

## Where it fits

CleiMesh governs **each tool call** and proves it; agent sandboxes (NVIDIA OpenShell, AWS Strands Box, Anthropic sandbox-runtime) contain the **process**. They complement each other: run the agent in one of those, and route the MCP tools that touch the user's data through CleiMesh. For putting an agent's own file/shell tools (not MCP) behind CleiMesh, use the `cleimesh-setup` skill.
