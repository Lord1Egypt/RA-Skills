# Sui Move Example — SimpleCounter

A minimal Sui Move package for demonstrating the audit & deploy workflow.

## Structure

```
sui_move/
├── Move.toml             # Package manifest
├── sources/
│   └── counter.move      # The module
└── README.md
```

## What This Contract Does

- Creates a shared `Counter` object (initialized to 0)
- Anyone can call `increment` to increase the counter by 1
- Only the admin (deployer, who holds `AdminCap`) can `reset` it
- Emits `CounterChanged` events on state changes

## Key Patterns Demonstrated

- **Capability-based access control** (`AdminCap`)
- **Shared objects** (`Counter`)
- **Event emission** (`CounterChanged`)
- **Init function** for one-time setup

## Quick Start

```bash
# Install Sui CLI (if not installed)
cargo install --locked --git https://github.com/MystenLabs/sui.git sui

# Build
sui move build

# Test
sui move test

# Audit with chain-audit-deploy
# (run from this directory)
```

## Audit This Contract

```bash
python3 ../../scripts/audit_sui_move.py --path .
```

## Deploy This Contract

```bash
python3 ../../scripts/deploy_helper.py \
  --chain sui_move \
  --path . \
  --network testnet \
  --gas-budget 100000000 \
  --dry-run
```
