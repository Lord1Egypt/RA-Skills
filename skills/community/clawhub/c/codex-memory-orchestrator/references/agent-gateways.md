# Agent 一键新对话承接 · 能力矩阵

> 规则：一切仍只在本机完成。不把任何会话内容发到云端；跳转第三方 Agent 只做本机应用启动 + 剪贴板注入。
> 生成/登记/复制/打开由 `scripts/handoff_gateway.py` 执行；Codex 的 `full_auto` 由 Agent 在本 app 内直接调用
> `create_thread` / `fork_thread`（同目录）并把续接文本作为新线程首条 user 消息。

## 能力分级

| 级别 | 含义 | 用户侧效果 |
|---|---|---|
| full_auto | 新对话 + 注入初始续接文本全自动 | 点“确定”即开新对话并承接 |
| deep_link | 支持深链带初始文本 | 打开新窗口 + 续接文本已在剪贴板，用户粘贴 |
| manual | 只有“开新窗口/打开应用”能力 | 生成恢复包 + 复制剪贴板 + 打开目标应用/目录，用户粘贴 |

## 矩阵（handoff_gateway.py CAPS 为准）

| Agent | 能力 | 新对话入口 | 是否支持注入初始文本 | 凭证/调用方式 | 验证方式 |
|---|---|---|---|---|---|
| codex | full_auto | 本 app `create_thread`/`fork_thread`（同目录） | 是（首条 user 消息） | 本 app 线程工具 | 新 thread 首条消息含续接文本 |
| claude | deep_link（应用未装时自动降级 manual） | `claude://new?text=<续接>` | 是（深链参数） | 深链 + 剪贴板 | 打开新窗口后粘贴文本可还原（2026-10-19 本机实测：Claude 桌面未安装 → 自动降级 manual） |
| cursor | manual | 打开 Cursor 新窗口 | 否 | `open -a Cursor` + 剪贴板 | 用户粘贴后 5 行复述 |
| cline | manual | 打开项目/VSCode | 否 | `open -a Cline` + 剪贴板 | 同上 |
| windsurf | manual | 打开 Windsurf | 否 | `open -a Windsurf` + 剪贴板 | 同上 |
| chatgpt | manual | 打开 ChatGPT | 否 | `open -a ChatGPT` + 剪贴板 | 同上 |
| local/未知 | manual | 无（仅恢复包+剪贴板，可选 `--open-app`） | 否 | 剪贴板 | 同上 |

## 命令

```sh
# Codex（full_auto，由 Agent 在本 app 内执行，脚本仅准备续接文本）
python3 <skill>/scripts/handoff_gateway.py --agent codex --project <项目> --thread-id <ID> --dry-run --json

# Claude（deep_link）
python3 <skill>/scripts/handoff_gateway.py --agent claude --project <项目> --thread-id <ID> --dry-run --json

# 手动 Agent（manual）：dry-run 只打印命令；去掉 --dry-run 才真正复制剪贴板并打开应用
HANDOFF_NO_CLIPBOARD=1 python3 <skill>/scripts/handoff_gateway.py --agent cursor --project <项目> --thread-id <ID> --dry-run
python3 <skill>/scripts/handoff_gateway.py --agent cursor --project <项目> --thread-id <ID>
```

## 私密与安全

- 脚本不调用 socket/requests/urllib/http；不开任何网络端口。
- 恢复包只在本机生成；打开新对话只做本机应用跳转，不涉及云端上报。
- 跳转第三方 Agent = 在本机启动该应用并注入文本；若第三方 Agent 连接到云（如 Claude/ChatGPT 网页版），装入公司内容前仍需先经用户确认是否外发。
- `handoff_gateway.py` 每次运行先探测目标应用是否可打开（macOS 用 `open -Ra`，只检测不启动）：deep_link 应用未安装时自动降级为 manual（生成恢复包 + 剪贴板），不再硬调 `claude://` 深链。
- 跨 Agent 开新对话框前必须确认目标 Agent 与目标对话框标题；真实执行期写入 `$CODEX_HOME/audit.log`。
