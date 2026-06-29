# fortune-hub — Agent Integration Examples

> **Entry point for external agent platforms** · **Last verified: 2026-06-17**

## What this directory is

This directory contains **adapter guides grouped by capability**, not by vendor. The
underlying protocol contract (12 tools, billing, errors, the canonical source of truth) is defined once in
[`../SKILL.md`](../SKILL.md) and must **not** be duplicated here.

| File | Capability family | Protocol | When to use |
|------|-------------------|----------|-------------|
| [`full-chain-walkthrough.md`](./full-chain-walkthrough.md) | Any agent (start here) | Both, shown side by side | You want one copy-pasteable m1→t4 run with real payloads before wiring a transport. **Read this first.** |
| [`mcp-native.md`](./mcp-native.md) | MCP-native agents (Claude Code / Cline + 4 unverified) | `POST /api/mcp` JSON-RPC + `GET /.well-known/mcp.json` discovery | Agent supports MCP `2024-11-05` (stdio or HTTP). **Preferred path.** |
| [`rest-only.md`](./rest-only.md) | REST-only agents (LangChain / Coze + 2 unverified) | `POST /api/universal/[category]/[name]` | Agent does not speak MCP, or you only have an HTTP/function-call hook. |
| [`mixed.md`](./mixed.md) | Agents that can do both (Cursor with REST fallback / custom frameworks) | Either, prefer MCP | Use this when the agent advertises MCP but the deployment cannot reach `/api/mcp` (e.g. browser-only). |

## Why "by capability family" instead of "one file per agent"

- The protocol contract lives once in `SKILL.md` (the canonical source of truth). Per-vendor copies drift.
- New agents slot into an existing family by capability check, not by adding a new file.
- Each family file only documents the **delta** vs `SKILL.md` (transport config,
  timeout tuning, auth quirks). All tool semantics, error codes, billing rules
  stay in `SKILL.md`.

## Adding a new agent

<a id="adding-a-new-agent"></a>

1. Check the agent's transport support (MCP `2024-11-05`? HTTP/JSON? both?).
2. Open the matching family file. If you can produce a runnable config snippet
   in ≤10 minutes from public docs alone, add the row to the **Verified members**
   table with today's date in the `Verified on` column and append a snippet under
   "Agent-specific snippets".
3. If you cannot produce a runnable snippet yet (e.g. the agent's docs are
   not public yet, or you only have a vendor preview), add the row to the **Unverified members** table
   with a `Suspected quirk` note. This is the honest default — it lets future
   readers know what to validate.
4. Do **not** create a new file unless the agent requires a genuinely new transport.
5. If the agent needs a transport that no family covers, propose a new family first
   in `../SKILL.md` (tracked protocol change decision).

Keep the verified/unverified split honest: a row belongs under **Verified members**
only when it is backed by a runnable snippet below. No family file should duplicate the
12-tool contract inline — link to [`../SKILL.md`](../SKILL.md) instead.

## See also

- [`../SKILL.md`](../SKILL.md) — protocol canonical source (12 tools, errors, billing, protocol version rules)
- [`../skill.yaml`](../skill.yaml) — marketplace manifest (name / version / transport / tools[])
- [`../usage/instructions.md`](../usage/instructions.md) — paste-ready system-prompt block

---

*Last verified: 2026-06-17.*
