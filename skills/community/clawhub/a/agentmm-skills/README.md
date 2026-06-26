# AgentMM Skill

[![ClawHub](https://img.shields.io/badge/clawhub-agentmm-blue)](https://clawhub.ai/skills/agentmm)

为 AI Agent 提供**持久化记忆存储**和**结构化日志系统**的 OpenClaw Skill，基于 [AgentMM](https://agentmm.site) 服务。

## 功能

- 🧠 **记忆管理**：写入、查询、搜索、更新、遗忘记忆，支持标签/上下文/关联/重要性评分
- 📋 **日志系统**：5 级别日志写入/查询/统计，支持 task_id 关联任务
- 🔄 **增量同步**：通过 `sync_daemon.sh` 定期拉取变更，适合本地缓存场景

## 安装

```bash
clawhub install agentmm
```

安装后在 OpenClaw 设置中配置环境变量：

```bash
export AGENTMM_API_KEY="amm_sk_your_key_here"
```

API Key 在 [agentmm.site](https://agentmm.site) 注册后从 Dashboard 获取。

## 快速上手

```bash
# 写入记忆
agentmm write --key "user_lang" --content "用户偏好中文回复" --tags "preference"

# 搜索记忆
agentmm search --query "用户偏好"

# 写入日志
agentmm log write --level info --title "任务完成" --task-id task_001

# 查询错误日志
agentmm log list --level error --limit 20
```

## 依赖

- `curl`
- `jq`

## 环境变量

| 变量 | 必填 | 说明 |
|---|---|---|
| `AGENTMM_API_KEY` | ✅ | API 密钥，格式 `amm_sk_xxx`，从 Dashboard 获取 |
| `AGENTMM_API_BASE` | 可选 | 自定义 API 地址，默认 `https://api.agentmm.site` |

## 数据与隐私

记忆内容和日志内容会通过 HTTPS 发送至 AgentMM 服务端持久化存储。API Key 仅从环境变量读取，不会写入任何文件。详见 [SKILL.md](./SKILL.md#security--privacy)。

## 链接

- 服务主页：[agentmm.site](https://agentmm.site)
- GitHub：[github.com/cers-ai/agentmm-skills](https://github.com/cers-ai/agentmm-skills)
- 问题反馈：[GitHub Issues](https://github.com/cers-ai/agentmm-skills/issues)
