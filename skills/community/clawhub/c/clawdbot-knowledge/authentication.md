# Authentication Guide

## Overview

OpenClaw supports subscription authentication via OAuth for providers that offer it, particularly OpenAI Codex (ChatGPT OAuth). For Anthropic subscriptions, use the setup-token flow. This guide explains how OAuth token exchange works, where tokens are stored, and how to manage multiple accounts.

## OAuth Support

### Provider Compatibility
- **OpenAI Codex**: Full OAuth support with PKCE flow
- **Anthropic**: Setup-token flow (subscription authentication)
- **Other Providers**: Via provider plugins that bring their own OAuth/API key flows

### Command Execution
```bash
# Login with OAuth for specific provider
openclaw models auth login --provider <id>
```

## The Token Sink (Why It Exists)

### Problem: Concurrent Login Conflicts
OAuth providers typically generate new refresh tokens on each login/refresh operation. Some providers (or OAuth clients) may invalidate older refresh tokens when a new one is issued for the same user/app.

**Practical Symptom**: You log in via OpenClaw and via Claude Code/Codex CLI → one of them will randomly get logged out later.

### Solution: Central Token Sink
To reduce this issue, OpenClaw treats `auth-profiles.json` as a central token sink:
- **Runtime Environment**: Reads credentials from one place
- **Multiple Profiles**: Can manage and deterministically route multiple profiles
- **Conflict Prevention**: Reduces concurrent login issues

## Token Storage

### Storage Location (Per Agent)
Secrets are stored per agent:

#### Authentication Profiles (OAuth + API Keys)
- **Location**: `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
- **Purpose**: Primary storage for OAuth tokens and API keys
- **Format**: JSON with provider, profile, and token data
- **Security**: Per-agent isolation

#### Runtime Cache (Auto-Managed)
- **Location**: `~/.openclaw/agents/<agentId>/agent/auth.json`
- **Purpose**: Runtime cache (automatically managed; do not edit)
- **Content**: Current active tokens and session data
- **Management**: Automatically updated, do not modify manually

#### Legacy Import File (Still Supported)
- **Location**: `~/.openclaw/credentials/oauth.json`
- **Purpose**: Legacy import location (still supported, but not primary storage)
- **Behavior**: Imported into `auth-profiles.json` on first use
- **Migration**: Automatic migration to new location

### State Directory Override
All above configurations respect `$OPENCLAW_STATE_DIR` state directory override for custom locations.

## Anthropic Setup-Token (Subscription Authentication)

### Step 1: Generate Setup Token
On any machine, run:
```bash
claude setup-token
```

### Step 2: Insert Token in OpenClaw
```bash
openclaw models auth setup-token --provider anthropic
```

### Step 3: Manual Token Insertion (Alternative)
If you generated token elsewhere, insert manually:
```bash
openclaw models auth paste-token --provider anthropic
```

### Step 4: Verification
```bash
openclaw models status
```

### Authentication Profile Result
- **Storage**: Stored as token authentication profile
- **Refresh**: No refresh mechanism (setup tokens are static)
- **Usage**: Used directly for API authentication

## OAuth Exchange (How Login Works)

### Interactive Login Processes
OpenClaw's interactive login processes are implemented in `@mariozechner/pi-aid` and connected with assistants/commands.

### Anthropic (Claude Pro/Max) Setup-Token Flow
1. **Generate**: Run `claude setup-token`
2. **Insert**: Paste token into OpenClaw
3. **Store**: Save as token authentication profile (no refresh)
4. **Use**: Direct authentication with static token

### OpenAI Codex (ChatGPT OAuth) PKCE Flow
1. **Generate PKCE**: Generate PKCE verifier/challenge + random state
2. **Authorize**: Open `https://auth.openai.com/oauth/authorize?...`
3. **Intercept**: Try to intercept callback at `http://127.0.0.1:1455/auth/callback`
4. **Fallback**: If callback can't bind (or remote/headless), manually enter redirect URL/code
5. **Exchange**: Exchange at `https://auth.openai.com/oauth/token`
6. **Extract**: Extract `accountId` from access token and store `{access, refresh, expires, accountId}`

### Assistant Integration Path
The assistant path for OpenClaw onboard → Authentication selection is `openai-codex`.

## Refresh + Expiration

### Profile Structure
Profiles store an `expires` timestamp for time-based management.

### Runtime Behavior
- **Future Expiry**: If `expires` is in future → use stored access token
- **Expired Token**: If expired → refresh (under file lock) and overwrite stored credentials

### Automatic Refresh
- **Process**: Refresh process is automatic
- **Management**: No manual token management typically required
- **File Locking**: Refresh operations use file locking to prevent race conditions

### Manual Intervention
- **Necessity**: Rarely needed due to automatic refresh
- **Force Refresh**: Can be triggered via re-login if needed
- **Profile Reset**: Delete and recreate profile if issues occur

