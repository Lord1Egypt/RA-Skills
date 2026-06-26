# Solana Example — SimpleCounter (Anchor)

A minimal Solana Anchor program for demonstrating the audit & deploy workflow.

## Structure

```
solana/
├── Anchor.toml                         # Anchor project config
├── Cargo.toml                          # Workspace config
├── programs/
│   └── simple_counter/
│       ├── Cargo.toml                  # Program dependencies
│       └── src/
│           └── lib.rs                  # The program
└── README.md
```

## What This Program Does

- Creates a `Counter` PDA account per authority
- Anyone can call `increment` to increase the counter by 1
- Only the original authority can `reset` the counter
- Uses checked arithmetic to prevent overflow
- Emits `CounterChanged` events on state changes

## Key Patterns Demonstrated

- **PDA (Program Derived Address)** with seeds
- **Signer validation** (`authority: Signer`)
- **Account constraints** (`has_one = authority`)
- **Checked arithmetic** (`checked_add`)
- **Custom error codes** (`ErrorCode::Overflow`)
- **Events** (`#[event]`)
- **Overflow protection** (`overflow-checks = true` in Cargo.toml)

## Quick Start

```bash
# Install Anchor (if not installed)
cargo install --git https://github.com/coral-xyz/anchor avm
avm install latest && avm use latest

# Build
anchor build

# Test
anchor test

# Audit with chain-audit-deploy
# (run from this directory)
```

## Audit This Program

```bash
python3 ../../scripts/audit_solana.py --path .
```

## Deploy This Program

```bash
python3 ../../scripts/deploy_helper.py \
  --chain solana \
  --path . \
  --network devnet \
  --dry-run
```
