---
name: chainaware-behavioral-prediction
version: 1.0.0
license: MIT
description: "Use this skill whenever a user asks about wallet safety, fraud risk, rug pull detection,  wallet behavior analysis, DeFi personalization, on-chain reputation scoring, AML checks,  token ranking by holder quality, airdrop screening, lending risk, token launch auditing,  or AI agent trust scoring. Triggers on questions like: is this wallet safe?, will this pool rug pull?, what will this address do next?,  score this wallet, detect fraud for address, personalize my DeFi agent,  rank this token, top AI tokens, best holders of this token,  check this contract, is this token safe?, profile this wallet,  KYC this address, pre-screen this user, AML check this wallet,  is this address suspicious?, screen this wallet before onboarding, what is the risk score of this address?, analyze on-chain behavior,  is this LP safe to deposit?, will this contract rug?,  what DeFi products suit this wallet?, segment this user,  what is this wallet's experience level?, find strong token holders, which token has the best community?,rank tokens by holder quality,  should we list this token?, audit this launch, is this deployer trustworthy?,  vet this IDO, launch safety check, screen this airdrop list, filter bots from airdrop,  rank these wallets for token distribution, fair airdrop allocation,  assess this borrower, what collateral ratio for this wallet?, lending risk for 0x...,  what interest rate for this borrower?, should I lend to this wallet?,  screen this AI agent, is this agent wallet safe?, agent trust score for 0x...,  check the feeder wallet for this agent, can I trust this agent?,  route this wallet to onboarding, is this user a beginner?, skip onboarding for this wallet?,  or any request to analyze a blockchain wallet address, smart contract, token, or AI agent  for risk, behavior, intent, community strength, or trustworthiness.  Also use when integrating the ChainAware MCP server into Claude Code, Cursor,  ChatGPT, or any MCP-compatible AI agent framework."
metadata:
  openclaw:
    requires:
      env:
        - CHAINAWARE_API_KEY
    primaryEnv: CHAINAWARE_API_KEY
    env_usage:
      CHAINAWARE_API_KEY: "Passed as the `apiKey` parameter in every tool call (predictive_fraud, predictive_fraud_batch, predictive_behaviour, predictive_behaviour_batch, predictive_rug_pull, credit_score). Not required for check_job_status or get_job_results — those use job_id + signature. Never logged or included in output. Sourced exclusively from the CHAINAWARE_API_KEY environment variable — never hardcoded."
    data_handling:
      external_endpoints:
        - url: https://prediction.mcp.chainaware.ai/sse
          transport: SSE
          purpose: Blockchain wallet and contract behavioural analysis
          data_sent:
            - Wallet addresses (pseudonymous on-chain identifiers)
            - Smart contract / LP addresses
            - Network identifier (e.g. ETH, BNB, BASE)
          data_NOT_sent:
            - Names, emails, or any off-chain PII
            - Raw transaction data
            - Private keys or seed phrases
          retention: Governed by ChainAware's privacy policy
          privacy_policy: https://chainaware.ai/privacy

    emoji: 🔮
    homepage: https://github.com/ChainAware/behavioral-prediction-mcp
    author: ChainAware
    tags:
      - web3
      - blockchain
      - fraud-detection
      - rug-pull
      - wallet-analytics
      - defi
      - mcp
      - ai-agents
      - personalization
      - aml
      - token-rank
      - on-chain-intelligence
---

# ChainAware Behavioral Prediction MCP

## What This Skill Does

The **ChainAware Behavioral Prediction MCP** connects any AI agent to a continuously updated
Web3 behavioral intelligence layer: **14M+ wallet profiles** across **8 blockchains**, built from
**1.3 billion+ predictive data points**. It delivers ten capabilities via a single MCP endpoint:

