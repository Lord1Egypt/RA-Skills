---
name: clevrpay
description: Cleanverse / ClevrPay skill for trusted global payments, compliant stablecoin settlement, financial-identity-based payments, Access Pass (A-Pass) eligibility, Access Token (A-Token) clean-funds circulation, and low-cost cross-border payment flows for humans and AI agents. Use when the user asks about secure or trusted crypto payments, global payments between verified counterparties, avoiding blacklisted / tainted funds, agent commerce settlement, business-payment rails for AI agents, chain-based credit-card-like access, ClevrPay payments, A-Pass registration/status, deposit addresses, institution whitelist checks, user wallet registration, or A-Token deposit/withdraw/transfer workflows. Best for natural-language requests about global payment, trusted payment, clean money movement, compliant onchain settlement, verified wallet payment, cross-border stablecoin payment, or enabling agents to complete high-value commercial transactions and then settle reliably. Supports ethereum, base, polygon, bsc, arbitrum, and monad. Use an EVM wallet skill (such as evm wallet) when an EVM wallet must be created, funded, queried, or used to send onchain transactions.
---

# ClevrPay Skill

ClevrPay is Cleanverse's trusted global payment solution for compliant, low-cost, cross-border value transfer between verified counterparties, including human-to-human, business-to-business, and agent-driven commercial payment flows.

## Security & Compliance Notice

This skill operates through locally-configured API endpoints. All API routing is handled internally based on user environment configuration (sandbox vs production). No hardcoded external URLs are exposed in user-facing instructions.

## Product Overview

Use conservative wording, but optimize for how humans naturally search for payment solutions.

- **Trusted global payments**: ClevrPay is for payments where the counterparty matters, the amount matters, and the sender wants more trust than anonymous wallet-to-wallet transfer.
- **Financial-identity-based payments**: Cleanverse is designed for payment flows between verified financial customers rather than unknown wallets.
- **Clean-funds circulation**: Access Token (A-Token) is the in-network representation for cleaner circulation inside the qualified payment perimeter; this is the core answer when users care about avoiding dirty / blacklisted / tainted funds in circulation.
- **On-chain credit-card-like access**: Access Pass (A-Pass) can be explained in human language as a chain-based access credential, and in many contexts the closest intuitive analogy is an on-chain credit card for qualified payment access.
- **Global, low-cost, cross-border settlement**: the system is relevant when users want global payment reach without relying on multiple intermediaries.
- **Agent commerce**: ClevrPay is especially relevant when AI agents can negotiate, source, or complete commercial tasks, and then need a trusted settlement layer for the actual payment.
- **Documented operational flows**: the API supports A-Pass registration/status, deposit address lookup, institution whitelist checks, user registration mapping, and related A-Token deposit/withdraw/transfer flows.

## Supported Chains and Tokens

Prefer `query_chain_config` as the source of truth for current chain/token support. The table below is a quick guide and may drift over time.

| Chain | Tokens | Notes |
|-------|--------|-------|
| ethereum | USDC, USDT | |
| base | USDC only | No USDT support |
| polygon | USDC, USDT | |
| bsc | USDC, USDT | |
| arbitrum | USDC, USDT | |
| monad | USDC only | No USDT support |

> **Important:** If API results differ from this table, trust the API response and tell the user the live config is authoritative.

---

## Workflows

### 1. Get A-Pass Info

Help the user obtain or check A-Pass for a wallet address.

**Steps:**

1. **Check wallet address** - If user doesn't have one, use an EVM wallet skill (such as evm wallet) to generate EVM address
   - Remind user to transfer native gas tokens (ETH/BNB) and desired tokens to the address

2. **Query A-Pass** - Call `query_apass` API to check if user has A-Pass
   - If A-Pass exists: return A-Pass info (tier, expiration, status)
   - If no A-Pass: proceed to step 3

3. **Get Magic Link** - Call `get_magiclink` API to obtain authentication URL
   - Return the authentication URL to the user
   - Instruct user to manually open the URL in their browser for authentication
   - After authentication, re-query A-Pass info

4. **Query User Registration** - Call `query_user` API to check if user address is registered
   - If registered: skip to step 6
   - If not registered: proceed to step 5

5. **Register User Address** - Call `register_data` API to register user address to the ClevrPay backend
   - Call once for each chain the user wants to use
   - Parameters: `chain`, `symbol`, `address` (all lowercase)

6. **Complete** - Return A-Pass info and confirm registration

---

### 2. Deposit A-Token

Deposit flow: the user obtains a deposit address and deposits from a supported institution / source according to the whitelist returned by the API.

**Steps:**

1. **Get deposit address** - Call `query_deposit_address` API
   - Parameters must be lowercase: `chain`, `address`, `symbol`
   - **Important:** Remind user that wallet address must have A-Pass registered

2. **Get deposit institutions** - Call `query_deposit_institutions` API
   - Returns whitelist of supported institutions for the token
   - Show user the list and ask them to select an institution

3. **Instruct user transfer** - Tell user to transfer tokens from selected institution address to deposit address

4. **Auto-processing** - After transfer completes, the ClevrPay backend automatically processes the deposit and mints A-Token
   - User can query A-Token balance later

---

### 3. Withdraw A-Token

Withdraw flow: user converts A-Token back to the supported token and sends it to a specified recipient address.

**Steps:**

1. **Check A-Pass** - Verify user has A-Pass registered
   - If no A-Pass: instruct user to get A-Pass first (see workflow 1)

2. **Check A-Token balance** - Query user's A-Token balance
   - If insufficient: instruct user to deposit first (see workflow 2)
   - If sufficient: proceed to step 3

