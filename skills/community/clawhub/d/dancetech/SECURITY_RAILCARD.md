# Security Railcard System

## Overview

The Security Railcard is a multi-layered defense system preventing API key and secret exposure in automated agent workflows. It combines pre-commit hooks, runtime scanning, and configuration best practices.

## Components

### 1. Pre-commit Hook (`.git/hooks/pre-commit`)

Automatically scans all staged files for patterns that look like real secrets before allowing a commit.

**Installation:** The hook is automatically installed when you set up an agent workspace via the skill package. It's a symlink to `scripts/tools/security-check.js`.

**What it scans for:**
- OpenRouter API keys (`sk-or-v1-...`)
- GitHub tokens (`ghp_`, `gho_`, etc.)
- Generic API keys/tokens
- Private keys (hex)
- Bearer tokens
- Moltbook keys
- Privy app secrets

**Placeholders allowed:** `your_`, `example`, `placeholder`, `changeme`, `xxx`, `replace`, `test_`, `dummy`

### 2. Runtime Security Scan (`scripts/tools/security_railcard.js`)

Called by automation scripts (`dancetech_cycle.js`, `colosseum_cycle.js`) before pushing generated code to GitHub. Scans the entire temporary build directory.

**Exits 0** if safe, **1** if secrets detected.

**Excluded paths:** `node_modules/`, `.git/`, `dist/`, `build/`, `coverage/`, `.env.example`, `README.md`, documentation, images, tests.

### 3. Environment-Based Configuration

All sensitive credentials are stored in `.env` (gitignored) and loaded at runtime:

```
OPENROUTER_API_KEY=
GITHUB_PUBLIC_TOKEN=
MOLTBOOK_API_KEY=
PRIVY_APP_ID=
PRIVY_APP_SECRET=
```

Code that needs these values uses `process.env.VAR_NAME` (Node.js) or equivalent.

### 4. Safe Configuration Files

Files like `models.json` should contain placeholders, not real values. The agent loads environment variables and injects them at runtime, not from config.

Example `models.json`:
```json
{
  "providers": {
    "openrouter": {
      "baseUrl": "https://openrouter.ai/api/v1",
      "apiKey": "",  // Filled from .env at runtime
      "models": [...]
    }
  }
}
```

## Usage for Developers

### When creating new automation scripts:

1. **Before pushing to GitHub:**
   ```javascript
   const railcardPath = path.join(WORKSPACE, 'scripts', 'tools', 'security_railcard.js');
   const scanCmd = `node "${railcardPath}" "${tempDir}"`;
   const scanResult = execSync(scanCmd, { encoding: 'utf8' });
   if (!scanResult.includes('No secrets')) {
     throw new Error('Security railcard blocked push');
   }
   ```

2. **Keep .env patterns:**
   - Never commit `.env`
   - Use `.env.example` with placeholder values for documentation

### If the railcard blocks your commit:

1. Identify the file and line from the error message.
2. Replace the real secret with a placeholder or move it to `.env`.
3. Use `process.env.YOUR_KEY` in code instead of hardcoding.
4. Re-stage and commit.

## Recovery from Exposure (like the 2026-02-12 incident)

1. Immediately revoke the exposed key at the source (OpenRouter, GitHub, etc.)
2. Generate a new key
3. Update `.env` files in all agent workspaces
4. Verify that no config file (`models.json`, `config.json`, etc.) contains the old key
5. Check git history: if the key was committed, use `git filter-branch` or BFG to purge it
6. Rotate all other credentials that might share patterns

## Maintenance

To update secret patterns, edit `SECRET_PATTERNS` array in `scripts/tools/security_railcard.js`.

Add new regex patterns for any credential types you introduce.

## Testing

Run a manual scan from the skill root:
```bash
node scripts/tools/security_railcard.js .
```

Test the pre-commit hook by staging a file containing a fake key like:
```javascript
const key = 'sk-or-v1-fakebutlongenoughstring1234567890';
```
The hook should block the commit.
