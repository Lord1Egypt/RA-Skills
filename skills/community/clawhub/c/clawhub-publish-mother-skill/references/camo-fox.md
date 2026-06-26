# Camo Fox for ClawHub Publishing 🦊

## Why Camo Fox Matters
ClawHub authentication (`clawhub login`) opens a browser for GitHub OAuth. Without Camo Fox:
- Bot detection may block authentication
- Login flows may fail
- Publishing may be unreliable

## Enabling Camo Fox

### BrowserBase Configuration
```bash
# Set Camo Fox environment variables
export BROWSERBASE_CAMO_FOX=true
export BROWSERBASE_PROXY_TYPE=residential
```

### Hermes Agent Configuration
In your Hermes config:
```yaml
browser:
  stealth:
    camo_fox: true
    proxy: residential
```

## Authentication Workflow with Camo Fox

### 1. Setup Environment
```bash
# Enable Camo Fox
export BROWSERBASE_CAMO_FOX=true

# Start browser session with stealth
hermes-browser --stealth --camo-fox
```

### 2. ClawHub Login
```bash
# This will now work with bot detection evasion
clawhub login
```

### 3. Verify Authentication
```bash
clawhub whoami
# Should show your username
```

## Troubleshooting

### Common Issues
1. **"Bot detected"** - Enable Camo Fox
2. **"Login timeout"** - Use residential proxies
3. **"Authentication failed"** - Check GitHub token permissions

### Solutions
- Always use Camo Fox for ClawHub operations
- Prefer token auth in headless environments
- Test with `clawhub whoami` before publishing

## Best Practices
1. **Always** use Camo Fox for ClawHub auth
2. **Test** authentication before publishing
3. **Monitor** for bot detection warnings
4. **Update** stealth configurations regularly

**HELL YEAH, stealth publishing!** 🎯