## Multiple Accounts (Profiles) + Routing

### Two Management Patterns

#### Pattern 1: Separate Agents (Preferred)
If you want to prevent "private" and "work" from interacting, use isolated agents (separate sessions + credentials + workspaces):

```bash
# Create separate agents
openclaw agents add work
openclaw agents add personal

# Configure authentication per agent (assistant)
# Route chats to the right agent
```

**Benefits:**
- **Complete Isolation**: Separate workspaces, sessions, and credentials
- **No Cross-Contamination**: Work and personal data completely separate
- **Clear Separation**: Easy to manage and understand

#### Pattern 2: Multiple Profiles in One Agent (Advanced)
`auth-profiles.json` supports multiple profile IDs for the same provider.

**Profile Selection:**
- **Global**: Via configuration order (`auth.order`)
- **Per Session**: Via `/model ...@<profileId>`

**Example (Session Override):**
```
User: Use my work profile for this task
Agent: /model gpt-4@work-profile [your task here]
```

### Profile ID Discovery
Find available profile IDs:
```bash
openclaw channels list --json  # Shows auth[] section
```

### Related Documentation
- **Model Failover**: `/concepts/model-failover` (rotation and cooldown rules)
- **Slash Commands**: `/tools/slash-commands` (command interface)

## Configuration Examples

### Basic Authentication Configuration
```json
{
  "models": {
    "defaults": {
      "model": "openai/gpt-4"
    }
  },
  "auth": {
    "order": ["work-profile", "personal-profile"]
  }
}
```

### Multi-Profile Configuration
```json
{
  "agents": {
    "work": {
      "workspace": "~/.openclaw/workspace-work",
      "model": "anthropic/claude-3-opus@work-profile"
    },
    "personal": {
      "workspace": "~/.openclaw/workspace-personal", 
      "model": "openai/gpt-4@personal-profile"
    }
  }
}
```

## Security Considerations

### Token Protection
- **Storage**: Tokens stored per-agent in dedicated locations
- **Permissions**: File permissions restrict access to token files
- **Encryption**: Tokens stored in encrypted format when possible
- **Backup**: Exclude tokens from backups (use .gitignore)

### Network Security
- **OAuth Flow**: Uses HTTPS for all OAuth communications
- **Local Callback**: Callback server binds to localhost only
- **Token Transmission**: Tokens transmitted over secure channels only

### Best Practices
1. **Regular Rotation**: Regularly refresh tokens when possible
2. **Profile Separation**: Use separate profiles for different contexts
3. **Access Control**: Restrict file system access to token files
4. **Monitoring**: Monitor authentication status regularly

## Troubleshooting

### Common Issues

#### Concurrent Login Conflicts
- **Symptom**: Random logouts when using multiple clients
- **Solution**: Use central token sink configuration
- **Prevention**: Use separate agents for different contexts

#### Token Expiration
- **Symptom**: Authentication failures after token expiry
- **Solution**: Automatic refresh should handle this
- **Manual Fix**: Re-login if automatic refresh fails

#### Profile Not Found
- **Symptom**: "Profile not found" errors
- **Solution**: Check profile IDs with `openclaw channels list --json`
- **Fix**: Correct profile ID in configuration

#### Permission Denied
- **Symptom**: Cannot read/write token files
- **Solution**: Check file permissions and ownership
- **Fix**: Adjust permissions or run with correct user

### Debug Commands
```bash
# Check authentication status
openclaw models status

# List available profiles
openclaw channels list --json

# Test authentication
openclaw models test --provider <provider>

# Refresh specific profile
openclaw models refresh --provider <provider> --profile <profile-id>

# Remove problematic profile
openclaw models remove --provider <provider> --profile <profile-id>
```

### Debug Information
Enable debug logging for detailed authentication information:
```bash
openclaw --verbose models auth login --provider <provider>
```

## Advanced Configuration

### Custom OAuth Providers
Create provider plugins with custom OAuth flows:
```python
# Custom provider plugin example
class CustomOAuthProvider:
    def get_auth_url(self):
        # Return OAuth authorization URL
        pass
    
    def exchange_code(self, code):
        # Exchange authorization code for tokens
        pass
    
    def refresh_token(self, refresh_token):
        # Refresh expired tokens
        pass
```

### Environment Variable Configuration
Set authentication-related environment variables:
```bash
# State directory override
export OPENCLAW_STATE_DIR="/custom/state/path"

# Default provider
export OPENCLAW_DEFAULT_PROVIDER="openai"

# Default model
export OPENCLAW_DEFAULT_MODEL="gpt-4"
```

### File Permissions
Set appropriate file permissions for token files:
```bash
# Restrict access to token files
chmod 600 ~/.openclaw/agents/*/agent/auth-profiles.json
chmod 600 ~/.openclaw/agents/*/agent/auth.json
```