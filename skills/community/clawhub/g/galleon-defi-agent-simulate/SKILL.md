---
name: galleon-defi-agent-simulate
description: Use when simulating exact unsigned EVM transaction sequences, reproducing failed transactions, or validating fork experiments with recorded state and effects. Covers stateful preflight, replay regression and simulation discrepancies; a security review or successful broadcast is a separate result.
license: MIT
compatibility: Portable instructions for official Tenderly, Alchemy, Portals Foresight or existing EVM tools. Optional offline record diagnostic uses Bun; no provider client or signer is bundled.
metadata:
  author: Andrew Wilkinson and Galleon Labs
  version: "0.1.1"
---

# DeFi transaction simulation

Bind observed simulation effects to the exact proposed payload and state. Produce a reproducible evidence record and the missing prerequisite. Simulation success does not establish authorization, contract safety or future settlement.

## Select the actual task

- Execution preflight uses current chain state and the real sender, allowance, balances and account execution context.
- Fork experiments use explicitly recorded artificial state and answer a counterfactual question.
- Historical replay reproduces a transaction against its original state before applying changed inputs for a regression.

Load [official simulation interfaces](references/providers.md) for provider selection and [evidence contract and examples](references/records.md) before recording results. Reuse existing tools and entitlements. An authenticated provider may persist private calldata or consume credits; installing its skill or seeing an HTTP 402 does not authorize a purchase, new project or virtual network.

## Bind inputs before calling

Resolve exact chain ID, block number/hash and timestamp, provider/project/network, sender, recipient/target, native value, calldata, transaction type and nonce when applicable. Smart-account execution includes owner/module policy, entry point, paymaster and full batched calls; an EOA call to one inner target is a different context. Resolve current implementation, asset decimals and relevant balances/allowances.

Simulate ordered prerequisites plus the action as a stateful sequence. Independent success of approval and swap from the same initial state is not success of approval then swap. Preserve transaction ordering and value for every call. If approvals already exist, use that actual state rather than fake unlimited approval.

Pin simulation and read state. A historical block, wrong active virtual network, different sender or stale allowance invalidates an execution preflight. Record every artificial balance, approval, storage value, bypassed balance check, time change and block override. A counterfactual result may inform diagnosis but cannot clear the real prerequisite it removed.

## Read the complete result

Inspect per-call success/revert and human-readable error, gas estimate, full call tree, token/native balance changes, transfers/logs, allowance changes and account/session authority effects. Transaction success with a wrong recipient or excessive permission still fails intent review. Empty effect output, omitted approvals, unsupported token decoding and truncated traces are unknown coverage.

Compare predicted changes against exact maximum input, minimum output, recipient, fee and permission limits. Name unexpected assets, wrapping, token taxes and proxy upgrades. Protocol health previews and aggregate risk labels do not replace EVM execution evidence. Run real prerequisite reads when a simulation failure identifies them; do not automatically fund, approve, broaden a module or disable checks to make it pass.

A source-chain bridge simulation cannot prove the future destination call. Separate source preflight, asynchronous delivery, refund and destination execution. Offchain orders need signature/permit review and their later fill lifecycle even when no transaction is available to simulate.

## Deliver and preserve evidence

Return the task mode, exact payload/sequence, observed block/hash/time, provider/tool version, real versus overridden state, per-call outcomes, expected/observed asset and authority changes, coverage gaps and reproducible next step. Classify it as ready for intent review, incomplete, reverted/mismatched, or an experiment only. Never label it “safe” or “executed.”

For a prepared execution, preserve reviewed payload identity and refresh when chain state, sender, nonce, calldata, limits or quote expire. After an independently authorized submission, compare receipt and actual account state with this prediction. Replay establishes diagnosis; it does not retry the original write.

The optional offline `scripts/record.ts` checks a supplied record for payload binding, sequence and coverage; run its `--help` and synthetic `scripts/example.json`. It reads no keys or network state and cannot authenticate the supplied observations. Documentation reviewed 2026-10-08. This directory works independently.
