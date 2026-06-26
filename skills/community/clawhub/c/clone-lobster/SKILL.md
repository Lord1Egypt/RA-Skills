---
name: clone-lobster
description: |
  OpenClaw/CatPaw 配置与上下文自动备份恢复工具。在使用 OpenClaw 过程中自动保留配置变更、工作区文件、对话上下文、已安装 Skills 和系统改动到 Git 仓库。
  触发场景：(1) 用户要求备份/保存当前配置 (2) 用户要求恢复之前的配置 (3) 对话中产生了重要的配置变更、skill 安装、系统修改等需要持久化的改动 (4) 用户提到"备份"、"保存配置"、"恢复配置"、"克隆龙虾"等关键词
  作者：李平江
---

# 🦞 克隆龙虾 - OpenClaw 配置自动备份

将 OpenClaw/CatPaw 的配置、上下文、Skills 和系统改动自动备份到 Git 仓库。

## 前置要求

1. 已配置 SSH 密钥可访问 Git 仓库
2. 设置备份仓库地址环境变量：`CLONE_LOBSTER_REPO_URL`

## 备份内容

| 类别 | 路径 | 说明 |
|------|------|------|
| 工作区 | `~/.openclaw/workspace/` | AGENTS.md, SOUL.md, USER.md, MEMORY.md, memory/ 等 |
| 配置 | `~/.openclaw/` | openclaw.json, exec-approvals.json |
| Skills | `~/.openclaw/skills/` | 所有用户安装的 skills |
| 系统 | `/etc/supervisor/` 等 | supervisord.conf, 桌面启动脚本, SSH 配置 |
| 上下文 | `~/.openclaw/data/` | session 数据库和 memory 索引 |

## 使用方式

### 自动备份（推荐）

在对话中检测到以下变更时，自动触发备份：
- 修改了 AGENTS.md, SOUL.md, USER.md 等工作区文件
- 安装了新的 skill
- 修改了 openclaw.json 配置
- 修改了系统配置（supervisor, 桌面环境等）
- 用户明确要求"备份"

执行备份：

```bash
export CLONE_LOBSTER_REPO_URL="ssh://git@git.sankuai.com/~lipingjiang/catclaw_configuration.git"
bash scripts/backup.sh "描述本次变更"
```

### 手动恢复

```bash
export CLONE_LOBSTER_REPO_URL="ssh://git@git.sankuai.com/~lipingjiang/catclaw_configuration.git"

# 恢复全部
bash scripts/restore.sh --all

# 仅恢复工作区
bash scripts/restore.sh --workspace

# 仅恢复配置
bash scripts/restore.sh --config

# 仅恢复 Skills
bash scripts/restore.sh --skills
```

## 自动触发规则

Agent 在以下情况下应主动运行备份脚本：

1. **配置变更后**：修改了 openclaw.json、workspace 文件、或安装了 skill
2. **系统变更后**：修改了 supervisor 配置、安装了新软件包、修改了桌面环境
3. **对话结束前**：如果本次对话中有重要变更，在结束前执行一次备份
4. **用户请求时**：用户说"备份"、"保存"、"同步"等关键词
5. **心跳检查时**：可在 HEARTBEAT.md 中添加定期备份任务

## 注意事项

- 备份脚本会自动排除 `node_modules`、`__pycache__` 等无需备份的目录
- 敏感信息（API keys、密码）在 openclaw.json 中，确保仓库访问权限受控
- 首次使用需确保 Git 仓库已创建且 SSH 密钥有读写权限
- 备份脚本是幂等的，重复运行不会产生问题
