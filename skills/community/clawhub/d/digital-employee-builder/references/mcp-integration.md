# MCP Wrapping Essentials

Protocol and engineering details for wrapping business capabilities as an MCP server.

## Contents

- [Choosing a Transport](#choosing-a-transport)
- [Tool Design Conventions](#tool-design-conventions)
- [Composite Tools (Flow-Level Packaging)](#composite-tools-flow-level-packaging)
- [Contract-First Tools](#contract-first-tools)
- [Python FastMCP Quick Reference](#python-fastmcp-quick-reference)
- [Smoke Testing](#smoke-testing)

## Choosing a Transport

| Mode | Use when | Notes |
|---|---|---|
| stdio | Harness runs on the same machine (default recommendation) | Harness spawns the server as a subprocess; no port management |
| streamable HTTP | Long-running server, shared by multiple harnesses, remote deployment | Handle auth and ports yourself |

## Tool Design Conventions

1. Naming: `verb_noun` snake_case (`query_order`, `create_refund`), one-to-one with the capability inventory.
2. Description is the contract: state what it does, parameter meanings/formats, what it returns, and side effects. Prefix write tools with `[WRITE — confirm with the user before executing]`.
3. Strongly typed parameters with per-field descriptions; list valid values for enums in the description.
4. Thin wrapper: validate params → call the existing business interface (HTTP client / SDK / imported module) → return structured results. Never copy business logic — dual implementations drift. (Composite flow tools are the deliberate exception — see below.)
5. Error handling: convert business exceptions to text with error codes (e.g., `ORDER_NOT_FOUND: order xxx does not exist`); never let raw tracebacks flood the context.
6. Credentials: inject via env vars (`BUSINESS_API_BASE`, `BUSINESS_API_TOKEN`, etc.); TOOLS.md records variable names only.
7. Response size: list tools take a `limit` parameter (default 20) so a single call can't blow up the context window.

## Composite Tools (Flow-Level Packaging)

The default route for multi-step flows is a skill `scripts/` executable (routing table in SKILL.md). When the user opts for MCP-only packaging, expose the flow as ONE composite tool — never as prose steps over separately-called CRUD tools, which lets the model skip/reorder steps and drop validations.

Rules:

1. One flow = one tool (`process_refund`, `reconcile_daily_settlement`). The server code orchestrates the CRUD calls in fixed order and holds every validation, branch, and compensation the business code has — run the Porting Checklist from `script-encapsulation.md` over this code.
2. This deliberately breaks the thin-wrapper convention for these tools: the server becomes a business-logic carrier. Provenance comments (`# Ported from ...`) and mapping registration in `docs/business-capabilities.md` are mandatory, same as script ports. Flow changes require editing and redeploying the server — make sure the user accepts this trade-off up front.
3. Dangerous flows take a `dry_run` parameter (default `true`): validate and report what would happen, with no side effects.
4. Do not expose the write-CRUD building blocks as standalone tools — read CRUD open, writes only via composite tools; otherwise the model can bypass the flow. Keep composite code in its own module (e.g. `flows/`), not inline in the tool registry.

```python
@mcp.tool()
def process_refund(order_id: str, amount: float, dry_run: bool = True) -> str:
    """[WRITE — confirm with the user before executing] Full refund flow:
    validate state and amount → create refund record → mark order refunding.
    dry_run: validate only, no side effects."""
    order = client.get_order(order_id)
    if order["status"] != "paid":            # validation lives in server code, not the model's memory
        return f"INVALID_STATE: order status is {order['status']}; only paid orders are refundable"
    if amount > order["amount"]:
        return "AMOUNT_EXCEEDED: refund exceeds order amount"
    if dry_run:
        return json.dumps({"ok": True, "dry_run": True, "would_refund": amount})
    if client.find_refund(order_id):          # idempotency: no duplicate side effects on re-run
        return "DUPLICATE: refund already exists for this order"
    refund = client.create_refund(order_id, amount)
    client.update_order_state(order_id, "refunding")   # on failure: compensate or report exactly how far it got
    return json.dumps({"ok": True, "refund_id": refund["id"]})
```

## Contract-First Tools

When a capability depends on a business-side interface that exists only as an approved proposal in `docs/business-api-proposals.md` (the builder never modifies business code):

1. Implement the tool — thin or composite — strictly against the approved contract: parameter names, response fields, and error codes verbatim. The proposal doc is the single source of truth.
2. Put the client behind a stub backend switched by env var (e.g. `BUSINESS_API_STUB=true`), serving canned responses derived from the contract's response schema, so the server starts and passes tools/list + tools/call smoke tests before the business side deploys.
3. Never ship a stub silently: record stubbed tools in TOOLS.md and `docs/harness-setup.md`, and mark them `contract-pending: <proposal-id>` in the plan.
4. On deployment: flip the env var, re-run the smoke test live, update the proposal status to `verified`. The tool definition must not change — if the deployed reality drifted from the contract, amend the proposal and the tool together; never patch one side silently.

## Python FastMCP Quick Reference

```bash
pip install "mcp[cli]"   # or: uv add mcp
```

Minimal server:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("<employee-name>-tools")

@mcp.tool()
def query_order(order_id: str) -> str:
    """Query order details (read-only). order_id: order number, e.g. SO20260101001."""
    ...

if __name__ == "__main__":
    mcp.run()  # stdio
```

## Smoke Testing

Quick stdio verification (send initialize + tools/list):

```bash
python3 - <<'EOF'
import json, subprocess
p = subprocess.Popen(["python3", "server.py"], stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE, text=True)
def send(msg):
    p.stdin.write(json.dumps(msg) + "\n"); p.stdin.flush()
send({"jsonrpc":"2.0","id":1,"method":"initialize","params":{
  "protocolVersion":"2024-11-05","capabilities":{},
  "clientInfo":{"name":"smoke","version":"0"}}})
send({"jsonrpc":"2.0","method":"notifications/initialized"})
send({"jsonrpc":"2.0","id":2,"method":"tools/list"})
for _ in range(2):
    print(p.stdout.readline())
p.kill()
EOF
```

Confirm the tool count in tools/list matches the capability inventory. For HTTP mode, curl the health endpoint, then connect with any MCP inspector to verify.
