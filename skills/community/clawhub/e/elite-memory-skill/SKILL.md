---
name: elite-memory
description: 终极 AI 记忆系统 - WAL 协议 + 每日记忆 + 长期记忆 + GitHub 自动同步 + 飞书通知
homepage: https://github.com/renguanjie/ai-memory
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["git","node"],"env":["FEISHU_USER_ID"]},"primaryEnv":"FEISHU_USER_ID"}}
---

# Elite Memory - 终极 AI 记忆系统

为 AI Agent 打造的完整记忆管理系统，支持双层记忆架构、GitHub 自动同步、飞书通知。

## 核心功能

### 双层记忆架构

```
当日对话 → memory/YYYY-MM-DD-temp.md (临时记忆，实时写入)
              ↓
         次日 08:00
              ↓
    分析临时记忆 → 提取关键点
              ↓
    ┌───────────┴───────────┐
    ↓                       ↓
memory/YYYY-MM-DD.md   MEMORY.md
(正式日记)            (长期记忆提炼)
```

### 自动化任务

| 时间 | 任务 | 脚本 |
|------|------|------|
| **每日 23:55** | Git 同步到 GitHub | `sync-memory-to-github.sh` |
| **每日 08:00** | 读取昨日记忆 + 创建今日记忆 | `morning-memory-read.sh` |
| **每次对话后** | 实时写入临时记忆 | 手动调用 `analyze-memory.sh` |

## 使用方法

### 初始化记忆系统

```bash
# 1. 创建记忆目录
node scripts/init.mjs

# 2. 配置 GitHub remote
gh repo create ai-memory --private
git remote add memory git@github.com:username/ai-memory.git

# 3. 配置飞书通知 (可选)
export FEISHU_USER_ID="ou_xxxxx"
```

### 记忆操作

```bash
# 分析对话并写入临时记忆
node scripts/analyze.mjs "对话内容" --topic "主题"

# 手动同步到 GitHub
node scripts/sync.mjs

# 查看记忆状态
node scripts/status.mjs
```

### 定时任务配置

```bash
# 添加到 crontab
crontab -e

# 每日 23:55 同步
55 23 * * * ~/.openclaw/workspace/scripts/sync-memory-to-github.sh

# 每日 08:00 读取
0 8 * * * ~/.openclaw/workspace/scripts/morning-memory-read.sh
```

## 记忆文件结构

```
workspace/
├── MEMORY.md                      # 长期记忆 (curated)
├── SESSION-STATE.md               # 会话状态
└── memory/
    ├── YYYY-MM-DD-temp.md         # 临时记忆 (当日)
    ├── YYYY-MM-DD.md              # 正式记忆 (归档后)
    ├── projects/
    │   └── [project-name].md      # 项目记忆
    ├── skills/
    │   └── [skill-name].md        # 技能学习记忆
    └── people/
        └── [person-name].md       # 人员记忆
```

## 飞书通知

配置 `FEISHU_USER_ID` 环境变量后，同步完成会自动发送通知：

- ✅ 同步成功：包含变更详情
- ❌ 同步失败：包含错误信息

## WAL 协议 (Write-Ahead Logging)

记忆写入规则：

1. **用户表达偏好** → 立即写入 `MEMORY.md` → 再回应
2. **用户做出决策** → 立即写入当日记忆 + `MEMORY.md` → 再回应
3. **发现错误/教训** → 立即写入当日记忆 → 再回应
4. **项目相关上下文** → 写入 `memory/projects/[project].md`

## 故障排查

### 日志位置

```bash
# 同步日志
tail -f ~/.openclaw/workspace/logs/memory-sync.log

# 晨间读取日志
tail -f ~/.openclaw/workspace/logs/memory-morning.log
```

### 常见问题

**Q: Git 推送失败**
A: 检查网络连接，运行 `git pull --rebase memory main` 后再试

**Q: 飞书通知不发送**
A: 检查 `FEISHU_USER_ID` 是否配置正确

**Q: 记忆文件丢失**
A: 从 GitHub 恢复：`git pull memory main`

## 相关资源

- GitHub 仓库：https://github.com/renguanjie/ai-memory
- 文档：https://docs.openclaw.ai/memory
