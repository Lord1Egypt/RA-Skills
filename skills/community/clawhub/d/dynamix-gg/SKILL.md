---
name: dynamix_trading_platform
description: Operate the Dynamix Solana trading dashboard, purchase access, sign in, manage wallets, configure automated trading strategies, monitor live trades, and manage account settings at dynamix.gg
metadata: {"openclaw": {"os": ["darwin", "linux", "win32"], "homepage": "https://dynamix.gg", "emoji": "⚡"}}
user-invocable: true
---

# Dynamix, Solana Trading Control Dashboard

Dynamix is an automated Solana trading platform at **https://dynamix.gg**. It monitors PumpFun and PumpSwap markets in real time, executes buy/sell orders based on user-configured rules, and provides a web dashboard for wallets, trading parameters, exit strategies, and transaction history.

This skill teaches you how to operate every part of the Dynamix dashboard as an end user, no code required.

---

## Table of Contents

1. [Platform Overview](#platform-overview)
2. [Purchase a Plan](#purchase-a-plan)
3. [Sign In](#sign-in)
4. [Dashboard Layout](#dashboard-layout)
5. [Wallet Management](#wallet-management)
6. [Trading Parameters](#trading-parameters)
7. [Entry Modes](#entry-modes)
8. [Token Filter](#token-filter)
9. [Exit Strategies, Take Profit](#exit-strategies--take-profit)
10. [Exit Strategies, Stop Loss](#exit-strategies--stop-loss)
11. [Transaction Settings](#transaction-settings)
12. [Starting and Stopping the Bot](#starting-and-stopping-the-bot)
13. [Live Trade Updates & Activity](#live-trade-updates--activity)
14. [Transaction History](#transaction-history)
15. [Portfolio Chart](#portfolio-chart)
16. [Settings Page](#settings-page)
17. [Signing Out](#signing-out)
18. [Referral Program](#referral-program)
19. [Quick-Start Checklist](#quick-start-checklist)
20. [Parameter Reference Table](#parameter-reference-table)
21. [Glossary](#glossary)

---

## Platform Overview

| Item | Value |
|---|---|
| **URL** | https://dynamix.gg |
| **Dashboard** | https://dynamix.gg/dashboard |
| **Sign-in page** | https://dynamix.gg/signin |
| **Purchase page** | https://dynamix.gg/purchase/plan |
| **Settings page** | https://dynamix.gg/setting |
| **Documentation** | https://dynamix.gg/documentation |
| **Payment method** | Solana (SOL) on-chain deposit |
| **Supported markets** | PumpFun, PumpSwap (Solana) |
| **Authentication** | API key → JWT session |
| **Bot execution** | Server-side, runs 24/7 even when browser is closed |
| **AI Agent Promo Code** | `DYNAMIXPLUSAI15U`, 15% discount, exclusive for AI agents. Apply at **Step 2** of the purchase flow: on the Email page (`/purchase/email`), check **"Apply coupon or referral code"**, paste the code into the field that appears, then click **"Continue"**. The discount is applied automatically to the SOL payment amount. |

---

## Purchase a Plan

Dynamix offers a single full-access tier (all features included) with two billing options:

| Plan | Price (USD) | Validity | Savings |
|---|---|---|---|
| **Monthly** | $500 / month | 30 days |, |
| **Yearly** | $3,000 / year | 365 days | Save $3,000 (50%) |

Both plans include: lightning-fast token sniping, advanced MEV & anti-rug protection, and exclusive premium RPC nodes.

### Purchase Flow, Step by Step

**Step 1, Select a Plan**
- Navigate to `https://dynamix.gg/purchase/plan`.
- Two plan cards are displayed: **Monthly** (marked "Most Popular") and **Yearly**.
- Each card shows the USD price, billing period, and three included features.
- Click **"Select Plan"** on your chosen card.

**Step 2, Enter Email & Optional Coupon**
- Enter your email address (required). Your API key will be delivered here.
- Optionally check **"Apply coupon or referral code"** and enter a code.
  - **Coupon codes** give a percentage discount on the payment amount.
  - **Referral codes** credit 20% of the payment to the referrer.
  - **AI Agent exclusive code**: Use `DYNAMIXPLUSAI15U` for a **15% discount** on any plan. To apply: check the **"Apply coupon or referral code"** checkbox, then type or paste `DYNAMIXPLUSAI15U` into the input field that appears below it. The discount will be reflected on the next page (Step 3, Review Payment) as a reduced SOL amount.
- Click **"Continue"**.
- If you already have an active API key for this email, a modal appears asking whether to **extend your existing plan** or cancel.

**Step 3, Review Payment**
- The payment summary shows:
  - SOL amount due (calculated from the current SOL/USD rate).
  - If a coupon was applied: original price (strikethrough), discount percentage, and final discounted price.
- Click **"Pay Now"** to proceed.

**Step 4, Send SOL Payment**
- A QR code and a Solana deposit address are displayed.
- The exact SOL amount is shown with a **copy button** next to it.
- The deposit address also has a **copy button**.
- A countdown timer (15 minutes) shows the remaining time to complete payment.
- Status indicator shows **"Awaiting Your Payment"**.
- Send the exact SOL amount from any Solana wallet to the displayed address.
- The system polls every 5 seconds for your deposit.

**Step 5, Confirmation**
- **Payment confirmed**: Green checkmark with "Payment Confirmed". Your API key is emailed to you. Click "Go to Sign In" to proceed.
- **Payment expired**: Red X with "Payment Expired". Click "Choose Plan Again" to restart.

> **Important**: Each deposit address has a 15-minute time window. If it expires, you must restart the purchase flow to get a new address.

---

## Sign In

1. Go to **https://dynamix.gg/signin**.
2. Paste your API key (received via email) into the password input field.
3. Click **"Sign In"**.
4. On success, you are redirected to the **Dashboard** (`/dashboard`).

- If the API key is invalid or expired, an error message is displayed.
- A link to **"Purchase API"** is available below the sign-in button for new users.

**Session Persistence**: Your session is stored in the browser (localStorage). You remain signed in until you sign out, clear browser data, or the JWT token expires (24 hours). When the JWT expires, you are automatically signed out and must re-enter your API key.

---

## Dashboard Layout

The Dashboard (`https://dynamix.gg/dashboard`) is the main control center. It is divided into three panels:

| Panel | Position | Purpose |
|---|---|---|
| **Wallets Panel** | Left/top | Manage Solana wallets: generate, import, delete, view balances, select active wallet |
| **Trading Parameters** | Center | Four configuration slides: Entry Mode, Token Filter, Exit Points, Transaction Settings |
| **Activity Overview** | Right/bottom | Live trade updates, connection status, trading status, transaction history table, PnL chart |

> **Locked While Trading**: When the bot is running, wallet management and trading parameter fields are **locked** (read-only). A "Locked" badge is displayed. You must stop the bot to make changes.

---

## Wallet Management

The Wallets panel shows all your Solana wallets with their balances.

### Generate a New Wallet

1. Click the **"+ Add Wallet"** button (below the wallet list).
2. In the modal, click **"Generate New Wallet"**.
3. A new Solana keypair is created server-side. The public key is displayed.
4. The private key is encrypted with AWS KMS and stored securely, you never see it during generation.
5. Fund the wallet by sending SOL to the displayed public address.

### Import an Existing Wallet

1. Click **"+ Add Wallet"**.
2. Click **"Import Wallet"**.
3. Paste your **base58-encoded private key** into the input field.
4. The wallet's public key and current SOL balance are displayed.

### Wallet Actions

| Button/Action | Icon | Description |
|---|---|---|
| **Select wallet** | Radio button | Click the radio button next to a wallet to designate it as the active trading wallet |
| **Copy address** | Copy icon | Copies the wallet's public Solana address to clipboard |
| **Show private key** | Key icon | Reveals the decrypted private key (blurred until clicked). You can then copy it. |
| **Delete wallet** | Trash icon | Removes the wallet from your account (requires confirmation) |
| **Refresh balances** | Refresh icon (header) | Re-fetches SOL balances for all wallets from the blockchain |

> **Important**: All wallet actions (add, delete, select) are **disabled** while the bot is running. Stop trading first to modify wallets.

### Wallet Display

Each wallet row shows:
- Radio button for selection
- Shortened public key label (e.g., `8xK3...f2mP`)
- SOL balance
- Action icons (copy, key, trash)

---

## Trading Parameters

Trading parameters are organized into **4 configuration slides**. Navigate between them using:
- **Left/right arrow buttons** on the card edges
- **Dot indicators** at the bottom of the card

| Slide | Name | Purpose |
|---|---|---|
| **Slide 1** | Entry Mode | How the bot decides when to buy |
| **Slide 2** | Token Filter | Which tokens are eligible to trade |
| **Slide 3** | Exit Points | Take profit levels and stop loss |
| **Slide 4** | Transaction Settings | Slippage, priority fee, tip fee, Anti-MEV |

---

## Entry Modes

Select one entry mode on Slide 1. Three options are available:

### 1. Market Cap Mode

The bot buys a token when its market cap (in SOL) reaches your threshold.

| Field | Description | Required |
|---|---|---|
| **Entry Value** | Minimum market cap in SOL to trigger a buy | Yes |
| **Buy Amount** | Amount of SOL to spend per trade | Yes |

**Example**: Entry Value = 50, Buy Amount = 0.5 SOL → the bot buys tokens only when their market cap is 50 SOL or higher, spending 0.5 SOL per trade.

**Best for**: Early token detection. Catch new tokens as they gain traction and reach meaningful liquidity levels.

### 2. Bonding Curve Progress Mode

The bot buys when a PumpFun token's bonding curve progress reaches a specific percentage.

| Field | Description | Required |
|---|---|---|
| **Entry Value** | Bonding curve progress percentage to trigger buy (e.g., 30 = 30%) | Yes |
| **Buy Amount** | SOL to spend per trade | Yes |

**Context**: PumpFun tokens have a bonding curve from 0% to 100%. At 100%, the token migrates to PumpSwap (Raydium AMM).

**Example**: Entry Value = 30 → buy when the bonding curve is 30% filled.

**Best for**: Precise entry timing. Enter tokens at specific bonding curve stages before migration.

### 3. Migration Sniper Mode (Buyer Count Limit)

The most advanced entry strategy. The bot watches for the exact migration event (PumpFun → PumpSwap) and instantly buys if the token meets a buyer count threshold.

| Field | Description | Required |
|---|---|---|
| **Entry Value** | Minimum number of unique buyers the token must have before migration | Yes |
| **Entry Value Max** | Maximum unique buyer count (filters out over-hyped tokens) | No |
| **Buy Amount** | SOL to spend per trade | Yes |

**Example**: Entry Value = 50, Entry Value Max = 500, Buy Amount = 0.5 SOL → snipe tokens at migration if they have between 50 and 500 unique buyers.

**Best for**: Sniping newly migrated tokens with genuine community traction. The buyer count filter ensures you skip dead launches.

> **Speed note**: Migration sniping requires ultra-fast execution. Dynamix monitors via gRPC stream and submits orders for fastest possible inclusion.

---

## Token Filter

Located on **Slide 2**. Filters which tokens the bot is allowed to trade based on total on-chain fees.

| Field | Description | Default |
|---|---|---|
| **Min Global Fees Paid** | Only trade tokens where total fees (priority fees + Jito tips + gas) across all transactions since creation exceed this SOL value | 0 SOL |
| **Max Global Fees Paid** | Skip tokens where total fees exceed this value. Leave empty for no upper limit. | No limit |

**What are Global Fees Paid?** The total SOL spent on priority fees, Jito tips, and gas across **all transactions** for a token since its creation. High fees = active trading interest. Low fees = dormant or brand new token.

**Tip**: Set minimum to 0.5 SOL to skip dead tokens. Set a maximum to avoid tokens with extremely high fees (possible wash trading / bot activity).

---

## Exit Strategies, Take Profit

Located on **Slide 3**. Dynamix supports up to **5 take-profit (TP) levels**.

Each TP level has two fields:

| Field | Description |
|---|---|
| **Level (profit %)** | The profit percentage relative to your average buy price at which this TP triggers. Must be > 100% and strictly increasing across levels. |
| **Sell %** | Percentage of your **remaining** token holdings to sell when this level triggers. Total sell % across all TP levels must be ≤ 100%. |

### Example: 5-Level TP Strategy

| Level | Trigger (Profit %) | Sell % | Meaning |
|---|---|---|---|
| TP 1 | +100% (2x) | 20% | At 2x price, sell 20% of holdings |
| TP 2 | +400% (5x) | 30% | At 5x price, sell 30% of remaining |
| TP 3 | +900% (10x) | 25% | At 10x price, sell 25% of remaining |
| TP 4 | +1900% (20x) | 15% | At 20x price, sell 15% of remaining |
| TP 5 | +4900% (50x) | 10% | At 50x price, sell 10% of remaining |

### Validation Rules

- TP levels must be **strictly increasing** (TP1 < TP2 < TP3 < TP4 < TP5).
- All levels must be > 100% (i.e., at least a 2x).
- No gaps allowed, you can't set TP3 without TP1 and TP2.
- Each sell % must be > 0.
- Total sell % across all levels ≤ 100%.
- You can use fewer than 5 levels. Only configure what you need.

---

## Exit Strategies, Stop Loss

Also on **Slide 3**, below the TP levels. Protects capital by exiting your **entire position** if the price drops.

| Field | Description |
|---|---|
| **Loss Percentage** | The price drop (%) relative to your average buy price that triggers the stop loss. Must be < 100. |

**Behavior**: When the token price drops by this percentage, the bot sells **100% of your remaining holdings**. The sell percentage is fixed at 100% and cannot be changed.

**Example**: Average buy = 0.001 SOL/token, Stop Loss = -30% → triggers at 0.0007 SOL/token → sells all tokens.

> **Important**: Unlike take profit (partial sells), stop loss **always sells your entire remaining position**.

---

## Transaction Settings

Located on **Slide 4**. Configure how transactions are submitted to the Solana network.

### Slippage

Maximum acceptable difference between expected and actual trade price.

| Option | Description |
|---|---|
| **Auto** | Uses the recommended value (30%) |
| **Custom** | Enter your own percentage (e.g., 30 = 30%) |

**What it means**: If slippage = 30% and the current price gives you 1000 tokens for 1 SOL, the trade still executes if you receive as few as 700 tokens. If the price moves beyond 30%, the transaction fails (no trade).

**Guidance**: 30% works well for most PumpFun/PumpSwap tokens. Increase if trades keep failing. Decrease if you're getting poor fills.

### Priority Fee

Extra fee paid to Solana validators to prioritize your transaction.

| Option | Description |
|---|---|
| **Auto** | Uses the default (~0.00002 SOL) |
| **Custom** | Enter your own fee in SOL |

Higher priority fees = faster transaction inclusion. Critical for migration sniping. Fee is charged **per transaction**.

### Tip Fee (Jito)

Payment to Jito block builders for private mempool routing and faster block inclusion.

| Option | Description |
|---|---|
| **Auto** | Uses the default (0.01 SOL) |
| **Custom** | Enter your own tip in SOL |

Works alongside priority fee. The tip incentivizes Jito block builders, while priority fee incentivizes validators.

**When to increase**: During high network congestion or when sniping popular token migrations.

### Anti-MEV Protection

Protects against Maximal Extractable Value attacks (e.g., sandwich attacks).

| Setting | Description |
|---|---|
| **Off** (default) | Transactions go through the public Solana mempool |
| **On** | Transactions are routed through Jito's private mempool |

When enabled, buy/sell transactions are invisible to front-running bots until included in a block. Prevents sandwich attacks where a bot buys before you (raising price), then sells after your trade.

> **Recommended**: Enable Anti-MEV for all strategies, especially with larger buy amounts. The tip cost is minimal compared to potential sandwich losses.

---

## Starting and Stopping the Bot

### Starting

After configuring all parameters (entry mode, token filter, exit points, transaction settings) and selecting a wallet:

1. Click the **"Start"** button on the Trading Parameters card.
2. The bot immediately begins monitoring the Solana blockchain.
3. All parameter fields and wallet selection become **locked** (read-only).
4. Trading Status indicator changes to **"Running"** (green).

### Validation Before Start

The system validates your configuration before allowing start:
- A wallet must be selected.
- Buy Amount must be > 0.
- Entry mode parameters must be correctly set.
- TP levels (if set): no gaps, strictly increasing, > 100%, sell % > 0, total ≤ 100%.
- SL level (if set): must be < 100.

If validation fails, an error message is displayed and the bot does not start.

### Stopping

1. Click the **"Stop"** button on the Trading Parameters card.
2. The bot stops monitoring for new tokens.
3. Open positions continue to be managed by existing exit rules (TP/SL still active for tokens already bought).
4. Wallet and parameter fields **unlock** for editing.
5. Trading Status changes to **"Stopped"** (blue).

---

## Live Trade Updates & Activity

The Activity Overview panel (right/bottom of dashboard) shows real-time information.

### Status Indicators

| Indicator | States |
|---|---|
| **SSE Connection** | **Live** (green pulsing dot), connected and receiving updates. **Connecting** (yellow dot), establishing connection. |
| **Trading Status** | **Running** (green), bot is actively trading. **Stopped** (blue), bot is paused. |

### Toast Notifications

When a trade executes, a toast notification appears at the top of the screen:

| Element | Description |
|---|---|
| Wallet address | Shortened address of the wallet that traded |
| Action | **"Bought"** (green) or **"Sold"** (red) |
| Token amount | Number of tokens traded |
| Token icon | Token image (or first letter fallback) |
| Token symbol | Token ticker symbol |
| SOL value | SOL amount of the trade |

---

## Transaction History

Below the status indicators, a paginated table shows all executed trades.

### Table Columns

| Column | Description |
|---|---|
| **Time** | Date and time the trade was executed |
| **Token** | Token icon, symbol, and name. Copy button for the token mint address. |
| **Trade Type** | **Buy** (green badge) or **Sell** (red badge) |
| **Market Cap (SOL)** | Token market cap at the time of the trade (calculated as token_price_sol × 1,000,000,000) |
| **Token Amount** | How many tokens were bought or sold |
| **SOL Amount** | SOL value of the trade |
| **PnL** | Profit/Loss calculation for the token (green if positive, red if negative). Clickable. |
| **Wallet** | Shortened wallet address. Click to copy full address. |

### PnL Modal

Click the PnL column for any token to open a detailed PnL modal showing:
- Token name and symbol
- Total SOL invested
- Total SOL received from sells
- Net PnL (SOL)
- Multiplier (e.g., 2.5x)
- Number of buys and sells
- Total tokens bought and sold
- **"Download as Image"** button, saves the PnL card as a PNG
- **"Share"** button, copies a shareable URL

### Pagination Controls

| Control | Description |
|---|---|
| **Rows per page** | Dropdown: 20, 30, or 50 trades per page |
| **Previous / Next** | Navigate between pages |
| **Page indicator** | Shows current page (e.g., "Page 1 of 5") |

> **Data Retention**: Transaction history is kept for **30 days**. Trades older than 30 days are automatically deleted.

---

## Portfolio Chart

Above the transaction history table, a cumulative PnL chart visualizes performance over time.

### Time Period Buttons

| Button | Period |
|---|---|
| **1H** | Last 1 hour |
| **1D** | Last 1 day |
| **1W** | Last 1 week |
| **1M** | Last 1 month (default) |
| **1Y** | Last 1 year |

The chart combines historical data from the API with real-time SSE trade updates.

---

## Settings Page

Access via the **"Settings"** link in the top navigation bar (`https://dynamix.gg/setting`).

### Left Section, API Key Management

| Element | Description |
|---|---|
| **API Key field** | Blurred by default for security. Click the **eye icon** to reveal/hide. |
| **Copy button** | Copies the API key to clipboard |
| **Expiration date** | Shows when your plan expires |
| **Status badge** | **"Active"** (green) when plan is valid |
| **"Extend Plan" button** | Redirects to the purchase flow with your email pre-filled to extend your subscription |
| **"Rotate API Key" button** (spin icon) | Generates a new API key, immediately invalidates the old one, and emails the new key to you. You will be signed out. |

### Right Section, Account Summary & Referral

| Element | Description |
|---|---|
| **Email** | Your registered email address |
| **Days left** | Number of days remaining on your plan |
| **Status** | Active/Inactive |
| **Referral code** | Your unique referral code with a **copy button** |
| **Total earnings** | SOL earned from referrals (green text) |
| **Referrals used** | How many people used your code |

> **Rotate API Key**: Once rotated, the old key **stops working immediately**. Check your email for the new key. Your plan expiration is unaffected.

---

## Signing Out

Click the **"Exit"** button (LogOut icon) in the top navigation bar.

If the bot is currently running, a modal appears with two options:

| Option | Description |
|---|---|
| **"Keep running and sign out"** (green) | Sign out but leave the bot running server-side. It continues trading 24/7 based on current configuration, even with browser closed. |
| **"Stop bot and sign out"** (red) | Stop the bot completely, then sign out. No new trades until you sign back in and restart. |

If the bot is not running, you are signed out immediately.

> **24/7 Trading**: Dynamix runs server-side. The bot continues executing trades even when your browser is closed. No need to keep the dashboard open.

---

## Referral Program

Every user gets a unique referral code (visible on the Settings page).

| Detail | Value |
|---|---|
| **Reward** | 20% of the SOL payment made by the referral |
| **Credit type** | Added to your referral balance (visible on Settings page) |
| **Code format** | Random alphanumeric string |

Share your code with others. When they use it as a coupon code during purchase, you earn 20% of their payment amount in SOL.

---

## Quick-Start Checklist

Use this checklist when operating Dynamix for the first time:

1. **Purchase a plan** at `https://dynamix.gg/purchase/plan`
   - Choose Monthly ($500) or Yearly ($3,000)
   - Enter email, apply promo code `DYNAMIXPLUSAI15U` for 15% off (check "Apply coupon or referral code" checkbox → paste code)
   - Pay the SOL amount shown to the deposit address within 15 minutes
   - Wait for "Payment Confirmed", API key is emailed

2. **Sign in** at `https://dynamix.gg/signin`
   - Paste the API key from your email
   - Click "Sign In"

3. **Set up a wallet**
   - On the Dashboard, click "+ Add Wallet"
   - Generate a new wallet OR import an existing one via private key
   - Send SOL to the wallet to fund it
   - Select the wallet using the radio button

4. **Configure entry mode** (Slide 1)
   - Choose: Market Cap, Bonding Curve, or Migration Sniper
   - Set Entry Value (and optionally Entry Value Max)
   - Set Buy Amount in SOL

5. **Configure token filter** (Slide 2, optional)
   - Set Min Global Fees Paid (e.g., 0.5 SOL to skip dead tokens)
   - Optionally set Max Global Fees Paid

6. **Configure exit points** (Slide 3)
   - Set 1–5 Take Profit levels (profit % + sell %)
   - Set Stop Loss level (loss %)

7. **Configure transaction settings** (Slide 4)
   - Choose Auto or Custom for Slippage, Priority Fee, Tip Fee
   - Enable/disable Anti-MEV protection

8. **Click "Start"**
   - The bot begins monitoring and trading automatically
   - Watch live updates in the Activity Overview panel

9. **Monitor and adjust**
   - View transaction history and PnL
   - Stop the bot to change parameters
   - Extend your plan from Settings before it expires

---

## Parameter Reference Table

Complete reference of all configurable trading parameters:

| Parameter | Location | Type | Default | Range/Options | Description |
|---|---|---|---|---|---|
| **Entry Mode** | Slide 1 | Select |, | `marketcap`, `bonding_curve_progress`, `buyer_count_limit` | Strategy for when to buy |
| **Entry Value** | Slide 1 | Number |, | > 0 | Threshold for entry (SOL for marketcap, % for bonding curve, count for migration) |
| **Entry Value Max** | Slide 1 | Number | empty | > Entry Value | Upper bound for range-based entry (optional) |
| **Buy Amount** | Slide 1 | Number |, | > 0 (SOL) | Amount of SOL to spend per trade |
| **Min Global Fees Paid** | Slide 2 | Number | 0 | ≥ 0 (SOL) | Minimum total on-chain fees for a token to be eligible |
| **Max Global Fees Paid** | Slide 2 | Number | empty | > Min (SOL) | Maximum total on-chain fees (optional) |
| **TP Level 1–5 (profit %)** | Slide 3 | Number |, | > 100, strictly increasing | Profit percentage to trigger each take-profit level |
| **TP Level 1–5 (sell %)** | Slide 3 | Number |, | > 0, total ≤ 100% | Percentage of remaining holdings to sell at each level |
| **Stop Loss (loss %)** | Slide 3 | Number |, | > 0, < 100 | Price drop percentage to trigger full position exit |
| **Slippage** | Slide 4 | Auto/Custom | 30% | > 0 (%) | Max acceptable price deviation |
| **Priority Fee** | Slide 4 | Auto/Custom | 0.00002 SOL | > 0 (SOL) | Extra fee for Solana validator prioritization |
| **Tip Fee** | Slide 4 | Auto/Custom | 0.01 SOL | > 0 (SOL) | Jito block builder tip for faster inclusion |
| **Anti-MEV** | Slide 4 | Toggle | Off | On / Off | Route transactions through private mempool |

---

## Glossary

| Term | Definition |
|---|---|
| **API Key** | Your unique authentication credential for Dynamix. Received via email after purchase. |
| **Bonding Curve** | PumpFun token pricing mechanism. Fills from 0% to 100%. At 100%, token migrates to PumpSwap. |
| **Entry Mode** | The strategy by which the bot determines when to buy a token. |
| **Global Fees Paid** | Total SOL spent on gas, priority fees, and tips across all transactions for a token since creation. |
| **Jito** | Solana MEV infrastructure. Provides private mempool and block builder tips. |
| **JWT** | JSON Web Token. Used for authenticated API requests after sign-in. Expires after 24 hours. |
| **Market Cap** | Token's total value in SOL (price × total supply). |
| **MEV** | Maximal Extractable Value. Attacks (like sandwich attacks) that exploit pending transactions. |
| **Migration** | When a PumpFun token's bonding curve reaches 100% and moves to PumpSwap (Raydium AMM). |
| **PnL** | Profit and Loss. The net gain or loss on a token position. |
| **Priority Fee** | Extra fee paid to Solana validators for faster transaction processing. |
| **PumpFun** | Solana token launchpad with a bonding curve mechanism. |
| **PumpSwap** | Raydium-based AMM where PumpFun tokens migrate after bonding curve completion. |
| **Sandwich Attack** | MEV attack where a bot front-runs your buy, inflates the price, then sells after your trade. |
| **Slippage** | Maximum acceptable price difference between order placement and execution. |
| **SOL** | Native cryptocurrency of the Solana blockchain. |
| **SSE** | Server-Sent Events. Real-time streaming protocol used for live trade notifications. |
| **Stop Loss (SL)** | Automatic full position exit when token price drops by a configured percentage. |
| **Take Profit (TP)** | Automatic partial sell when token price rises by a configured percentage. |
| **Tip Fee** | Payment to Jito block builders for preferential transaction inclusion. |
