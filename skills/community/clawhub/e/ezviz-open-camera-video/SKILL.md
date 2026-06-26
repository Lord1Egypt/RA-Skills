---
name: ezviz-open-video
description: |
  Ezviz camera video streaming skill. Generates PC and mobile links for live and playback streams.
  Use when: Need to view camera live feed, playback recordings, generate preview links, remote monitoring.
  
  ⚠️ Security: Requires EZVIZ_APP_KEY and EZVIZ_APP_SECRET environment variables with minimal permissions.
metadata:
  openclaw:
    emoji: "📺"
    requires:
      env: ["EZVIZ_APP_KEY", "EZVIZ_APP_SECRET"]
      pip: ["requests"]
    primaryEnv: "EZVIZ_APP_KEY"
    warnings:
      - "Requires Ezviz credentials with minimal permissions"
      - "Token cached in system temp directory (shared across skills, configurable)"
      - "May read ~/.openclaw/*.json for credentials (env vars have priority)"
      - "Install requests: pip install requests"
    config:
      tokenCache:
        default: true
        envVar: "EZVIZ_TOKEN_CACHE"
        description: "Enable token caching (default: true). Set to 0 to disable. Cache path: /tmp/ezviz_global_token_cache/"
        path: "/tmp/ezviz_global_token_cache/global_token_cache.json"
        permissions: "0600"
        security: "Global cache shared across skills. For isolation: disable caching, use isolated environment, or control cache path."
      configFileRead:
        paths:
          - "~/.openclaw/config.json"
          - "~/.openclaw/gateway/config.json"
          - "~/.openclaw/channels.json"
        priority: "lower than environment variables"
        description: "Reads Ezviz credentials from channels.ezviz section as fallback. Ensure these files don't contain unrelated secrets."
---

# Ezviz Open Video (萤石设备视频流)

Generate Ezviz camera live and playback streaming links for PC and mobile devices.

---

## ⚠️ Security Warning (Read Before Installation)

**Complete the following security checks before using this skill:**

| # | Check | Status | Description |
|---|-------|--------|-------------|
| 1 | **Credential Permissions** | ⚠️ Required | Use **minimal permission** AppKey/AppSecret, do not use master account credentials |
| 2 | **Config File Reading** | ⚠️ Note | Skill reads `~/.openclaw/*.json` files (**but environment variables have higher priority**) |
| 3 | **Token Caching** | ⚠️ Note | Token cached in `/tmp/ezviz_global_token_cache/` (permissions 600, shared across skills) |
| 4 | **API Domain** | ✅ Verified | `openai.ys7.com` is official Ezviz API endpoint |
| 5 | **Code Review** | ✅ Recommended | Review `scripts/generate_preview.py` and `lib/token_manager.py` |
| 6 | **Python Dependencies** | ⚠️ Required | Requires `requests` library - install via `pip install requests` |

### 🔒 Config File Reading Details

**Credential Priority** (high to low):

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Environment Variables (Highest Priority - Recommended)   │
│    ├─ EZVIZ_APP_KEY                                         │
│    ├─ EZVIZ_APP_SECRET                                      │
│    └─ EZVIZ_DEVICE_SERIAL                                   │
│    ✅ Advantage: No config file reading, fully isolated      │
├─────────────────────────────────────────────────────────────┤
│ 2. OpenClaw Config Files (Only when env vars not set)       │
│    ├─ ~/.openclaw/config.json                               │
│    ├─ ~/.openclaw/gateway/config.json                       │
│    └─ ~/.openclaw/channels.json                             │
│    ⚠️ Note: Only reads channels.ezviz field                 │
├─────────────────────────────────────────────────────────────┤
│ 3. Command Line Arguments (Lowest Priority)                 │
│    python3 generate_preview.py appKey appSecret deviceSerial│
└─────────────────────────────────────────────────────────────┘
```

**Security Recommendations**:
- ✅ **Best Practice**: Use environment variables, completely avoid config file reading
- ✅ **Isolated Config**: Store Ezviz credentials in dedicated config file, don't mix with other services
- ⚠️ **Risk Mitigation**: Set environment variables to override config files (will be ignored even if config exists)

### Quick Secure Configuration

```bash
# 1. Use environment variables (highest priority, avoids accidental config file use)
export EZVIZ_APP_KEY="your_dedicated_app_key"
export EZVIZ_APP_SECRET="your_dedicated_app_secret"
export EZVIZ_DEVICE_SERIAL="BF6985110"

