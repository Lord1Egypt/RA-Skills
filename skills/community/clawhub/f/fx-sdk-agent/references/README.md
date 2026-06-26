# FX SDK Agent — References

This folder holds canonical reference material for the **fx-sdk-agent** skill. Use them when generating or validating SDK integration code.

## Files

| File | Purpose |
|------|---------|
| **sdk-playbook.md** | Request shapes (templates) for every SDK method, minimal code snippets (read-only, tx planning, sequential execution), and a validation checklist. Use when you need the exact parameter shape for `getPositions`, `increasePosition`, `reducePosition`, `adjustPositionLeverage`, `depositAndMint`, `repayAndWithdraw`, bridge, or fxSAVE (config, balance, redeem status, claimable, getRedeemTx, deposit, withdraw). |
| **agent-adapter-example.ts** | Typed adapter pattern: `FxAction` union (all action kinds including fxSAVE), `runFxAction(action, options)` with `planOnly`, and sample payloads. Use when building an agent that dispatches to SDK methods from a single entry point or from tool schemas (e.g. `agent-tools.json`). |

## When to read which

- **Request shapes / “what parameters does X take?”** → `sdk-playbook.md`
- **Example commands for tests/examples** → `sdk-playbook.md` (Validation Checklist)
- **Adapter pattern / single entry for many actions** → `agent-adapter-example.ts`
- **Canonical operation list and errors** → repo root `AGENTS.md`
- **Concrete runnable examples** → repo root `example/*.ts` (see SKILL.md Project-Specific References)

## Amounts and tool schema

- All amounts in SDK are **bigint** in wei. If the agent receives decimal strings (e.g. from `agent-tools.json`), convert with `BigInt(amountWei)` before calling the SDK.
