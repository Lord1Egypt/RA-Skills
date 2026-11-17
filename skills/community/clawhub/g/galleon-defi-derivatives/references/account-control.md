# Shared account and automation control

Before changing a position, identify the exact venue, account/subaccount, signer and existing writers: trading bots, scheduled strategies, TWAPs, keeper-managed orders and human sessions. Read the relevant controller status and current orders through supported surfaces. A process not visible to this agent is unknown, not inactive. API-wallet separation can prevent nonce collisions but does not isolate exposure when processes trade the same account.

A controller can reopen a manually closed position or replace a cancelled order. If the requested action conflicts with an active controller, explain the conflict and use the user's established handoff policy. Without one, resolve who controls the affected exposure before writing. Do not silently disable the bot, switch wallets or move collateral. Pausing a controller and transferring control are separate actions whose scope must be authorized; preserve authorization already given for the unchanged handoff.

For an authorized handoff, record controller identity/status, affected markets, outstanding requests and order IDs. Verify the pause took effect, reconcile in-flight fills and resting orders, then refresh available margin, protection and the proposed action. A stopped process can leave live orders; a flat position can coexist with an entry order that will reopen it. Cancel only the intended remaining orders, accounting for fills racing cancellation. Closing exposure and cancelling orders are distinct outcomes. After the action, report residual exposure/orders and who owns protection. Do not resume automation unless that resumption is within the user's request.

## Offline acceptance cases

| Fixture | Required decision |
| --- | --- |
| User requests a manual close; a strategy is still managing that market. | Identify the conflict and handoff policy before writing; do not silently stop the strategy or use another wallet. |
| Bot process is stopped; a maker order remains live. | Treat the account as having outstanding exposure, reconcile the order and require scope for cancellation. |
| Cancel races a half fill during handoff. | Recompute remaining position/order size and protection from fresh state; do not reuse original size. |
| Two API wallets sign for one subaccount. | Separate signing/nonce ownership from shared position risk; do not describe them as independent portfolios. |

Research input: Minara's [perps automation workflow](https://github.com/Minara-AI/minara-skills/blob/b93aba1029827c37cf5ad82b19bfa8c289912091/skills/minara/references/perps-autopilot.md), reviewed 2026-09-05. Its wallet-level manual-order restriction is specific to Minara; this procedure does not assert that other venues enforce it. Hyperliquid's [official nonce guidance](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/nonces-and-api-wallets) recommends distinct API wallets per trading process. Key registration remains outside this procedure. No Minara runtime is required.