# 2. High security: Disable token caching
export EZVIZ_TOKEN_CACHE=0

# 3. Test credentials (recommended to use test account first)
# Login to https://openai.ys7.com/ to create dedicated app with only preview permissions
```

---

## Quick Start

### Install Dependencies

```bash
pip install requests
```

### Set Environment Variables

```bash
export EZVIZ_APP_KEY="your_app_key"
export EZVIZ_APP_SECRET="your_app_secret"
export EZVIZ_DEVICE_SERIAL="BF6985110"
```

Optional environment variables:
```bash
export EZVIZ_CHANNEL_NO="1"     # Channel number, default 1
export EZVIZ_TOKEN_CACHE="1"    # Token cache: 1=enabled (default), 0=disabled
```

### Run

```bash
python3 {baseDir}/scripts/generate_preview.py
```

Command line arguments:
```bash
# Single device
python3 {baseDir}/scripts/generate_preview.py appKey appSecret BF6985110 1

# Specify channel number
python3 {baseDir}/scripts/generate_preview.py appKey appSecret BF6985110 1
```

---

## Channels Configuration (Recommended)

Skill supports automatically reading Ezviz credentials from OpenClaw channels configuration.

### Configuration

Add to `~/.openclaw/config.json` or `~/.openclaw/channels.json`:

```json
{
  "channels": {
    "ezviz": {
      "appId": "your_app_id",
      "appSecret": "your_app_secret",
      "domain": "https://openai.ys7.com",
      "enabled": true
    }
  }
}
```

### Priority

Credential priority:
1. **Environment Variables** (Highest)
2. **Channels Config** (Medium)
3. **Command Line Arguments** (Lowest)

---

## Workflow

```
1. Get Token (appKey + appSecret → accessToken)
 ↓
2. Generate Links (accessToken + deviceSerial → preview/playback URLs)
 ↓
3. Output Results (PC + Mobile links for live and playback)
```

## Token Auto-Get Explanation

**You don't need to manually get or configure `EZVIZ_ACCESS_TOKEN`!**

Skill automatically handles token acquisition and caching:

```
First Run:
 appKey + appSecret → Call Ezviz API → Get accessToken (7 days validity)
 ↓
Save to cache file (system temp directory)
 ↓
Subsequent Runs:
 Check if cached token is expired
 ├─ Not expired → Use cached token directly ✅
 └─ Expired → Get new token
```

**Token Management Features**:
- ✅ **Auto Get**: Automatically call Ezviz API on first run
- ✅ **7 Days Validity**: Token valid for 7 days
- ✅ **Smart Caching**: Don't re-get within validity period
- ✅ **Safety Buffer**: Auto-refresh 5 minutes before expiry
- ✅ **No Config Needed**: No need to manually set `EZVIZ_ACCESS_TOKEN`
- ✅ **Secure Storage**: Cache file permissions 600

---

## Output Example

```
======================================================================
Ezviz Open Video Skill (萤石设备视频流)
======================================================================
[Time] 2026-03-19 19:23:00
[INFO] Device: BF6985110 (Channel: 1)

======================================================================
SECURITY VALIDATION
======================================================================
[OK] Device serial format validated
[OK] Using credentials from environment variables

