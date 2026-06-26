# Solidity Example — SimpleStorage

A minimal Solidity contract for demonstrating the audit & deploy workflow.

## Structure

```
solidity/
├── foundry.toml          # Foundry project config
├── src/
│   └── SimpleStorage.sol # The contract
└── README.md
```

## What This Contract Does

- Stores a single `uint256` value
- Only the owner can update the value
- Supports ownership transfer
- Emits events on state changes

## Quick Start

```bash
# Install Foundry (if not installed)
curl -L https://foundry.paradigm.xyz | bash && foundryup

# Build
forge build

# Test
forge test

# Audit with chain-audit-deploy
# (run from this directory)
```

## Audit This Contract

```bash
python3 ../../scripts/audit_solidity.py --path .
```

## Deploy This Contract

```bash
python3 ../../scripts/deploy_helper.py \
  --chain solidity \
  --path . \
  --network sepolia \
  --contract src/SimpleStorage.sol:SimpleStorage \
  --args "42" \
  --dry-run
```
