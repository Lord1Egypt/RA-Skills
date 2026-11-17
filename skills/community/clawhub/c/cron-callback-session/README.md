# cron-callback-session

**OpenClaw / QClaw 技能：会话回调（Session Callback）**

实现「用 A 会话调起/注入 B 会话」的能力：cron 任务、外部进程或另一个会话可向目标会话注入消息，唤醒其 agent 带完整上下文继续推进。

> 姊妹技能（WorkBuddy 版）：[workbuddy-skill-session-callback](https://github.com/onesfuture/workbuddy-skill-session-callback) — 基于 WorkBuddy ACP 协议的原生实现。

## 能力

- **cron 回调当前对话**：一次性/周期 cron job 执行完毕后，把结果通过 `sessions_send` 注入当前对话，使 agent 基于原上下文继续推进任务
- **非 cron 用法**：
  - 另一个会话处理完长任务后，把结果回传到主会话继续汇总
  - 外部脚本/进程在特定时机向指定会话注入提示，触发其 agent 执行
  - 监控/看门狗类任务发现异常时，向主对话注入警报并让 agent 介入处理

## 解决的问题

默认 `cron sessionTarget=isolated` 会在独立会话运行，任务结果上报到新对话，原对话不推进。本技能通过 `sessions_send` 把结果注入当前对话。

**关键前提**：`tools.sessions.visibility` 需设为 `agent`（默认 `tree` 只允许同一会话树内发送，cron isolated 会话不在树内 → forbidden）。

## 平台

- **OpenClaw**（原生）：`sessions_send` / cron 机制直接适用
- **QClaw**（桌面客户端/界面）：基于 OpenClaw 内核，同一套配置体系，完全适用
- 配置路径不硬编码：用 `openclaw config file` 自动发现

## 忙时队列行为（重要）

`sessionTarget=isolated` 的 cron 会话调用 `sessions_send` 时，消息经过**内部消息队列**投递：

- **目标会话空闲**：消息立即投递，注入方很快收到 `accepted`
- **目标会话忙**（正在处理其他回合/长任务）：消息**挂起等待**，不丢不打断；待目标会话空闲后逐条投递
- **一个空闲窗口可能只投递一条**，多条注入按序逐条到达（实测间隔 3-5 分钟）

> ⚠️ **`gateway timeout` 是误报，不是发送失败**：
> 当目标会话忙时，注入方的 `sessions_send` 调用可能返回 `gateway timeout after 10000ms`（10s 工具调用超时）。**这代表消息已入队、投递挂起，不代表发送失败。**
> **不要据此重发**——消息最终会到达，重发会造成**重复注入**（同一内容出现多次）。
>
> 注入延迟取决于目标会话的空闲节奏，实测可达 20+ 分钟。若需确认消息是否送达，以目标会话实际收到的 inter-session message 为准，而非调用返回值。

## 安全注意

- **杀进程重启网关**会中断所有活跃会话/定时任务，需在维护窗口执行
- **放宽会话路由权限**（`visibility = agent`）会让当前 agent 下任意会话可互相发送消息，使用完毕建议恢复默认 `tree`
- 详细风险警告见 [SKILL.md](SKILL.md)

## 安装

### 方式一：ClawHub（推荐）

```bash
openclaw skills install @onesfuture/cron-callback-session
```

或使用 ClawHub CLI：

```bash
clawhub install @onesfuture/cron-callback-session
```

### 方式二：手动安装

1. 下载本仓库
2. 把 `SKILL.md` 放入你的 skills 目录（OpenClaw：`~/.claw/skills/` 或发行版对应目录）
3. 按 SKILL.md 中的流程配置 `tools.sessions.visibility = agent`

## 反馈

发现 bug 或有改进建议？请开 [GitHub Issue](https://github.com/onesfuture/cron-callback-session/issues)。

## 许可证

MIT
