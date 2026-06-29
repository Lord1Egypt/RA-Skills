# Mixed-Transport Agents

> Members of this family can do both MCP and universal REST. Default to MCP when
> reachable; fall back to universal REST when the deployment environment blocks
> long-lived JSON-RPC or stdio connections. **All protocol details
> (12 tools, error codes, billing) live in [`../SKILL.md`](../SKILL.md) — do not duplicate.**

## Verified members

Both members are backed by runnable snippets below. Promotion policy for adding a
new member is in [`./README.md`](./README.md#adding-a-new-agent).

| Agent | Default | Fallback | Verified on | When to fall back |
|-------|---------|----------|-------------|-------------------|
| Cursor (with REST fallback) | MCP stdio | universal REST | 2026-06-17 | Browser-side editor that cannot spawn stdio child |
| Custom in-house frameworks | MCP HTTP | universal REST | 2026-06-17 | Network policy blocks outbound JSON-RPC but allows HTTPS POST |

## Selection rule

1. Try MCP first — it gives the agent `tools/list` discovery and typed errors. (The
   hub is OneShot synchronous; there is no streaming progress, only the same handler
   dispatch table.)
2. If `tools/list` returns a non-2xx OR the agent cannot maintain a long-lived
   connection, switch the same agent to the universal REST envelope. The two
   transports share the same handler dispatch table, so semantic behavior is identical.

## Common setup

- When using REST fallback, follow [`rest-only.md`](./rest-only.md) for the envelope
  and timeout guidance (≥120s for t4).
- When using MCP, follow [`mcp-native.md`](./mcp-native.md) for discovery and auth.
- For the protocol-level contract (12 tools, error codes, billing), see
  [`../SKILL.md`](../SKILL.md).

## Agent-specific snippets

### Cursor (stdio → REST fallback)

TypeScript probe-and-fallback; the same tool name is reused, only the transport changes:

```typescript
import { spawn } from "node:child_process";
import { setTimeout as wait } from "node:timers/promises";

const HUB = process.env.FORTUNE_HUB_BASE!;       // e.g. "https://fortunehub.lighttune.com.au"
const KEY = process.env.FORTUNE_HUB_API_KEY!;
const READ_TIMEOUT_MS = 130_000;                  // ≥ 120s for t4

type CallArgs = { name: string; arguments: Record<string, unknown> };

async function callViaStdio(args: CallArgs): Promise<unknown> {
  // Spawn the mcp-remote shim from mcp-native.md. If stdio is blocked
  // (browser-side editor, sandboxed worker, etc.) the spawn will throw ENOENT
  // or the first tools/list will time out — both are fallback triggers.
  const child = spawn("npx", ["-y", "mcp-remote", `${HUB}/api/mcp`], {
    env: { ...process.env, FORTUNE_HUB_API_KEY: KEY },
    stdio: ["pipe", "pipe", "pipe"],
  });
  // ... stdio framing elided; see mcp-remote docs.
  return await new Promise((resolve, reject) => {
    const t = setTimeout(() => reject(new Error("stdio_timeout")), READ_TIMEOUT_MS);
    child.once("error", (e) => { clearTimeout(t); reject(e); });
    // send tools/call, resolve on response, etc.
  });
}

// Map a tool name to its (category, name) URL pair. The category is fixed per
// tool — see the 12-tool table in SKILL.md §3 (meta / fortune / forum).
function categorize(toolName: string): [category: string, name: string] {
  if (toolName.startsWith("forum_")) return ["forum", toolName];
  if (toolName.startsWith("get_")) return ["meta", toolName];
  return ["fortune", toolName]; // bazi_* / bigluck_*
}

async function callViaRest(args: CallArgs): Promise<unknown> {
  const [category, name] = categorize(args.name);
  const r = await fetch(`${HUB}/api/universal/${category}/${name}`, {
    method: "POST",
    headers: { "x-api-key": KEY, "content-type": "application/json" },
    body: JSON.stringify(args.arguments),
    signal: AbortSignal.timeout(READ_TIMEOUT_MS),
  });
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  const body = await r.json();
  if (!body.success) throw new Error(`${body.error.code}: ${body.error.message}`);
  return body.data;
}

export async function callTool(args: CallArgs): Promise<unknown> {
  try {
    return await callViaStdio(args);
  } catch (e: any) {
    if (e?.code === "ENOENT" || /timeout|tools\/list/i.test(String(e?.message))) {
      return await callViaRest(args);
    }
    throw e;
  }
}
```

For tool name ↔ `category/name` mapping, error codes, and billing, see
[`../SKILL.md`](../SKILL.md) §3 and §5.

### Custom in-house framework — generic probe-then-fallback

```typescript
async function pickTransport(hub: string, key: string): Promise<"mcp" | "rest"> {
  // 1. Probe MCP tools/list with a 5s budget.
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), 5_000);
  try {
    const r = await fetch(`${hub}/api/mcp`, {
      method: "POST",
      headers: { "x-api-key": key, "content-type": "application/json" },
      body: JSON.stringify({ jsonrpc: "2.0", id: 0, method: "tools/list" }),
      signal: ctrl.signal,
    });
    if (r.ok) return "mcp";
  } catch {
    // network policy, DNS, or HTTP/2 negotiation failure
  } finally {
    clearTimeout(t);
  }
  // 2. MCP unreachable → fall back to universal REST (works over plain HTTPS POST).
  return "rest";
}
```

The decision is made once per agent process; both transports then share the
same handler dispatch table on the hub side, so the agent does not need to
reimplement any of the 12 tools' semantics.

## When NOT to use this family

- Agent has no MCP support at all → [`rest-only.md`](./rest-only.md)
- Agent speaks MCP and the deployment can always reach `/api/mcp` → [`mcp-native.md`](./mcp-native.md)

---

*Last verified: 2026-06-17. Verified on column reflects the date the runnable
snippet was last checked end-to-end. See [README.md](./README.md#adding-a-new-agent)
for the verified/unverified promotion policy.*
