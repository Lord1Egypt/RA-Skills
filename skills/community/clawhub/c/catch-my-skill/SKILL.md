---
name: catch-my-skill
description: 自动检测本地与线上 skill 版本差异 - 支持 ClawHub/GitHub，定期检查更新
metadata:
  openclaw:
    emoji: 🎯
---

# Catch My Skill

自动检测本地与线上 skill 版本差异

## 功能

- 📋 **维护两个列表**
  - 本地 skill 列表（含版本）
  - 线上 skill 列表（ClawHub + GitHub）
  
- ⏰ **定时检查**
  - 每半小时自动获取线上版本
  - 对比本地与线上版本差异
  
- 🔔 **版本告警**
  - 本地落后时提醒更新
  - 支持手动触发检查

## 列表文件

| 文件 | 说明 |
|------|------|
| `data/local.json` | 本地 skill 列表 |
| `data/online.json` | 线上 skill 列表 |

## 设计初衷

**高粘性使用** - 只保留用户真正在用的 skills，避免装一堆不用的。

## 初始化流程

```
1. 首次运行 init
   ↓
2. 自动获取线上所有 skills（ClawHub + GitHub）
   ↓
3. 生成完整本地列表（含版本）
   ↓
4. 用户删除不想要的 skill
   ↓
5. 后续只跟踪保留下来的 skills
```

## 用户操作

```bash
# 首次初始化（从线上拉取全部）
/catch-my-skill init

# 删除不想要的 skill（减少跟踪）
/catch-my-skill remove white-stone-mem

# 添加回想跟踪的 skill
/catch-my-skill add elegant-sync

# 检查版本
/catch-my-skill check

# 本地落后时自动更新（任选一个渠道）
/catch-my-skill update elegant-sync
```

## 数据格式

### local.json
```json
{
  "skills": [
    {"name": "white-stone-mem", "version": "1.0.0", "path": "~/.openclaw/skills/white-stone-mem"},
    {"name": "elegant-sync", "version": "1.0.1", "path": "~/.openclaw/skills/elegant-sync"}
  ],
  "updated": "2026-02-28T16:00:00Z"
}
```

### online.json
```json
{
  "clawhub": [
    {"name": "white-stone-mem", "version": "1.0.0", "owner": "russellfei"},
    {"name": "elegant-sync", "version": "1.0.3", "owner": "russellfei"}
  ],
  "github": [
    {"name": "minimax-mcp-call", "version": "1.0.0", "owner": "russellfei", "repo": "russellfei/minimax-mcp-call"}
  ],
  "updated": "2026-02-28T16:00:00Z"
}
```

## 配置

### 自动检查间隔

在 `.backup.env` 中配置：

```bash
# 检查间隔（分钟），默认 30 分钟
CATCH_INTERVAL=30
```

### GitHub 用户名

```bash
GITHUB_USERNAME=russellfei
```

## 工作流程

```
1. 定时触发（每30分钟）
   ↓
2. 获取 ClawHub 线上版本（clawhub inspect）
   ↓
3. 获取 GitHub 线上版本（gh api）
   ↓
4. 对比本地版本
   ↓
5. 输出差异报告
   ↓
6. 本地落后 → 提醒更新
```

## 输出示例

```
=== Skill 版本检查 ===

本地落后需更新:
  ⚠️ elegant-sync: 本地 1.0.1 < 线上 1.0.3

本地已是最新:
  ✅ white-stone-mem: 1.0.0
  ✅ minimax-mcp-call: 1.0.0

线上新技能:
  (无)
```

## 定时任务

自动添加到 crontab：

```bash
# 每30分钟检查
*/30 * * * * node /path/to/catch-my-skill/index.js check >> /home/orangepi/.openclaw/logs/catch-my-skill.log 2>&1
```

## 安装

```bash
# 复制到 skills 目录
cp -r catch-my-skill ~/.openclaw/workspace/skills/

# 初始化
node index.js init
```

## 更新日志

- 2026-02-28: 初始版本
