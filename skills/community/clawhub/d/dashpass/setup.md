# DashPass — First-Time Setup

> This guide walks you through the one-time setup needed before using DashPass.
> Once complete, you won't need to read this file again.

---

## Prerequisites Checklist

### 1. Node.js 18 or newer

```bash
node --version
# Should print v18.x.x or higher
```

If you don't have Node.js, install it from [nodejs.org](https://nodejs.org/) or use `nvm`:

```bash
nvm install 18
nvm use 18
```

### 2. Install the Dash Platform SDK

DashPass uses the Dash Evo SDK to talk to the Dash blockchain. Install the specific version:

```bash
npm install @dashevo/evo-sdk@3.1.0-dev.1
```

> **Why this exact version?** DashPass requires the `3.1.0-dev.1` development release of the Evo SDK. The stable release has a different API surface that is not compatible. Using the wrong version will cause import errors or silent failures.

### 3. A Dash Testnet Wallet with tDASH

You need a small amount of testnet DASH (tDASH) to pay for blockchain operations. Testnet DASH is free — it has no real-world value.

**Get testnet DASH from the faucet:**

1. Visit: **https://testnet-faucet.dash.org/**
2. Enter your testnet wallet address
3. Receive free tDASH (you only need ~0.01 tDASH to get started)

> **What is a "wallet address"?** It's a string like `yXf7j8Vk...` that identifies where to send DASH. If you don't have a wallet yet, you'll create one as part of the Identity setup in Step 4.

### 4. A Dash Platform Identity

A **Platform Identity** is your on-chain identity on the Dash network. It's like a blockchain account — you need one to read and write data on Dash Platform.

Creating an Identity involves:
1. Having a funded Dash testnet wallet
2. Registering the Identity on-chain (costs a small fee)
3. Getting back an **Identity ID** — a base58 string like `36SxvpAKXeBJByUdJ364Hnhp2NfVDe6Gkj7xtTRZj6hh`

