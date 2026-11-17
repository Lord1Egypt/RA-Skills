---
name: checkly-auth
description: Manage Checkly CLI authentication including login/logout, current user and service API keys, legacy-key migration, auth status, and account switching. Use when setting up Checkly CLI for the first time or troubleshooting credentials. Triggers on checkly login, checkly logout, authentication, user API key, service API key, legacy account API key, account ID, credentials.
---

# checkly auth

Manage Checkly CLI authentication.

## Quick start

```bash
# Interactive login (browser-based)
npx checkly login

# Check authentication status
npx checkly whoami

# Switch to a known account in multi-account setups
npx checkly switch --account-id <account-id>

# Log out of saved local-session credentials
npx checkly logout

# Manual configuration (for CI/CD)
export CHECKLY_API_KEY="your-api-key"
export CHECKLY_ACCOUNT_ID="your-account-id"
```

## Authentication methods

Checkly accepts two current API-key types in addition to browser login credentials:

- **User API key (`cu_...`)**: tied to one user and inherits that user's roles and account memberships. Create it under **User Settings → API Keys**.
- **Service API key (`sv_...`)**: tied to one account with a role assigned to the key. Create it under **Account Settings → API Keys**; service keys require an Enterprise plan.

Deprecated account API keys and old `sk_...` service-key formats are legacy credentials. Do not use them for organization usage reporting. Never print a key while identifying its type.

### Interactive login (recommended for local development)

```bash
npx checkly login
```

Opens browser to authenticate and automatically saves credentials to your system config.

**Credential storage location:**
- Linux/macOS: `~/.config/@checkly/cli/config.json`
- Windows: `%APPDATA%\@checkly\cli\config.json`

### Environment variables (recommended for CI/CD)

```bash
export CHECKLY_API_KEY="cu_abc123..."
export CHECKLY_ACCOUNT_ID="12345"

# Test authentication
npx checkly whoami
```

