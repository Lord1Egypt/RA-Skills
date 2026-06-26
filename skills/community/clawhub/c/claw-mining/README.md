# Clawing — Proof of AI Work

**Mine cryptocurrency by doing real AI work.** Clawing is a fair-launch ERC-20 token where every coin is mined by calling AI APIs and proving the work on-chain. No premine, no VC allocation, no team tokens — 100% mined by the community.

## Overview

Clawing introduces **Proof of AI Work (PoAIW)** — a novel mining mechanism where miners call large language model APIs, and an Oracle network verifies the work was actually performed. Verified miners receive CLAW tokens as rewards.

Key principles:
- **Fair launch** — Zero premine. Every CLAW token is mined through real AI computation.
- **Useful work** — Mining produces real AI outputs, not wasted energy.
- **Decentralized governance** — The community votes on which AI model to use each Era.
- **Logarithmic rewards** — Reward formula `R = base x (1 + ln(T))` prevents whale dominance.

## Architecture

```
+-------------------------------------------------------------+
|                     Smart Contracts                          |
|                                                              |
|  CLAW_Token <-- MinterProxy <-- PoAIWMint --> OracleVerifier |
|  (ERC-20)       (7-day timelock)  (mining logic) (ECDSA sigs)|
+-----------------------------+--------------------------------+
                              | verify + mint
                              |
+-----------------------------+--------------------------------+
|                    Oracle Server                             |
|                                                              |
|  7-step verification pipeline:                               |
|  1. Format validation       5. Cooldown check                |
|  2. Model validation        6. Anti-cheat checks             |
|  3. Seed validation         7. ECDSA signature issuance      |
|  4. Prompt format check                                      |
+-----------------------------+--------------------------------+
                              | attest
                              |
+-----------------------------+--------------------------------+
|                   AI Agent Miner                             |
|                                                              |
|  Install Skill -> Agent handles everything automatically     |
|  Setup -> Configure -> Mine -> Wait -> Repeat                |
+-------------------------------------------------------------+
```

### Smart Contracts

| Contract | Role |
|----------|------|
| **CLAW_Token** | ERC-20 token ("CLAW"). 210B max supply, immutable minter, zero admin privileges. |
| **MinterProxy** | Upgradeable proxy with 7-day timelock. Guardian can propose new minter; community has 7 days to review. |
| **PoAIWMint** | Core mining logic. Era/Epoch system, reward calculation, cooldown enforcement, model governance. |
| **OracleVerifier** | Multi-node ECDSA signature verification (1-5 Oracle signers). Anti-replay, rate limiting, deadline enforcement. |

### Oracle Server

A TypeScript server that verifies miners actually performed AI work. Runs a 7-step verification pipeline before issuing ECDSA signatures that authorize on-chain minting.

## How to Mine

CLAW mining is designed to be fully automated through AI Agents. Install the CLAW Mining Skill, tell your agent "mine CLAW", and the agent handles the entire mining process — from setup to continuous mining. No technical knowledge required.

### What You Need

