---
name: github-backup
description: |
  GitHub 仓库备份技能 - 将 OpenClaw 工作空间备份到 GitHub 私有仓库。
  支持两种模式：(1) 自动模式 - 定时自动备份 (2) 手动模式 - 交互式配置向导。
  自动引导用户完成：GitHub Token 配置 → 仓库创建 → 初始化备份 → 设置定时任务。
  用途：(1) 首次设置 (2) 手动备份 (3) 恢复 (4) 修改配置
metadata: {"openclaw": {"emoji": "📦"}}
---

# GitHub 仓库备份

自动将工作空间备份到 GitHub 私有仓库的完整解决方案。

## 触发方式

| 触发词 | 模式 | 说明 |
|--------|------|------|
| "设置 GitHub 备份" | 手动 | 运行交互式配置向导 |
| "自动备份到 GitHub" | 自动 | 设置定时任务 |
| "立即备份" | 手动 | 立即执行一次备份 |
| "查看备份状态" | 手动 | 检查备份状态 |

---

## 手动模式：交互式配置向导

当用户说"设置 GitHub 备份"时，进入交互式问答：

### 问题 1：GitHub 用户名
> 请告诉我你的 GitHub 用户名是什么？

等待用户回答（如：ziqi-jin）

### 问题 2：仓库名
> 你想用什么名字创建备份仓库？
> 建议：`jeremy-agents-backup` 或 `openclaw-backup`

等待用户回答

### 问题 3：GitHub Token
> 现在需要生成 GitHub Token：
> 1. 访问 https://github.com/settings/tokens
> 2. 点击 "Generate new token (classic)"
> 3. Note 填写：`backup-token`
> 4. 勾选 `repo` 权限
> 5. 点击生成，然后复制 Token 给我

等待用户粘贴 Token（验证 Token 格式：ghp_ 开头）

### 问题 4：备份时间
> 选择每天自动备份的时间：
> - A) 凌晨 3:00
> - B) 早上 7:00  
> - C) 中午 12:00
> - D) 下午 6:00
> 
> 或者输入你希望的具体时间（如：每天下午 5 点）

等待用户选择或输入

### 问题 5：确认
> 配置确认：
> - GitHub 用户名：[用户名]
> - 仓库名：[仓库名]
> - 备份时间：[时间]
> 
> 确认请回复"确认"或"yes"，修改请回复具体要改的部分

用户确认后，执行初始化并设置定时任务。

---

## 自动模式：定时备份

当用户选择自动模式或确认配置后：

### 1. 执行首次备份
```bash
git add AGENTS.md SOUL.md USER.md IDENTITY.md TOOLS.md HEARTBEAT.md skills/ memory/
git commit -m "Initial backup: $(date +%Y-%m-%d)"
git push origin main
```

### 2. 设置 OpenClaw Cron
```bash
openclaw cron add --name "github-backup" --cron "0 <hour> * * *" --message "执行 GitHub 备份" --agent main
```

---

## 手动触发：立即备份

当用户说"立即备份"或"现在备份"时：

```bash
cd /root/.openclaw/workspace
git add AGENTS.md SOUL.md USER.md IDENTITY.md TOOLS.md HEARTBEAT.md skills/ memory/
git commit -m "Manual backup: $(date +%Y-%m-%d_%H:%M)"
git push origin main
```

完成后告诉用户备份结果。

---

## 查看备份状态

当用户说"备份状态"或"上次备份什么时候"时：

```bash
cd /root/.openclaw/workspace
git log -1 --format="最后备份: %cd"
git status
git remote -v
```

显示：
- 最后备份时间
- 当前状态（有/无未提交更改）
- 远程仓库配置

---

## 故障排除

### 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| Token 无效 | token 过期或权限不足 | 重新生成有 repo 权限的 token |
| 仓库不存在 | 仓库名拼写错误 | 检查仓库名是否正确 |
| Push 失败 | 没有权限或网络问题 | 检查 token 权限和网络 |
| 定时不执行 | cron 配置错误 | 用 `openclaw cron list` 检查 |

### 手动修复命令

```bash
# 检查远程仓库
git remote -v

# 重新设置远程
git remote set-url origin https://x-access-token:TOKEN@github.com/user/repo.git

# 查看 cron 任务
openclaw cron list

# 手动运行备份
bash ~/.openclaw/workspace/skills/github-backup/scripts/backup.sh
```

---

## 备份内容

✅ **会备份**
- `skills/` - 所有已安装的技能
- `memory/` - 记忆文件
- `AGENTS.md` - Agent 配置
- `SOUL.md` - AI 身份
- `USER.md` - 用户信息
- `IDENTITY.md` - 身份信息
- `TOOLS.md` - 工具配置
- `HEARTBEAT.md` - 心跳任务
- `README.md`, `SYNC.md` - 文档

❌ **不会备份**
- `.clawhub/` - 缓存
- `.openclaw/` - 运行时
- `node_modules/` - 依赖
- `*.log` - 日志
- `*.tmp` - 临时文件
- API Keys - 敏感信息

---

## 恢复指南

用户需要恢复时说"从 GitHub 恢复"：

```bash
# 1. 克隆仓库
git clone https://github.com/[user]/[repo].git /tmp/restore

# 2. 恢复文件
cp -r /tmp/restore/* ~/.openclaw/workspace/

# 3. 重新配置环境变量
# (因为敏感信息不在备份中)
```

---

## 交互提示词

触发本技能的关键词：
- "设置 GitHub 备份"
- "备份到 GitHub"
- "自动备份"
- "手动备份"
- "立即备份"
- "备份状态"
- "查看备份"
- "github backup"
- "配置定时备份"