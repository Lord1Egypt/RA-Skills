# PROJECT: SOLANA-RELEASE (v1.18.26)
## Part of Operation IRONCLAD / Landslide

> **IMPORTANT:** This directory contains the Solana SDK and core CLI toolset. It is the primary engineering environment for simulating the Solana cluster and developing high-leverage trading/bot components as part of Ryan Molinich's survival strategy.

---

## 1. MISSION CONTEXT & STRATEGY
This environment is used to support the **High-Leverage Scalping (SOL/USDT)** and **"God-Bot"** initiatives described in the global `../GEMINI.md`.

- **Cluster Simulation:** Use the `solana-test-validator` in `bin/` to mock the Solana mainnet for backtesting liquidation hunting and mean reversion strategies without risking capital.
- **Custom Development:** The `src/` directory and root `Cargo.toml` are available for building custom Rust-based Solana programs or CLI tools.
- **SBF SDK:** The full Solana Bytecode Format (SBF) SDK is available in `bin/sdk/sbf/` for program development.

---

## 2. HARDWARE & OPERATIONAL GUIDELINES (MBP 13" 2020)
Given the Intel i5 2020 MacBook Pro's thermal constraints:
- **Thermal Management:** Monitor CPU temperatures via `/temp` (Telegram C2) when running the `solana-test-validator`. The local validator can be CPU-intensive; ensure auxiliary cooling is active.
- **Process Monitoring:** Use `top` or `psutil`-based scripts to ensure the validator doesn't throttle the system during critical data execution or remote DoorDash monitoring.

---

## 3. CORE DIRECTORY MAP

| Path | Description |
| :--- | :--- |
| `bin/` | Full Solana CLI Suite (v1.18.26): `solana`, `solana-keygen`, `solana-test-validator`, `spl-token`, etc. |
| `test-ledger/` | Local ledger state for the test validator. Includes pre-configured `validator-keypair.json`. |
| `src/main.rs` | Entry point for custom Rust experiments or strategy wrappers. |
| `bin/sdk/sbf/` | Solana SBF SDK for building on-chain programs. |
| `version.yml` | Version manifest (Current: `v1.18.26`, target: `x86_64-apple-darwin`). |

---

## 4. ESSENTIAL COMMANDS

### 4.1 Running the Local Cluster
To start a local Solana validator with the existing ledger:
```bash
./bin/solana-test-validator --ledger test-ledger --rpc-port 8899
```

### 4.2 Pointing CLI to Localhost
```bash
./bin/solana config set --url localhost
```

### 4.3 Keypair Inspection
Check the default validator keypair:
```bash
./bin/solana-keygen pubkey test-ledger/validator-keypair.json
```

### 4.4 Managing SPL Tokens
```bash
./bin/spl-token --version
```

---

## 5. SECURITY & SURVIVAL PROTOCOLS
- **DO NOT** use this environment to interact with the compromised NAS (`192.168.1.140` / "segatesuck").
- **DO NOT** add funds to the bricked wallet `5sQr...Zwyz` (Nonce authority hijack).
- **DEVELOPMENT ONLY:** Keep all testing on `localhost` or `devnet` until strategies are fully validated against the Aggr.trade and CoinGlass heatmaps.

---
**EOF - Solana Release Environment Manifest**
