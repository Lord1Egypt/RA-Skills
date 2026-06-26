# Bailian Usage Query Skill

## Installation

This skill is built into the workspace, no additional installation required.

## Usage

### Quick Commands

Send any of the following messages to trigger:

- `查百炼额度` (Check Bailian quota)
- `百炼用量` (Bailian usage)
- `看看阿里云还剩多少额度` (Check Alibaba Cloud remaining quota)
- `Coding Plan`
- `查一下百炼套餐用量` (Check Bailian package usage)

### Manual Invocation

Tell the AI: "Call bailian-usage Skill to query Bailian package"

## Output Example

```markdown
## 📊 Bailian Coding Plan Package Details

**Package Status:** ✅ Active | **18 days** remaining (Expires 2026-04-03)
**Auto-renewal:** ❌ Disabled

**Usage Consumption:**
- Last updated: 2026-03-15 19:54:33
- Last 5 hours: **47%** (Resets 2026-03-15 19:54:34)
- Last week: **42%** (Resets 2026-03-16 00:00:00)
- Last month: **39%** (Resets 2026-04-03 00:00:00)

**Available Models:** Qwen Series / Zhipu / Kimi / MiniMax

---

### 💡 Usage Analysis
- ✅ Sufficient quota
```

## Authentication

### Automated Login (Default)

The script automatically reads credentials from `TOOLS.md` and logs in:

```markdown
## 🔐 Alibaba Cloud Bailian Account
- **URL**: https://bailian.console.aliyun.com/cn-beijing/?tab=coding-plan#/efm/index
- **Email**: your-email@example.com
- **Password**: your-password
```

**Process:**
1. Open Bailian Console
2. Check login status
3. If not logged in, auto-fill credentials and login
4. Extract data and return results

### Manual Verification (Fallback)

If automated login triggers CAPTCHA/SMS verification:
1. Script will prompt that manual verification is needed
2. Complete verification in the browser window
3. Continue query after successful verification

## Technical Implementation

- **Browser**: Uses `openclaw browser` tool
- **Login**: Direct login each time, no cookie dependency
- **Data Extraction**: Uses `evaluate` to execute JS and read DOM directly
- **Code Size**: ~100 lines (minimal version)

## Notes

1. **Direct login each time** - No cookie dependency, simpler and more reliable
2. **High risk control scenario** - If SMS/CAPTCHA verification is triggered, manual completion required
3. **Usage refresh time** - May be delayed, refer to page display
4. **Browser management** - Follows memory-saving strategy, proactively closes non-essential tabs

## 🔐 Security Notes

- **Credential Storage**: Credentials stored only in user's local `TOOLS.md` file, not committed to Git/VCS
- **Credential Usage**: Script reads credentials into memory only, never logged or transmitted externally
- **Browser Session**: Login state saved in local browser Profile, not uploaded to any server
- **Network Requests**: All requests sent directly to `bailian.console.aliyun.com`, no third-party relay
- **ClawHub Security Scan**: v1.0.2+ passed ClawHub security scan (no suspicious patterns warnings)

## Related Files

- **Script**: `~/.openclaw/workspace/skills/bailian-usage/query_browser.sh`
- **Config**: `~/.openclaw/workspace/TOOLS.md` (credentials)
- **Docs**: `~/.openclaw/workspace/skills/bailian-usage/SKILL.md`
