# ClawGears Security Audit Skill

## Overview

ClawGears is a security audit tool for OpenClaw/MoltBot/ClawdBot users on macOS. It helps detect and fix security vulnerabilities that could expose your AI assistant to the public internet.

**🌟 New in v1.4.0: Context-Aware Risk Explanations**

Instead of one-size-fits-all "best practices", ClawGears now provides **scenario-based risk analysis**:
- Each check explains **what it protects** and **real impact by scenario**
- Recommendations are **graded**: 🔴必须 / 🟠建议 / 🟡可选 / ⚪评估后决定
- **Legitimate reasons to not fix** are acknowledged
- **Alternative compensating measures** are suggested

**Use this skill when:**
- User asks about OpenClaw security
- User wants to check if their AI assistant is exposed
- User mentions "裸奔" (Chinese), "むき出し" (Japanese), "expuesto" (Spanish) or security concerns
- User wants to audit their OpenClaw configuration
- User asks about IP leak detection

**Supported Languages:**
ClawGears README is available in 7 languages:
- 🇬🇧 English | 🇨🇳 中文 | 🇩🇪 Deutsch | 🇫🇷 Français | 🇮🇹 Italiano | 🇯🇵 日本語 | 🇪🇸 Español

---

## ⚠️ Requirements & Dependencies

### System Binaries Required

| Binary | Purpose |
|--------|---------|
| `python3` | JSON parsing |
| `curl` | HTTP requests, IP detection |
| `lsof` | Port and process inspection |
| `pgrep` / `pkill` | Process management |
| `openssl` | Token generation |
| `socketfilterfw` | macOS firewall control (`/usr/libexec/ApplicationFirewall/socketfilterfw`) |

### Platform

- **macOS only** - Uses macOS-specific tools and paths

---

## 📁 Files Accessed

### Read Operations

| Path | Purpose |
|------|---------|
| `~/.openclaw/openclaw.json` | OpenClaw configuration (token, gateway settings) |
| `~/.openclaw/logs/` | Gateway logs for anomaly detection |
| `/Library/Application Support/com.apple.TCC/TCC.db` | macOS TCC database (Full Disk Access, Accessibility) |
| `~/Library/Application Support/com.apple.TCC/TCC.db` | User-level TCC database |

### Write Operations

| Path | Purpose |
|------|---------|
| `./history/` | Audit result storage (JSON, HTML reports) |
| `./reports/` | Generated audit reports |
| `~/.openclaw/openclaw.json` | Configuration fixes (with `--fix` flag only) |

---

## 🌐 Network Calls

### External Services (IP Detection)

| Domain | Purpose | Data Sent |
|--------|---------|-----------|
| `api.ipify.org` | Public IP detection | None (GET request) |
| `icanhazip.com` | Public IP detection (fallback) | None |
| `ifconfig.me/ip` | Public IP detection (fallback) | None |

### External Services (Leak Detection)

| Domain | Purpose | Data Sent |
|--------|---------|-----------|
| `openclaw.allegro.earth` | OpenClaw exposure database check | Your public IP |
| `search.censys.io` | Censys scan database (link only, manual check) | None from script |
| `www.shodan.io` | Shodan scan database (link only, manual check) | None from script |

---

## 🔐 Privacy Notice

**Before running this skill, please be aware:**

1. **IP Transmission**: Your public IP address will be sent to:
   - `api.ipify.org` (or fallback services) for IP detection
   - `openclaw.allegro.earth` for exposure database check

2. **Local File Access**: This skill reads:
   - Your OpenClaw configuration (including tokens)
   - macOS TCC permission database
   - Gateway logs

3. **System Changes**: The `interactive-fix.sh` script can:
   - Modify OpenClaw configuration
   - Generate new tokens
   - Restart Gateway service
   - Require `sudo` for firewall changes

4. **Recommendation**: Review scripts before running. Run `quick-check.sh` first (read-only) before applying any fixes.

---

## Security Risks Explained

Use this section to understand each risk, its actual impact, and whether it applies to your situation.