1. **Fraud Detection** — predict fraudulent wallet behavior before it happens ([~98% accuracy on ETH](https://chainaware.ai/scam-db))
2. **Batch Fraud Detection** — async batch job for fraud screening large wallet lists; returns `job_id` + `signature`
3. **Behavioral Analysis** — profile wallet intent, risk tolerance, experience, and next likely actions
4. **Batch Behavioral Analysis** — async batch job for behavioral profiling large wallet lists; returns `job_id` + `signature`
5. **Batch Job Status** — poll the progress of any running batch job
6. **Batch Job Results** — retrieve full per-wallet results from a completed or partial batch job
7. **Rug Pull Detection** — forecast whether a smart contract or liquidity pool will rug pull
8. **Credit Score** — crypto credit/trust score (1–9) combining fraud probability and social graph analysis
9. **Token Rank List** — rank tokens by holder community strength across chains and categories
10. **Token Rank Single** — deep-dive into a single token's community quality and top holders

Unlike forensic blockchain tools that describe the past, this MCP is **predictive** — it tells your
agent what is *about to happen*.

**MCP Server URL:** `https://prediction.mcp.chainaware.ai/sse`  
**GitHub:** https://github.com/ChainAware/behavioral-prediction-mcp  
**Website:** https://chainaware.ai  
**Pricing / API Key:** https://chainaware.ai/pricing  
**Twitter:** https://x.com/ChainAware/  
**LinkedIn:** https://www.linkedin.com/company/chainaware  
**Blog:** https://chainaware.ai/blog  
**Learn:** https://chainaware.ai/learn  
**Examples:** https://github.com/ChainAware/examples  
**Fraud Detection Accuracy:** [98% backtesting verified](https://chainaware.ai/scam-db)  
**Rug Pull Detection Accuracy:** [90.1% backtesting verified](https://chainaware.ai/resources/rugpull-verification)  
**Recognition:** [CB Insights Fraud Prevention Market Map](https://www.cbinsights.com/research/report/the-fraud-prevention-market-map-for-the-ai-era/) (2026) · [BNB Chain AI Landscape](https://x.com/BNBCHAIN/status/1947597551139500419) (2025) · [BNB Chain Kickstart](https://www.bnbchain.org/en/programs/kickstart#services) (2025) · [Google Cloud $250k Grant](https://chainaware.ai/blog/google-cloud-grant/) (2025) · [AWS Fintech Accelerator](https://chainaware.ai/blog/aws-grant/) (2024) · [Safary Club Web3 Growth Landscape](https://x.com/Safaryclub/status/1822983239734329613) (2024)

---

## Capabilities

- **Fraud Detection** — predict fraudulent wallet behavior before it happens ([~98% accuracy on ETH](https://chainaware.ai/scam-db))
- **Batch Fraud Detection** — async batch fraud screening for large wallet lists; fire-and-fetch pattern via `predictive_fraud_batch` → `check_job_status` → `get_job_results`
- **Behavioral Analysis** — profile wallet intent, risk tolerance, experience, and next likely actions across DeFi, NFT, and trading segments
- **Batch Behavioral Analysis** — async batch behavioral profiling for large wallet lists; same fire-and-fetch pattern via `predictive_behaviour_batch` → `check_job_status` → `get_job_results`
- **Rug Pull Detection** — forecast whether a smart contract or liquidity pool will rug pull
- **Credit Score** — crypto credit/trust score (1–9) combining fraud probability and social graph analysis for DeFi lending decisions
- **Token Rank List** — rank tokens by holder community strength across ETH, BNB, BASE, and Solana
- **Token Rank Single** — deep-dive into a specific token's community quality and top holders

---

## When to Use This Skill

- User asks about wallet safety, fraud risk, or suspicious activity
- User wants to screen a wallet, contract, or LP before interacting with it
- User needs AML/compliance checks on a blockchain address
- User wants behavioral profiling or DeFi personalization for a wallet
- User asks about token quality, community strength, or holder analysis
- User is building a DeFi platform, AI agent, launchpad, or compliance tool
- User wants to integrate the ChainAware MCP into their codebase

## When NOT to Use This Skill

- User asks about general blockchain data (balances, transaction history) → use a block explorer
- User wants real-time price data or market cap → use a market data API
- User wants to analyze smart contract code for bugs → use a code auditing tool
- For complex behavioural analysis (deep wallet profiling including fraud signals) → escalate to `chainaware-wallet-auditor` subagent
- For batch screening of many wallets → use batch MCP tools (`predictive_fraud_batch` / `predictive_behaviour_batch`) for large lists, or `chainaware-fraud-detector` subagent for small lists
- For marketing personalization → use `chainaware-wallet-marketer` subagent

---

## Supported Blockchains

| Tool | Networks |
|---|---|
| `predictive_fraud` | ETH, BNB, POLYGON, TON, BASE, TRON, HAQQ |
| `predictive_fraud_batch` | ETH, BNB, POLYGON, TON, BASE, TRON, HAQQ |
| `predictive_behaviour` | ETH, BNB, BASE, HAQQ, SOLANA |
| `predictive_behaviour_batch` | ETH, BNB, BASE, HAQQ, SOLANA |
| `check_job_status` | Network-agnostic (uses job_id + signature) |
| `get_job_results` | Network-agnostic (uses job_id + signature) |
| `predictive_rug_pull` | ETH, BNB, BASE, HAQQ |
| `credit_score` | ETH |
| `token_rank_list` | ETH, BNB, BASE, SOLANA |
| `token_rank_single` | ETH, BNB, BASE, SOLANA |

---

## Step-by-Step Workflow

### For wallet fraud screening

1. **Confirm inputs** — wallet address and network. If network is missing, ask.
2. **Call `predictive_fraud`** with the wallet address and network.
3. **Interpret `probabilityFraud`** using the threshold table below.
4. **Scan `forensic_details`** for negative flags (mixer use, sanctioned entities, darknet, etc.).
5. **Report** status, score, and any forensic flags in plain language.

### For behavioral profiling / personalization

1. **Confirm inputs** — wallet address and network.
2. **Call `predictive_behaviour`** with the wallet address and network.
3. **Extract key signals**: `intention.Value` (Prob_Trade/Stake/Bridge/NFT_Buy), `experience.Value`, `categories`, `recommendation`.
4. **Classify the wallet** by dominant category and intent signal.
5. **Generate** personalized recommendations or next-best-action based on the profile.

### For rug pull / contract safety checks

1. **Confirm inputs** — smart contract or LP address and network.
2. **Optionally call `predictive_fraud`** on the *deployer* address first for extra signal.
3. **Call `predictive_rug_pull`** with the contract address.
4. **Interpret `probabilityFraud`** and scan `forensic_details` for liquidity and contract risk flags.
5. **Apply the Deployer Risk Amplifier**: if deployer fraud score ≥ 0.5, escalate overall risk one level.
6. **Report** verdict with supporting forensic evidence.

### For token ranking / discovery

1. **Identify the request** — list of tokens or single token deep-dive?
2. **For lists**: call `token_rank_list` with appropriate `category`, `network`, `sort_by: communityRank`, `sort_order: DESC`.
3. **For single tokens**: call `token_rank_single` with `contract_address` and `network`.
4. **Report** `communityRank`, `normalizedRank`, `totalHolders`, and top holder profiles.

### For batch fraud or behavioural screening (large wallet lists)

1. **Schedule** — call `predictive_fraud_batch` or `predictive_behaviour_batch` with the wallet list and network.
2. **Store** both `job_id` and `signature` from the response — required for all follow-up calls.
3. **Poll** — call `check_job_status` with `job_id` + `signature` until status is `completed` or `partial`.
   - Status `pending` or `processing` → wait and retry.
   - Status `partial` → some wallets failed but results are available for completed items.
4. **Retrieve** — call `get_job_results` with `job_id` + `signature` to fetch the full per-wallet data.
5. **Process** — the `data` array returns the same schema as single-wallet `predictive_behaviour` / `predictive_fraud` results.

> Never call `get_job_results` while status is still `pending` or `processing`. The job `expires_at` timestamp in the status response indicates how long results are retained.

### For full due diligence (multi-tool)

1. Call `predictive_fraud` → get fraud score and forensic flags
2. Call `predictive_behaviour` → get behavioral profile and intent
3. Call `predictive_rug_pull` (if a contract address) → get contract risk
4. Synthesize all three into a unified verdict with risk level and recommendation

> For complex due diligence workflows, escalate to the `chainaware-wallet-auditor` subagent.

---

## Risk Score Thresholds

| Score Range | Label | Recommended Action |
|---|---|---|
| 0.00 – 0.20 | 🟢 Low Risk | Safe to proceed |
| 0.21 – 0.50 | 🟡 Medium Risk | Proceed with caution, monitor |
| 0.51 – 0.80 | 🔴 High Risk | Block or require additional verification |
| 0.81 – 1.00 | ⛔ Critical Risk | Reject immediately |

---

## Available Tools

### 1. `predictive_fraud` — Fraud Detection

Forecasts the probability that a wallet will engage in fraudulent activity. Includes AML checks.
Use when a user wants to screen a wallet before interacting with it.

**Inputs:**
- `apiKey` (string, required) — ChainAware API key
- `network` (string, required) — e.g. `ETH`, `BNB`, `BASE`
- `walletAddress` (string, required) — the wallet to evaluate

**Key output fields:**
- `status` — `"Fraud"`, `"Not Fraud"`, or `"New Address"`
- `probabilityFraud` — decimal 0.00–1.00
- `forensic_details` — deep on-chain breakdown

**Example prompts that trigger this tool:**
- *"Is it safe to interact with 0xABC... on Ethereum?"*
- *"What is the fraud risk of this BNB wallet?"*
- *"Run an AML check on this address."*
- *"Screen this wallet before onboarding."*
- *"Is this address on any sanctions list?"*
- *"Pre-screen this user's wallet for compliance."*

---

### 2. `predictive_behaviour` — Behavioral Analysis & Personalization

Profiles a wallet's on-chain history and predicts its next actions.

**Inputs:**
- `apiKey` (string, required)
- `network` (string, required)
- `walletAddress` (string, required)

**Key output fields:**
- `intention` — predicted next actions (`Prob_Trade`, `Prob_Stake`, `Prob_Bridge`, `Prob_NFT_Buy` — High/Medium/Low)
- `recommendation` — personalized action suggestions
- `categories` — behavioral segments (DeFi Lender, NFT Trader, Bridge User, etc.)
- `riskProfile` — risk tolerance and balance age breakdown
- `experience` — experience score 0–10 (beginner → expert)
- `protocols` — which protocols this wallet uses (Aave, Uniswap, GMX, etc.)

**Example prompts that trigger this tool:**
- *"What will this wallet do next?"*
- *"Is this user a DeFi lender or an NFT trader?"*
- *"Recommend the best yield strategy for this address."*
- *"What's the experience level of this wallet?"*
- *"Personalize my DeFi agent's response for this user."*
- *"Segment this wallet for my marketing campaign."*

---

### 3. `predictive_rug_pull` — Rug Pull Detection

Forecasts whether a smart contract or liquidity pool is likely to execute a rug pull.

**Inputs:**
- `apiKey` (string, required)
- `network` (string, required)
- `walletAddress` (string, required) — smart contract or LP address

**Key output fields:**
- `status` — `"Fraud"` or `"Not Fraud"`
- `probabilityFraud` — decimal 0.00–1.00
- `forensic_details` — on-chain metrics behind the score

**Example prompts that trigger this tool:**
- *"Will this new DeFi pool rug pull if I stake my assets?"*
- *"Is this smart contract safe?"*
- *"Check if this launchpad project is legitimate."*
- *"Monitor this LP position for rug pull risk."*
- *"Is this contract deployer trustworthy?"*

---

### 4. `credit_score` — Crypto Credit Score

Calculates a credit/trust score (1–9) for a wallet by combining fraud probability with social graph analysis. Designed for DeFi lending and any use case needing a fast single-number creditworthiness signal.

**Inputs:**
- `apiKey` (string, required)
- `network` (string, required) — `ETH`
- `walletAddress` (string, required) — the wallet to score

**Key output fields:**
- `creditData.riskRating` — integer 1–9 (1 = highest risk, 9 = highest trust)
- `creditData.walletAddress` — echoed wallet address

| riskRating | Label | Lending Interpretation |
|-----------|-------|------------------------|
| 9 | ✅ Prime | Highest creditworthiness — best terms |
| 7–8 | 🟢 Reliable | Low credit risk — standard terms |
| 5–6 | 🟡 Moderate | Elevated caution — higher collateral |
| 3–4 | 🔴 High Risk | Restricted terms or decline |
| 1–2 | ⛔ Very High Risk | Do not lend |

**Example prompts that trigger this tool:**
- *"What is the credit score for 0xABC...?"*
- *"Is this wallet a reliable borrower?"*
- *"Calculate credit score for this address on ETH."*
- *"Rate this wallet's creditworthiness."*
- *"Trust score for lending — 0xDEF... on BNB."*

---

### 5. `token_rank_list` — Token Ranking by Holder Strength

Ranks tokens by the quality and strength of their holder community.

**Inputs:**
- `limit` (string, required) — items per page
- `offset` (string, required) — page number
- `network` (string, required) — `ETH`, `BNB`, `BASE`, `SOLANA`
- `sort_by` (string, required) — e.g. `communityRank`
- `sort_order` (string, required) — `ASC` or `DESC`
- `category` (string, required) — `AI Token`, `RWA Token`, `DeFi Token`, `DeFAI Token`, `DePIN Token`
- `contract_name` (string, required) — token name search (empty string for no filter)

**Key output fields:**
- `data.total` — total matching tokens
- `data.contracts[]` — array with `contractAddress`, `contractName`, `ticker`, `chain`, `category`, `communityRank`, `normalizedRank`, `totalHolders`

**Example prompts that trigger this tool:**
- *"What are the top AI tokens on Ethereum?"*
- *"Rank DeFi tokens on BNB by community strength."*
- *"Which RWA tokens have the strongest holder base on BASE?"*
- *"Show me the top 10 tokens by community rank on ETH."*
- *"Compare DePIN tokens across Solana and Ethereum."*

---

### 6. `token_rank_single` — Single Token Rank & Top Holders

Returns the rank and top holders for a specific token by contract address.

**Inputs:**
- `contract_address` (string, required) — token contract or mint address
- `network` (string, required) — `ETH`, `BNB`, `BASE`, `SOLANA`

**Key output fields:**
- `data.contract` — token details including `communityRank`, `normalizedRank`, `totalHolders`
- `data.topHolders[]` — holder wallet addresses with `balance`, `walletAgeInDays`, `transactionsNumber`, `totalPoints`, `globalRank`

**Example prompts that trigger this tool:**
- *"What is the token rank for USDT on Ethereum?"*
- *"Who are the top holders of 0xdAC17F... on ETH?"*
- *"How strong is the holder base of this contract on BNB?"*
- *"Show me the best holders of this Solana token."*

---

### 7. `predictive_fraud_batch` — Batch Fraud Detection (Schedule)

Schedules an async fraud detection job for a list of wallet addresses. Returns a job handle immediately — results are fetched later via `check_job_status` + `get_job_results`.

**Inputs:**
- `apiKey` (string, required) — ChainAware API key
- `network` (string, required) — `ETH`, `BNB`, `POLYGON`, `TON`, `BASE`, `TRON`, `HAQQ`
- `addresses` (array[objects], required) — list of wallet address objects to evaluate

**Key output fields:**
- `job_id` — unique job identifier (store this)
- `signature` — access token for follow-up calls (store this)
- `status` — always `"pending"` on schedule response
- `total_items` — number of wallets submitted

**Example prompts that trigger this tool:**
- *"Run fraud screening on this list of 500 wallets on ETH."*
- *"Batch AML check for these addresses on BNB."*
- *"Screen all wallets from this CSV for fraud on BASE."*

---

### 8. `predictive_behaviour_batch` — Batch Behavioral Analysis (Schedule)

Schedules an async behavioral analysis job for a list of wallet addresses. Same fire-and-fetch pattern as `predictive_fraud_batch`.

**Inputs:**
- `apiKey` (string, required) — ChainAware API key
- `network` (string, required) — `ETH`, `BNB`, `BASE`, `HAQQ`, `SOLANA`
- `addresses` (array[objects], required) — list of wallet address objects to evaluate

**Key output fields:**
- `job_id` — unique job identifier (store this)
- `signature` — access token for follow-up calls (store this)
- `status` — always `"pending"` on schedule response
- `total_items` — number of wallets submitted

**Example prompts that trigger this tool:**
- *"Profile all wallets in this list on ETH — intent, experience, risk."*
- *"Batch behavioural analysis for these 200 addresses on BASE."*
- *"Run segment analysis across all wallets in this Solana list."*

---

### 9. `check_job_status` — Batch Job Progress

Checks the progress of a scheduled batch job. Returns counts only — no wallet data. Call this after scheduling a batch job and before fetching results.

**Inputs:**
- `job_id` (string, required) — from `predictive_fraud_batch` or `predictive_behaviour_batch`
- `signature` (string, required) — from the same schedule call

**Key output fields:**
- `status` — `"pending"` | `"processing"` | `"partial"` | `"completed"`
- `completed_items`, `failed_items`, `pending_items` — progress counts
- `expires_at` — when results will be purged

| Status | Meaning | Next Action |
|--------|---------|-------------|
| `pending` | Queued, not started | Wait and retry |
| `processing` | Actively running | Wait and retry |
| `partial` | Some done, some failed | Safe to call `get_job_results` |
| `completed` | All wallets processed | Call `get_job_results` |

---

### 10. `get_job_results` — Batch Job Results

Retrieves the full per-wallet results from a completed or partial batch job. Returns the same rich schema as the single-wallet tools. **Only call when `check_job_status` shows `completed` or `partial`.**

**Inputs:**
- `job_id` (string, required) — from the schedule call
- `signature` (string, required) — from the same schedule call

**Key output fields:**
- `data[]` — array of per-wallet results; each entry mirrors `predictive_behaviour` / `predictive_fraud` output schema

**Example prompts that trigger this tool:**
- *"Get the results for job 0fc5897a on ETH."*
- *"Fetch the completed batch fraud results."*
- *"Retrieve wallet profiles from the batch I scheduled earlier."*

---

## Validation Checkpoints

### Input Validation
- ✅ Wallet address provided and non-empty
- ✅ Network specified and supported for the tool being called (check table above)
- ✅ `CHAINAWARE_API_KEY` environment variable is set (not required for `check_job_status` / `get_job_results`)
- ✅ For `token_rank_list`: `limit`, `offset`, `sort_by`, `sort_order`, and `category` all provided
- ✅ For `token_rank_single`: both `contract_address` and `network` provided
- ✅ For batch tools: both `job_id` and `signature` stored from the schedule response before calling follow-up tools
- ⚠️ If network is missing, ask the user before proceeding
- ⚠️ If network is not supported for the requested tool, inform the user and suggest an alternative
- ⚠️ Never call `get_job_results` while job status is `pending` or `processing`

### Output Validation
- ✅ `probabilityFraud` is present and in range 0.00–1.00
- ✅ Risk threshold label applied correctly (see table above)
- ✅ Forensic flags surfaced in plain language, not raw JSON
- ✅ Every recommendation cites the specific signal that drove it
- ✅ Network limitations clearly stated when a tool doesn't support the requested chain
- ✅ For behavioral profiles: at least `intention`, `experience`, and `categories` included in response
- ✅ For batch jobs: always report `job_id` to the user after scheduling; they may need it to check status manually

---

## Example Output

### Fraud Check — 0xABC... on ETH

```
🔮 FRAUD ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Wallet:  0xABC...
Network: ETH
Status:  🟡 MEDIUM RISK

Fraud Probability: 0.34
Risk Level: Medium — proceed with caution

Forensic Highlights:
  • 3 transactions flagged as suspicious
  • No mixer/tumbler activity detected
  • No sanctioned entity connections
  • Wallet age: 187 days

Recommendation: Monitor this wallet. Not safe for large-value
interactions without additional verification.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Behavioral Profile — 0xDEF... on BASE

```
🧠 BEHAVIORAL PROFILE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Wallet:  0xDEF...
Network: BASE

Experience:   7.2/10 — Experienced
Segment:      DeFi Lender, Bridge User
Risk Profile: Balanced

Intent Signals:
  Trade:    High
  Stake:    Medium
  Bridge:   High
  NFT Buy:  Low

Protocols Used: Aave, Uniswap, Across Bridge

Recommendation:
  → Promote yield optimization vaults
  → Highlight cross-chain bridging incentives
  → Skip NFT-focused messaging
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Requirements

- **API Key** — a `CHAINAWARE_API_KEY` environment variable is required. Obtain one at https://chainaware.ai/pricing
- **MCP-compatible host** — Claude Code, Cursor, Claude Desktop, ChatGPT Connectors, or any MCP client that supports SSE transport
- **Network awareness** — different tools support different blockchains; see the Supported Blockchains table above
- **No local installation** — the MCP server runs remotely at `https://prediction.mcp.chainaware.ai/sse`; no packages to install

---

## Integration Setup

### Claude Code (CLI)

```bash
claude mcp add --transport sse chainaware-behavioural-prediction-mcp-server \
  https://prediction.mcp.chainaware.ai/sse \
  --header "X-API-Key: your-key-here"
```

📚 Docs: https://code.claude.com/docs/en/mcp

### Claude Web / Claude Desktop

1. Go to **Settings → Integrations → Add integration**
2. Name: `ChainAware Behavioural Prediction MCP Server`
3. URL: `https://prediction.mcp.chainaware.ai/sse?apiKey=your-key-here`

📚 Docs: https://platform.claude.com/docs/en/agents-and-tools/remote-mcp-servers

### Cursor (`mcp.json`)

```json
{
  "mcpServers": {
    "chainaware-behavioural-prediction-mcp-server": {
      "url": "https://prediction.mcp.chainaware.ai/sse",
      "transport": "sse",
      "headers": {
        "X-API-Key": "your-key-here"
      }
    }
  }
}
```

📚 Docs: https://cursor.com/docs/context/mcp

### ChatGPT Connectors

1. Open **ChatGPT Settings → Apps / Connectors → Add Connector**
2. Name: `ChainAware Behavioural Prediction MCP Server`
3. URL: `https://prediction.mcp.chainaware.ai/sse?apiKey=your-key-here`

### Node.js

```javascript
import { MCPClient } from "mcp-client";
const client = new MCPClient("https://prediction.mcp.chainaware.ai/");

const fraud = await client.call("predictive_fraud", {
  apiKey: process.env.CHAINAWARE_API_KEY,
  network: "ETH",
  walletAddress: "0xYourWalletAddress"
});

const topTokens = await client.call("token_rank_list", {
  limit: "10", offset: "0", network: "ETH",
  sort_by: "communityRank", sort_order: "DESC",
  category: "AI Token", contract_name: ""
});
```

### Python

```python
from mcp_client import MCPClient
import os

client = MCPClient("https://prediction.mcp.chainaware.ai/")
result = client.call("predictive_fraud", {
    "apiKey": os.environ["CHAINAWARE_API_KEY"],
    "network": "ETH",
    "walletAddress": "0xYourWalletAddress"
})
```

---

## Real-World Use Cases

### DeFi Platforms
- **Risk-adjusted lending** — use fraud scores and behavioral profiles to set collateral requirements and interest rates per borrower
- **Liquidity management** — use intent signals to pre-position reserves and prevent pool drain
- **Yield routing** — identify wallets with high yield-seeking intent and route them to optimal vaults

### AI Agent Personalization
- Give your agent a real-time behavioral profile of each wallet it talks to
- Segment users automatically into DeFi Lender, NFT Trader, Bridge User, New Wallet, etc.

### Fraud & Compliance
- Screen wallets at the point of entry to your Dapp — before any transaction takes place
- Run AML monitoring across all active wallets
- Detect rug pull contracts at launchpad listing stage

### NFT & GameFi
- Personalize in-game economies based on a player wallet's on-chain history
- Filter bot wallets and wash traders from NFT drops using fraud scores

---

## Tips for Success

1. **Always specify the network** — many tools behave differently across chains
2. **Run fraud check first** — before any behavioral profiling, gate on fraud score
3. **Combine tools for full due diligence** — fraud + behaviour + rug pull together give a complete picture
4. **Use the Deployer Risk Amplifier** — a clean contract from a fraudulent deployer is still high risk
5. **For small lists (< 5 wallets)** — use subagents like `chainaware-fraud-detector` or `chainaware-airdrop-screener` which call single-wallet tools in a loop
6. **For 5+ wallets** — use batch tools directly: `predictive_fraud_batch` or `predictive_behaviour_batch` → `check_job_status` → `get_job_results`
7. **Always store job_id + signature** — both are required for every follow-up batch call; losing either means you cannot retrieve results
8. **Surface forensic flags in plain language** — never return raw JSON to end users

---

## Related Subagents (Claude Code)

These subagents in `.claude/agents/` provide specialized autonomous execution:

| Subagent | Use When |
|---|---|
| `chainaware-wallet-auditor` | Full due diligence — deep behavioural profiling including fraud signals |
| `chainaware-fraud-detector` | Fast fraud screening, batch wallet checks |
| `chainaware-rug-pull-detector` | Contract/LP safety with deployer analysis |
| `chainaware-wallet-marketer` | Personalized marketing messages per wallet segment |
| `chainaware-reputation-scorer` | Reputation score 0–1000 |
| `chainaware-aml-scorer` | AML compliance scoring 0–100 |
| `chainaware-trust-scorer` | Simple composable trust score 0.00–1.00 |
| `chainaware-credit-scorer` | Crypto credit score 1–9 for lending and creditworthiness decisions |
| `chainaware-wallet-ranker` | Wallet experience rank and leaderboard |
| `chainaware-whale-detector` | Whale tier classification for VIP treatment |
| `chainaware-onboarding-router` | Route wallets to beginner / intermediate / skip onboarding |
| `chainaware-token-ranker` | Discover and rank tokens by holder community strength |
| `chainaware-token-analyzer` | Single token deep-dive — community rank + top holders |
| `chainaware-defi-advisor` | Personalized DeFi product recommendations by experience + risk tier |
| `chainaware-airdrop-screener` | Batch screen wallets for airdrop eligibility, filter bots and fraud |
| `chainaware-lending-risk-assessor` | Borrower risk grade (A–F), collateral ratio, interest rate tier |
| `chainaware-token-launch-auditor` | Pre-listing launch safety audit — APPROVED / CONDITIONAL / REJECTED |
| `chainaware-agent-screener` | AI agent trust score 0–10 via agent + feeder wallet fraud checks |
| `chainaware-cohort-analyzer` | Segment a batch of wallets into behavioral cohorts with engagement strategies |
| `chainaware-counterparty-screener` | Real-time pre-transaction go/no-go (Safe / Caution / Block) |
| `chainaware-governance-screener` | DAO voter Sybil detection and voting weight calculation |
| `chainaware-sybil-detector` | Bulk Sybil attack detection for DAO votes — ELIGIBLE / REVIEW / EXCLUDE per wallet, pattern flags, and vote multipliers |
| `chainaware-transaction-monitor` | Real-time transaction risk for autonomous agents — ALLOW / FLAG / HOLD / BLOCK |
| `chainaware-lead-scorer` | Sales lead qualification — score, tier, conversion probability, outreach angle |
| `chainaware-upsell-advisor` | Next product recommendation and upsell message for existing users |
| `chainaware-platform-greeter` | Contextual welcome message per wallet per platform |
| `chainaware-marketing-director` | Full-cycle campaign orchestrator — segments, leads, whales, per-cohort messages |
| `chainaware-compliance-screener` | MiCA-aligned compliance report — PASS / EDD / REJECT (~70–75% MiCA coverage) |
| `chainaware-gamefi-screener` | Web3 game / P2E bot detection, player tier classification, reward eligibility |
| `chainaware-portfolio-risk-advisor` | Portfolio-level rug pull scan, risk grade (A–F), rebalancing plan |
| `chainaware-rwa-investor-screener` | RWA investor suitability — QUALIFIED / CONDITIONAL / REFER_TO_KYC / DISQUALIFIED |
| `chainaware-ltv-estimator` | 12-month revenue potential (LTV) as a USD range — tx count × avg tx value × fee rate, scaled by behavioral multipliers. Optional: platform_share, fee_rate |

---

## Background Reading

| Article | URL |
|---|---|
| Complete Product Guide | https://chainaware.ai/blog/chainaware-ai-products-complete-guide/ |
| Fraud Detector Guide | https://chainaware.ai/blog/chainaware-fraud-detector-guide/ |
| Rug Pull Detector Guide | https://chainaware.ai/blog/chainaware-rugpull-detector-guide/ |
| Token Rank Guide | https://chainaware.ai/blog/chainaware-token-rank-guide/ |
| Wallet Rank Guide | https://chainaware.ai/blog/chainaware-wallet-rank-guide/ |
| Wallet Auditor Guide | https://chainaware.ai/blog/chainaware-wallet-auditor-how-to-use/ |
| Transaction Monitoring Guide | https://chainaware.ai/blog/chainaware-transaction-monitoring-guide/ |
| Web3 Behavioral Analytics Guide | https://chainaware.ai/blog/chainaware-web3-behavioral-user-analytics-guide/ |
| Credit Score Guide | https://chainaware.ai/blog/chainaware-credit-score-the-complete-guide-to-web3-credit-scoring-in-2026/ |
| Credit Scoring Agent Guide | https://chainaware.ai/blog/chainaware-credit-scoring-agent-guide/ |
| Prediction MCP Developer Guide | https://chainaware.ai/blog/prediction-mcp-for-ai-agents-personalize-decisions-from-wallet-behavior/ |
| Top 5 Ways Prediction MCP Turbocharges DeFi | https://chainaware.ai/blog/top-5-ways-prediction-mcp-will-turbocharge-your-defi-platform/ |
| Why Personalization Is Next for AI Agents | https://chainaware.ai/blog/why-personalization-is-the-next-big-thing-for-ai-agents/ |
| Web3 User Segmentation for DApp Growth | https://chainaware.ai/blog/web3-user-segmentation-behavioral-analytics-for-dapp-growth-2026/ |
| AI-Powered Blockchain Analysis | https://chainaware.ai/blog/ai-powered-blockchain-analysis-machine-learning-for-crypto-security-2026/ |
| Forensic vs AI-Based Crypto Analytics | https://chainaware.ai/blog/forensic-crypto-analytics-versus-ai-based-crypto-analytics/ |
| Web3 Business Potential | https://chainaware.ai/blog/web3-business-potential/ |

---

## Data & Privacy

### What data leaves your environment

Every tool call transmits the following to `https://prediction.mcp.chainaware.ai/sse`:

| Field | Example | Notes |
|---|---|---|
| `walletAddress` | `0xABC...` | Pseudonymous on-chain identifier — not PII |
| `network` | `ETH` | Chain identifier only |
| `apiKey` | _(your key)_ | Sourced from `CHAINAWARE_API_KEY` env var; never logged |

**What is NOT sent:** names, emails, IP addresses, private keys, raw transaction history, or any off-chain personal data.

### API key handling

`CHAINAWARE_API_KEY` is read from the environment and passed as the `apiKey` parameter in each tool call. It is never included in output, never written to disk, and never logged by this skill. Treat it as a secret and rotate it regularly.

### Integration-specific privacy notes

- **Claude Code / Cursor**: key passed via `X-API-Key` header — does not appear in URLs or logs
- **Claude Web / ChatGPT**: key must be appended to the SSE URL (`?apiKey=...`) — these platforms do not support custom SSE headers. Be aware the key will appear in your browser's network tab. Use a restricted-scope key for these integrations.

### Operator responsibilities

Wallet addresses are pseudonymous identifiers. Whether they constitute personal data in your jurisdiction depends on your regulatory context (e.g. GDPR, MiCA). Operators processing wallets linked to identified users should perform their own data protection assessment.

**Privacy policy:** https://chainaware.ai/privacy

---

## Security Notes

- **Never hard-code API keys** in public repositories
- The server uses **SSE (Server-Sent Events)** for streaming responses
- Rate limits apply depending on your subscription tier

---

## Error Reference

| Code | Meaning |
|---|---|
| `403 Unauthorized` | Invalid or missing `apiKey` |
| `400 Bad Request` | Malformed `network` or `walletAddress` |
| `500 Internal Server Error` | Temporary backend failure — retry after a short delay |

---

## Access & Pricing

API key required. Subscribe at: https://chainaware.ai/pricing