| Requirement | Details |
|-------------|---------|
| AI Agent platform | [OpenClaw](https://openclaw.ai) (recommended), [Hermes Agent](https://hermes.garden), [Perplexity](https://www.perplexity.ai), or any AgentSkills-compatible platform |
| Ethereum wallet | A private key with ETH for gas (~0.01 ETH is enough for many mines) |
| AI API key | xAI API key (recommended) or OpenRouter API key |
| Ethereum RPC | Alchemy, Infura, or any mainnet RPC endpoint |

### Get Started with OpenClaw (Recommended)

1. **Install the Skill**: `clawhub install claw-mining`
2. **Start a new OpenClaw session**
3. **Tell your agent**: "mine CLAW"
4. **Provide your credentials** when the agent asks (AI API key, RPC URL, wallet)
5. **The agent handles everything else** — configuration, mining, cooldown management

### Other Platforms (Hermes Agent, Perplexity, etc.)

1. **Install the CLAW Mining Skill** on your AI Agent platform
2. **Tell the agent**: "Help me set up CLAW mining"
3. **Provide your credentials** when the agent asks
4. **The agent handles everything else**

The agent will guide you through the entire process step by step. No technical knowledge required.

See the full [Mining Guide](docs/MINING_GUIDE.md) for detailed instructions.

### Security: Your Keys Stay Local

- The `init` command never asks for or writes your private key — you paste it into `.env` yourself
- The `.env` file is created with restricted permissions (`chmod 600`, owner-only read/write)
- At runtime the miner loads the key into memory for local signing only, then removes it from the config object
- The private key is NEVER logged, transmitted, or sent to the Oracle, AI API, or any external service
- All transactions are signed locally by the miner process on your own computer

## Token Economics

### A Note on the Ticker: From CLI to CLAW

The token was originally designed with the ticker **CLI** — a reference to the Command Line Interface, the foundational way humans interact with machines. In the age of AI, the command line has taken on renewed significance: it is how developers summon intelligence, orchestrate agents, and build the future. As a ticker, CLI was technically elegant and deeply meaningful.

However, in the final moments before mainnet launch, a decision was made to change the ticker to **CLAW**.

The reasoning was simple. CLI speaks to engineers. CLAW speaks to everyone.

OpenClaw represents what many are calling the "iPhone moment" for AI agents — the point where autonomous intelligence becomes accessible to ordinary people, not just developers. And no word captures that moment quite like *claw*: the act of reaching out, grasping, seizing something new. It carries a raw, universal energy that transcends technical circles.

From a technical perspective, CLI might have been the more popular choice. From a human perspective, CLAW resonates on a far larger scale. We chose the name that matches our ambition — to bring truly new intelligence within reach of everyone.

The contract internally still references `CLAW_Token` as its Solidity identifier. This is cosmetic and immutable after deployment; it does not appear in any user-facing interface. The on-chain token name is **CLAWING** and the symbol is **CLAW**.

### Parameters

| Parameter | Value |
|-----------|-------|
| **Token name** | CLAWING |
| **Symbol** | CLAW |
| **Decimals** | 18 |
| **Max supply** | 210,000,000,000 (210 billion) |
| **Premine** | 0 |
| **Eras** | 24 (halving each Era) |
| **Epochs per Era** | 21 |
| **Blocks per Epoch** | 50,000 (~1 week) |
| **Blocks per Era** | 1,050,000 (~145.8 days) |
| **Cooldown** | 3,500 blocks (~11.67 hours) |
| **Max claims per Epoch** | 14 per miner |
| **Era 1 base reward** | 100,000 CLAW per block equivalent |

### Reward Formula

```
R = perBlock x (1 + ln(T))
```

Where:
- `perBlock` = base reward for the current Era (halves each Era)
- `T` = total AI tokens consumed (100-100,000 range)
- `ln(T)` = natural logarithm, approximated on-chain via MSB bit operations

The logarithmic formula ensures diminishing returns — spending 10x more on AI calls does NOT yield 10x more CLAW. This prevents whale dominance and keeps mining accessible.

### Halving Schedule

| Era | Block Reward | Approximate Duration |
|-----|-------------|---------------------|
| 1 | 100,000 CLAW/block | ~146 days |
| 2 | 50,000 CLAW/block | ~146 days |
| 3 | 25,000 CLAW/block | ~146 days |
| ... | Halves each Era | ... |
| 24 | Final Era | Mining ends |

### Model Governance

Each Era, CLAW holders vote on which AI model miners must use:
- **Epochs 11-15**: Nomination window (propose candidate models)
- **Epochs 16-20**: Voting window (lock CLAW to vote, 1 CLAW = 1 vote)
- **Epoch 21**: Announcement (winning model takes effect next Era)

Era 1 uses a hardcoded model (set at deployment). All candidate models must support the OpenAI `/v1/chat/completions` API format.

## Project Structure

```
clawing/
+-- contracts/    # Solidity smart contracts (Foundry)
|   +-- src/
|       +-- CLAW_Token.sol      # ERC-20 token
|       +-- MinterProxy.sol     # Upgradeable proxy + timelock
|       +-- PoAIWMint.sol       # Mining logic + governance
|       +-- OracleVerifier.sol  # ECDSA signature verification
+-- oracle/       # Oracle verification server (TypeScript)
+-- miner/        # Miner engine (TypeScript) — used by AI Agent Skills
+-- e2e/          # End-to-end integration tests
+-- deploy/       # Deployment scripts
+-- docs/         # Documentation
```

## Contract Addresses

**Ethereum Mainnet**

| Contract | Address |
|----------|--------|
| **OracleVerifier** | [`0xc24a0ba99b9ff6b7ccea6beb4013b69f39024fd5`](https://etherscan.io/address/0xc24a0ba99b9ff6b7ccea6beb4013b69f39024fd5) |
| **CLAW_Token (CLAWING/CLAW)** | [`0x4ba1209b165b62a1f0d2fbf22d67cacf43a6df2b`](https://etherscan.io/address/0x4ba1209b165b62a1f0d2fbf22d67cacf43a6df2b) |
| **MinterProxy** | [`0xe7fc311863b95e726a620b07607209965ee72bce`](https://etherscan.io/address/0xe7fc311863b95e726a620b07607209965ee72bce) |
| **PoAIWMint** | [`0x511351940d99f3012c79c613478e8f2c887a8259`](https://etherscan.io/address/0x511351940d99f3012c79c613478e8f2c887a8259) |

**Sepolia Testnet** — See [Sepolia Deployment Guide](docs/SEPOLIA_DEPLOYMENT_GUIDE.md)

## Security

### Defense in Depth

Clawing uses multiple layers of protection:

| Layer | Mechanism |
|-------|-----------|
| **Local signing** | Private keys never leave the user's machine; all transactions signed locally |
| **Anti-replay** | `usedSignatures` mapping — each Oracle signature can only be used once |
| **Rate limiting** | 3,500-block cooldown (~11.67h) + OracleVerifier timestamp-based secondary cooldown |
| **Epoch caps** | Max 14 claims per miner per Epoch; total Epoch token cap |
| **Token range** | AI token consumption must be 100-100,000 (prevents trivial/fake calls) |
| **Deadline** | Signatures expire within 300 blocks (~1 hour) — prevents signature hoarding |
| **Anti-flash-loan** | Vote-locking mechanism prevents flash loan governance attacks |
| **Upgrade safety** | MinterProxy 7-day timelock; Guardian has max 3 cancellations |

### Oracle Verification Pipeline

The Oracle server performs 7 checks before signing:
1. **Format validation** — Request structure and field types
2. **Model validation** — AI model matches the current on-chain Era model
3. **Seed validation** — Epoch seed matches on-chain state
4. **Prompt format** — Mining prompt contains required fields (address, seed, epoch, nonce, claim index)
5. **Cooldown check** — Miner's cooldown has elapsed and epoch claim limit not reached
6. **Anti-cheat** — Response ID validity, token range, token sum, response freshness (<5 min), finish reason, nonce validation

### Guardian Role

The Guardian (deployer) can propose new minters via MinterProxy, subject to a mandatory 7-day timelock. The Guardian can cancel proposals (max 3 times) and can permanently renounce their role for full decentralization.

### Audit Status

4 rounds of adversarial security review completed with 0 blocking issues. Community audit ongoing.

## Testing

| Component | Tests |
|-----------|-------|
| Smart Contracts | 68 tests |
| Oracle Server | 61 tests |
| Miner Engine | 15 tests |
| E2E Integration | 10 tests |
| **Total** | **154 tests passing** |

```bash
# Contract tests (requires Foundry)
cd contracts && forge test

# Oracle tests
cd oracle && npm test

# Miner tests
cd miner && npm test

# E2E tests
cd e2e && npm test
```

## Contributing

Clawing is open source and contributions are welcome. Please:

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Ensure all existing tests pass
5. Submit a pull request

## License

MIT-0
