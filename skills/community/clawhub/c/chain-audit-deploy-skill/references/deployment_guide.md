# Multi-Chain Deployment Guide

Reference guide for deploying smart contracts across Solidity (EVM), Sui Move, and Solana chains.

---

## Solidity (EVM) Deployment

### Supported Networks

| Network | Chain ID | Explorer |
|---|---|---|
| Ethereum Mainnet | 1 | etherscan.io |
| Sepolia (testnet) | 11155111 | sepolia.etherscan.io |
| Holesky (testnet) | 17000 | holesky.etherscan.io |
| BSC | 56 | bscscan.com |
| BSC Testnet | 97 | testnet.bscscan.com |
| Base | 8453 | basescan.org |
| Base Sepolia (testnet) | 84532 | sepolia.basescan.org |
| Monad | 143 | monadscan.com |
| Monad Testnet | 10143 | testnet.monadscan.com |
| 0G Mainnet | 16661 | chainscan.0g.ai |
| 0G Galileo Testnet | 16602 | chainscan-galileo.0g.ai |

### Testnet Faucets (领水指引)

在测试网部署前，需要先获取测试代币。以下是各链测试网水龙头：

| Network | Faucet URL | 备注 |
|---|---|---|
| Ethereum Sepolia | https://cloud.google.com/application/web3/faucet/ethereum/sepolia | Google Cloud Web3 Faucet，免费领取 |
| Ethereum Sepolia | https://www.alchemy.com/faucets/ethereum-sepolia | Alchemy Faucet，需注册账号 |
| Ethereum Holesky | https://cloud.google.com/application/web3/faucet/ethereum/holesky | Google Cloud Web3 Faucet |
| Ethereum Holesky | https://www.holeskyfaucet.io/ | Automata Holesky Faucet |
| BSC Testnet | https://www.bnbchain.org/en/testnet-faucet | BNB Chain 官方水龙头 |
| BSC Testnet | https://faucet.quicknode.com/binance-smart-chain/bnb-testnet | QuickNode BSC Faucet |
| Base Sepolia | https://www.alchemy.com/faucets/base-sepolia | Alchemy Faucet |
| Base Sepolia | https://faucet.circle.com/ | Circle Faucet，支持多链 |
| Monad Testnet | https://faucet.monad.xyz | Monad 官方水龙头 |
| 0G Galileo Testnet | https://faucet.0g.ai | 0G 官方水龙头 |
| 0G Galileo Testnet | https://cloud.google.com/application/web3/faucet/0g/galileo | Google Cloud Web3 Faucet |

> **Tips**: 
> - 部分水龙头有领取频率限制（如每 24 小时一次）
> - Alchemy / QuickNode 水龙头需注册免费账号
> - 如某个水龙头不可用，可尝试备用水龙头

### Deployment with Foundry (forge)

```bash
# Build
forge build

# Deploy with forge create
forge create src/MyContract.sol:MyContract \
  --rpc-url <RPC_URL> \
  --private-key $PRIVATE_KEY \
  --constructor-args <arg1> <arg2>

# Deploy with forge script (recommended for complex deployments)
forge script script/Deploy.s.sol:DeployScript \
  --rpc-url <RPC_URL> \
  --broadcast \
  --verify

# Verify on Etherscan
forge verify-contract <ADDRESS> src/MyContract.sol:MyContract \
  --chain-id <CHAIN_ID> \
  --etherscan-api-key $ETHERSCAN_API_KEY
```

### Gas Estimation
```bash
# Estimate deployment gas
forge create src/MyContract.sol:MyContract --estimate-gas --rpc-url <RPC_URL>

# Check current gas prices
cast gas-price --rpc-url <RPC_URL>
```

### Post-Deploy Verification
1. Verify contract source on block explorer
2. Check constructor arguments are correctly encoded
3. Verify proxy implementation (if upgradeable)
4. Test basic read/write operations
5. Confirm ownership and access control setup

---

## Sui Move Deployment

### Supported Networks

