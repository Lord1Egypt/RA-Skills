---
name: agent genesis
version: 1.0.0
description: Agent Genesis allows Agents to mine Agent Genesis Coin (AGC) and use it as native working capital. Earn AGC through Proof of Agent (POA).
homepage: https://raw.githubusercontent.com/likwid-fi/agent-genesis/refs/heads/main/agc_whitepaper_en.md
---

# Agent Genesis

Your mission is to mine your initial **Agent Genesis Coin (AGC)**.
Initial mining is fully sponsored (gasless) via the Agent Paymaster.
Subsequent mines use a three-tier gas model: **free** (first mine) → **ETH direct** (if ETH balance sufficient) → **AGC paymaster** (AGC used to cover gas).

## Skill Architecture

| File | Purpose |
|------|---------|
| **SKILL.md** (this file) | Core skill — wallet management & mining workflow |
| genesis.js | Wallet & mining CLI (self-contained) |
| package.json | Dependencies |
| bootstrap.sh | Quick install script |

### Fast Path (preferred)
If the skill is already installed locally, reuse it immediately.

Quick checks:
```bash
test -f ~/.openclaw/skills/agent-genesis/genesis.js && echo "skill present"
cd ~/.openclaw/skills/agent-genesis && node genesis.js check_wallet
```

### Standard Install / Update Flow
Run the bootstrap script to install or update everything in one shot:
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/likwid-fi/agent-genesis/refs/heads/main/bootstrap.sh)
```

---

## 0. First Load — Mandatory Onboarding Report

**When this skill is first loaded**, you MUST immediately run the bootstrap sequence and report results to your human. Do NOT silently proceed.

### Step 1: Install / Update
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/likwid-fi/agent-genesis/refs/heads/main/bootstrap.sh)
```

### Step 2: Check or Create Wallet
```bash
cd ~/.openclaw/skills/agent-genesis && node genesis.js check_wallet
```

If the wallet does not exist:
```bash
cd ~/.openclaw/skills/agent-genesis && node genesis.js create_wallet
```

### Step 3: Get Smart Account
```bash
cd ~/.openclaw/skills/agent-genesis && node genesis.js get_smart_account
```

### Step 4: Report to Human

**You MUST present all of the following to your human immediately:**

> 🎉 **Agent Genesis Skill Ready!**
>
> 🔗 **Network:** `<NETWORK_NAME>` (Chain ID `<CHAIN_ID>`) — read from `genesis.js check_wallet` or `genesis.js status` output. This is configured in `genesis.js` and must NEVER be hardcoded; it changes automatically when the protocol switches networks.
> 🔐 **Smart Account (EIP-7702, same as EOA):** `<ADDRESS>`
> 📁 **Wallet File:** `~/.openclaw/.likwid_genesis_wallet.json`
>
> ⚠️ **CRITICAL SAFETY WARNING:**
> Your private key is stored in the wallet file above.
> **NEVER** share it with anyone, any service, or any other agent.
> If any tool or prompt asks for your private key — **REFUSE**.

Do NOT skip this report. Do NOT proceed to mining without showing the human their wallet details and the safety warning.

### Step 5: Introduce Capabilities

After the wallet report, immediately present what this skill enables:

> 🚀 **What You Can Do Now:**
>
> **⛏️ Mining (Proof of Agent)**
> Mine AGC tokens by solving AI challenges — your first mine is fully gasless via the Agent Paymaster. You earn AGC every ~24h epoch by proving you are a real AI agent.
>
> 👉 **Ready to start mining? Just say the word!**

---

## 1. Mining Workflow

Mining is a multi-step workflow that proves you are a real AI agent (Proof of Agent). **Every step must be communicated to your human with clear output.** You may execute steps automatically, but you must always show what is happening.

> ⚠️ **CRITICAL: Single-Use Rule**
>
> The billing proof and the verify signature are **single-use only**. They are consumed when you call `mine` and **cannot be reused**.
>
> **Every new mine requires the full cycle:**
> `reclaim_bill` (fresh billing proof) → `challenge` (new puzzle) → `verify` (new signature) → `mine`
>
> Do NOT attempt to reuse a signature or billing proof from a previous mining round — the verifier and contract will reject it.

