# Publishing to ClawHub

This document provides verification steps for publishing this skill to ClawHub.

## Pre-Publish Checklist

Before running `clawhub publish`, verify:

### 1. Metadata Format Validation

The root `SKILL.md` frontmatter must use the **ClawHub metadata format**, not the legacy `requirements:` format.

**✅ Correct format:**
```yaml
metadata:
  {
    "openclaw":
      {
        "emoji": "✓",
        "requires": { "bins": ["checkly", "npx"], "env": ["CHECKLY_API_KEY", "CHECKLY_ACCOUNT_ID"] },
        "primaryEnv": "CHECKLY_API_KEY",
        ...
      },
  }
```

**❌ Incorrect format (will not publish metadata correctly):**
```yaml
requirements:
  binaries:
    - checkly
  env_vars:
    - CHECKLY_API_KEY
```

### 2. Required Metadata Fields

Ensure `SKILL.md` frontmatter includes:

- ✅ `metadata.openclaw.requires.bins` - Array of required binaries
- ✅ `metadata.openclaw.requires.env` - Array of required environment variables
- ✅ `metadata.openclaw.primaryEnv` - Primary authentication env var (if applicable)
- ✅ `metadata.openclaw.emoji` - Display emoji (optional but recommended)
- ✅ `metadata.openclaw.install` - Array of installation methods (optional but helpful)

### 3. Example Variables Are Clearly Marked

Check documentation files for user-defined example variables:

- `API_TOKEN` - User's API authentication token (NOT Checkly CLI requirement)
- `TEST_EMAIL` - User's test login email (NOT Checkly CLI requirement)
- `TEST_PASSWORD` - User's test login password (NOT Checkly CLI requirement)
- `API_BASE_URL` - User's API base URL (NOT Checkly CLI requirement)

These should be clearly documented as **examples** for user-specific checks, not as skill installation requirements.

**Look for clarifying comments like:**
- "Note: API_TOKEN is a user-defined environment variable for YOUR API checks."
- "Example variables for YOUR checks - NOT required by Checkly CLI itself."

### 4. Actual Runtime Requirements

Verify the actual skill requirements:

**Required binaries:**
- `checkly` - Checkly CLI
- `npx` - npm package runner (usually bundled with Node.js)

**Required environment variables:**
- `CHECKLY_API_KEY` - Checkly API key for deployment
- `CHECKLY_ACCOUNT_ID` - Checkly account ID

**Optional binaries:**
- `playwright` - For browser checks (documented in notes, not in strict requires)

**Optional environment variables:**
- User-defined variables (API_TOKEN, TEST_EMAIL, etc.) - These are for user's own checks

## Publishing Steps

### 1. Authenticate

```bash
clawhub login
clawhub whoami  # Verify authentication
```

### 2. Test Locally

Before publishing, verify the skill works:

```bash
# In a test environment
cd /path/to/checkly-cli-skills
export CHECKLY_API_KEY=your_test_key
export CHECKLY_ACCOUNT_ID=your_test_account

# Verify binaries are available
which checkly
which npx

# Test sub-skill invocation (if applicable)
```

### 3. Publish

```bash
clawhub publish . \
  --slug checkly-cli-skills \
  --name "Checkly CLI Skills" \
  --version 1.0.4 \
  --changelog "Refresh Checkly CLI skills for 8.7.0 members and test-sessions commands"
```

### 4. Verify Published Metadata

After publishing, verify the registry shows correct metadata:

```bash
clawhub search checkly-cli-skills
```

**Check the output shows:**
- ✅ Required binaries: `checkly`, `npx`
- ✅ Required env vars: `CHECKLY_API_KEY`, `CHECKLY_ACCOUNT_ID`
- ✅ NO mention of `API_TOKEN`, `TEST_EMAIL`, `TEST_PASSWORD` as required

If metadata is missing or incorrect, the frontmatter format may be wrong.

### 5. Test Installation

In a clean environment, test installation:

```bash
clawhub install checkly-cli-skills --version 1.0.4
```

Verify ClawHub warns about missing binaries/env vars if they're not available.

## Common Issues

### Issue: ClawHub shows no required binaries or env vars

**Cause:** Frontmatter uses `requirements:` format instead of `metadata.openclaw.requires`

**Fix:** Convert frontmatter to ClawHub metadata format (see section 1 above)

### Issue: Example variables (API_TOKEN, etc.) shown as required

**Cause:** Documentation doesn't clearly distinguish user-defined variables from skill requirements

**Fix:** Add clarifying comments in code examples (see section 3 above)

### Issue: Metadata format validation error

**Cause:** YAML/JSON syntax error in frontmatter

**Fix:** Validate frontmatter JSON structure:
```bash
# Extract and validate frontmatter
head -40 SKILL.md | grep -A 30 "metadata:" | python3 -m json.tool
```

## Version History

- **v1.0.2** - Added `checkly deploy --verbose` documentation
- **v1.0.3** - Fixed ClawHub metadata format and clarified example env vars
- **v1.0.4** - Refreshed Checkly CLI 8.7.0 coverage for members and test-sessions commands

## References

- ClawHub metadata format: See `/opt/homebrew/lib/node_modules/openclaw/skills/*/SKILL.md` for examples
- ClawHub CLI: `clawhub --help` and `clawhub publish --help`
