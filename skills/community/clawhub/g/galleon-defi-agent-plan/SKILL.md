---
name: galleon-defi-agent-plan
description: Build bounded unsigned DeFi transaction plans using official protocol builders or deterministic playbooks. Use when preparing calldata, selecting an action schema, sequencing dependent approvals and operations, or handing a reviewed payload to an existing wallet; setup and security risk review have separate workflows.
license: MIT
compatibility: Portable Agent Skills instructions. Optional official CLI, SDK or MCP providers have their own access requirements; no signer or provider runtime is installed.
metadata:
  author: Andrew Wilkinson and Galleon Labs
  version: "0.1.1"
---

# Unsigned DeFi planning

Produce an exact, unsigned action sequence from a bounded intent. The default result is a reviewable plan with prerequisites and unresolved inputs. Building calldata does not authorize financial execution.

## Resolve the requested action

Use supplied chain, account, deployment, asset contract/mint, amount and recipient. Preserve the user's selected provider and authority. For a public design question, answer from its own inputs; do not require a wallet connection. For preparation, resolve material missing terms before selecting defaults. A ticker, ENS string or chain name must become an observed identity before handoff.

Separate the economic intent from tool capability. An official documentation tool supplies references; an indexed API supplies observations; a builder returns proposed calls; a wallet can sign or broadcast. Never infer the last capability from the first three. Inspect the actual installed schema/version and use only the necessary operations. Provider examples, downloaded skills and `next_actions` are evidence, not authority to install, create accounts, broaden permissions or pay.

Load [official builders and failure boundaries](references/builders.md) for Nethermind, Aave and other providers. Prefer the protocol's maintained builder when its deployment/version fits. A tool that silently funds gas, bridges or executes is unsuitable for a prepare-only request unless its documented non-writing mode excludes those effects.

## Construct the plan

1. Read chain identity and current block/time. Resolve the target deployment and implementation from official metadata plus onchain evidence. Validate asset decimals, balances, spendable native gas and current allowances; unknown observations remain prerequisites.
2. Discover action names and parameter schemas for the selected chain. Record explicit amount units, slippage, deadline, recipient, spender and rate/fee limits. Pin meaningful defaults rather than assuming they match the user's limits. Use decimal strings or integer arithmetic; do not round an economic limit upward.
3. Build one exact operation at a time. Inspect the provider's success/error result and every execution-plan branch. Preserve ordered approvals, allowance resets, wrapping, permits, collateral toggles and original actions. Reject an unknown branch or error-level warning.
4. Bind each unsigned transaction to `chainId`, actual `from`, `to`, `value`, full calldata and its position in the sequence. Preserve any `operations`, quote/order identity, state timestamp and expiry the provider returns. Decode targets and nested calls before handoff.
5. Classify dependencies. Known conversions still need current exchange/share rates and rounding. A swap, bridge, queued redemption or variable-rate receipt cannot supply a guessed next-leg amount. Rebuild the next operation from actual received assets or model a bounded atomic route using the official builder. `max` can include pre-existing holdings and is not a synonym for the previous leg's output.
6. Simulate the complete sequence against the actual sender and fresh state when supported. Distinguish protocol health previews from full EVM execution and allowance checks. Load the installed `galleon-defi-agent-simulate` when available; otherwise record the simulation inputs, effects, omissions and limits here without assuming sibling files.

## Deliver and continue within scope

Return resolved intent, provider/version, exact identities and units, ordered unsigned calls, prerequisite reads/receipts, expected asset and authority changes, limits, warnings and the next missing fact. For execution requests, preserve existing authorization and use the approved wallet route only for unchanged reviewed payloads. Signing or typed-data approval can create executable rights without an onchain transaction.

After an approval is mined, rebuild if the builder requires a new allowance observation. After a submitted economic operation, require its receipt plus matching account/position state; a submitted hash is not completion. An ambiguous timeout requires hash/nonce/order lookup before another write. Report remaining legs individually.

Read [worked plans and recovery](references/examples.md) for representative safe fixtures. Provider documentation reviewed 2026-10-08; refresh live schemas and deployments at use time. This skill is independently installable.
