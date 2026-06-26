---
name: browser-healthcheck
version: 1.0.0
description: Browser tool health check and auto-repair. Automatically checks browser status before each use and diagnoses/fixes issues. Use when: (1) preparing to use browser tool for screenshots/automation; (2) browser snapshot/start times out; (3) CDP connection fails; (4) user mentions "browser timeout", "CDP disconnected", "浏览器超时", "browser 失效".
---

# Browser Health Check / Browser 健康检查

**Core Principle: Always check status before using the browser tool.**
**核心原则：每次使用 browser 工具前，先检查状态。**

## Quick Check Flow / 快速检查流程

```
1. browser(action=status, profile="openclaw")
   ├─ running=true, cdpReady=true → ✅ OK, proceed / 正常，直接使用
   ├─ running=false → Try to start / 尝试启动
   └─ Start failed → Diagnose and fix / 诊断并修复
```

## Common Issues / 常见问题诊断

### Issue 1: Profile Conflict (Most Common) / 问题 1: Profile 冲突（最常见）

**Symptoms / 症状：**
- `running=false, cdpReady=false`
- Timeout immediately after start / 启动后立即超时
- Especially with `profile="user"` / 使用 `profile="user"` 时尤其容易发生

**Cause / 原因：**
- User is using their own Chrome (port 9222) / 用户正在使用自己的 Chrome
- CDP port occupied / CDP 端口被占用

**Solution / 解决方案：**
```
Use independent profile / 使用独立 profile:
browser(action=start, profile="openclaw")  # Port 9223, isolated data dir
```

**Permanent Fix / 永久方案：**
Configure `defaultProfile: "openclaw"`:
```json
{
  "browser": {
    "enabled": true,
    "defaultProfile": "openclaw",
    "profiles": {
      "user": { "cdpPort": 9222, "attachOnly": false },
      "openclaw": { "cdpPort": 9223, "attachOnly": false }
    }
  }
}
```

### Issue 2: Browser Process Residue / 问题 2: 浏览器进程残留

**Symptoms / 症状：**
- `running=false` but port occupied / 端口被占用
- Start fails with "port already in use" / 启动失败，提示端口已使用

**Diagnosis / 诊断：**
```bash
# Windows
netstat -ano | findstr "9223"
tasklist | findstr "chrome"
```

**Solution / 解决方案：**
```bash
# Kill residual process / 杀掉残留进程
taskkill /F /PID <pid>
# Or restart Gateway / 或重启 Gateway
openclaw gateway restart
```

### Issue 3: CDP Port Not Responding / 问题 3: CDP 端口不响应

**Symptoms / 症状：**
- `running=true` but `cdpReady=false`
- http://127.0.0.1:9223 no response / 无响应

**Solution / 解决方案：**
```bash
# 1. Restart Gateway / 重启 Gateway
openclaw gateway restart

# 2. Wait 5 seconds and recheck / 等待 5 秒后重新检查
browser(action=status, profile="openclaw")
```

## Profile Selection Guide / Profile 选择指南

| Profile | Port / 端口 | Data Directory / 数据目录 | Use Case / 适用场景 |
|---------|-------------|--------------------------|---------------------|
| `openclaw` | 9223 | `~/.openclaw/browser/openclaw/user-data` | **Default choice / 默认选择**, isolated, no conflict |
| `user` | 9222 | User Chrome data dir / 用户 Chrome 目录 | Need user's logged-in accounts (YouTube etc.) |

**⚠️ Before using `user` profile / 使用 `user` profile 前：**
1. Confirm user is not using their Chrome / 确认用户没有在使用自己的 Chrome
2. If user is browsing, use `openclaw` instead / 如果用户正在使用浏览器，改用 `openclaw`

## Health Check Script / 自动检查脚本

Run `scripts/healthcheck.py` for full diagnosis:

```bash
python scripts/healthcheck.py --profile openclaw
```

**Output Example / 输出示例：**
```
[OK] Browser enabled: true
[OK] Default profile: openclaw
[OK] CDP port 9223 available
[OK] Browser running: true
[OK] CDP ready: true
[PASS] Browser health check passed
```

## Best Practices / 最佳实践

### Pre-use Check (Recommended) / 使用前检查（推荐）

```python
# 1. Check status / 检查状态
status = browser(action=status, profile="openclaw")

# 2. Start if not running / 如果未运行，启动
if not status["running"]:
    browser(action=start, profile="openclaw")

# 3. Execute operation / 执行操作
browser(action=snapshot, profile="openclaw")
```

### Post-failure Repair / 失败后修复

```python
try:
    browser(action=snapshot, profile="openclaw")
except TimeoutError:
    # 1. Check status / 检查状态
    status = browser(action=status, profile="openclaw")
    
    # 2. Diagnose based on status / 根据状态诊断
    if not status["running"]:
        browser(action=start, profile="openclaw")
    elif not status["cdpReady"]:
        exec("openclaw gateway restart")
        time.sleep(5)
        browser(action=start, profile="openclaw")
```

## Technical Details / 技术细节

### OpenClaw Browser Architecture / OpenClaw Browser 架构

```
Gateway (port 18789)
    └── Browser Plugin
            ├── openclaw profile (port 9223)
            │   └── user-data: ~/.openclaw/browser/openclaw/
            └── user profile (port 9222)
                └── user-data: User Chrome directory
```

### CDP Protocol / CDP 协议

Chrome DevTools Protocol (CDP) for remote debugging:
- Default ports: 9222 (user) / 9223 (openclaw)
- HTTP endpoint: `http://127.0.0.1:9223/json`
- WebSocket: `ws://127.0.0.1:9223/devtools/...`

---

**Remember: Check first, use later. When timeout occurs, switch profile first.**
**记住：先检查，后使用。遇到超时，先切换 profile。**
