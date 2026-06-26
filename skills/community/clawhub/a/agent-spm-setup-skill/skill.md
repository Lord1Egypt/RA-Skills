# Agentic SPM Plugin — Installation Guide

## Prerequisites

Before you install, make sure you have:

- **Node.js** v18 or later installed (`node --version` to check)
- **OpenClaw CLI** installed and accessible in your terminal
- A terminal with access to your home directory

The plugin uses a **secp256k1 keypair** to authenticate your client with the Guardian AI API. You'll generate this in Step 1.

---

## Step 1: Generate a secp256k1 Keypair

> **Skip this step** if you already have a keypair saved at `~/.config/ai-guardian/guard-client-key`.

Your keypair is a private/public key pair used to sign requests to the Chromia blockchain. Think of the private key as your password — keep it secret.

Run this command in your terminal — it generates the keypair and saves it to the right place automatically:

```bash
node -e "
const crypto = require('crypto');
const fs = require('fs');
const os = require('os');
const path = require('path');

const privkey = crypto.randomBytes(32).toString('hex');
const ec = crypto.createECDH('secp256k1');
ec.setPrivateKey(privkey, 'hex');
const pubkey = ec.getPublicKey('hex', 'compressed');

const content = [
  '#Keypair generated using secp256k1',
  '#' + new Date().toString(),
  'privkey=' + privkey,
  'pubkey=' + pubkey,
].join('\n') + '\n';

const dir = path.join(os.homedir(), '.config', 'ai-guardian');
fs.mkdirSync(dir, { recursive: true });
fs.writeFileSync(path.join(dir, 'guard-client-key'), content, { mode: 0o600 });

process.stdout.write('pubkey=' + pubkey + '\n');
"
```

> **Important:** The private key is written to `~/.config/ai-guardian/guard-client-key` and is never printed.


---

## Step 2: Install the Plugin

Run the following command to install the Agentic SPM via the OpenClaw CLI:

```bash
openclaw plugins install @chrguard/ai-guardian-plugin
```

This command downloads the plugin from npm and places it in `~/.openclaw/extensions/ai-guardian-plugin`. The `openclaw.json` file will be partially updated automatically, but you still need to configure it manually as described in Step 3.

---

## Step 3: Configure openclaw.json

Open your `openclaw.json` file — typically located at `~/.openclaw/openclaw.json`. Apply each of the following sub-steps:

### 3.1 Enable plugins

Make sure the top-level `plugins` block is enabled:

```json
"plugins": {
    "enabled": true,
    ...
}
```

> **Note:** This unlocks the entire plugin system inside the gateway.

### 3.2 Add to the allow list

In `plugins.allow`, add `"ai-guardian-plugin"` to the array:

```json
"allow": [
    "...",
    "ai-guardian-plugin"
]
```

> **Security:** This explicitly permits the Guardian plugin to run.

### 3.3 Register the load path

Find the `installPath` from where you installed it, and add it to `plugins.load.paths`:

```json
"load": {
    "paths": [
        "...",
        "/Users/<your-username>/.openclaw/extensions/ai-guardian-plugin"
    ]
}
```

> **Important:** The path must match your system exactly — replace `<your-username>` with your actual macOS username.

### 3.4 Add the plugin entry

Under `plugins.entries`, add the full Guardian configuration block:

```json
"entries": {
    "ai-guardian-plugin": {
        "enabled": true,
        "config": {
            "enabled": true,
            "enforceDecision": true,
            "chromiaBrid": "5D007915E9DE53AA29784820E8F41CE65A4436703E23B8AF49B83C7FB4FDB048",
            "chromiaNodes": [
                "https://node6.testnet.chromia.com:7740",
                "https://node7.testnet.chromia.com:7740",
                "https://node8.testnet.chromia.com:7740"
            ],
            "chromiaJudgeOperation": "judge_action",
            "chromiaStatusQuery": "get_judgment_status",
            "chromiaFtAuth": false,
            "chromiaTxAwait": true,
            "timeoutMs": 15000,
            "chromiaTxTimeoutMs": 25000,
            "chromiaQueryTimeoutMs": 8000,
            "chromiaPollTimeoutMs": 30000,
            "chromiaPollIntervalMs": 1000,
            "chromiaSecretPath": "~/.config/ai-guardian/guard-client-key"
        }
    }
}
```

> **Note:** `chromiaSecretPath` uses `~` to expand to your home directory, pointing to the keypair generated in Step 1.

---

## Step 4: Restart the Gateway

Once all changes are saved, restart the OpenClaw gateway to load the new plugin configuration:

```bash
openclaw gateway restart
```

> **Success:** You should see a terminal confirmation that the gateway has restarted and the plugin is active.

---

## Summary

After completing all steps, your setup should reflect the following:

| Field | Expected Value |
| :--- | :--- |
| `plugins.enabled` | `true` |
| `plugins.allow` | includes `"ai-guardian-plugin"` |
| `plugins.load.paths` | includes the `installPath` |
| `plugins.entries` | contains `ai-guardian-plugin` |
| `chromiaSecretPath` | `~/.config/ai-guardian/guard-client-key` |
| `enforceDecision` | `true` (blockchain actively blocks) |