**Getting your credentials:**
1. For a personal user key, open [User Settings → API Keys](https://app.checklyhq.com/settings/user/api-keys) and create a `cu_...` key.
2. For a stable account-scoped automation identity on Enterprise, open [Account Settings → API Keys](https://app.checklyhq.com/settings/account/api-keys), create a service key, and assign the least required role; current service keys start with `sv_...`.
3. Copy the target Account ID from the URL or **Account Settings → General**.

`npx checkly login` is the preferred local-development path and creates an accepted user-scoped browser session without requiring you to copy a key into the shell.

Environment variables take precedence over saved `npx checkly login` credentials. `npx checkly whoami` tells you when the active account is resolved from `CHECKLY_API_KEY` / `CHECKLY_ACCOUNT_ID`, and `npx checkly logout` warns if those env vars still keep you authenticated after local session cleanup.

### Configuration file (manual)

Create/edit config file at `~/.config/@checkly/cli/config.json`:

```json
{
  "apiKey": "cu_abc123...",
  "accountId": "12345"
}
```

## Workflows

### First-time setup

1. **Sign up for Checkly account** (if needed):
   ```bash
   # Opens signup page
   npx checkly login
   ```

2. **Authenticate CLI**:
   ```bash
   npx checkly login
   ```

3. **Verify authentication**:
   ```bash
   npx checkly whoami
   ```

   Expected output:
   ```
   Logged in as john@example.com
   Account: Acme Corp (ID: 12345)
   ```

4. **Initialize project**:
   ```bash
   npm create checkly@latest
   ```

### Switching accounts

If you have multiple Checkly accounts:

1. **List or verify the current account**:
   ```bash
   npx checkly whoami
   ```

2. **Switch directly when you know the target account ID**:
   ```bash
   npx checkly switch --account-id <account-id>
   ```

3. **If you need a fresh browser login, clear saved local-session credentials first**:
   ```bash
   npx checkly logout --force
   npx checkly login
   ```

4. **Verify the selected account**:
   ```bash
   npx checkly whoami
   ```

If `CHECKLY_API_KEY` or `CHECKLY_ACCOUNT_ID` are set in the shell or a project `.env`, they override the saved account. Remove or update those variables before using `login` / `switch` to change the effective account.

### CI/CD authentication

For automated pipelines (GitHub Actions, GitLab CI, etc.):

1. **Create a current API key in Checkly UI**:
   - Prefer an account-scoped service API key (`sv_...`) for shared/non-interactive automation when the Enterprise feature is available.
   - Otherwise create a dedicated user API key (`cu_...`) under the automation user's **User Settings → API Keys**; it remains tied to that user's membership.
   - Assign the least role needed by the pipeline: read-only inspection does not need deploy permissions, while deployment needs write access.

2. **Add secrets to CI/CD platform**:
   - `CHECKLY_API_KEY`: Your API key
   - `CHECKLY_ACCOUNT_ID`: Your account ID

3. **Use in pipeline**:
   ```yaml
   # GitHub Actions example
   - name: Test checks
     env:
       CHECKLY_API_KEY: ${{ secrets.CHECKLY_API_KEY }}
       CHECKLY_ACCOUNT_ID: ${{ secrets.CHECKLY_ACCOUNT_ID }}
     run: npx checkly test
   
   - name: Deploy checks
     env:
       CHECKLY_API_KEY: ${{ secrets.CHECKLY_API_KEY }}
       CHECKLY_ACCOUNT_ID: ${{ secrets.CHECKLY_ACCOUNT_ID }}
     run: npx checkly deploy --force
   ```

## Troubleshooting

### "Could not find Checkly credentials"

**Cause**: No authentication configured

**Solution**:
```bash
# Option 1: Interactive login
npx checkly login

# Option 2: Set environment variables
export CHECKLY_API_KEY="your-key"
export CHECKLY_ACCOUNT_ID="your-account-id"
```

### `whoami` still shows an account after logout

**Cause**: `CHECKLY_API_KEY` or `CHECKLY_ACCOUNT_ID` are still set in the shell or loaded from a project `.env`. `npx checkly logout` can clear saved local-session credentials but cannot remove environment variables.

**Solution**:
```bash
# Inspect environment-backed credentials without printing secret values
env | grep '^CHECKLY_.*=' | sed 's/=.*$/=<set>/'

# Unset for the current shell if you want to use browser login credentials instead
unset CHECKLY_API_KEY CHECKLY_ACCOUNT_ID
npx checkly whoami
```

### "401 Unauthorized"

**Possible causes**:
- API key has been deleted or revoked
- API key doesn't have required permissions
- Account ID doesn't match API key

**Solution**:
1. Verify credentials:
   ```bash
   npx checkly whoami
   ```

2. If invalid, re-authenticate:
   ```bash
   npx checkly login
   ```

3. For CI/CD, regenerate API key in Checkly UI

### "Account not found"

**Cause**: Account ID is incorrect

**Solution**:
1. Log into [app.checklyhq.com](https://app.checklyhq.com)
2. Check URL: `app.checklyhq.com/accounts/{ACCOUNT_ID}/...`
3. Or check Account Settings → Account ID
4. Update `CHECKLY_ACCOUNT_ID` environment variable

### Permission errors during deploy

**Cause**: API key has read-only permissions

**Solution**:
1. Go to Account Settings → API Keys in Checkly UI
2. Create new API key with "Read/Write" permissions
3. Update your API key

## Environment variables reference

| Variable | Required | Description |
|----------|----------|-------------|
| `CHECKLY_API_KEY` | Yes | Current user (`cu_...`) or service (`sv_...`) API key |
| `CHECKLY_ACCOUNT_ID` | Yes | Numeric account ID |
| `CHECKLY_API_URL` | No | Override the local API URL when `CHECKLY_ENV=local` (default: `http://127.0.0.1:3000`) |
| `CHECKLY_MQTT_URL` | No | Override the local events/MQTT broker when `CHECKLY_ENV=local` |
| `CHECKLY_SKIP_AUTH` | No | Skip authentication (for debugging flags) |

`CHECKLY_MQTT_URL` is advanced troubleshooting configuration for local or custom setups where test-session event streams come from a different broker. It is analogous to `CHECKLY_API_URL` for local endpoint overrides, not a normal hosted Checkly credential or default CI setting.

## Security best practices

### Local development

- ✅ Use `npx checkly login` (credentials stored securely)
- ✅ Add config file to `.gitignore` (if using manual config)
- ❌ Don't commit API keys to version control

### CI/CD pipelines

- ✅ Store credentials as encrypted secrets
- ✅ Use API keys with minimal required permissions
- ✅ Rotate API keys regularly
- ❌ Don't log API keys in pipeline output

### API key management

- ✅ Create separate API keys for different purposes (CI/CD, local dev)
- ✅ Name keys descriptively ("GitHub Actions Deploy", "John's Laptop")
- ✅ Revoke unused or compromised keys immediately
- ❌ Don't share API keys between team members

## Related Skills

**Next steps after authentication:**
- See `checkly-config` to configure your project
- See `checkly-test` to run checks locally
- See `checkly-deploy` to deploy checks to Checkly
- See `checkly-usage` for account plan/entitlement checks and organization usage access requirements

**Project setup:**
- New project: Use `npm create checkly@latest` (includes auth setup)
- Existing project: Install `checkly` package and authenticate
