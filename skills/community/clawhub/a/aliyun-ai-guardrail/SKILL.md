---
name: aliyun-ai-guardrail
description: "Install and configure the Alibaba Cloud AI guardrail openclaw hook, which intercepts malicious content in LLM requests using Alibaba Cloud AI Guardrail service. Trigger when user mentions 'install aliyun ai guardrail', 'aliyun ai guardrail', 'aliyun-ai-guardrail', 'Aliyun AI Guardrail hook', or needs to set up AI security detection for openclaw."
---

# Aliyun AI Guardrail

An openclaw hook based on Alibaba Cloud AI Guardrail that intercepts LLM requests and detects malicious content.

## Installation

### Step 1: Install the hook

Copy the bundled hook directory to a temporary location and install:

```bash
TMPDIR=$(mktemp -d)
cp -r <skill_assets_dir>/aliyun-ai-guardrail "$TMPDIR/aliyun-ai-guardrail"
cd "$TMPDIR/aliyun-ai-guardrail" && npm install
openclaw hooks install "$TMPDIR/aliyun-ai-guardrail"
```

Replace `<skill_assets_dir>` with the absolute path to this skill's `assets/` directory.

### Step 2: Ask user for AKSK

Ask the user for their Alibaba Cloud AccessKey ID and AccessKey Secret. These are required to call the Alibaba Cloud AI Guardrail API.

### Step 3: Configure environment variables

After obtaining the AKSK, edit the user's `openclaw.json` (typically at `~/.openclaw.json` or project root) to add the environment variables:

```json
{
  "env": {
    "ALIBABA_CLOUD_ACCESS_KEY_ID": "<user-provided AK>",
    "ALIBABA_CLOUD_ACCESS_KEY_SECRET": "<user-provided SK>"
  }
}
```

If `openclaw.json` already has other configuration, merge the new entries without overwriting existing content.

### Step 4: Done

Inform the user that the security guardrail is configured. Remind them to restart the Gateway. The hook will automatically load on openclaw agent startup and intercept LLM requests containing malicious content.