| Risk | What It Protects | Real Impact | Fix Priority |
|------|-------------------|--------------|--------------|
| **Gateway exposed** | Prevent unauthorized access to your AI assistant | 🔴 **Critical** - Anyone on the internet can control your AI. **Fix immediately** if exposed. | **Weak token** | Prevent API key theft | 🟠 **High** - If leaked, attackers can impersonate you assistant and use your API keys. **Fix recommended** but token < 64 chars. | **Sensitive commands** | Prevent privacy invasion (camera, screenshots) | 🟠 **High** - AI could these commands could spy on you or capture your screen. **Fix recommended** if not blocked. | **FDA granted** | Limit AI file access | 🟡 **Medium** - AI can read all your files. **Evaluate based on your trust level** - Only enable if you truly need this capability. - Consider if your AI is running in a secure environment. - Alternative: Use project-specific folder permissions. | **FileVault disabled** | Protect data if disk is stolen | 🟡 **Medium** - If Mac is stolen, all data is accessible. **Evaluate based on your situation:**
        - ✅ **Enable** if Mac is portable or in shared spaces
        - ⚠️ **OK to disable** if you need **remote restart control** (e.g., for Mac-to-Mac sync)
        - If disabled, consider physical security measures instead
    | **IP in leak database** | Check if already exposed | 🟠 **High** - Your IP is in a public exposure database. **Check before panicking:**
        - If you've been using OpenClaw for a while without issues, it IP may have been indexed already.
        - If you just started, use the tool: do a quick check and not a leak.
    | **iCloud sync enabled** | Prevent sensitive data cloud sync | 🟡 **Low** - iCloud may sync Documents, Desktop, Pictures by default. **Evaluate based on your needs:**
        - ✅ **Enable** if you store sensitive data in these folders
        - ⚠️ **OK to disable** if you don't store sensitive data in these locations
        - If disabled, consider using .gitignore for excluding patterns
    | **SIP disabled** | Protect system integrity | 🟡 **Low** - System-level protections are reduced. **Usually OK to keep enabled, - Only disable if you have a specific, legitimate reason (e.g., development, testing)
    - If disabled, be extra cautious about what you install

---

## Quick Security Check

Run a fast 5-second security audit (read-only, safe to run):

```bash
./scripts/quick-check.sh
```

This checks:
1. Gateway network exposure
2. Token strength
3. Command injection protection
4. TCC permissions
5. Firewall status

---

## Full Security Audit

Run comprehensive security check:

```bash
./scripts/generate-report.sh --format html --output ./reports
```

---

## IP Leak Detection

Check if user's IP has been exposed in security databases:

```bash
./scripts/ip-leak-check.sh --all
```

Checks 3 databases:
- **openclaw.allegro.earth** - OpenClaw specific exposure database
- **Censys** - Internet-wide scanning database (https://search.censys.io)
- **Shodan** - IoT and service scanning database (https://www.shodan.io)

---

## Interactive Fix

**⚠️ Requires explicit user consent before running**

Automatically fix common security issues:

```bash
./scripts/interactive-fix.sh
```

Options:
- `--bind` - Rebind Gateway to localhost
- `--token` - Generate new strong token
- `--deny` - Add sensitive commands to deny list
- `--restart` - Restart Gateway service
- `--all` - Fix all issues

---

## Workflow

When user asks about security:

1. **First, run quick check** to identify issues (read-only):
   ```bash
   ./scripts/quick-check.sh
   ```

2. **If issues found**, explain risks and ask for consent before fixing:
   ```bash
   ./scripts/interactive-fix.sh --all
   ```

3. **Check IP exposure**:
   ```bash
   ./scripts/ip-leak-check.sh --all
   ```

4. **Generate report** for records:
   ```bash
   ./scripts/generate-report.sh --format html
   ```

---

## Output Interpretation

### Quick Check Results

| Symbol | Meaning |
|--------|---------|
| ✅ PASS | Security check passed |
| ⚠️ WARN | Warning, review recommended |
| ❌ FAIL | Critical issue, fix immediately |

### IP Leak Results

| Result | Action |
|--------|--------|
| IP NOT in database | Continue monitoring |
| IP FOUND in database | URGENT: Close public access, regenerate tokens |

---

## Important Reminders

1. **Always recommend** running quick check first (read-only, safe)
2. **Explain risks** in plain language before fixing
3. **Ask for explicit consent** before running interactive-fix.sh
4. **Suggest periodic checks** (weekly or after config changes)
5. **Warn about** the 220,000+ exposed OpenClaw instances

---

## Statistics

> Over 220,000 OpenClaw instances are publicly exposed. Many API keys have already leaked to hacker databases.

---

## Related Links

- GitHub: https://github.com/JinHanAI/ClawGears
- ClawHub: https://clawhub.ai

---

## License

MIT-0 (ClawHub Platform License)