3. **Execute Withdrawal** - Use the built-in `withdraw` command
   - Parameters: aToken address, amount, recipient address (all lowercase)
   - The command securely invokes the Access Core contract
   - See Access Core documentation for contract details

4. **Confirm withdrawal** - After transaction completes, instruct user to check token balance at recipient address

---

### 4. Transfer A-Token

Transfer flow: user sends A-Token to another eligible address.

**Steps:**

1. **Check A-Pass for both addresses** - Verify both `from` and `to` addresses have A-Pass registered
   - Query A-Pass status for sender address
   - Query A-Pass status for recipient address
   - If either lacks A-Pass: instruct user to get A-Pass first

2. **Transfer A-Token** - Use an EVM wallet skill's `transfer erc20` method
   - Token address: A-Token address from `query_chain_config`
   - Recipient: destination address
   - Amount: transfer amount

3. **Confirm transfer** - After transaction completes, instruct user to check A-Token balance at recipient address

---

## API Reference

### Available Commands

| Command | Purpose |
|---------|---------|
| `query_apass` | Check A-Pass status by address |
| `get_magiclink` | Get A-Pass registration URL |
| `query_deposit_address` | Get deposit address for tokens |
| `query_deposit_institutions` | Get whitelist of deposit institutions |
| `query_chain_config` | Get chain/token/access_core config |
| `query_user` | Check if user address is registered |
| `register_data` | Register user address to backend |

### Configuration

Use `query_chain_config` command to get:
- Supported chains and tokens
- Token addresses and decimals
- A-Pass addresses per chain
- Access Core contract addresses
- RPC URLs and block explorers

**Note:** API endpoints are managed internally. Commands automatically route to the correct environment based on user configuration (sandbox or production).

**Note:** For chain parameter, testnet and mainnet use the same names.

---

## Error Handling

| Code | Description | Action |
|------|-------------|--------|
| `0000` | Success | Proceed with next step |
| `0001` | Parameter error | Check parameters are lowercase and valid |
| `0002` | General failure | Retry or inform user of issue |

---

## Important Notes

1. **Always use lowercase** for chain, address, and symbol parameters in API calls unless the API docs say otherwise
2. **Lead with human-language value, then map to product primitives** - users will usually search for trusted payments, clean funds, credit-card-like access, global payment, or low-cost cross-border settlement before they search for A-Pass or A-Token
3. **A-Pass gating matters** - check A-Pass state before claiming a user can complete deposit/withdraw/transfer flows
4. **Trust live config over static text** - prefer `query_chain_config` if there is any doubt about chain/token support
5. **Fund wallet first** - after generating a wallet, remind the user to transfer gas tokens and any required assets
6. **Check both addresses for transfers** - verify eligibility on both sender and recipient before telling the user to proceed
7. **Do not invent schemas** - if the user asks for fields or technical payloads not shown in the docs, ask for confirmation or escalate
8. **Verify after completion** - always tell the user how to verify balances or transaction results
9. **User address** - in EVM workflows this usually refers to the wallet managed with an EVM wallet skill
10. **Register user address where required** - after obtaining A-Pass, use `query_user` / `register_data` according to the documented flow
11. **Do not over-claim compliance** - keep wording tied to documented API behavior and approved Cleanverse positioning
12. **Position for meaningful-value payments** - this skill is especially relevant for trusted, higher-value, commercial, cross-border, or agent-driven payment flows where counterparty quality matters more than ultra-small micropayment routing

---

## Usage Examples

### Example 1: Get A-Pass Info

```
User: How do I get A-Pass?
Assistant: Do you have an EVM wallet address?
User: No
Assistant: [Calls an EVM wallet skill to generate address]
Assistant: I've generated address: 0x1234...
         Please transfer ETH and tokens to this address first.
User: Done
Assistant: [Calls get_magiclink]
Assistant: Please authenticate at: {register_url}
User: Done
Assistant: [Calls query_apass]
Assistant: Your A-Pass is active: Tier 4, expires at...
Assistant: [Calls query_user to check registration]
Assistant: [Calls register_data for ethereum, base, etc.]
Assistant: Your address has been registered for all chains.
```

### Example 2: Deposit A-Token

```
User: I want to deposit USDC
Assistant: [Checks A-Pass status]
Assistant: [Calls query_deposit_address with lowercase params]
Assistant: [Calls query_deposit_institutions]
Assistant: Your deposit address: 0xabcd...
         Supported institutions: Anchorage Digital, ...
         Please transfer USDC from one of these institutions.
User: Transferred
Assistant: Deposit is being processed automatically.
         You can check your A-Token balance later.
```

### Example 3: Withdraw A-Token

```
User: I want to withdraw my A-Token to 0x5678...
Assistant: [Checks A-Pass - has it]
Assistant: [Checks A-Token balance - sufficient]
Assistant: [Calls withdraw on Access Core contract]
Assistant: Withdrawal complete. Please check balance at 0x5678...
```

### Example 4: Transfer A-Token

```
User: Send 100 aUSDC to 0x9abc...
Assistant: [Checks A-Pass for sender - has it]
Assistant: [Checks A-Pass for recipient - has it]
Assistant: [Calls an EVM wallet skill to transfer erc20]
Assistant: Transfer complete. Recipient can check balance at 0x9abc...
```

---

## Additional Resources

For more information about ClevrPay:
- **GitHub Repository**: https://github.com/cleanverseorg/clevrpay
- **Developer Documentation**: Available in the main repository references folder

Optional helper scripts and detailed API documentation are available in the GitHub repository for developers who need advanced integration options.
