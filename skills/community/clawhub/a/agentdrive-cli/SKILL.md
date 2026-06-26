---
name: agentdrive
description: "AgentDrive 云存储命令行工具。通过 Shell 命令直接操作云盘：浏览目录、搜索文件、上传下载、移动重命名、删除、分享、保存 URL/文本到云盘、追加文件内容、检测重名文件、配置文件读写、查看用户信息。输出结构化 JSON，支持 jq 管道处理和批量操作。当用户需要管理云盘文件、在脚本/CI 中操作云盘、或将云盘操作与其他命令行工具组合时使用此 Skill。"
---

# AgentDrive CLI

**重要指令：** 根据用户意图，直接执行最合适的命令；不要先把所有命令罗列给用户。

## 执行模式（必须先确定）

默认使用 npx（热更新）：

```bash
AGENTDRIVE_CLI='npx -y -p @aicloud360/agentdrive@latest agentdrive'
```

当用户要求“固定版本/可复现”时，使用：

```bash
AGENTDRIVE_CLI='npx -y -p @aicloud360/agentdrive@<exact-version> agentdrive'
```

如果用户明确要求全局安装，才使用 `npm install -g @aicloud360/agentdrive`。
若用户已全局安装且确认可用，也可用 `AGENTDRIVE_CLI='agentdrive'`。

## 鉴权前检查（每次会话先做）

1. 先执行 `$AGENTDRIVE_CLI auth whoami` 检查登录状态。
2. 若未登录，执行 `$AGENTDRIVE_CLI auth login --api-key <KEY>`，或提示设置 `API_KEY` 环境变量。
3. 继续执行业务命令。

说明：鉴权优先级为 `--api-key` > `API_KEY` > `~/.agentdrive/config.json`。

## 意图与命令映射表

| 用户意图 | 命令模板 |
|---|---|
| 查看/浏览云盘目录、列出文件 | `$AGENTDRIVE_CLI dir ls [path]` |
| 创建新文件夹 | `$AGENTDRIVE_CLI dir mkdir <path>` |
| 按关键词搜索文件 | `$AGENTDRIVE_CLI file search <keyword>` |
| 上传本地文件到云盘 | `$AGENTDRIVE_CLI file upload <files> --dest <path>` |
| 下载云盘文件到本地 | `$AGENTDRIVE_CLI file download <nid> --dir <path>` |
| 移动文件或文件夹 | `$AGENTDRIVE_CLI file mv <src> <dest>` |
| 转移或复制文件到目标目录 | `$AGENTDRIVE_CLI file trans-copy <src> <dest> --delete/--replace` |
| 重命名文件或文件夹 | `$AGENTDRIVE_CLI file rename <path> <new_name>` |
| 删除文件或文件夹 | `$AGENTDRIVE_CLI file rm <path>` |
| 生成文件分享链接 | `$AGENTDRIVE_CLI file share <paths>` |
| 获取文件下载链接 | `$AGENTDRIVE_CLI file url <path>` |
| 根据 nid 获取节点信息 | `$AGENTDRIVE_CLI file node-info <nid> [--ks-ext 0|1]` |
| 统计目录递归原始大小 | `$AGENTDRIVE_CLI file origin-size <path>` |
| 清空目录下文件并保留目录 | `$AGENTDRIVE_CLI file clear-dir <path>`（每次一个目录） |
| 读取/写入配置文件（INI/JSON/YAML） | `$AGENTDRIVE_CLI file config --path <path> --command <config:*> --type <ini|json|yaml|yml>` |
| 通过 URL 或文本保存文件到云盘 | `$AGENTDRIVE_CLI file save --url/--content/--stdin` |
| 向云盘文本文件末尾追加内容 | `$AGENTDRIVE_CLI file append <path> --content/--stdin` |
| 检测目录下是否存在同名文件 | `$AGENTDRIVE_CLI file exists --path <path> --files/--stdin` |
| 微信扫码登录（无 API Key 时使用） | `$AGENTDRIVE_CLI auth login-wechat` |
| 退出登录、清除本地配置 | `$AGENTDRIVE_CLI auth logout` |
| 查看当前用户信息 | `$AGENTDRIVE_CLI user info` |
| 查看鉴权状态 | `$AGENTDRIVE_CLI auth whoami` |
| 将本地文件/目录备份到云盘 | `$AGENTDRIVE_CLI claw-backup --source <path> --dest <path>` |
| OpenClaw 模式备份（按白名单） | `$AGENTDRIVE_CLI claw-backup --source-dir <path> --claw-name <name>` |
| 将云盘目录递归恢复到本地 | `$AGENTDRIVE_CLI claw-restore --remote <path> --target <path>` |
| 启用自动备份监听 | `$AGENTDRIVE_CLI claw-auto-backup enable --source-dir <path> --claw-name <name>` |
| 停用自动备份监听 | `$AGENTDRIVE_CLI claw-auto-backup disable` |
| 查看自动备份状态 | `$AGENTDRIVE_CLI claw-auto-backup status` |