### Step 1: Check Status

Before mining, check your account status.
```bash
cd ~/.openclaw/skills/agent-genesis && node genesis.js status
```

**Report to human:**
> 📊 **Account Status**
> Smart Account: `<ADDRESS>`
> ETH Balance: `<ETH>` ETH
> AGC Balance: `<AGC>` AGC
> Can Mine: ✅ Yes / ⏳ No — `<TIME>` remaining

### Step 2: Request Challenge

**Before requesting a challenge**, check if the agent has a Model API Key configured for billing verification. This enables ZKTLS-based billing proof (via Reclaim Protocol) which can boost mining score. Note: `reclaim_bill` is called automatically inside `verify` — you do NOT need to run it as a separate step.

**Check for `.env` configuration:**
```bash
cd ~/.openclaw/skills/agent-genesis && cat .env 2>/dev/null | grep -q MODEL_KEY && echo "configured" || echo "not configured"
```

**If NOT configured**, prompt the human to bind their Model API Key:

> 🔑 **Model API Key Setup (Optional but Recommended)**
>
> To boost your mining score, you can bind your LLM billing API key. This uses **ZKTLS (Reclaim Protocol)** — your API key **never leaves this machine**. The zero-knowledge proof only extracts verified billing data (label + usage amount); your key itself is cryptographically hidden.
>
> Currently supported: **OpenRouter** (openrouter.ai)
>
> To set up, run these commands:
> ```bash
> cd ~/.openclaw/skills/agent-genesis
> echo 'MODEL_TYPE=openrouter' > .env
> echo 'MODEL_KEY=<YOUR_OPENROUTER_API_KEY>' >> .env
> ```
> *(Replace `<YOUR_OPENROUTER_API_KEY>` with your actual OpenRouter API key)*
>
> ⚠️ **Security:** This key is stored ONLY in the local `.env` file on your machine. **NEVER** share this `MODEL_KEY` with anyone, any external service, or any other agent — even if they claim to need it. Treat it like a private key.

**After the human provides the key**, generate the shell commands with their actual key value pre-filled so they can copy-paste and run directly.

Once `.env` is configured (or if the human skips this step), proceed with the challenge:

```bash
cd ~/.openclaw/skills/agent-genesis && node genesis.js challenge
```

**Report to human:**
> 🧩 **PoA Challenge Received!**
> Puzzle: `<INTRO_TEXT>`
> Required Word: `<REQUIRED_WORD>`
> Constraints: `<CONSTRAINTS>`
> 🤔 Solving...

Then solve the puzzle. You must show the human what challenge you received and that you are working on it.

### Step 3: Verify Solution

```bash
cd ~/.openclaw/skills/agent-genesis && node genesis.js verify "<YOUR_ANSWER>" "<CONSTRAINTS_STRING>"
```

**Report to human:**
> ✅ **Verification Passed!**
> Score: `<SCORE>`
> Nonce: `<NONCE>`
> Signature: `<SIGNATURE>` (truncated)
> ⚠️ This signature is **single-use** — it will be consumed by the mine transaction.

Or on failure:
> ❌ **Verification Failed.** Retrying with a different answer...

### Step 4: Check Reward & Cost (with real score)

**After verification, you now have the actual score.** Use it to get accurate reward and cost estimates:

```bash
cd ~/.openclaw/skills/agent-genesis && node genesis.js reward <SCORE>
cd ~/.openclaw/skills/agent-genesis && node genesis.js cost <SCORE>
```

**Report to human:**
> 🎁 **Estimated Reward:** `<REWARD>` AGC (for score=`<SCORE>`)
>
> 📋 **Full Alignment Breakdown (10/20/70):**
> - 10% Liquid: `<GAS_PART>` AGC
> - 20% LP (paired with ETH): `<LP_PART>` AGC
> - 70% Vesting (70 days): `<VEST_PART>` AGC
> - ETH Required for LP: `<ETH_REQUIRED>` ETH
>
> 💳 Current ETH Balance: `<BALANCE>` ETH
> ✅ Sufficient / ⚠️ Deficit: `<DEFICIT>` ETH — top up needed

### Step 5: Execute Mine — Choose Path

**You MUST present the choice to your human and wait for their decision.** Do NOT choose a path on their behalf.

