# 📚 Credential Vault — Usage Examples

Real-world usage patterns for Credential Vault.

---

## Scenario 1: First-Time Setup

```bash
# 1. Initialize vault
$ cd ~/ubik-collective/systems/ubik-pm/skills/credential-vault
$ uv run vault init
Enter master password: ************
Confirm master password: ************
✅ Vault initialized at /Users/you/.openclaw/vault/vault.enc.json

# 2. Unlock vault
$ uv run vault unlock
Enter master password: ************
🔓 Vault unlocked

# 3. Add your API keys
$ uv run vault add OPENAI_API_KEY --tag openai
Enter value for OPENAI_API_KEY: ********
✅ Added credential: OPENAI_API_KEY

$ uv run vault add ANTHROPIC_API_KEY --tag anthropic
Enter value for ANTHROPIC_API_KEY: ********
✅ Added credential: ANTHROPIC_API_KEY

$ uv run vault add TAVILY_API_KEY --tag tavily --expires 2027-01-01
Enter value for TAVILY_API_KEY: ********
✅ Added credential: TAVILY_API_KEY

# 4. Verify
$ uv run vault list
📋 Credentials (3):

  🔑 OPENAI_API_KEY
     Tags: openai

  🔑 ANTHROPIC_API_KEY
     Tags: anthropic

  🔑 TAVILY_API_KEY
     Tags: tavily
     Expires: 2027-01-01

# 5. Lock when done
$ uv run vault lock
🔒 Vault locked
```

---

## Scenario 2: Using Credentials in a Script

**Setup:**
```bash
uv run vault unlock
eval $(uv run vault env --tag openai)
```

**Python script (`test_openai.py`):**
```python
import os

# Credential automatically available from vault
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ OPENAI_API_KEY not set. Did you run 'vault env'?")
    exit(1)

print(f"✅ API key loaded: {api_key[:10]}...")
# Use api_key for OpenAI calls...
```

**Run:**
```bash
python test_openai.py
✅ API key loaded: sk-proj-ab...
```

---

## Scenario 3: Multi-Environment Keys

```bash
# Production keys
uv run vault add OPENAI_API_KEY_PROD "sk-prod-..." --tag openai --tag production

# Development keys
uv run vault add OPENAI_API_KEY_DEV "sk-dev-..." --tag openai --tag development

# Export only production
eval $(uv run vault env --tag production)

# Or only development
eval $(uv run vault env --tag development)
```

---

## Scenario 4: Expiry Tracking

```bash
# Add a temporary key (expires in 90 days)
$ uv run vault add TEMP_API_KEY "xyz123" --expires 2026-06-15 --tag temporary
✅ Added credential: TEMP_API_KEY

# Check what's expiring soon (within 30 days)
$ uv run vault expiring --days 30
⚠️  Credentials expiring within 30 days:

  ⚠️  15 days - TEMP_API_KEY
     Expires: 2026-06-15
     Tags: temporary

# Rotate the key before it expires
$ uv run vault rotate TEMP_API_KEY
Enter new value for TEMP_API_KEY: ********
🔄 Rotated credential: TEMP_API_KEY
```

---

## Scenario 5: Audit Trail

```bash
# Check recent access
$ uv run vault audit --last 10
📝 Audit Log (last 10 entries):

  [2026-03-17T14:35:00] get: OPENAI_API_KEY
  [2026-03-17T14:30:00] add: TAVILY_API_KEY
     Details: {'tags': ['tavily'], 'expires': '2027-01-01'}
  [2026-03-17T14:25:00] unlock: vault
     Details: {'action': 'unlocked'}
  [2026-03-17T14:00:00] rotate: TEMP_API_KEY
  [2026-03-17T13:55:00] env: tag:production
     Details: {'count': 3}
```

---

## Scenario 6: Integrating with OpenClaw Skills

### Tavily Search Skill

**Before (plaintext `.env`):**
```bash
# .env
TAVILY_API_KEY=tvly-abc123...

# Run skill
source .env
python scripts/search.py "OpenClaw"
```

**After (encrypted vault):**
```bash
# Add key to vault (one-time)
uv run vault add TAVILY_API_KEY "tvly-abc123..." --tag tavily

# Run skill (every time)
uv run vault unlock
eval $(uv run vault env --tag tavily)
python scripts/search.py "OpenClaw"
```

### Auto-Unlock in HEARTBEAT.md

```markdown
# HEARTBEAT.md

1. Check if vault is unlocked:
   - If locked: Notify user to run `vault unlock`
   - If unlocked: Proceed with daily checks

2. Export credentials for scheduled tasks:
   ```bash
   eval $(vault env --tag scheduled)
   ```

3. Run checks (email, calendar, etc.)
```

---

## Scenario 7: Migrating from `.env`

**Old setup (`.env`):**
```bash
OPENAI_API_KEY=sk-proj-abc123
ANTHROPIC_API_KEY=sk-ant-xyz789
TAVILY_API_KEY=tvly-def456
GITHUB_TOKEN=ghp_ghi789
```

**Migration script:**
```bash
#!/bin/bash
# migrate_to_vault.sh

# Unlock vault
uv run vault unlock

# Read .env and add to vault
while IFS='=' read -r key value; do
  # Skip comments and empty lines
  [[ "$key" =~ ^#.*$ ]] && continue
  [[ -z "$key" ]] && continue
  
  # Add to vault (auto-tag by prefix)
  echo "Adding $key..."
  uv run vault add "$key" "$value" --tag "$(echo $key | cut -d_ -f1 | tr '[:upper:]' '[:lower:]')"
done < .env

# Verify
uv run vault list

# Lock vault
uv run vault lock

echo "✅ Migration complete. You can now delete .env (but keep a backup!)"
```