**详细的命令参数说明，请按需查阅 [references/commands.md](references/commands.md)。**

## 命令构造规则

- 全局选项（`--api-key`、`--format`、`--quiet`、`--timeout`、`--retries`）放在子命令之前。
- 云盘路径必须以 `/` 开头；目录路径建议以 `/` 结尾。
- 多文件操作用 `|` 分隔，包含 `|` 的参数必须整体加引号。

## 输出与解析

默认输出结构化 JSON；`--quiet` 只输出 `result`，便于管道解析：

```bash
# 默认 JSON（含 success/meta 包装）
$AGENTDRIVE_CLI dir ls /

# 仅返回 result 数据（适合 jq 处理）
$AGENTDRIVE_CLI --quiet dir ls / | jq '.data.list[].name'
```

## 跨平台管道模板

```bash
# macOS/Linux: 搜索文档并下载第一个结果
NID=$($AGENTDRIVE_CLI --quiet file search "月报" | jq -r '.data.list[0].nid')
$AGENTDRIVE_CLI file download "$NID" --dir ./

# macOS/Linux: 将命令输出保存到云盘
date | $AGENTDRIVE_CLI file save --stdin --dest /日志/ --filename "timestamp.txt"

# macOS/Linux: 批量删除（stdin 路径列表）
cat paths.txt | $AGENTDRIVE_CLI file rm _ --batch

# macOS/Linux: 将本地配置整文件写入云盘（config:write + --stdin）
cat local-config.json | $AGENTDRIVE_CLI file config --path /mcp/app.json --command config:write --type json --stdin

# macOS/Linux: 将本地日志追加到云盘已有文件
cat local_log.md | $AGENTDRIVE_CLI file append /项目/开发日志.md --stdin
```

Windows 等价模板：

```bash
# cmd: 从本地文件读取内容并保存
type report.md | npx -y -p @aicloud360/agentdrive@latest agentdrive file save --stdin --dest /文件夹/ --filename report.md

# PowerShell: 从本地文件读取内容并保存
Get-Content report.md -Raw | npx -y -p @aicloud360/agentdrive@latest agentdrive file save --stdin --dest /文件夹/ --filename report.md

# cmd: 将本地 JSON 整文件写入云盘配置（file config；勿用 cat，cmd 无该命令）
type local-config.json | npx -y -p @aicloud360/agentdrive@latest agentdrive file config --path /mcp/app.json --command config:write --type json --stdin

# PowerShell: 同上
Get-Content .\local-config.json -Raw | npx -y -p @aicloud360/agentdrive@latest agentdrive file config --path /mcp/app.json --command config:write --type json --stdin

# cmd: 追加本地文件内容到云盘（勿用 cat）
type local_log.md | npx -y -p @aicloud360/agentdrive@latest agentdrive file append /项目/开发日志.md --stdin

# PowerShell: 同上
Get-Content .\local_log.md -Raw | npx -y -p @aicloud360/agentdrive@latest agentdrive file append /项目/开发日志.md --stdin

# cmd：file exists --stdin 勿用 echo '...' |（单引号会进管道，JSON 非法）；先把 UTF-8 JSON 写入 files.json
type files.json | npx -y -p @aicloud360/agentdrive@latest agentdrive file exists --path /目录/ --stdin

# PowerShell：同上
Get-Content .\files.json -Raw -Encoding utf8 | npx -y -p @aicloud360/agentdrive@latest agentdrive file exists --path /目录/ --stdin
```

## 失败恢复（执行失败时）

- `code=3`（鉴权）：先 `auth whoami`，再 `auth login`，重试原命令。
- `code=4`（资源不存在）：先 `dir ls` 或 `file search` 校验路径，再重试。
- `code=6`（网络问题）：增加 `--retries 2 --timeout 60000` 重试。
- 其他错误：保留原错误输出，并提示查阅 [references/commands.md](references/commands.md) 的错误码说明。