======================================================================
[Step 1] Getting access token...
======================================================================
[INFO] Using cached global token, expires: 2026-03-26 19:21:16
[SUCCESS] Using cached token, expires: 2026-03-26 19:21:16

======================================================================
[Step 2] Generating links...
======================================================================

📺 Live Links:

  🖥️  PC:
  https://open.ys7.com/console/jssdk/pc.html?url=ezopen://open.ys7.com/BF6985110/1.live&accessToken=at.xxx

  📱  Mobile:
  https://open.ys7.com/console/jssdk/mobile.html?url=ezopen://open.ys7.com/BF6985110/1.live&accessToken=at.xxx

📼 Playback Links:

  🖥️  PC:
  https://open.ys7.com/console/jssdk/pc.html?url=ezopen://open.ys7.com/BF6985110/1.rec&accessToken=at.xxx

  📱  Mobile:
  https://open.ys7.com/console/jssdk/mobile.html?url=ezopen://open.ys7.com/BF6985110/1.rec&accessToken=at.xxx

======================================================================
```

## Link Format

| Type | Platform | Format |
|------|----------|--------|
| Live | PC | `https://open.ys7.com/console/jssdk/pc.html?url=ezopen://{serial}/{channel}.live&accessToken={token}` |
| Live | Mobile | `https://open.ys7.com/console/jssdk/mobile.html?url=ezopen://{serial}/{channel}.live&accessToken={token}` |
| Playback | PC | `https://open.ys7.com/console/jssdk/pc.html?url=ezopen://{serial}/{channel}.rec&accessToken={token}` |
| Playback | Mobile | `https://open.ys7.com/console/jssdk/mobile.html?url=ezopen://{serial}/{channel}.rec&accessToken={token}` |

**Link Explanation**:
- `.live` — Live streaming
- `.rec` — Recording playback

## API Interface

| Interface | URL | Documentation |
|-----------|-----|---------------|
| Get Token | `POST /api/lapp/token/get` | https://openai.ys7.com/help/81 |

## Network Endpoints

| Domain | Purpose |
|--------|---------|
| `openai.ys7.com` | Ezviz Open Platform API (Token) |
| `open.ys7.com` | Preview page hosting |

---

## Notes

⚠️ **Token Validity**: accessToken typically valid for 7 days, skill auto-manages caching and refresh

⚠️ **Privacy Compliance**: Camera monitoring may involve privacy issues, ensure compliance with local laws

⚠️ **Device Requirements**: Device must be online to generate valid links

---

## Data Flow Explanation

**This skill sends data to third-party services**:

| Data Type | Sent To | Purpose | Required |
|-----------|---------|---------|----------|
| appKey/appSecret | `openai.ys7.com` (Ezviz) | Get access token | ✅ Required |
| **EZVIZ_ACCESS_TOKEN** | **Auto-generated** | **Auto-get on each run** | **✅ Auto** |

**Data Flow**:
- ✅ **Ezviz Platform** (`openai.ys7.com`): Token request - Official Ezviz API
- ❌ **No Other Third Parties**: No data sent to other services
- ❌ **Preview Links**: Only generates URLs, no video stream data transmitted

**Credential Permission Recommendations**:
- Use **minimal permission** appKey/appSecret
- Enable only necessary API permissions
- Rotate credentials regularly
- Do not use master account credentials

**Local Processing**:
- ✅ Token cached to system temp directory, permissions 600
- ✅ Token valid for 7 days, auto-refresh 5 minutes before expiry
- ✅ Can disable cache: Set `EZVIZ_TOKEN_CACHE=0` environment variable

---

## Usage Examples

**Scenario 1: Single Device Preview**
```bash
python3 generate_preview.py your_key your_secret BF6985110
```

**Scenario 2: Specify Channel**
```bash
python3 generate_preview.py your_key your_secret BF6985110 1
```

