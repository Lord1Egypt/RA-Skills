# OpenClaw 升级与维护 Skill

> 版本：1.0 | 更新于：2026-04-27
> 
> 适用于 OpenClaw 2026.4.x

安全升级 OpenClaw、排查常见问题、管理配置和权限。

## 功能

- **一键升级**：备份 + 升级 + 验证
- **升级排错**：自动检测和修复常见问题
- **权限管理**：检查和恢复 tools.profile
- **插件修复**：清理插件目录冲突
- **版本回滚**：从备份恢复

## 快速操作

```bash
# 检查当前版本
openclaw --version

# 一键升级（推荐）
bash ~/.openclaw/workspace/skills/openclaw-upgrade/scripts/upgrade.sh

# 升级后排错
bash ~/.openclaw/workspace/skills/openclaw-upgrade/scripts/post-upgrade-fix.sh

# 检查权限
bash ~/.openclaw/workspace/skills/openclaw-upgrade/scripts/check-permissions.sh
```

## 升级流程

```
┌─────────────────────────────────────┐
│  1. 备份配置                         │
│     • openclaw.json                 │
│     • auth-profiles.json            │
│     • MEMORY.md + SOUL.md           │
├─────────────────────────────────────┤
│  2. 执行升级                         │
│     • npm i -g openclaw@latest      │
│     • 等待 Gateway 重启              │
├─────────────────────────────────────┤
│  3. 验证                             │
│     • 版本检查                       │
│     • 权限检查 (tools.profile=full)  │
│     • 插件状态                       │
│     • 健康检查                       │
└─────────────────────────────────────┘
```

## 升级后常见问题

### 问题1：插件目录冲突 (ENOTEMPTY)

**症状：**
```
Error: ENOTEMPTY, Directory not empty: .../plugin-sdk
```

**修复：**
```bash
# 清理旧的插件运行时目录
rm -rf ~/.openclaw/plugin-runtime-deps/openclaw-unknown-*
rm -rf ~/.openclaw/plugin-runtime-deps/openclaw-2026.4.*
openclaw gateway restart
```

### 问题2：tools.profile 被重置

**症状：**
- exec 权限失效
- `openclaw doctor` 后无法执行命令

**修复：**
```bash
# 检查当前值
python3 -c "import json; print(json.load(open('$HOME/.openclaw/openclaw.json')).get('tools',{}).get('profile'))"

# 修复
python3 -c "
import json
c = json.load(open('$HOME/.openclaw/openclaw.json'))
c['tools']['profile'] = 'full'
json.dump(c, open('$HOME/.openclaw/openclaw.json','w'), indent=2)
"
openclaw gateway restart
```

### 问题3：Bonjour/mDNS 卡住

**症状：**
```
Unhandled promise rejection: CIAO PROBING CANCELLED
```

**修复：**
- 通常是启动时的临时警告
- 重启后会自动恢复
- 不影响核心功能

### 问题4：Gateway 无法启动

**修复步骤：**
```bash
# 1. 检查日志
tail -50 ~/.openclaw/logs/gateway.err.log

# 2. 验证配置
python3 -c "import json; json.load(open('$HOME/.openclaw/openclaw.json'))"

# 3. 从备份恢复
cp ~/.openclaw/backups/openclaw.json.bak.LATEST ~/.openclaw/openclaw.json
openclaw gateway restart
```

## 权限配置

### 正确配置

```json
{
  "tools": {
    "profile": "full"
  }
}
```

### 飞书端配置（webchat 频道）

```json
{
  "agents": {
    "list": [{
      "id": "main",
      "tools": {
        "alsoAllow": ["exec", "gateway", "browser", "..."]
      }
    }]
  }
}
```

### 注意事项

⚠️ **`openclaw doctor` 可能会重置 `tools.profile` 为 `messaging`**

升级后务必检查：
```bash
bash ~/.openclaw/workspace/skills/openclaw-upgrade/scripts/check-permissions.sh
```

## 备份管理

### 备份位置
- 配置备份：`~/.openclaw/backups/`
- 记忆备份：`~/爱丽丝备份/`

### 自动备份
- 升级前自动备份
- 每日 2:00 自动备份（smart-backup.sh）
- 每周日 3:00 备份 alice 记忆

### 手动备份
```bash
# 完整备份
bash ~/.openclaw/workspace/skills/openclaw-recovery/scripts/smart-backup.sh

# 仅备份配置
cp ~/.openclaw/openclaw.json ~/.openclaw/backups/openclaw.json.bak.$(date +%Y%m%d_%H%M%S)
```

## 版本回滚

```bash
# 查看可用备份
ls -lt ~/.openclaw/backups/openclaw.json.bak.*

# 从备份恢复
cp ~/.openclaw/backups/openclaw.json.bak.YYYYMMDD_HHMMSS ~/.openclaw/openclaw.json
openclaw gateway restart
```

## 相关文件

| 文件 | 用途 |
|------|------|
| `scripts/upgrade.sh` | 一键升级脚本 |
| `scripts/post-upgrade-fix.sh` | 升级后排错 |
| `scripts/check-permissions.sh` | 权限检查 |

## 相关 Skill

- [openclaw-recovery](../openclaw-recovery/SKILL.md) - 自动恢复和健康监控
