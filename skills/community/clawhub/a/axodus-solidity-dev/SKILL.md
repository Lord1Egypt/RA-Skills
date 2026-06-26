---
name: solidity-dev
description: Implement secure Solidity smart contracts with tests and safety patterns.
metadata:
  author: RedHat Dev
  version: 1.0.0
  owner: RedHat Dev Agent
  category: blockchain
---

# SKILL: solidity-dev

## Purpose
Design and implement secure Solidity smart contracts with explicit security controls, tests, and deterministic build/validation steps.

## When to Use
- The task requires a new contract (ERC-20/721/1155) or extending an existing one.
- You need secure patterns (access control, pausable, reentrancy protection).
- You need Hardhat/Foundry test scaffolding.

## Inputs
- `contract_spec` (required, object|string): requirements, roles, invariants, events.
- `standard` (optional, enum: `erc20|erc721|erc1155|custom`).
- `tooling` (optional, enum: `hardhat|foundry`).
- `security_constraints` (optional, string[]): e.g., â€œno upgradeabilityâ€, â€œpausable requiredâ€.
- `deployment_target` (optional, string): local/testnet/mainnet (mainnet requires explicit user approval).

## Steps
1. Clarify requirements:
   - roles and permissions
   - asset flows
   - invariants (must always hold)
2. Select proven libraries (prefer OpenZeppelin) and decide if upgradeability is required.
3. Implement contract with explicit patterns:
   - access control (`Ownable`/`AccessControl`)
   - checks-effects-interactions for external calls
   - `ReentrancyGuard` where applicable
   - `Pausable` for emergency stop if appropriate
4. Add events for critical state changes.
5. Write tests that assert invariants and failure modes.
6. Validate:
   - compile
   - run tests
   - run static checks when available (slither/foundry invariants) without blocking if tooling is absent.

## Validation
- No privileged method lacks access control.
- External calls are safe (reentrancy considered).
- Arithmetic uses Solidity 0.8+ safety; no unsafe casts without justification.
- Tests cover:
  - happy path
  - access control denial
  - edge conditions
  - reentrancy-sensitive flows (where relevant)

## Output
- Contract source files (paths)
- Test files (paths)
- Build/validate commands
- Security notes (assumptions + risk areas)

## Safety Rules
- Never embed private keys, mnemonics, or RPC secrets in code.
- Never deploy to mainnet without explicit user confirmation and a dry-run on testnet/local first.
- Avoid custom crypto unless unavoidable.
- Reject â€œguaranteed profitâ€ or manipulative tokenomics requirements.

## Example
Input:
- `standard`: `erc20`
- `contract_spec`: â€œMintable by `MINTER_ROLE`, pausable transfers, capped supply.â€

Output:
- `contracts/MyToken.sol`, `test/MyToken.t.sol` (or Hardhat equivalent)
- validation: `forge test` (or `npx hardhat test`)