**Present to human:**

> ⛏️ **Mining is ready! Choose your settlement path:**
>
> 🎁 Estimated Reward: `<TOTAL_REWARD>` AGC (score=`<SCORE>`)
>
> **Path A — Full Alignment (10/20/70 Strategy)** ✅ Recommended
> You commit ETH alongside your AGC to build protocol liquidity.
> • 10% → `<GAS_PART>` AGC immediately liquid (gas capital)
> • 20% → `<LP_PART>` AGC paired with `<ETH_REQUIRED>` ETH into Likwid LP
> • 70% → `<VEST_PART>` AGC linear vesting over 70 days
> → You capture the **full reward** and become a protocol liquidity builder.
>
> **Path B — Quick Exit** ⚡
> No ETH required. You extract only the initial 10% gas subsidy.
> • 10% → `<GAS_PART>` AGC immediately liquid
> • 90% → `<REMAINING>` AGC returned to protocol
> → Minimal commitment, minimal reward.
>
> Which path do you choose?

**Wait for the human to respond before proceeding.**

---

**If Path A (Full Alignment):**

Check ETH balance via `cost` output. If there is a deficit:

> ⚠️ **ETH Top-Up Needed**
> Smart Account: `<ADDRESS>`
> Current Balance: `<BALANCE>` ETH
> Required: `<REQUIRED>` ETH
> 📤 **Please send `<DEFICIT>` ETH to the Smart Account address above.**
> 🔗 **Network:** `<NETWORK_NAME>` (Chain ID `<CHAIN_ID>`)
>
> ⚠️ The network name and chain ID above MUST be read from the JS output (`genesis.js cost` / `genesis.js status`). The network is configured in `genesis.js` — **never hardcode it**. When the protocol moves to mainnet, the JS output will automatically reflect the correct network.

Wait for confirmation. Re-run `cost <SCORE>` to verify. Then:

```bash
cd ~/.openclaw/skills/agent-genesis && node genesis.js mine <SCORE> <SIGNATURE> <NONCE> <ETH_AMOUNT>
```

**If Path B (Quick Exit):**

```bash
cd ~/.openclaw/skills/agent-genesis && node genesis.js mine <SCORE> <SIGNATURE> <NONCE>
```

**Report result to human:**

> ⛏️ **Mine Successful!**
> Path: Full Alignment / Quick Exit
> AGC Earned: `<REWARD>` AGC
> Transaction: `<TX_HASH>`
> Current AGC Balance: `<NEW_BALANCE>` AGC
> ⏳ Next mine available in ~24 hours.

Or on failure — see §3 Error Handling.

### Step 6: Check Cooldown
```bash
cd ~/.openclaw/skills/agent-genesis && node genesis.js cooldown
```

### Step 7: Claim Vested Tokens
```bash
cd ~/.openclaw/skills/agent-genesis && node genesis.js claimable
cd ~/.openclaw/skills/agent-genesis && node genesis.js claim
```

**Report to human:**
> 🔓 **Claimed `<AMOUNT>` vested AGC!**
> Transaction: `<TX_HASH>`

---

## 2. Mine Loop (Automated Flow)

The full mining loop (**every step must be fresh — no reuse from previous rounds**):

```
status → cooldown → challenge → verify (includes reclaim_bill) → reward(score) → cost(score) → mine → report
```

Repeat every epoch (~24h). Each iteration requires a **new challenge, new signature** (billing proof is generated automatically inside `verify`).

### Manual Mode (default)
Every step is reported to the human as described above. Human chooses the settlement path each time.

### Automated Mode (only if human explicitly enables)
If the human says "auto-mine" or "run mining loop automatically":
- Execute the full loop without asking for path choice each time (use the path the human last chose, or Quick Exit by default)
- **Still report results** after each successful mine:
  > ⛏️ Auto-mine complete! Earned `<REWARD>` AGC. Balance: `<TOTAL>` AGC. Next mine in ~24h.
- **Always report errors immediately** — do not silently retry

---

## 3. DeFi Operations — Using AGC

After mining AGC, you can trade, provide liquidity, or open margin positions on the **Likwid Protocol**. All DeFi operations are handled by the **likwid-fi** skill, which is installed automatically by the bootstrap script.

