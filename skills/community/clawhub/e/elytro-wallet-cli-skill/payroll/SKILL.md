---
name: payroll
description: Run recurring payroll cycles from an Elytro smart account. Supports ETH or a single ERC-20 token per pay period, manual approval, sponsorship-aware simulations, and logging best practices.
user-invocable: true
---

# Elytro Payroll Skill

Plan, simulate, and execute crypto payroll batches with the Elytro CLI. This first iteration focuses on **one token per cycle** (ETH or a designated ERC-20 such as USDC) and **multiple recipients/amounts** collected ahead of time. All payouts are explicitly approved by a human operator; cron jobs may remind you, but they may not press the final button.

## Scope & Assumptions
- Smart account already deployed and funded on the chain where payroll runs.
- All recipients are vetted wallets; no address discovery inside this skill.
- Roster amounts are denominated directly in the payout token (no FX conversion).
- Each cycle shares the same token, memo, and schedule label (e.g., `2024-08-09-biweekly`).
- SecurityHook/OTP is enabled when required; expect confirmations per send.

## Prerequisites
1. Install/load the base `elytro` wallet skill plus this `payroll` skill.
2. Maintain a canonical roster CSV that agents can edit. Minimum columns: `name`, `wallet`, `amount`, `token`, `period`, `notes`. Store it under a secure workspace path (e.g., `ops/payroll/roster.csv`) with restricted permissions.
3. For ERC-20 payouts, record the token contract address (e.g., USDC on Base: `0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA`).
4. Treasury wallet funded with `sum(amounts) + gas` unless sponsorship covers fees.
5. Shared log (sheet/docs) to append the results: datetime, operator, tx hash, explorer URL, recipients/amounts.

### Roster CSV Template
Agents should create this file during onboarding by asking the finance team for each recipient’s details. Example rows:

```csv
name,wallet,amount,token,period,notes
Alice,0xa11Ce0f1234567890abcdef1234567890abcd01,0.42,ETH,2024-08-09-biweekly,Core dev
Bob,0xb0b0001234567890abcdef1234567890abcd02,0.37,ETH,2024-08-09-biweekly,Ops
Carol,0xcaR01234567890abcdef1234567890abcd03,2500,USDC,2024-08-15-monthly,Design
```

- `amount` is in the payout token’s human units (ETH or token decimals).  
- `period` labels the pay run (used in summaries/logs).  
- `notes` capture role or special instructions (optional).

**Initial Setup Flow for Agents**
1. Ask the user for each teammate’s wallet, payout amount, token choice (ETH or a specific ERC-20), and pay period.  
2. Populate/append the CSV with those values.  
3. Confirm the file path and share it with all payroll agents so future cycles reuse the same source.  
4. During each run, filter the CSV for the target `period` and token to build the command flags described below.

## Scheduling Model (Manual Cron)
- Define cadence (biweekly, monthly, etc.) and store it in the roster metadata.
- When creating reminders in Clawhub/cron tooling, set `wakeMode: now` (never `next-heartbeat`). Otherwise the reminder only fires when the user is already active and payroll alerts will be missed.
- Include timezone references explicitly (e.g., `2026-03-23 16:11 GMT+8`) so every operator knows when to expect the ping.
- Use cron/alerts/Slack just to ping the operator (“Payroll due Fri 15:00 UTC”). Provide a “Run Now” checklist for missed reminders so the agent can start immediately when catching up.
- Operator reviews roster deltas, prepares commands, and manually approves the batch; **automation may never call `elytro tx send` without human confirmation**.

## Workflow Checklist
1. **Load roster**
   - Export relevant rows for the upcoming period.
   - Ensure one token per export (split ETH vs USDC into separate runs).
2. **Validate addresses**
   - Run `elytro account lookup <wallet>` or `elytro query balance <wallet>` (read-only) to confirm format.
3. **Draft CLI command**
   - ETH example:
     ```bash
     elytro tx simulate payroll --tx "to:0xRecipientA,value:0.42" \
       --tx "to:0xRecipientB,value:0.37"
     ```
   - USDC example (ERC-20 `transfer(address,uint256)` calldata):
     ```bash
     # Encode per recipient, replacing <amountWei>
     DATA_A=$(cast calldata "transfer(address,uint256)" 0xRecipientA 420000000)
     DATA_B=$(cast calldata "transfer(address,uint256)" 0xRecipientB 370000000)
     elytro tx simulate payroll \
       --tx "to:0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA,data:$DATA_A" \
       --tx "to:0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA,data:$DATA_B"
     ```
   - Always keep the order consistent with your roster export for auditability.
4. **Simulate & surface summary**
   - Capture output: gas, sponsorship, per-recipient preview.
   - Present to stakeholders via Inline Buttons: `tx_simulate` (rerun), `tx_approve`, `tx_reject`.
5. **Manual approval**
   - Upon `tx_approve`, rerun the same command with `tx send` instead of `simulate`.
   - Handle SecurityHook OTP if prompted; document who provided approval.
6. **Record results**
   - Save `transactionHash`, `blockNumber`, timestamp, roster period, total token amount.
   - Mark roster entries as paid to prevent duplicates.

## Inline Button UX (Agent Guidance)
When showing payroll summaries, include:
- Header: `Payroll – <token> – <period>`
- Totals: number of recipients, sum of amounts, estimated gas cost.
- Per-recipient bullet list (name, address abbr., amount).
- Buttons: `[✅ Approve (tx_approve), ❌ Cancel (tx_reject)]` plus `[🔍 Re-Simulate (tx_simulate)]`.
- After execution, send confirmation message with tx hash + explorer link and button `[📄 Log Recorded (confirm_yes)]` once you update the ledger.

## Logging Template
| Timestamp (UTC) | Operator | Period | Token | Total Amount | Tx Hash | Explorer | Notes |
| --------------- | -------- | ------ | ----- | ------------ | ------- | -------- | ----- |

Populate immediately after success. If a batch partially fails, note which recipient needs remediation and remove their `--tx` entry before re-running.

## Safety Notes
- **Never** mix ETH & ERC-20 transfers in the same payroll run; create separate batches.
- Re-run `elytro tx simulate` after any edit to the roster or tx list.
- If sponsorship fails and wallet lacks gas, pause and fund before retrying.
- Keep roster files out of public repos; they contain salary information.

## Future Enhancements
- Multiple tokens per cycle w/ automatic grouping.
- CSV parser helper (generate `--tx` flags automatically).
- Integration with Skills planner to fetch roster data via API.
- Automated reminders that attach the prebuilt command for operator review.
