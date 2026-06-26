# CLS CLI

腾讯云日志服务 (Cloud Log Service) 命令行工具，专为 **AI Agent** 和开发者设计。

> 安装后配合 Claude Code / Cursor 等 AI 编程工具使用，用自然语言即可完成日志检索、告警管理、采集配置等操作——无需记忆任何命令。

## 快速开始

### 安装

```bash
cd cls-cli
go build -o cls-cli .
sudo mv cls-cli /usr/local/bin/
```

### 升级到最新版

```bash
cls-cli upgrade
```

### 初始化配置

```bash
cls-cli config init --secret-id <YOUR_SECRET_ID> --secret-key <YOUR_SECRET_KEY> --region ap-guangzhou
```

也支持环境变量：

```bash
export TENCENTCLOUD_SECRET_ID=xxx
export TENCENTCLOUD_SECRET_KEY=xxx
export CLS_DEFAULT_REGION=ap-guangzhou
```

### 使用方式

**推荐：自然语言 + AI Agent**

在 Claude Code 等工具中直接说：

```
"帮我查一下最近1小时 topic xxx 里有没有 ERROR 日志"
"创建一个告警，当错误数超过100就通知我"
"看一下机器组里哪些机器离线了"
```

AI 会自动调用 cls-cli 完成操作。

**直接使用 CLI：**

```bash
# 搜索日志
cls-cli log +search --topic-id xxx --query "level:ERROR" --from "1 hour ago"

# 列出日志主题
cls-cli topic +list

# 查看告警历史
cls-cli alarm +history --alarm-id xxx --from "7 days ago"

# 查看机器组状态
cls-cli machinegroup +status --group-id xxx
```

## 命令总览

| 域 | 别名 | 快捷命令 | 说明 |
|---|---|---|---|
| `log` | - | `+search` `+context` `+tail` `+histogram` `+download` | 日志检索与分析 |
| `topic` | - | `+list` `+create` `+info` `+delete` `+logsets` | 日志主题管理 |
| `alarm` | - | `+list` `+history` `+create` `+delete` `+notices` | 告警策略管理 |
| `machinegroup` | `mg` | `+list` `+create` `+delete` `+info` `+status` | 机器组管理 |
| `collector` | `col` | `+list` `+create` `+delete` `+info` `+guide` | 采集配置管理 |
| `dashboard` | `dash` | `+list` `+info` `+create` `+update` `+delete` | 仪表盘管理 |
| `loglistener` | `ll` | `+install` `+init` `+start` `+stop` `+restart` `+status` `+uninstall` `+check` | LogListener 管理 |
| `config` | - | `init` `show` | 配置管理 |
| `api` | - | `<Action>` | 通用 API 调用（支持所有 CLS API 3.0） |
| `upgrade` | - | - | 自动升级到最新版 |

## 架构设计

```
用户 (自然语言)
    ↓
AI Agent (Claude Code / Cursor / IM Bot)
    ↓
cls-cli (命令行工具)
    ↓
腾讯云 CLS API 3.0
```

- **两层命令体系**：`+` 前缀快捷命令（语义化）+ `api` 通用命令（覆盖全量 API）
- **极简依赖**：仅依赖 `cobra`，签名算法自行实现
- **灵活时间解析**：支持 `15 minutes ago`、`today`、`2024-01-01` 等多种格式
- **多输出格式**：`--format json|pretty|table|csv`
- **Dry-run 模式**：`--dry-run` 预览请求，不实际执行
- **全局 Region 切换**：`--region ap-beijing` 任何命令都可以临时切换地域

## AI Agent Skill

仓库根目录的 [SKILL.md](./SKILL.md) 是面向 AI Agent 的完整使用文档。将它加载到你的 AI 编程工具（Claude Code / Cursor / CodeBuddy 等）中，AI 就能自动安装、配置和使用 cls-cli 完成各种 CLS 操作。

也可以从 [ClawHub](https://clawhub.ai) 搜索 `cls-cli` 一键安装此 Skill。

## License

MIT
