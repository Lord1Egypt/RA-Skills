# AGENTS.md

> 给任意 AI 编码/助手代理（Codex、Cursor、Cline、Aider、OpenClaw 等）或人类使用的入口说明。
> 本仓库是一个**工具**，不是某个助手专属的 skill。`SKILL.md` 只是 Claude Code 的自动触发外壳；
> 真正的功能是下面这些可直接运行的 Node 脚本。任何能执行 shell 的代理都能驱动它。

## 这是什么

把 BOSS 直聘"新招呼收件箱"自动化：读简历 → 同步飞书多维表格 → 有附件下附件、没附件要简历。
内置反风控节奏层。详见 [README.md](./README.md)。⚠️ 使用前读 [DISCLAIMER.md](./DISCLAIMER.md)。

## 前置

- Node.js ≥ 20
- [OpenCLI](https://github.com/jackwener/opencli) + Browser Bridge 扩展，且 Chrome 已登录 BOSS 招聘端（`opencli doctor` 全绿）
- 安装配套适配器：`cp adapters/boss/attachment.js ~/.opencli/clis/boss/`
- 配置飞书目标表（见下）

## 代理该怎么用（不依赖任何特定助手）

1. **首次配置飞书表**（解析链接+持久化）：
   ```bash
   node scenarios/setup.mjs "<飞书/base/链接?table=...>" --token "pt-<授权码>"
   # 或本机 lark-cli OAuth 模式：node scenarios/setup.mjs "<飞书表链接>"
   node scenarios/setup.mjs --show
   ```

2. **跑场景1**：
   ```bash
   node scenarios/inbox.mjs --limit 10          # 安全：只读+同步，打招呼仅 DRY-RUN
   node scenarios/inbox.mjs --live --limit 3    # 对外：真发要简历消息（不可撤回，小批量盯着跑）
   ```

3. **解析输出**：脚本输出结构化进度与汇报到 stdout；记忆/状态存于 `~/.opencli/boss-recruit/task-memory.json`。

## 代理须遵守的硬规则（来自反风控设计）

- `--live` 是**对外、不可撤回**动作：代理**不得**在用户未明确同意的情况下自行加 `--live`。默认 DRY-RUN。
- 首次真发务必小批量（`--limit 2~3`）并向用户汇报每条将发送的话术。
- 出现验证码/登录失效/权益耗尽 → 脚本会自动熔断暂停；代理应如实转达，不要绕过重试。
- 不要把飞书授权码、登录凭证写进任何提交或日志。

## 内核可复用

`lib/` 下的模块（`rhythm.mjs` 反风控节奏层、`feishu-base.mjs` 授权码 base-api 后端、`task-memory.mjs` 状态机）都是无第三方依赖的纯 ESM，可被其它项目直接 import 复用。