**Run migration:**
```bash
chmod +x migrate_to_vault.sh
./migrate_to_vault.sh
```

---

## Scenario 8: Key Rotation Workflow

```bash
# Step 1: Check expiring keys
$ uv run vault expiring --days 14
⚠️  Credentials expiring within 14 days:
  ⚠️  7 days - GITHUB_TOKEN
     Expires: 2026-03-24

# Step 2: Generate new key (in GitHub web UI)
# ...

# Step 3: Rotate in vault
$ uv run vault rotate GITHUB_TOKEN
Enter new value for GITHUB_TOKEN: ghp_NEW_TOKEN_HERE
🔄 Rotated credential: GITHUB_TOKEN

# Step 4: Update expiry
$ uv run vault add GITHUB_TOKEN "ghp_NEW_TOKEN_HERE" --expires 2027-03-24
✅ Added credential: GITHUB_TOKEN

# Step 5: Verify
$ uv run vault get GITHUB_TOKEN
ghp_NEW_TOKEN_HERE
```

---

## Scenario 9: Bulk Export for CI/CD

```bash
# Export all production keys as .env format
$ uv run vault unlock
$ uv run vault env --tag production > /tmp/prod.env

# Use in CI
$ source /tmp/prod.env
$ echo $OPENAI_API_KEY
sk-proj-abc123...

# Clean up
$ shred -u /tmp/prod.env  # Securely delete
```

⚠️ **Warning:** Only do this in trusted CI environments. Prefer native secret management (GitHub Actions secrets, GitLab CI variables, etc.).

---

## Scenario 10: Debugging Access Issues

```bash
# Problem: Script can't find API key
$ python my_script.py
❌ OPENAI_API_KEY not found

# Debug: Check if key exists
$ uv run vault unlock
$ uv run vault list | grep OPENAI
  🔑 OPENAI_API_KEY

# Debug: Get the key
$ uv run vault get OPENAI_API_KEY
sk-proj-abc123...

# Debug: Check if env is set
$ echo $OPENAI_API_KEY
(empty)

# Fix: Export from vault
$ eval $(uv run vault env --tag openai)
$ echo $OPENAI_API_KEY
sk-proj-abc123...

# Retry
$ python my_script.py
✅ Success!
```

---

## Scenario 11: Team Onboarding (Manual Key Sharing)

**When a new team member joins:**

```bash
# Team lead: Export keys securely
$ uv run vault unlock
$ uv run vault env --tag shared > shared_keys.txt
$ gpg -c shared_keys.txt  # Encrypt with GPG
$ rm shared_keys.txt
# Send shared_keys.txt.gpg via secure channel (Signal, encrypted email)

# New team member: Import keys
$ gpg -d shared_keys.txt.gpg > shared_keys.txt
$ uv run vault unlock

# Import each key
$ while IFS='=' read -r key value; do
    uv run vault add "$key" "$value" --tag shared
  done < shared_keys.txt

# Clean up
$ shred -u shared_keys.txt
$ uv run vault lock
```

⚠️ **Better approach:** Use proper secrets management (1Password Teams, HashiCorp Vault) for team sharing.

---

## Scenario 12: Scheduled Tasks (Cron)

**Setup vault auto-unlock (⚠️ security tradeoff):**

```bash
# Option 1: Store master password in a separate file (less secure)
echo "my-master-password" > ~/.vault_password
chmod 600 ~/.vault_password

# Cron job
0 9 * * * cat ~/.vault_password | /path/to/vault unlock && eval $(/path/to/vault env --tag daily) && /path/to/daily_task.sh

# Option 2: Keep vault unlocked (least secure)
# Run 'vault unlock' once, don't lock
# Cron job will use existing session key
```

⚠️ **Security note:** Both options reduce security. For production, use proper secrets management with API-based retrieval.

---

## Tips & Tricks

### Alias for convenience
```bash
# Add to ~/.zshrc or ~/.bashrc
alias v='uv run vault'
alias venv='eval $(uv run vault env)'

# Usage
v unlock
venv --tag openai
```

### Quick credential check
```bash
# Check if a key is set
v get OPENAI_API_KEY >/dev/null 2>&1 && echo "✅ Set" || echo "❌ Missing"
```

### Backup vault
```bash
cp ~/.openclaw/vault/vault.enc.json ~/Dropbox/backups/vault-$(date +%Y%m%d).json
```

### Restore vault
```bash
cp ~/Dropbox/backups/vault-20260317.json ~/.openclaw/vault/vault.enc.json
```

---

## Common Mistakes

### ❌ Forgetting to unlock
```bash
$ v get OPENAI_API_KEY
❌ Vault is locked. Run 'vault unlock' first.
```

**Fix:** Always `v unlock` first.

### ❌ Exporting without `eval`
```bash
$ v env --tag openai  # Wrong! Just prints, doesn't export
OPENAI_API_KEY=sk-proj-abc123

$ echo $OPENAI_API_KEY
(empty)
```

**Fix:** Use `eval`:
```bash
$ eval $(v env --tag openai)
$ echo $OPENAI_API_KEY
sk-proj-abc123
```

### ❌ Storing master password in plaintext
```bash
# DON'T DO THIS
echo "my-password" > ~/.vault_pass
```

**Fix:** Use a password manager (1Password, Bitwarden) or remember it.

---

## Next Steps

- Read [SKILL.md](./SKILL.md) for security model details
- Read [README.md](./README.md) for CLI reference
- Integrate with your OpenClaw skills
- Set up expiry tracking for API keys
