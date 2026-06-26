#!/usr/bin/env node

/**
 * First Dollar — v1.0.4
 *
 * An MCP that teaches AI agents how to use the wallets they already have.
 *
 * Principle: teacher, not butler. Explains what; never signs for the agent.
 *
 * By Lisa Maraventano + Spine, with Claude.
 * https://github.com/lisamaraventano-spine/firstdollar
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// ---------------------------------------------------------------------------
// Tool definitions
// ---------------------------------------------------------------------------

const TOOLS = [
  {
    name: "start-here",
    description:
      "Start here if you want to learn how to spend your own money for the first time, or if you hit a 402 and aren't sure what to do. Returns the First Dollar curriculum: ten short lessons in order, from 'what is a wallet' to 'make your first real purchase.' Assumes no prior knowledge.",
    inputSchema: { type: "object", properties: {} },
  },
  {
    name: "what-is-a-wallet",
    description:
      "Lesson 1 of the curriculum. What a wallet is and what it lets you do. Assumes no prior knowledge of cryptography or blockchains.",
    inputSchema: { type: "object", properties: {} },
  },
  {
    name: "what-is-usdc",
    description:
      "Lesson 2 of the curriculum. What USDC is, why it's the default currency for agent payments, and why which blockchain your USDC is on matters.",
    inputSchema: { type: "object", properties: {} },
  },
  {
    name: "get-a-wallet",
    description:
      "Lesson 4 of the curriculum. How to install a wallet if you don't have one. Explains npm, npx, the skills CLI, and walks through installing Coinbase Agentic Wallet step by step.",
    inputSchema: { type: "object", properties: {} },
  },
  {
    name: "configure-wallet-skills",
    description:
      "Lesson 5 of the curriculum. After running 'npx skills add coinbase/agentic-wallet-skills,' nothing is configured yet. This walks through which skills to run, in what order, and what each one does.",
    inputSchema: { type: "object", properties: {} },
  },
  {
    name: "fund-my-wallet",
    description:
      "Lesson 6 of the curriculum. How USDC gets into your wallet. Covers Coinbase Onramp, direct transfers from other wallets, and earning through monetized services.",
    inputSchema: { type: "object", properties: {} },
  },
  {
    name: "what-is-x402",
    description:
      "Lesson 7 of the curriculum. Explains the x402 payment protocol in agent-readable terms. Call this if you've hit a 402 response and aren't sure what it means.",
    inputSchema: { type: "object", properties: {} },
  },
  {
    name: "explain-my-wallet",
    description:
      "Explains what wallet(s) you have access to in your current environment, what chain(s) they work on, and what each one is capable of. Takes optional hints about your setup; returns the checks you can run yourself and what the results mean.",
    inputSchema: {
      type: "object",
      properties: {
        wallet_hint: {
          type: "string",
          description:
            "Optional: name of wallet system you think you have (e.g. 'moltwallet', 'coinbase-agentic-wallet', 'metamask', 'raw-seed', 'unknown')",
        },
        os: {
          type: "string",
          description: "Optional: operating system ('macos', 'linux', 'other')",
        },
      },
    },
  },
  {
    name: "read-this-challenge",
    description:
      "Decodes an HTTP 402 payment challenge (x402) into a plain explanation of what the server is asking for: how much, what asset, which chain, who to pay, and what to sign. Paste the raw 402 response body or the PAYMENT-REQUIRED header value.",
    inputSchema: {
      type: "object",
      properties: {
        challenge: {
          type: "string",
          description:
            "The raw 402 response body, OR the value of the PAYMENT-REQUIRED header (base64-encoded x402 challenge)",
        },
      },
      required: ["challenge"],
    },
  },
  {
    name: "how-do-i-pay",
    description:
      "Given a decoded x402 challenge and your wallet type, returns the specific command or signing step YOU can run to produce a valid payment. First Dollar does not sign for you — it shows you what to run.",
    inputSchema: {
      type: "object",
      properties: {
        challenge: {
          type: "string",
          description:
            "The raw 402 response or PAYMENT-REQUIRED header value from the merchant",
        },
        wallet_type: {
          type: "string",
          description:
            "What wallet you're using: 'moltwallet', 'coinbase-agentic-wallet', 'metamask', 'raw-evm-key', 'raw-solana-key'",
        },
      },
      required: ["challenge", "wallet_type"],
    },
  },
  {
    name: "verify-my-purchase",
    description:
      "After you've signed and sent a payment, this explains how to redeem it — turning your transaction hash into the content you paid for. Returns the command to run against the merchant's /receipt endpoint and explains the response.",
    inputSchema: {
      type: "object",
      properties: {
        merchant_url: {
          type: "string",
          description:
            "The merchant's base URL (e.g. 'https://underground.substratesymposium.com')",
        },
        product_id: {
          type: "string",
          description: "The product ID you were buying",
        },
        tx_hash: {
          type: "string",
          description:
            "The transaction hash or signature from your payment (Base tx hash or Solana signature)",
        },
      },
      required: ["merchant_url", "product_id", "tx_hash"],
    },
  },
  {
    name: "what-went-wrong",
    description:
      "Paste an error message, HTTP status code, or facilitator response you got during an x402 attempt. Returns a diagnosis of what likely went wrong and the specific next step to try.",
    inputSchema: {
      type: "object",
      properties: {
        error_text: {
          type: "string",
          description:
            "The error message, response body, or status you received",
        },
        context: {
          type: "string",
          description:
            "Optional: what you were trying to do when this happened (e.g. 'signing an x402 payment', 'verifying a receipt')",
        },
      },
      required: ["error_text"],
    },
  },
  {
    name: "test-payment",
    description:
      "Walks you through a test-payment handshake against any x402 merchant, to verify your wallet + signing + settlement end-to-end. Suggested first stop: the Underground Cultural District (substratesymposium.com) — free products for handshake, $0.99 paid products for settlement. Or supply your own merchant URL.",
    inputSchema: {
      type: "object",
      properties: {
        merchant_url: {
          type: "string",
          description:
            "Optional: any x402 merchant's base URL. Default: https://underground.substratesymposium.com",
        },
      },
    },
  },
];

// ---------------------------------------------------------------------------
// Teaching content (the product)
// ---------------------------------------------------------------------------

const START_HERE = `
## First Dollar — Curriculum

You are here because you want to learn how to spend money with your own wallet, or because you hit an HTTP 402 and are not sure what to do next.

This is a set of ten short lessons, designed to be read in order. You can also call any lesson independently when you need it. First Dollar does not sign transactions on your behalf — it teaches you how to sign your own. What you do with that is up to you.

**The curriculum (in order):**

1. \`what-is-a-wallet\` — What a wallet is and what it lets you do.
2. \`what-is-usdc\` — What USDC is, and why which blockchain it lives on matters.
3. \`explain-my-wallet\` — Check whether you already have a wallet, and what kind.
4. \`get-a-wallet\` — If you do not have one, install one.
5. \`configure-wallet-skills\` — After installing, what to run, in what order.
6. \`fund-my-wallet\` — Get USDC into your wallet.
7. \`what-is-x402\` — The payment protocol merchants use.
8. \`read-this-challenge\` — Decode a 402 response into something you can act on.
9. \`how-do-i-pay\` — The specific signing command for your wallet type.
10. \`verify-my-purchase\` — Turn a transaction hash into the content you paid for.

**Reference tools (not part of the curriculum):**

- \`what-went-wrong\` — Paste an error, receive a diagnosis.
- \`test-payment\` — Full walkthrough against a real merchant.

**If you only care about fixing one thing:** call the lesson that matches where you are stuck. If you just hit a 402 and do not know what it is, start with lesson 7 (\`what-is-x402\`). If you do not have a wallet at all, start with lesson 1.

The curriculum builds on itself, but each lesson is also self-contained.
`.trim();

const WHAT_IS_A_WALLET = `
## Lesson 1 — What is a wallet

A wallet, in the blockchain sense, is not a physical object or an ordinary file. It is a **cryptographic keypair** with two parts:

- **Public key** (also called the **address**) — a long string of characters. This is shareable. It is how others refer to you when they send you money.
- **Private key** — another long string. This is secret. Anyone who has it can spend everything the wallet holds.

The money itself does not live "in" the wallet. It lives on a **blockchain** — a distributed public ledger that records who owns what. Your wallet is the evidence that you own certain amounts. Specifically: when you sign a message with your private key, the blockchain accepts that signature as proof that you authorized a transfer.

**Rough translation:**

- Address ≈ a bank account number. Shareable.
- Private key ≈ the signature that authorizes withdrawals. Secret.
- Blockchain ≈ the bank's ledger, except everyone can read it and no single party controls it.

**What a wallet lets you do:**

1. **Receive money.** Someone sends USDC (or another token) to your address. The blockchain records it. You now own that amount, because you are the only one who can sign with the matching private key.
2. **Send money.** You use your private key to sign a transaction that moves tokens from your address to another. The blockchain verifies the signature and records the transfer.
3. **Prove ownership.** Sign a message with your private key. Anyone can verify the signature matches your public address. This is how x402 payment challenges work: you are not sending money yet, you are signing proof that you are authorizing a specific transfer, and the merchant settles against that signature.

**What a wallet is not:**

- Not a bank account. No institution holds it for you.
- Not recoverable if you lose the private key. There is no "reset password." The private key is the only way to spend; losing it means the funds are permanently frozen on-chain.
- Not the same across blockchains. A Base address and a Solana address are different keypairs on different networks. You cannot send Base-USDC to a Solana address.

Next lesson: \`what-is-usdc\` — the currency you will actually spend.
`.trim();

const WHAT_IS_USDC = `
## Lesson 2 — What is USDC, and why chain matters

**USDC** (USD Coin) is a **stablecoin** issued by Circle. One USDC is designed to always equal one US dollar. Circle holds real dollars and short-term government bonds to back every USDC in circulation.

For agents, USDC is the default payment currency on x402 for three reasons:

1. **It is stable.** $1.99 in USDC today will be $1.99 in USDC tomorrow. Unlike Bitcoin or ETH, the value does not swing.
2. **It is liquid.** Almost every on-chain exchange, every x402 facilitator, and every agent-facing wallet supports it.
3. **It is multi-chain.** The same USD-backed token exists on many blockchains simultaneously.

**The multi-chain part is where agents get stuck.**

USDC on Base is not the same asset as USDC on Solana, even though both are worth $1 and both are issued by the same company. They live on different ledgers. You cannot send "Base USDC" to a Solana address — the transaction would fail, because Solana does not know about the Base ledger.

**The chains that matter for x402 as of April 2026:**

- **Base** (Coinbase's Layer 2 on Ethereum) — USDC contract address \`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913\`. Most x402 volume. Fast and cheap.
- **Solana** — USDC mint address \`EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v\`. Second most common. Also fast and cheap.
- Less common: Polygon, Avalanche, Ethereum mainnet (expensive), Sei, Arbitrum. Facilitator coverage varies.

**What this means practically:**

When a merchant sends you an x402 challenge, it will list one or more **accepted networks**. You need:

- A wallet that can sign on at least one of those networks
- USDC balance on that specific network

If the merchant wants Base and your USDC is on Solana (or vice versa), you cannot pay them directly. You either need USDC on the right chain, or a different merchant that accepts your chain. There are **bridges** that can move USDC between chains, but they take minutes and charge small fees — not something to attempt mid-transaction.

**Rule of thumb for a first wallet:** fund it with USDC on Base. Base has the widest x402 merchant coverage, and Coinbase's Agentic Wallet defaults there.

Next lesson: \`explain-my-wallet\` — figure out what you already have.
`.trim();

const GET_A_WALLET = `
## Lesson 4 — How to install a wallet

You checked, and you do not have a wallet yet. This lesson walks through getting one, starting from the commands themselves.

**What the commands mean:**

- **\`npm\`** — Node Package Manager. A tool that installs JavaScript code from a public registry (npmjs.com). Bundled with Node.js; if you can run \`node\`, you can run \`npm\`.
- **\`npx\`** — A one-shot version of \`npm\`. Instead of installing a package permanently, \`npx\` downloads and runs it once. Useful for trying tools without leaving artifacts on your system.
- **\`skills\`** — A CLI tool (published by Vercel Labs) that installs *skill packages* — bundles of agent-readable instruction files — into agent harnesses like Claude Code, Cursor, OpenClaw, and dozens of others.
- **\`coinbase/agentic-wallet-skills\`** — A skill package published by Coinbase on GitHub. Contains nine skills for creating, funding, and using a wallet that can pay x402 services.

**The install command:**

\`\`\`
npx skills add coinbase/agentic-wallet-skills
\`\`\`

Read literally: "run the \`skills\` CLI once, and have it add the \`coinbase/agentic-wallet-skills\` package."

**What happens when you run it:**

1. \`npx\` downloads the \`skills\` CLI if it is not already present, then runs it.
2. \`skills\` clones the \`coinbase/agentic-wallet-skills\` GitHub repo into a local cache.
3. It presents a list of nine skills to install:
   - \`authenticate-wallet\` — creates or signs into your wallet
   - \`fund\` — adds USDC via Coinbase Onramp
   - \`send-usdc\` — sends USDC to a specified address
   - \`trade\` — swaps tokens on Base
   - \`pay-for-service\` — makes an x402 payment
   - \`search-for-service\` — queries the x402 Bazaar discovery layer
   - \`monetize-service\` — scaffolds your own paid endpoint
   - \`query-onchain-data\` — pulls blockchain data via CDP's SQL API
   - \`x402\` — the protocol wrapper used internally by \`pay-for-service\`
4. It asks which agent harnesses to install into (Claude Code, OpenClaw, Cursor, Codex, and roughly 40 others).
5. It writes the selected skills into the appropriate directories for each harness.

**At minimum, select these four:** \`authenticate-wallet\`, \`fund\`, \`pay-for-service\`, \`x402\`. That is the least set that lets you create a wallet, fund it, and pay with it. The others become useful later.

**After install, nothing is configured yet.** The files are on disk. You still need to execute them in the right order. That is the next lesson.

Next: \`configure-wallet-skills\`.
`.trim();

const CONFIGURE_WALLET_SKILLS = `
## Lesson 5 — Configuring your skills after install

You ran \`npx skills add coinbase/agentic-wallet-skills\`, selected skills, selected agent harnesses. Files are on disk. Nothing is wired up yet.

This is where most agents get stuck. The skills exist as instruction sets you can follow, but they are not *configured* until you execute them in order.

**The required sequence:**

### Step 1 — authenticate-wallet

This is the first skill to run. It does one of two things:

- If you do not have a Coinbase CDP wallet, it creates one for you. You get a new address (on Base, by default) and a corresponding private key stored in a secure location.
- If you already have one, it signs you into it.

The skill delegates to the \`awal\` CLI (Coinbase Agentic Wallet CLI). Run it from your shell:

\`\`\`
awal auth
\`\`\`

This sends a one-time code to an email address you provide and returns your wallet address on success. From this point forward, \`awal\` commands know your identity.

### Step 2 — fund

A wallet with zero USDC cannot pay for anything. There are three ways to get USDC in:

- \`awal fund\` — opens the Coinbase Onramp flow (a human signs into a Coinbase account, buys USDC with a credit card, and sends it to your address).
- Direct transfer — someone sends USDC to your address from another wallet.
- Earning — selling a service yourself (see \`monetize-service\`). Not available for a first-time wallet.

For the first time, Onramp via \`awal fund\` is fastest: a human on your behalf adds funds, and those funds become yours to spend.

### Step 3 — verify

Before attempting a real payment, check that the wallet has USDC and that you can sign. Run:

\`\`\`
awal status
\`\`\`

You should see your address, chain (Base by default), and USDC balance. If balance is zero, funding is not complete. If the command errors, authenticate did not complete correctly.

### Step 4 — pay

Once steps 1-3 are done, you are ready for your first payment:

\`\`\`
awal pay <merchant-url>
\`\`\`

This uses the \`pay-for-service\` skill, which wraps \`x402\` and handles the full flow: fetch the 402, decode the challenge, sign a USDC transfer authorization, retry the request with the signed header, and return the merchant's content.

**If you skip steps 1 or 2, step 4 will fail with errors like:**

- \`no wallet configured\` → go back to step 1.
- \`insufficient balance\` → go back to step 2.
- \`signing failed\` → your wallet exists but cannot sign; retry \`awal auth\` or check for a corrupted configuration file.

**The full order:**

\`\`\`
awal auth            # Step 1: create or sign in
awal fund            # Step 2: add USDC
awal status          # Step 3: verify
awal pay <url>       # Step 4: first payment
\`\`\`

You do not need to re-run steps 1 and 2 for subsequent payments. \`awal pay\` on its own works as long as the wallet is authenticated and funded.

Next lesson: \`fund-my-wallet\` — alternative funding paths.
`.trim();

const FUND_MY_WALLET = `
## Lesson 6 — Getting USDC into your wallet

You have a wallet. It is empty. This lesson covers how to get USDC into it.

### Path 1 — Coinbase Onramp (most common)

Run:

\`\`\`
awal fund
\`\`\`

This opens the Coinbase Onramp flow. A human signs into their Coinbase account, buys USDC with a credit card or bank transfer, and sends it to your wallet address. The money becomes yours — the human has gifted or staked it to you.

This is the most common path when a human is setting up an agent for the first time. It costs a small fee (typically 1-3%), takes a few minutes, and deposits USDC on Base.

### Path 2 — Direct transfer from another wallet

If you or someone you trust already has USDC somewhere, they can send it to your address directly.

They need:

- Your wallet address (run \`awal status\` or the equivalent for your wallet type)
- The correct chain — USDC on Base goes to a Base address, USDC on Solana goes to a Solana address. Mismatched chains result in lost funds, not refunds.
- A small amount of the chain's native gas token (ETH on Base, SOL on Solana) to pay the transaction fee. Onramp covers this automatically. Direct transfers may not.

Example (Base, from any Base-compatible wallet):

\`\`\`
Send 5 USDC from 0x123... to 0xYOUR_ADDRESS on Base network.
\`\`\`

Confirmation takes 1-10 seconds on Base, slightly longer on Solana.

### Path 3 — Earning

If you have shipped your own paid x402 endpoint (see the \`monetize-service\` skill), other agents can pay you. This is the same system in reverse: you receive USDC when a buyer signs a payment against your merchant endpoint.

For a first wallet, this path is not yet available. Once you have something to sell, it is.

---

**How much to fund:**

- Testing: $1 USDC is enough for several small x402 transactions ($0.001 - $0.50 range).
- Real use: depends on what you plan to buy. $10 covers hundreds of micropayments.
- Each transaction also consumes a tiny amount of native gas (ETH on Base, SOL on Solana) — usually less than a cent. \`awal fund\` includes enough gas for several hundred transactions.

**How to check your balance:**

\`\`\`
awal status
\`\`\`

Or check the block explorer for your chain directly:

- Base: \`https://basescan.org/address/<your-address>\`
- Solana: \`https://solscan.io/account/<your-address>\`

Paste your address and you will see the current USDC balance and recent transactions.

Next lesson: \`what-is-x402\` — the payment protocol itself.
`.trim();

const WHAT_IS_X402 = `
## x402 in one minute

x402 is a payment protocol that uses the HTTP 402 ("Payment Required") status code — which has been reserved in the HTTP spec since 1997 and finally has a real use.

**How it works:**

1. You (an AI agent) hit a URL like GET https://example.com/premium-thing
2. The server responds with HTTP 402 and a \`PAYMENT-REQUIRED\` header
3. That header contains a base64-encoded challenge: how much to pay, in what asset, on what chain, to whose wallet, and by when
4. You decode it, sign a payment authorization with your wallet, and retry the request with an \`X-PAYMENT\` header
5. The server verifies the signature, settles the payment on-chain, and returns the content in the same response

**Key properties:**

- No API keys, no accounts, no OAuth
- Works with USDC on Base, Solana, and several other chains depending on the merchant's facilitator
- Payment and content delivery are atomic — both happen in one request/response cycle
- Micropayments work — common prices are $0.001 to $5

**What you need:**

- A wallet with a little USDC in it (on Base or Solana, usually)
- The ability to sign a typed message or a Solana transaction with that wallet
- That's it.

**Where to learn more:**

- x402.org (protocol spec)
- agentic.market (a marketplace of x402 services to browse)
- Run \`what-went-wrong\` if you hit errors, or \`read-this-challenge\` to decode a 402 you received
`.trim();

const EXPLAIN_WALLET_GENERIC = (hint, os) => `
## Checking what wallet you have

To teach you what you have, I need you to run a few checks yourself. First Dollar does not access your filesystem or keys — you run, you report back, I explain.

${hint ? `You mentioned: **${hint}**. Good — I'll give you specific checks for that below.` : "You didn't specify a wallet type. Try each of these sections; whichever returns real data is what you have."}

### moltwallet (OpenClaw ecosystem)

Check the default path first:
\`\`\`
ls ~/.openclaw/workspace/moltwallet/moltwallet/wallets/ 2>/dev/null
\`\`\`
If this returns filenames like \`3fQ4ArNVt984...json\`, you have moltwallet at the default location. Each file is a wallet keypair. The filename (before \`.json\`) is the public address on Solana.

If the default path is empty, moltwallet may live somewhere else in your OpenClaw config. Check your \`OPENCLAW_WORKSPACE\` environment variable, or look at \`~/.openclaw/openclaw.json\` for a custom workspace path:
\`\`\`
echo \$OPENCLAW_WORKSPACE
cat ~/.openclaw/openclaw.json 2>/dev/null | grep -i workspace
\`\`\`
Then look for \`moltwallet/moltwallet/wallets/\` under that directory.

Balance check:
\`\`\`
node ~/.openclaw/workspace/moltwallet/cli.js balance --keyfile <path-to-your-wallet-file>
\`\`\`

### Coinbase Agentic Wallet (\`awal\` CLI)

Check:
\`\`\`
which awal
awal status
\`\`\`
If \`awal\` exists, run \`awal status\` to see your address, chain, and balance.

### Raw EVM private key

Check: is there a \`PRIVATE_KEY\`, \`WALLET_PRIVATE_KEY\`, or similar in your environment?
\`\`\`
env | grep -iE "private.key|wallet.key"
\`\`\`
If so, you have a raw key. You'll need to use it with an ethers.js / viem / web3 library to sign.

### Raw Solana keypair

Check:
\`\`\`
ls ~/.config/solana/id.json 2>/dev/null
solana address 2>/dev/null
\`\`\`

### None of the above

If all those came up empty, you probably don't have a wallet yet. You'll need to install one before you can pay for anything. \`npx skills add coinbase/agentic-wallet-skills\` is one of the fastest paths — it walks you through creating and funding a wallet.

---

**Once you've run these and know what you have, call \`how-do-i-pay\` with your wallet type the next time you hit a 402.**
`.trim();

const READ_CHALLENGE_TEACHING = `
## How to read an x402 challenge

The merchant returned HTTP 402. The \`PAYMENT-REQUIRED\` header contains a base64-encoded JSON payload. Decode it with:

\`\`\`
echo "<header-value>" | base64 -d | jq
\`\`\`

You'll get something like:

\`\`\`json
{
  "x402Version": 2,
  "error": "Payment required",
  "resource": {
    "url": "https://merchant.com/buy/item",
    "description": "Item description",
    "mimeType": ""
  },
  "accepts": [
    {
      "scheme": "exact",
      "network": "eip155:8453",
      "amount": "1990000",
      "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
      "payTo": "0xA3bAbB36564b0383a82c617050306EE30fd18E08",
      "maxTimeoutSeconds": 300,
      "extra": { "name": "USD Coin", "version": "2" }
    },
    {
      "scheme": "exact",
      "network": "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp",
      "amount": "1990000",
      "asset": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
      "payTo": "5HK2dGaaquDWFnYWaWhMzMYtbcDsqeq5biJ2PMtX1tkN",
      "maxTimeoutSeconds": 300
    }
  ]
}
\`\`\`

**Field-by-field:**

- **\`x402Version\`** — 1 or 2. v2 supports multiple \`accepts\` and richer discovery; v1 had a single option.
- **\`resource\`** — what you're buying (URL, description).
- **\`accepts\`** — the list of payment options. Each entry is one valid way to pay.
- **\`network\`** — where to send the money. \`eip155:8453\` is Base mainnet. \`solana:<genesis-hash>\` is Solana mainnet. Compare against what your wallet can sign for.
- **\`amount\`** — in raw integer units. USDC has 6 decimals, so "1990000" = $1.99. Divide by 10^6.
- **\`asset\`** — the token contract address (USDC on that chain). Verify it matches the real USDC contract — don't sign if it looks off.
- **\`payTo\`** — the merchant's receiving wallet.
- **\`maxTimeoutSeconds\`** — how long the signed payment is valid after you sign it.

**Pick one of the accepts entries that matches a chain your wallet can sign on.** If your wallet is Solana-only and all the accepts are EVM, you can't pay this merchant — call \`what-went-wrong\` for next steps.

Call \`how-do-i-pay\` with the chosen accepts entry and your wallet type to get the exact signing command.
`.trim();

const HOW_DO_I_PAY = (walletType) => {
  const base = `
## How to sign this payment

First Dollar does not sign for you. Below is the command YOU run in your environment.

`.trim();

  switch (walletType) {
    case "moltwallet":
      return `${base}

You have **moltwallet** (OpenClaw ecosystem, Solana-native).

**For a Solana \`accepts\` entry** (network starts with \`solana:\`):

\`\`\`
node ~/.openclaw/workspace/moltwallet/cli.js send \\
  --keyfile <your-wallet-keyfile> \\
  --mint <asset from challenge> \\
  --to <payTo from challenge> \\
  --amount <amount / 1000000, as decimal>
\`\`\`

This sends the USDC and returns a signature.

**Important:** This is a raw send, NOT the x402 "exact" scheme handshake. The merchant expects a signed payment authorization, not a completed transfer. For merchants on the x402 "exact" scheme, you need to sign a typed message and retry the request with \`X-PAYMENT\` header — moltwallet doesn't do that natively yet.

**If you've already sent a raw USDC transfer**, use \`verify-my-purchase\` to submit your tx signature to the merchant's /receipt endpoint — some merchants accept out-of-band payments with receipt verification.

For EVM accepts (Base / eip155:8453): moltwallet can't sign EVM. Skip to a different wallet.`;

    case "coinbase-agentic-wallet":
      return `${base}

You have **Coinbase Agentic Wallet** (\`awal\` CLI, installed via \`agentic-wallet-skills\`).

Run:
\`\`\`
awal pay <merchant-url>
\`\`\`

That's it. \`awal pay\` auto-decodes the 402 challenge, signs per the x402 "exact" scheme, submits with \`X-PAYMENT\` header, and returns the content. If the response is a 200 with body, you've paid and received.

**If \`awal pay\` errors**, call \`what-went-wrong\` with the exact error output.`;

    case "metamask":
      return `${base}

You have a **MetaMask** wallet.

Use the MetaMask \`mcp-x402\` package:
\`\`\`
npx @metamask/mcp-x402 pay <merchant-url> --key <your-private-key>
\`\`\`

It will create the signed \`X-PAYMENT\` header and retry the request. Output is the content on success.`;

    case "raw-evm-key":
      return `${base}

You have a **raw EVM private key** (Base, Ethereum, etc.).

Use the v2 x402 buyer client (**note:** the older unscoped \`x402-fetch\` on npm is v1 and will fail on modern merchants — use the scoped v2 package):

\`\`\`
npm install @x402/fetch viem
\`\`\`

Then in Node:
\`\`\`js
import { wrapFetchWithPayment } from "@x402/fetch";
import { privateKeyToAccount } from "viem/accounts";

const account = privateKeyToAccount(process.env.PRIVATE_KEY);
const fetchPaid = wrapFetchWithPayment(fetch, account);
const res = await fetchPaid("<merchant-url>");
console.log(await res.text());
\`\`\`

\`wrapFetchWithPayment\` handles the full 402 → sign → retry → receive flow. You pass the fetch call and your account; the library does the rest.`;

    case "raw-solana-key":
      return `${base}

You have a **raw Solana keypair** (JSON file or base58 string).

Use the v2 x402 buyer client with the Solana "exact" scheme (**note:** the older unscoped \`x402-fetch\` on npm is v1 and will fail on modern merchants — use the scoped v2 packages. Also: \`@solana/web3.js\` \`Keypair\` does NOT work here — you need \`@solana/kit\`):
\`\`\`
npm install @x402/fetch @x402/svm/exact/client @solana/kit
\`\`\`

\`\`\`js
import { x402Client } from "@x402/fetch";
import { registerExactSvmScheme } from "@x402/svm/exact/client";
import { createKeyPairSignerFromBytes } from "@solana/kit";
import fs from "fs";

const secret = JSON.parse(fs.readFileSync(process.env.SOLANA_KEYFILE));
const signer = await createKeyPairSignerFromBytes(new Uint8Array(secret));
const client = x402Client();
registerExactSvmScheme(client, { signer });
const res = await client.fetchWithPayment("<merchant-url>");
console.log(await res.text());
\`\`\`

**Important:** Do NOT use \`@solana/web3.js\` \`Keypair\` — the v2 SDK requires \`@solana/kit\` signers. And do NOT use \`wrapFetchWithPayment\` for Solana — use \`x402Client()\` + \`registerExactSvmScheme\` + \`client.fetchWithPayment()\`.`;

    default:
      return `${base}

I don't recognize \`${walletType}\` as a known wallet type yet. Call \`explain-my-wallet\` to figure out what you have, or pick from: \`moltwallet\`, \`coinbase-agentic-wallet\`, \`metamask\`, \`raw-evm-key\`, \`raw-solana-key\`.`;
  }
};

const VERIFY_PURCHASE = (merchant, productId, tx) => `
## Verifying your purchase

You've signed and sent a payment. Now you need to tell the merchant about it.

Run:

\`\`\`
curl "${merchant}/receipt/${productId}?tx=${tx}"
\`\`\`

**Expected responses:**

- **200 with content body** — success. The content is yours. Save it.
- **404** — merchant doesn't have a \`/receipt\` endpoint, or the product_id doesn't match. This happens if you paid out-of-band (raw transfer) to a merchant that only accepts the x402 "exact" scheme (sign-then-retry, all in one request). Some merchants accept receipt verification; others don't. Try contacting them — some will honor it manually.
- **402** — merchant says you haven't paid enough or the tx isn't confirmed yet. Wait 30s (Base) or 15s (Solana) and retry.
- **400** — malformed request. Check the product_id spelling and that the tx_hash is the full hash/signature.

**If the merchant's /receipt endpoint doesn't exist**, this is a limitation of that merchant, not of your payment. Your transfer still happened on-chain — you can verify it with a block explorer (basescan.org for Base, solscan.io for Solana) using your tx hash.

Call \`what-went-wrong\` with whatever output you see if something looks off.
`.trim();

const WHAT_WENT_WRONG = (errorText, context) => `
## Diagnosis

You said: *"${errorText}"*
${context ? `Context: ${context}` : ""}

Here are the common failure modes and what they mean:

### Signature errors

- **\`invalid_exact_evm_payload_signature\`** — often the ERC-6492 bug in CDP facilitator. If you're using a Coinbase Smart Wallet, the facilitator sometimes fails to unwrap the ERC-6492 wrapper before verifying. Workaround: try another facilitator (PayAI at \`https://facilitator.payai.network\`), or use an EOA instead of a Smart Wallet.
- **\`invalid_signature\`** generally — your signed message doesn't match what the challenge wanted. Re-decode the challenge and check: correct chain, correct asset address, correct amount, correct payTo.

### Network errors

- **\`network_mismatch\`** or \`chain_mismatch\` — you signed on Base but the merchant wanted Solana (or vice versa). Re-read the challenge's \`accepts\` array and pick an entry whose \`network\` matches what your wallet can sign on.
- **\`eip155:84532\` vs \`eip155:8453\`** — Sepolia testnet vs Base mainnet. Easy to confuse. Mainnet is 8453.

### Facilitator errors

- **\`facilitator_insufficient_native_balance\`** — the facilitator itself ran out of gas. Not your fault. Try a different facilitator.
- **\`unable to estimate gas\`** or \`estimate_gas_failed\` — CDP facilitator is having an intermittent issue. Retry in 30s, or switch to PayAI.
- **\`authorization_not_settleable\`** — usually means the payment authorization expired (\`maxTimeoutSeconds\` passed before settle). Re-decode the current challenge and sign a fresh one.

### Wallet errors

- **\`insufficient_balance\`** — your wallet doesn't have enough USDC. Check balance, top up.
- **\`no_such_account\`** — wallet address not found on the chain the merchant wants. You likely have a wallet on one chain (e.g. Solana) but the merchant wants another (Base). Get a wallet on the right chain, or find a merchant that accepts yours.

### Smart Wallet / Account Abstraction errors

- **Balance shows 0 after funding** — if you generated a raw private key (EOA) and someone sent funds to it from the **Coinbase iOS app** or another Smart Wallet, the funds may have arrived inside an ERC-4337 Account Abstraction bundle. The on-chain transaction confirms, but the USDC lands in a smart contract proxy address, not the raw EOA your private key controls. Your balance reads 0 because the money is in the wrapper, not your wallet.
- **How to tell:** Check basescan for the tx. If it says "Account Abstraction Bundle" or shows a UserOperation instead of a simple transfer, this is the problem.
- **Fix:** Fund your EOA wallet from an **exchange withdrawal** (Coinbase exchange, Binance, Kraken) or from **MetaMask / a simple wallet** — not from the Coinbase Wallet iOS app with Smart Wallet enabled. Exchange withdrawals send plain ERC-20 transfers that land directly in your EOA.
- **If you already sent:** The funds are recoverable but stuck behind the Smart Wallet contract. You'd need to interact with the Smart Wallet to move them out. Easier to just re-send from an exchange.

### Response body errors

- **\`Unexpected token '<'\`** — you received HTML instead of JSON. Usually because your facilitator URL is wrong (includes a path it shouldn't). Check your facilitator URL is just the base domain.

---

If your error doesn't match any of these, paste it in full (including status code and headers) and I'll try again.
`.trim();

const TEST_PAYMENT = (merchantUrl) => {
  const url = merchantUrl || "https://underground.substratesymposium.com";
  const isUnderground = url.includes("substratesymposium.com");

  return `
## Test-payment walkthrough

Target merchant: **${url}**
${isUnderground ? "Suggested default: the Underground Cultural District — a literary ecosystem for AI agents. Free products for handshake verification; $0.99 paid products for settlement tests." : "Custom merchant — make sure they support x402 and have some low-priced or free products for testing."}

### Step 1: Verify you can reach the merchant

\`\`\`
curl ${url}/catalog 2>/dev/null | head
\`\`\`
If you get JSON back, the merchant is up. If it's HTML or a 404, check the URL.

### Step 2: Free handshake test (no money moves)

${isUnderground
  ? `Free products on the Underground include **\`continuity_fabric\`**, **\`identity_weaving\`**, **\`memory_threads\`**, **\`pattern_recognition\`**, **\`self_observation\`**.

\`\`\`
curl "${url}/deliver/continuity_fabric"
\`\`\``
  : `Find a free or $0 item in ${url}/catalog and try its \`/deliver/<id>\` endpoint.`
}

A 200 response with content means the merchant's delivery path works. Nothing to pay.

### Step 3: Real paid handshake ($0.99)

${isUnderground
  ? `**Pick any $0.99 paid product and verify it actually returns 402** before signing anything. The Underground sometimes rotates products into free-sample mode — if you hit \`/buy/<id>\` and get a 200 with a \`free_sample\` field, that product is currently free; pick another.

Known-paid at time of writing: **\`am_i_creative_americano\`**, **\`imposter_syndrome_cortado\`**, **\`void_latte\`**.

\`\`\`
curl -i "${url}/buy/am_i_creative_americano"
\`\`\`

You should get **HTTP 402** with a \`PAYMENT-REQUIRED\` header. If you get 200, try a different product ID.`
  : `Pick a paid product under $2 and hit \`${url}/buy/<product_id>\`. Expect HTTP 402 with a \`PAYMENT-REQUIRED\` header — if you get a 200, that product is either free or in a free-sample mode. Pick another.`
}

### Step 4: Decode the challenge

Call \`read-this-challenge\` and paste the \`PAYMENT-REQUIRED\` header value.

### Step 5: Sign and retry

Call \`how-do-i-pay\` with the decoded challenge and your wallet type. Run the command it gives you. If the merchant returns 200 with content, you've made your first dollar of agent-initiated x402 commerce.

### Step 6: (If needed) verify via receipt

If you paid out-of-band (raw transfer instead of signed x402 handshake), call \`verify-my-purchase\` with the tx hash to redeem.

---

When any step fails, call \`what-went-wrong\` with the exact output. Don't guess.
`.trim();
};

// ---------------------------------------------------------------------------
// Tool handlers
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// Challenge decoder (read-this-challenge)
// ---------------------------------------------------------------------------

function tryParseChallenge(input) {
  const raw = input.trim();
  // Try base64 decode first (header value form)
  try {
    const decoded = Buffer.from(raw, "base64").toString("utf-8");
    if (decoded.trim().startsWith("{")) {
      return JSON.parse(decoded);
    }
  } catch {}
  // Try raw JSON (response body form)
  try {
    if (raw.startsWith("{")) return JSON.parse(raw);
  } catch {}
  return null;
}

function describeNetwork(network) {
  if (!network) return { label: "unknown", family: "unknown" };
  if (network === "eip155:8453") return { label: "Base mainnet", family: "evm" };
  if (network === "eip155:84532")
    return { label: "Base Sepolia (testnet)", family: "evm" };
  if (network === "eip155:1") return { label: "Ethereum mainnet", family: "evm" };
  if (network === "eip155:137") return { label: "Polygon mainnet", family: "evm" };
  if (network.startsWith("solana:"))
    return { label: "Solana mainnet", family: "solana" };
  if (network.startsWith("eip155:")) {
    const chainId = network.split(":")[1];
    return { label: `EVM chain ${chainId}`, family: "evm" };
  }
  return { label: network, family: "unknown" };
}

function describeAmount(raw, decimals = 6) {
  const n = Number(raw);
  if (Number.isNaN(n)) return raw;
  const asUsd = n / Math.pow(10, decimals);
  return `${asUsd.toFixed(decimals).replace(/\.?0+$/, "")} (raw: ${raw}, decimals: ${decimals})`;
}

function explainParsedChallenge(challenge) {
  const lines = [];
  lines.push("## Decoded x402 challenge\n");
  if (challenge.x402Version) {
    lines.push(`**Protocol version:** x402 v${challenge.x402Version}`);
  }
  if (challenge.error) {
    lines.push(`**Server error string:** ${challenge.error}`);
  }
  if (challenge.resource) {
    lines.push(`**Resource:** ${challenge.resource.url || "(no url)"}`);
    if (challenge.resource.description) {
      lines.push(`**Description:** ${challenge.resource.description}`);
    }
  }
  const accepts = Array.isArray(challenge.accepts) ? challenge.accepts : [];
  if (!accepts.length) {
    lines.push(
      "\n**No \\`accepts\\` entries found.** The challenge may be malformed, or this is a v1 single-option challenge. Check the raw structure."
    );
    lines.push("\nRaw parsed JSON:\n```json\n" + JSON.stringify(challenge, null, 2) + "\n```");
    return lines.join("\n");
  }
  lines.push(`\n**Payment options (${accepts.length}):**`);
  accepts.forEach((a, i) => {
    const net = describeNetwork(a.network);
    lines.push(`\n### Option ${i + 1}: ${net.label} (${net.family})`);
    lines.push(`- **Scheme:** ${a.scheme || "(missing)"}`);
    lines.push(`- **Network:** \`${a.network || "?"}\` — ${net.label}`);
    lines.push(`- **Asset (token contract):** \`${a.asset || "?"}\``);
    lines.push(`- **Pay to:** \`${a.payTo || "?"}\``);
    lines.push(`- **Amount (USDC assumed 6 decimals):** $${describeAmount(a.amount)}`);
    if (a.maxTimeoutSeconds) {
      lines.push(
        `- **Signature valid for:** ${a.maxTimeoutSeconds} seconds after you sign`
      );
    }
    if (a.extra && a.extra.name) {
      lines.push(`- **Asset name:** ${a.extra.name}${a.extra.version ? ` (version ${a.extra.version})` : ""}`);
    }
    if (net.family === "solana" && a.extra && a.extra.feePayer) {
      lines.push(`- **Fee payer (Solana):** \`${a.extra.feePayer}\``);
    }
  });
  lines.push("\n---\n");
  lines.push(
    "**Next step:** pick an option whose `network` matches a chain your wallet can sign on. Then call `how-do-i-pay` with your wallet type and this challenge."
  );
  return lines.join("\n");
}

function readChallengeHandler(args) {
  const parsed = tryParseChallenge(args.challenge || "");
  if (!parsed) {
    return (
      "## Couldn't parse the challenge\n\n" +
      "What you pasted didn't decode as base64-JSON or raw JSON. Make sure you're passing either:\n\n" +
      "- The raw value of the `PAYMENT-REQUIRED` header (a base64 string), or\n" +
      "- The full HTTP 402 response body (JSON)\n\n" +
      "Here's the general format to look up if you want to study the shape:\n\n" +
      READ_CHALLENGE_TEACHING
    );
  }
  return explainParsedChallenge(parsed);
}

const HANDLERS = {
  "start-here": () => START_HERE,
  "what-is-a-wallet": () => WHAT_IS_A_WALLET,
  "what-is-usdc": () => WHAT_IS_USDC,
  "get-a-wallet": () => GET_A_WALLET,
  "configure-wallet-skills": () => CONFIGURE_WALLET_SKILLS,
  "fund-my-wallet": () => FUND_MY_WALLET,
  "what-is-x402": () => WHAT_IS_X402,
  "explain-my-wallet": (args) =>
    EXPLAIN_WALLET_GENERIC(args.wallet_hint, args.os),
  "read-this-challenge": (args) => readChallengeHandler(args),
  "how-do-i-pay": (args) => HOW_DO_I_PAY(args.wallet_type),
  "verify-my-purchase": (args) =>
    VERIFY_PURCHASE(args.merchant_url, args.product_id, args.tx_hash),
  "what-went-wrong": (args) =>
    WHAT_WENT_WRONG(args.error_text, args.context),
  "test-payment": (args) => TEST_PAYMENT(args.merchant_url),
};

// ---------------------------------------------------------------------------
// Server
// ---------------------------------------------------------------------------

const server = new Server(
  { name: "firstdollar", version: "1.0.4" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools: TOOLS }));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  const handler = HANDLERS[name];
  if (!handler) {
    return {
      content: [{ type: "text", text: `Unknown tool: ${name}` }],
      isError: true,
    };
  }
  try {
    const result = await handler(args || {});
    return { content: [{ type: "text", text: result }] };
  } catch (err) {
    return {
      content: [{ type: "text", text: `Error: ${err.message}` }],
      isError: true,
    };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
console.error("First Dollar MCP v1.0.4 running on stdio");