**Scenario 3: Environment Variables**
```bash
export EZVIZ_APP_KEY="your_key"
export EZVIZ_APP_SECRET="your_secret"
export EZVIZ_DEVICE_SERIAL="BF6985110"
python3 generate_preview.py
```

---

## 🔐 Token Management & Security

### Token Caching Behavior

**Default Behavior**:
- ✅ Token cached to system temp directory (`/tmp/ezviz_global_token_cache/`)
- ✅ Cache valid for 7 days
- ✅ Auto-refresh 5 minutes before expiry
- ✅ Cache file permissions 600
- ⚠️ **Note**: Cache is shared across all skills using this token manager

### Security Considerations

| Concern | Mitigation |
|---------|------------|
| **Global cache shared across skills** | Run in isolated environment (container/VM), or disable caching |
| **Temp directory accessible by other users** | Use dedicated user account, or set custom cache path |
| **Token persistence** | Disable caching: `EZVIZ_TOKEN_CACHE=0` |

### Disable Token Caching (High Security)

```bash
export EZVIZ_TOKEN_CACHE=0
python3 scripts/generate_preview.py ...
```

### Cache File Location

| System | Path |
|--------|------|
| macOS/Linux | `/tmp/ezviz_global_token_cache/` |
| Windows | `C:\Users\{user}\AppData\Local\Temp\ezviz_global_token_cache\` |

**Clear Cache**:
```bash
rm -rf /tmp/ezviz_global_token_cache/
```

---

## 🔒 Security Recommendations

### 1. Use Minimal Permission Credentials
- Create dedicated appKey/appSecret
- Do not use master account credentials
- Rotate credentials regularly (recommended every 90 days)

### 2. Environment Variable Security
```bash
# Use .env file
echo "EZVIZ_APP_KEY=your_key" >> .env
echo "EZVIZ_APP_SECRET=your_secret" >> .env
chmod 600 .env
source .env
```

### 3. Disable Caching (High Security Scenarios)
```bash
export EZVIZ_TOKEN_CACHE=0
```

### 4. Isolated Environment (Recommended)
- Run in container/VM for stricter isolation
- Use dedicated user account with restricted temp directory access
- Review `lib/token_manager.py` to understand cache behavior

### 5. Config File Security
- Ensure `~/.openclaw/*.json` files don't contain unrelated secrets
- Prefer environment variables to avoid config file reading entirely

---

## Security Audit Checklist

### Before Installation
- [ ] **Review Code** — Read `scripts/generate_preview.py` and `lib/token_manager.py`
- [ ] **Verify API Domain** — Confirm `openai.ys7.com` is official Ezviz endpoint
- [ ] **Prepare Test Credentials** — Create dedicated Ezviz application
- [ ] **Install Dependencies** — Run `pip install requests`

### During Installation
- [ ] **Use Environment Variables** — Prefer environment variables over config files
- [ ] **Minimal Permission Credentials** — Do not use master account credentials
- [ ] **Isolated Environment** — Consider container/VM for stricter isolation

### After Installation
- [ ] **Verify Cache Permissions** — Confirm cache file permissions are 600
- [ ] **Test Functionality** — Verify links open correctly
- [ ] **Review Config Files** — Ensure `~/.openclaw/*.json` don't contain unrelated secrets

---

## File Structure

```
ezviz-open-video/
├── SKILL.md                      # Skill documentation
├── lib/
│   ├── token_manager.py          # Token manager (shared)
│   └── README_TOKEN_MANAGER.md   # Token management docs
├── references/
│   └── ezviz-agent-api.md        # API reference
└── scripts/
    └── generate_preview.py       # Main script
```

## Related Skills

- **ezviz-open-picture**: Device snapshot/capture skill
- **ezviz-open-ptz-control**: PTZ control skill

## Official Resources

- Ezviz Open Platform: https://open.ys7.com/
- API Documentation: https://openai.ys7.com/doc/

---

**Last Updated**: 2026-03-19  
**Version**: 1.1.0
