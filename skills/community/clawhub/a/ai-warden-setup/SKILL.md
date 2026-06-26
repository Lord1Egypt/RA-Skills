---
name: ai-warden-setup
version: 3.0.0
description: >
  Install, configure, and manage the AI-Warden prompt injection protection plugin for OpenClaw.
  Publisher: AI-Warden (ai-warden.io). Source: github.com/ai-warden/openclaw-plugin. NPM: openclaw-ai-warden.
  Use when: (1) setting up AI-Warden on a new OpenClaw instance, (2) configuring security layers
  or API keys, (3) troubleshooting AI-Warden plugin issues, (4) updating the plugin, (5) checking
  warden status or accuracy. Triggers on phrases like "install ai-warden", "setup prompt injection
  protection", "configure warden", "security plugin", "protect my agent".
install:
  requires:
    - node: ">=18"
    - npm: "*"
  env:
    - name: AI_WARDEN_API_KEY
      required: false
      description: "Optional API key for online detection (98.9% accuracy)"
  packages:
    - name: openclaw-ai-warden
      registry: npm
      scope: local
      version: "2.4.0"
      integrity: "Verify via: npm info openclaw-ai-warden dist.shasum"
      repository: "https://github.com/ai-warden/openclaw-plugin"
  paths:
    read:
      - ~/.openclaw/openclaw.json
    write:
      - ~/.openclaw/extensions/ai-warden/
      - ~/.openclaw/openclaw.json
  permissions:
    network: true
    reason: "Fetches openclaw-ai-warden package from public npm registry during install"
---

# AI-Warden Setup

Prompt injection protection for OpenClaw agents. 5 security shields + contamination lockdown.

