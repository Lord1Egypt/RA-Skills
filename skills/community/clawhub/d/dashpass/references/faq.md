# DashPass FAQ & Known Limitations

## Frequently Asked Questions

### "Cannot find module '@dashevo/evo-sdk'"

The Dash Platform SDK is not installed. Install it:

```bash
npm install @dashevo/evo-sdk@3.1.0-dev.1
```

Make sure you're in the same directory as `dashpass-cli.mjs`, or that `node_modules` is in a parent directory.

### "CRITICAL_WIF not set"

You haven't set the `CRITICAL_WIF` environment variable. Set it:

```bash
export CRITICAL_WIF="your-testnet-wif-here"
```

The error message `[fatal] CRITICAL_WIF not set. Export CRITICAL_WIF with your wallet WIF.` means the CLI checked for this variable and found it empty.

### "DASHPASS_IDENTITY_ID not set"

You haven't set your Identity ID. Set it:

```bash
export DASHPASS_IDENTITY_ID="your-identity-id-here"
```

Or use the `--identity-id` flag:

```bash
node dashpass-cli.mjs status --identity-id "your-identity-id-here"
```

### "Invalid signature" or "Key not found on identity"

Your WIF (private key) does not match any authentication key on your Platform Identity. This means:
- The WIF you exported belongs to a different wallet than the one that created the Identity, **or**
- The Identity was created with different keys

**Fix:** Make sure `CRITICAL_WIF` contains the WIF that corresponds to the AUTHENTICATION CRITICAL key (purpose=0, securityLevel=1) on your Identity.

### "invalid identity nonce"

This happens when you do write operations (put, rotate) too quickly in succession. The Dash Platform needs a few seconds between operations to process each transaction.

**Fix:** Wait 3-5 seconds between consecutive write operations. This is a known platform timing limitation, not a DashPass bug.

### "insufficient credits" or balance-related errors

Your Identity doesn't have enough Platform credits to pay for the write operation.

**Fix:** Top up your Identity's credits by converting tDASH to credits:

```bash
# Check your current balance first
node dashpass-cli.mjs status
```

If the balance is low, follow the [top-up tutorial](https://docs.dash.org/en/stable/docs/tutorials/identities-and-names.html#top-up-an-identity).

### "Can other people read my encrypted credentials?"

**They can see the ciphertext (encrypted blob) and metadata, but they cannot decrypt the actual secret values.**

What's visible on-chain to anyone:
- Service name (e.g., "anthropic-api") — **plaintext**
- Label (e.g., "Anthropic production key") — **plaintext**
- Credential type and security level — **plaintext**
- Version number and status — **plaintext**
- The encrypted blob — **encrypted** (unreadable without your WIF)

What only you can see:
- The actual secret value (e.g., `sk-ant-api03-xxxxx`)

If metadata privacy matters, deploy your own contract (see Known Limitations).

### "Using shared testnet contract" warning

This is informational, not an error. It means you're using the default shared testnet contract instead of your own. This is fine for testing. For production, deploy your own contract and set `DASHPASS_CONTRACT_ID`.

### "How do I generate a WIF?"

A WIF is generated from a private key. If you created a Dash wallet (via the SDK, Dash Core, or a mobile wallet), you already have one. To extract or generate a testnet WIF:

```javascript
import { PrivateKey } from '@dashevo/evo-sdk';
const pk = new PrivateKey({ network: 'testnet' });
console.log('WIF:', pk.toWIF());
console.log('Address:', pk.toAddress().toString());
```

**Store the WIF securely. It controls access to your entire credential vault.**

---

## Known Limitations

### Testnet only

DashPass has been tested and verified on the **Dash testnet only**. Mainnet deployment has not been validated. Do not store real production credentials on testnet — testnet can be reset.

### Rapid successive writes may fail

Performing multiple write operations (put, rotate, delete) in quick succession (under 3 seconds apart) can trigger an "invalid identity nonce" error from the Dash Platform. This is a platform-level timing constraint.

**Workaround:** Wait 3-5 seconds between write operations.

### Plaintext metadata on-chain

Service names, labels, credential types, security levels, and version numbers are stored **unencrypted** on the blockchain. Anyone who knows your Identity ID or Contract ID can query this metadata. They cannot decrypt the actual secret values, but they can see *which services* you use and *how many credentials* you manage.

**Mitigation:** Deploy your own contract to avoid sharing metadata space with other users. The shared testnet contract is for testing convenience only.

### Single key (SPOF)

All credentials are encrypted with a single master key derived from `CRITICAL_WIF`. If you lose this key, all credentials are permanently unrecoverable. If someone steals this key, they can decrypt everything.

**Recommendation:** Back up your WIF securely (e.g., encrypted USB, paper wallet in a safe). Consider key backup strategies before storing important credentials.

### No setup wizard

Currently, DashPass requires manual setup of the Identity, credits, and environment variables. There is no automated `setup` command. Plan for 30-60 minutes of setup time if you're new to Dash Platform.

### Cache is per-machine

The local cache (`~/.dashpass/cache/`) is specific to the machine it's on. It provides faster repeated access but is not shared across machines.
