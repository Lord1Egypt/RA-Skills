---
name: gateway-validator
description: Validate OpenClaw gateway configuration changes before applying them to production. Use when the user wants to change models, API keys, providers, or any gateway settings. Tests changes first on an isolated test gateway if possible, or validates provider connectivity directly as a fallback.
---

# Gateway Validator

Safely validate gateway config changes before they break production.

## How It Works

**Primary approach:**
1. Create temp config with your changes
2. Start isolated test gateway on different port
3. Send test completion request
4. Works? → Apply to production
5. Fails? → Block and show error

**Fallback approach** (when isolated gateway can't start):
1. Validate config syntax
2. Test provider APIs directly (check API keys, models)
3. Works? → Apply to production  
4. Fails? → Block and show error

## Usage

I'll automatically use this when you request gateway changes:
- "Change model to gpt-4o"
- "Update API key"
- "Switch to anthropic"
- Any config modification

## Examples

### Bad API Key
```
You: "Set API key to fake-key"
Me: "🧪 Testing changes...
     ❌ API key is invalid
     Config unchanged."
```

### Bad Model
```
You: "Use model gpt-99"
Me: "🧪 Testing changes...
     ❌ Model not found
     Config unchanged."
```

### Valid Change
```
You: "Change temperature to 0.5"
Me: "🧪 Testing changes...
     ✅ Test passed
     ✅ Config updated"
```

## Technical Details

**Level 1: Config Syntax**
- YAML valid?
- Required fields present?
- Value ranges valid (temp 0-2, etc.)?

**Level 2: Provider Test** (direct API calls)
- API key valid?
- Model exists?
- Can connect to provider?

**Level 3: Full Gateway Test** (when possible)
- Start temp gateway
- Send completion request
- Verify end-to-end works

## Limitations

- **Isolated gateway test** requires systemd/launchd (not available in all containers)
- When isolated test unavailable, falls back to provider-level validation
- Provider testing needs ~5-10 seconds for API calls