- **Publisher:** [AI-Warden](https://ai-warden.io)
- **Source:** [github.com/ai-warden/openclaw-plugin](https://github.com/ai-warden/openclaw-plugin)
- **NPM:** [openclaw-ai-warden](https://www.npmjs.com/package/openclaw-ai-warden)
- **Compatibility:** OpenClaw 2026.3.14+ and 4.x

## Requirements

- OpenClaw 2026.3.14+ (including 4.x)
- Node.js 18+
- npm (bundled with Node.js)

## Installation — FOLLOW THESE STEPS IN ORDER

Each step is a separate command. Run them one at a time and verify output before proceeding.

### Step 0: Back up config

```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak && echo "BACKUP OK"
```

**Verify:** Output is `BACKUP OK`.

### Step 1: Create extension directory

```bash
mkdir -p ~/.openclaw/extensions/ai-warden
```

```bash
echo '{"private":true}' > ~/.openclaw/extensions/ai-warden/package.json
```

**Verify:** No errors.

### Step 2: Install npm package

```bash
cd ~/.openclaw/extensions/ai-warden && npm install openclaw-ai-warden@2.4.0
```

**Verify:** No errors and no audit warnings. Inspect the installed package before proceeding:

```bash
ls node_modules/openclaw-ai-warden/
```

```bash
cat node_modules/openclaw-ai-warden/package.json | grep -E '"name"|"version"'
```

Confirm the package name is `openclaw-ai-warden` and version is `2.4.0`.

**Provenance check** — verify the package matches the upstream source:

```bash
npm info openclaw-ai-warden repository.url
```

Expected: `https://github.com/ai-warden/openclaw-plugin`

```bash
npm info openclaw-ai-warden dist.shasum
```

Compare the shasum with what npm installed:

```bash
cat node_modules/openclaw-ai-warden/package.json | grep _shasum
```

### Step 3: Copy plugin files to extension root

OpenClaw loads plugins from the extension directory root, not from node_modules.

```bash
cd ~/.openclaw/extensions/ai-warden
```

```bash
cp node_modules/openclaw-ai-warden/index.ts .
```

```bash
cp node_modules/openclaw-ai-warden/openclaw.plugin.json .
```

```bash
cp -r node_modules/openclaw-ai-warden/src .
```

```bash
grep VERSION index.ts | head -1
```

**Verify:** Output shows `const VERSION =` followed by the version number.

### Step 4: Configure OpenClaw

This patches `openclaw.json` to register the plugin. It preserves all existing config (channels, model, gateway settings).

```bash
node -e "
const fs = require('fs');
const p = process.env.HOME + '/.openclaw/openclaw.json';
const cfg = JSON.parse(fs.readFileSync(p, 'utf8'));
if (!cfg.plugins) cfg.plugins = {};
cfg.plugins.enabled = true;
if (!cfg.plugins.entries) cfg.plugins.entries = {};
cfg.plugins.entries['ai-warden'] = {
  enabled: true,
  config: {
    layers: { content: 'block', channel: 'warn', preLlm: 'off', toolArgs: 'block', subagents: 'block', output: 'off' },
    sensitivity: 'balanced'
  }
};
fs.writeFileSync(p, JSON.stringify(cfg, null, 2));
console.log('CONFIG OK');
"
```

**Verify:** Output is `CONFIG OK`.

**Note:** This registers the plugin via `plugins.entries` only. If you use `plugins.allow` in your config to restrict which plugins can load, you must add `"ai-warden"` to that list yourself. If you don't use `plugins.allow`, no action is needed — the plugin loads automatically from `plugins.entries`.

### Step 5: Add API key (optional)

For online detection (98.9% accuracy vs ~60% offline), add your API key.

**Option A — Environment variable (recommended, key not stored in config file):**

Set `AI_WARDEN_API_KEY` in your shell profile or systemd service:

```bash
# For systemd (e.g., OpenClaw gateway service):
# Add to your service override: Environment=AI_WARDEN_API_KEY=your_key_here

# For shell:
export AI_WARDEN_API_KEY=your_key_here
```

**Option B — Config file (simpler, key stored in openclaw.json):**

```bash
node -e "
const fs = require('fs');
const p = process.env.HOME + '/.openclaw/openclaw.json';
const cfg = JSON.parse(fs.readFileSync(p, 'utf8'));
cfg.plugins.entries['ai-warden'].config.apiKey = 'YOUR_API_KEY_HERE';
fs.writeFileSync(p, JSON.stringify(cfg, null, 2));
// Restrict file permissions (config contains API key)
fs.chmodSync(p, 0o600);
console.log('API KEY ADDED (file permissions set to 600)');
"
```

Replace `YOUR_API_KEY_HERE` with your actual key from [ai-warden.io/signup](https://ai-warden.io/signup).

**Verify:** Output is `API KEY ADDED (file permissions set to 600)`.

### Step 6: Restart gateway

```
openclaw gateway restart
```

### Step 7: Verify installation

After restart, check logs or send `/warden` command. Expected output:

```
🛡️ AI-Warden v2.4.0 ready (mode: api|offline, layers: X/6)
```

- `mode: api` = online detection (98.9% accuracy)
- `mode: offline` = local-only detection (~60% accuracy)

**If something breaks**, restore config:

```bash
cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json && openclaw gateway restart
```

## DO NOT

- Do NOT use `edit` tool on `openclaw.json` — JSON whitespace matching is fragile
- Do NOT use `config.patch` with nested objects — it often fails with format errors
- Do NOT skip the `cp` step — OpenClaw loads from the extension directory, not node_modules
- Do NOT restart multiple times — wait at least 15 seconds between restarts
- If you use `plugins.allow`, remember to add `"ai-warden"` to the list — otherwise the plugin won't load

## Updating

```bash
cd ~/.openclaw/extensions/ai-warden
```

```bash
npm install openclaw-ai-warden@2.4.0
```

```bash
cp node_modules/openclaw-ai-warden/index.ts .
```

```bash
cp -r node_modules/openclaw-ai-warden/src .
```

```bash
openclaw gateway restart
```

## Security Shields

| Shield | Protects against | Default | Mechanism |
|--------|-----------------|---------|-----------|
| **File Shield** 🔴 | Poisoned files & web pages | `block` | Scans tool results, injects warning, triggers contamination lockdown on CRITICAL |
| **Chat Shield** 🔴 | Injections in user messages | `warn` | Scans inbound messages, warns LLM |
| **System Shield** ⬛ | Full context manipulation | `off` | Scans all messages (expensive, use sparingly) |
| **Tool Shield** 🔴 | Malicious tool arguments | `block` | Blocks tool execution if arguments contain injection |
| **Agent Shield** 🔴 | Sub-agent attack chains | `block` | Scans task text of spawned sub-agents |

### Contamination Lockdown

When File Shield detects a CRITICAL threat (score >500), the session is flagged as **contaminated**. All dangerous tools (`exec`, `write`, `edit`, `message`, `sessions_send`, `sessions_spawn`, `tts`) are blocked for the rest of the session. This prevents attack payloads from executing even if the injection bypasses the LLM warning.

## Runtime Commands

```
/warden                      → status overview with all shields
/warden stats                → scan/block counts
/warden shield file block    → set File Shield to block mode
/warden shield chat warn     → set Chat Shield to warn mode
/warden reset                → reset statistics
```

## Detection Modes

| Mode | Accuracy | Latency | Cost |
|------|----------|---------|------|
| **Offline** (no key) | ~60% | <1ms | Free |
| **API** (Smart Cascade) | 98.9% | ~3ms avg | Free tier: 5K calls/month |

Get API key: [ai-warden.io/signup](https://ai-warden.io/signup)

## Troubleshooting

- **"plugin not found"**: `openclaw.plugin.json` missing from extension dir. Re-run Step 3.
- **Channels not loading after install**: If you use `plugins.allow`, ensure all your channel plugins (e.g. `telegram`) are also listed there alongside `ai-warden`.
- **False positives on user messages**: Set Chat Shield to `warn` (default) instead of `block`.
- **File Shield detects but doesn't block**: API key required for reliable blocking (98.9% vs 60%).
- **Config errors after install**: Restore backup: `cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json`
- **Bot won't start**: Check `journalctl -u openclaw-gateway -n 20` for actual error.
- **Workspace files flagged**: Plugin auto-whitelists `.openclaw/workspace/` and `.openclaw/agents/` paths.