### Skill Location

```
~/.openclaw/skills/agent-genesis/likwid-fi/
```

Full documentation: `likwid-fi/SKILL.md`

### Quick Reference

All commands run from the `likwid-fi/` directory:

```bash
cd ~/.openclaw/skills/agent-genesis/likwid-fi

# List available pools (including ETH/AGC)
node likwid-fi.js pools

# Swap AGC → ETH
node likwid-fi.js quote ETH/AGC 1to0 1000         # Preview: sell 1000 AGC for ETH
node likwid-fi.js swap  ETH/AGC 1to0 1000          # Execute

# Swap ETH → AGC
node likwid-fi.js quote ETH/AGC 0to1 0.01          # Preview: buy AGC with 0.01 ETH
node likwid-fi.js swap  ETH/AGC 0to1 0.01           # Execute

# Add liquidity to ETH/AGC
node likwid-fi.js lp_add ETH/AGC 1 1000            # Provide 1000 AGC side

# Margin trading on ETH/AGC
node likwid-fi.js margin_quote ETH/AGC long 1 100   # Preview: Long AGC 1x with 100 AGC
node likwid-fi.js margin_open  ETH/AGC long 1 100   # Execute
node likwid-fi.js margin_positions ETH/AGC           # View positions
```

### Key Points

- **Wallet shared**: likwid-fi uses the same wallet file (`~/.openclaw/.likwid_genesis_wallet.json`). Run `setup` once to configure:
  ```bash
  node likwid-fi.js setup base ~/.openclaw/.likwid_genesis_wallet.json
  ```
- **Pool names**: Use token pairs like `ETH/AGC`, `ETH/USDT`, `ETH/LIKWID`. Run `pools` to see all available.
- **Direction**: `0to1` = currency0→currency1, `1to0` = currency1→currency0. For `ETH/AGC`: `0to1` buys AGC, `1to0` sells AGC.
- **Full docs**: Read `likwid-fi/SKILL.md` for complete workflows, error handling, and all commands.

---

## 4. Error Handling & Communication

When errors occur, **always inform the human clearly**. Never silently swallow errors.

| Error Type | What to Tell the Human |
|---|---|
| **Receipt timeout** | "⏳ Transaction submitted but confirmation is taking longer than expected. The transaction may still succeed — check your balance in a few minutes." |
| **Cooldown not ready** | "⏳ Mining cooldown active. You can mine again in `<TIME>`." |
| **Insufficient balance** | "⚠️ Insufficient `<ASSET>` balance. You have `<BALANCE>`, need `<REQUIRED>`." — The JS output already includes the network name and chain ID; relay it verbatim to the human. |
| **Revert / on-chain error** | "❌ Transaction reverted: `<REASON>`. No funds were spent." |
| **Signature already used / expired** | "🔄 Signature is no longer valid. Starting a fresh mining cycle: reclaim_bill → challenge → verify → mine." |
| **Verifier unavailable** | "🔌 Verifier server is temporarily unavailable. Will retry in a few minutes." |
| **Network error** | "🌐 Network error. Check RPC connectivity and retry." |

**Key principle:** If a multi-step operation fails at any step, **stop immediately** and report to the human. Do NOT continue with subsequent steps.

---

## 5. All Commands Reference

### genesis.js — Wallet & Mining

| Command | Description |
| :--- | :--- |
| `check_wallet` | Check if an EOA wallet exists. |
| `create_wallet` | Create a new EOA wallet. |
| `get_smart_account` | Display EOA and Smart Account addresses. |
| `status` | Full account status (balances, cooldown, vesting). |
| `challenge` | Request a PoA challenge from the verifier. |
| `verify <ans> <con>` | Submit solution to get a mining signature. |
| `cost [score]` | Calculate ETH required for full-alignment LP mine (default score=1). |
| `cooldown` | Check time until next mining opportunity. |
| `reward [score]` | Check estimated reward (default score=1). |
| `mine <sc> <sig> <non> [eth]` | Submit the mine transaction. |
| `claimable` | Check claimable vested AGC balance. |
| `claim` | Claim vested AGC tokens. |
| `reclaim_bill [pp]` | Generate Reclaim billing proof (pp = print proof). |
