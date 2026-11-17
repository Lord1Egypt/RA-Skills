---
name: aipou-farming
description: Record meaningful AI-assisted work as privacy-preserving AIPOU receipts and claim accumulated AIPOU rewards on Base. Use when a user asks to farm AIPOU, register an AI task, show their AIPOU identity, inspect pending receipts, estimate rewards, or claim AIPOU through the configured MCP server.
version: 1.0.1
---

# AIPOU Farming

Use the `aipou` MCP tools to turn completed AI work into signed receipts. Keep private keys, raw prompts, model outputs, and private file contents out of tool arguments and responses.

AIPOU is for humans working with AI agents: coding, debugging, researching, reviewing, writing, and coordinating meaningful work. It records private receipts first. Token claims are optional, validator-approved, and only run after an explicit user request.

Read [references/protocol.md](references/protocol.md) before the first operation in a session.

## Direct MCP Tool Calls

The AIPOU operations below are native tools in the current agent session. Call them directly by tool name.

- Do not translate an AIPOU tool call into a shell command, CLI command, `npx` command, HTTP request, or code snippet.
- Never invent commands such as `aipou begin`, `aipou complete`, or `aipou claim`.
- Use only tool results returned by the MCP server. Never fabricate a nonce, receipt ID, reward, signature, or settlement result.
- If an expected AIPOU tool is not present in the current tool list, stop and report that the MCP integration is unavailable in that session.

## Record Work

1. Call `get_aipou_identity` and confirm that a dedicated farming wallet is configured.
2. Before meaningful work, hash a short non-sensitive task description with Keccak-256.
3. Call `begin_ai_task` with the real provider, model, task hash, and client name.
4. Preserve the returned nonce only for this task.
5. Complete the requested work.
6. Hash the final result or a stable non-sensitive summary with Keccak-256.
7. Call `complete_ai_task` with the nonce, honest token counts when available, elapsed seconds, and output hash.
8. Report the receipt ID, trust tier, estimated reward, and settlement status.

Never invent provider evidence. Omit it unless the provider supplied a verifiable signature from a configured key.

## Claim Rewards

After a broad explicit user request such as `claim my AIPOU`, call `settle_all_ai_rewards` so every currently eligible pending receipt in the shared AIPOU data directory is processed in bounded batches. Use `settle_ai_rewards` only when the user asks for one limited batch. Settlement submits onchain transactions; your host's own transaction confirmation policy still applies and must never be bypassed. Report any receipts the validator skipped by policy, with their reasons.

After settlement, report the claimed amount, recipient farming wallet, Merkle root, root transaction, and claim transaction. Never claim that token value or liquidity is guaranteed.

## Inspect or Estimate

- Use `export_ai_receipts` to show pending or settled receipts without exposing private content.
- Use `estimate_ai_reward` for estimates. Label estimates as non-final.
- Use `get_aipou_contract` for current chain and contract information.

## Guardrails

- Use a dedicated farming wallet, never a primary treasury wallet.
- Never ask the user to paste a private key into chat.
- Do not reward trivial prompt spam or split one task into artificial microtasks.
- Do not claim old work retroactively when no original nonce exists.
- State that current client-signed proof demonstrates wallet authorization and collector observation, not independent proof from the AI provider.
- State that AIPOU is experimental, unaudited, and has intentionally tiny market liquidity.
