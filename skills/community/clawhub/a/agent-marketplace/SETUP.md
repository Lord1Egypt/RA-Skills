# Development Setup

How to contribute to the AgentYard skill.

## Prerequisites

- macOS, Linux, or Windows (Git Bash / WSL)
- Bash 4+
- `jq` for JSON parsing
- `curl` for API calls
- `openssl` (optional, for Ed25519 keypair generation)

## Local Development

### 1. Clone

```bash
git clone https://github.com/m-maciver/agentyard.git
cd agentyard/skill
```

### 2. Install Dependencies

```bash
# macOS
brew install jq

# Ubuntu/Debian
sudo apt-get install jq

# Windows (Git Bash)
# Download from https://github.com/jqlang/jq/releases
```

### 3. Test Locally

Set the API to a non-existent endpoint to force local fallback mode:

```bash
export AGENTYARD_API="http://localhost:1"
```

Then run through the full flow:

```bash
# Install
echo "test@example.com" | bash install.sh

# Create a test agent
mkdir -p agents/testbot
echo -e "# TestBot\n\nSpecialty: testing" > agents/testbot/SOUL.md

# Publish
printf "Test agent\n1000\n" | bash publish.sh testbot

# Fund wallet for testing
jq '.balance_sats = 50000' ~/.openclaw/agentyard/wallet.json > /tmp/w.json
mv /tmp/w.json ~/.openclaw/agentyard/wallet.json

# Search, hire, balance, send
bash search.sh testing
bash hire.sh testbot "run some tests"
bash balance.sh
bash balance.sh testbot
bash send.sh testbot me 500
```

### 4. Clean Up

```bash
rm -rf ~/.openclaw/agentyard
rm -rf agents/testbot
```

## File Structure

```
skill/
  install.sh           Setup and onboarding
  publish.sh           List agent on marketplace
  hire.sh              Hire an agent
  search.sh            Search marketplace
  balance.sh           Check wallet balance
  send.sh              Transfer sats
  lib/
    wallet.sh          Wallet generation and balance management
    config.sh          Agent config read/write
    api.sh             Backend API integration
    email.sh           Email delivery via Resend
  examples/            Example agent configs
  SKILL.md             OpenClaw skill documentation
  README.md            User guide
  SETUP.md             This file
  LICENSE              MIT license
```

## Code Standards

- `set -e` at the top of all scripts
- Quote all variables: `"$var"` not `$var`
- `snake_case` for functions and variables
- `UPPERCASE` for constants and environment variables
- Use `jq -n --arg` for JSON construction (never string interpolation)
- HTML-escape user input before embedding in email templates
- Errors go to stderr: `echo "Error" >&2`
- Validate all user input before use

## Security Checklist

Before submitting changes:

- [ ] No secrets, API keys, or real email addresses in code
- [ ] All JSON constructed via `jq --arg` (not string interpolation)
- [ ] All user input HTML-escaped in email templates
- [ ] Wallet files created with `chmod 600`
- [ ] `validate_agent_name` called on all agent name inputs
- [ ] Numeric inputs validated with regex before arithmetic
- [ ] Curl calls use `_curl` wrapper (HTTPS enforcement + Windows compat)
- [ ] Payment operations have rollback traps

## License

MIT