See the [Dash Platform Identity tutorial](https://docs.dash.org/en/stable/docs/tutorials/identities-and-names.html) for step-by-step instructions.

> **What is "base58"?** It's an encoding format used in cryptocurrency — looks like a mix of letters and numbers without confusing characters (no `0`, `O`, `I`, `l`). You don't need to understand it — just copy-paste the ID string.

### 5. Platform Credits

**Credits** are the "gas" that pays for writing data to Dash Platform. You get credits by converting tDASH to credits via a "top-up" transaction.

```bash
# Top up credits using the Dash SDK
# See: https://docs.dash.org/en/stable/docs/tutorials/identities-and-names.html#top-up-an-identity
```

The `status` command (shown later) tells you your current credit balance.

> **How many credits do I need?** Each credential storage operation costs roughly 0.0001 DASH worth of credits. 0.01 DASH worth of credits is enough for hundreds of operations.

### 6. Environment Variables Set

You need two environment variables configured before running DashPass:

```bash
export CRITICAL_WIF="your-testnet-WIF-private-key"
export DASHPASS_IDENTITY_ID="your-platform-identity-id"
```

> **What is a WIF?** WIF stands for **Wallet Import Format**. It's a way to represent a private key as a human-readable string starting with `c` (testnet) or `5`/`K`/`L` (mainnet). Example: `cVt4o7BGAig1UXywgGSmARhxMdzP5qvQsxKkSsc1XEkw3tDTQFpy`. This key is what encrypts and decrypts your credentials. **Never share it. Never commit it to git. Never paste it in chat.**

---

## Getting Started — Step by Step

This walkthrough takes you from zero to your first stored-and-retrieved credential.

### Step 1: Locate the DashPass CLI

The CLI script is at:

```
skills/dashpass/scripts/dashpass-cli.mjs
```

Or if you're working from the `scripts/credits-test/` directory:

```
scripts/credits-test/dashpass-cli.mjs
```

### Step 2: Install Dependencies

```bash
cd skills/dashpass/scripts   # or wherever dashpass-cli.mjs lives
npm install @dashevo/evo-sdk@3.1.0-dev.1
```

Verify the SDK is installed:

```bash
node -e "import('@dashevo/evo-sdk').then(() => console.log('OK'))"
# Should print: OK
```

### Step 3: Get Testnet DASH

1. Go to **https://testnet-faucet.dash.org/**
2. Paste your testnet wallet address
3. Click "Get coins"
4. Wait 1-2 minutes for the transaction to confirm

### Step 4: Create a Platform Identity

If you already have an Identity, skip to Step 5. Otherwise, follow the [Dash Platform tutorial](https://docs.dash.org/en/stable/docs/tutorials/identities-and-names.html) to:

1. Register a new Identity using the SDK
2. Note your **Identity ID** (base58 string)
3. The registration adds authentication keys to your Identity automatically

> **Important:** The WIF (private key) you use must correspond to an authentication key on your Identity. If they don't match, you'll get cryptic "Invalid signature" errors when trying to write credentials.

### Step 5: Top Up Credits

Your Identity needs Platform credits to pay for storing documents:

```javascript
// Example using evo-sdk (run as a script)
import { EvoSDK } from '@dashevo/evo-sdk';

const sdk = EvoSDK.testnetTrusted({ version: await EvoSDK.getLatestVersionNumber() });
await sdk.connect();
// Use sdk.identities.topUp() with your identity and funded wallet
```

See the [Dash docs on topping up](https://docs.dash.org/en/stable/docs/tutorials/identities-and-names.html#top-up-an-identity).

### Step 6: Set Environment Variables

```bash
# Required: your private key (WIF format)
export CRITICAL_WIF="cVt4o7BGAig1UXywgGSmARhxMdzP5qvQsxKkSsc1XEkw3tDTQFpy"

# Required: your Platform Identity ID
export DASHPASS_IDENTITY_ID="36SxvpAKXeBJByUdJ364Hnhp2NfVDe6Gkj7xtTRZj6hh"

# Optional: use your own deployed contract (otherwise uses shared testnet contract)
# export DASHPASS_CONTRACT_ID="ATamKoznYgWsQGP6JBpmVuFGiqAXTVWdjpeSGeEVSikq"
```

> **Security reminder:** The `CRITICAL_WIF` value above is an **example only**. Use your own testnet WIF. Never use a mainnet WIF for testing.

### Step 7: Store Your First Credential (put)

```bash
echo "sk-test-fake-api-key-12345" | node dashpass-cli.mjs put \
  --service my-first-test \
  --type api-key \
  --level normal \
  --label "My first test credential" \
  --value-stdin
```

Expected output:

```
[warn] Using shared testnet contract. Set DASHPASS_CONTRACT_ID for your own vault.
[sdk] Connecting to testnet...
[sdk] Connected (platform v12)
[put] Service: my-first-test
[put] Type: api-key | Level: normal
[put] Encrypted with Scheme C
[put] Writing to Platform...
[put] OK
  Document ID: 7Hk9x...  (your document ID will differ)
  Service: my-first-test
  Type: api-key
  Level: normal
```

> **What just happened?** The CLI encrypted your value (`sk-test-fake-api-key-12345`) using your WIF-derived key, then stored the encrypted blob on the Dash blockchain. The plain-text value never left your machine.

### Step 8: Retrieve Your Credential (get)

```bash
node dashpass-cli.mjs get --service my-first-test
```

Expected output:

```
---
  Document ID: 7Hk9x...
  Service:     my-first-test
  Label:       My first test credential
  Type:        api-key
  Level:       normal
  Status:      active
  Version:     1
  Expires:     never
  Value:       sk-test-fake-api-key-12345
---
```

### Step 9: Verify

The value you got back (`sk-test-fake-api-key-12345`) matches what you stored. The round-trip is complete: **put → encrypt → blockchain → fetch → decrypt → get**.

You can also try pipe-friendly output for use in scripts:

```bash
# Returns just the value, no formatting, no newline
node dashpass-cli.mjs get --service my-first-test --pipe
# Output: sk-test-fake-api-key-12345
```

Or JSON output:

```bash
node dashpass-cli.mjs get --service my-first-test --json
```
