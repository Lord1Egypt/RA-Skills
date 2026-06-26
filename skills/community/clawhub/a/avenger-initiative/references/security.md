# Security Reference — Avenger Initiative

## Threat Model

| Threat | Mitigation |
|--------|------------|
| GitHub breach / repo goes public | `openclaw.json` encrypted with AES-256 |
| Stolen encryption key | Without the vault, key alone is useless |
| Stolen vault (repo) | Without the key, `.enc` files are unreadable |
| Key lost | All API keys must be regenerated manually |

## Encryption Details

- **Algorithm:** AES-256-CBC
- **Key derivation:** PBKDF2 with 100,000 iterations (SHA-256)
- **Key format:** 64 hex chars (256 bits of entropy)
- **What's encrypted:** Only `openclaw.json` (contains all API keys, bot tokens)
- **Everything else:** Plaintext (no secrets in SOUL.md, MEMORY.md, etc.)

## Key Rotation

To rotate the encryption key:

```bash
# 1. Generate new key
openssl rand -hex 32 > /tmp/new.key

# 2. Decrypt with old key
OLD_KEY=$(cat ~/.openclaw/credentials/avenger.key)
openssl enc -d -aes-256-cbc -pbkdf2 -iter 100000 \
  -pass "pass:$OLD_KEY" \
  -in config/openclaw.json.enc \
  -out /tmp/openclaw_plain.json

# 3. Re-encrypt with new key
NEW_KEY=$(cat /tmp/new.key)
openssl enc -aes-256-cbc -pbkdf2 -iter 100000 \
  -pass "pass:$NEW_KEY" \
  -in /tmp/openclaw_plain.json \
  -out config/openclaw.json.enc

# 4. Install new key
cp /tmp/new.key ~/.openclaw/credentials/avenger.key
rm /tmp/new.key /tmp/openclaw_plain.json

# 5. Commit updated vault
cd /path/to/vault && git add config/openclaw.json.enc && git commit -m "🔐 Key rotation" && git push
```

## What Is NOT Backed Up

- `/root/.openclaw/.env` (excluded intentionally — usually just API overrides)
- `/root/.openclaw/credentials/avenger.key` (never goes to git)
- `node_modules/` directories
- Large binary files, PDFs, images
- `/root/.openclaw/media/` (user-uploaded media)

## Vault Repo Recommendations

- Set repo to **private** (GitHub → Settings → Danger Zone → Change visibility)
- Enable **branch protection** on `main` (prevents force-push accidents)
- Enable **secret scanning** (GitHub will alert if a key is accidentally committed)
- Consider enabling **2FA** on the GitHub account owning the vault
