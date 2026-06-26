# SKILL: trading-integration

## Purpose
Integrate trading infrastructure safely (hummingbot and/or MCP Axodus Trading) with paper-first execution, full logging/auditability, and strict risk gating.

## When to Use
- Adding or updating connectors for hummingbot.
- Wiring execution to MCP Axodus Trading interfaces.
- Building market data ingestion, order routing, or strategy execution surfaces.

## Inputs
- `targets` (required, string[]): e.g., `["hummingbot", "mcp-axodus-trading"]`
- `mode` (optional, enum: `paper|live`, default: `paper`)
- `markets` (optional, string[]): symbols/venues to support.
- `risk_limits` (optional, object): max risk per trade, max drawdown, exposure caps, kill-switch.
- `logging_requirements` (optional, string[]): required audit events.

## Steps
1. Confirm non-negotiables:
   - no profit guarantees
   - paper mode default
   - full logs for signal/decision/execution/result
2. Map integration points:
   - market data feeds
   - execution endpoints
   - capital allocation interface
3. Implement configuration surfaces:
   - env/config references (no secrets in repo)
   - explicit mode flag for `live`
4. Implement deterministic execution flow:
   - preflight checks (risk limits, connectivity)
   - order submission
   - order state tracking
   - post-trade recording
5. Implement failure handling:
   - bounded retries
   - fallback to safe stop
   - kill-switch triggers on abnormal loss
6. Validate in paper mode:
   - dry-run order lifecycle
   - audit logs produced
   - risk gating blocks unsafe actions

## Validation
- Live mode cannot run without an explicit flag and passing preflight checks.
- All actions emit audit logs (no silent decisions).
- Risk limits are enforced before order placement.
- Secrets are not printed or committed.

## Output
- Integration summary (what’s wired)
- Config contract (required env vars, mode flags)
- Validation commands/runbook (paper test loop)

## Safety Rules
- Never enable live trading by default.
- Never request or store exchange API keys in plaintext.
- Never frame outcomes as guaranteed profit; treat as experimental systems with controlled risk.

## Example
Paper-first integration:
- `targets`: `["hummingbot"]`
- `mode`: `paper`
- Output: runbook describing simulated order placement and expected audit log entries.