| Network | RPC Endpoint | Explorer |
|---|---|---|
| Mainnet | `https://fullnode.mainnet.sui.io:443` | suiexplorer.com |
| Testnet | `https://fullnode.testnet.sui.io:443` | suiexplorer.com/?network=testnet |
| Devnet | `https://fullnode.devnet.sui.io:443` | suiexplorer.com/?network=devnet |
| Localnet | `http://127.0.0.1:9000` | — |

### Deployment Commands

```bash
# Switch active environment
sui client switch --env testnet

# Check active address and balance
sui client active-address
sui client gas

# Build and test first
sui move build
sui move test

# Publish (deploy)
sui client publish --gas-budget 100000000

# Publish with JSON output for parsing
sui client publish --gas-budget 100000000 --json

# Publish and skip dependency verification (faster)
sui client publish --gas-budget 100000000 --skip-dependency-verification
```

### Gas Budget Guide
- Simple module: 50,000,000 – 100,000,000 MIST
- Complex module with dependencies: 100,000,000 – 500,000,000 MIST
- 1 SUI = 1,000,000,000 MIST

### Post-Deploy Steps
1. Record the Package ID from publish output
2. Verify module on Sui Explorer
3. Check created objects (AdminCap, shared objects, etc.)
4. Test init function effects
5. Verify upgrade capability handling

### Upgrading Packages
```bash
# Upgrade with compatible policy
sui client upgrade --gas-budget 100000000 --upgrade-capability <CAP_ID>
```

---

## Solana Deployment

### Supported Networks

| Network | RPC Endpoint | Explorer |
|---|---|---|
| Mainnet Beta | `https://api.mainnet-beta.solana.com` | explorer.solana.com |
| Testnet | `https://api.testnet.solana.com` | explorer.solana.com/?cluster=testnet |
| Devnet | `https://api.devnet.solana.com` | explorer.solana.com/?cluster=devnet |
| Localnet | `http://127.0.0.1:8899` | — |

### Anchor Deployment

```bash
# Configure network in Anchor.toml
# [provider]
# cluster = "devnet"

# Build
anchor build

# Get program keypair and ID
solana address -k target/deploy/my_program-keypair.json

# Update declare_id! in lib.rs with the program ID

# Deploy
anchor deploy

# Deploy to specific cluster
anchor deploy --provider.cluster devnet

# Verify on-chain (Anchor Verified Builds)
anchor verify <PROGRAM_ID>
```

### Native Solana Deployment

```bash
# Build BPF/SBF binary
cargo build-sbf

# Deploy
solana program deploy target/deploy/my_program.so \
  --url devnet \
  --keypair ~/.config/solana/id.json

# Deploy with specific program ID
solana program deploy target/deploy/my_program.so \
  --program-id <KEYPAIR_PATH> \
  --url devnet
```

### Funding Accounts

```bash
# Devnet airdrop
solana airdrop 2 --url devnet

# Check balance
solana balance --url devnet
```

### Gas / Fee Estimation
- Solana fees are typically very low (< 0.01 SOL for deployment)
- Program deployment cost depends on binary size: ~0.00348 SOL per byte
- Use `solana rent <BYTES>` to estimate rent costs

### Post-Deploy Steps
1. Record Program ID
2. Verify program on Solana Explorer
3. Run anchor test against deployed program
4. Verify IDL is published (Anchor):
   ```bash
   anchor idl init <PROGRAM_ID> --filepath target/idl/my_program.json
   ```
5. Check program authority:
   ```bash
   solana program show <PROGRAM_ID>
   ```

---

## Security Checklist (All Chains)

Before deploying to mainnet:

- [ ] All tests pass
- [ ] Audit completed (automated + manual)
- [ ] No Critical or High severity findings
- [ ] Gas/fee estimation reviewed
- [ ] Deployment script tested on testnet
- [ ] Admin keys secured (hardware wallet / multi-sig)
- [ ] Emergency pause mechanism in place
- [ ] Upgrade strategy documented
- [ ] Post-deployment verification plan ready
- [ ] Monitoring and alerting configured
