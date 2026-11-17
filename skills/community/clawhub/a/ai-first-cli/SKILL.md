---
name: ai-first-cli
description: "This skill should be used when designing, building, or reviewing a command-line tool that AI agents will call, not just humans. Use it when deciding output format (JSON vs text), error handling, exit codes, flags, discoverability, dependencies and packaging, or autonomous-operation safety for a CLI. Also use it when asked how to make an existing CLI agent-friendly, or to evaluate a tool against the agent-first design philosophy. Grounded in Vercel's cloud-for-agents methodology."
---

# AI-First CLI 设计哲学

## 核心命题

**CLI 的首要读者正在从人变成 agent。** 过去 CLI 为人优化（漂亮的表格、交互式提示、彩色输出、man page）；agent-first 的 CLI 把这些当成"次要降级路径"，把**机器可调用、可预测、可解析**当成主路径——同时不牺牲人的体验。

一句话判据：**一个 agent 读完命令的输出，应该确切知道下一步做什么——不用猜、不用幻觉命令、不用卡住。**

这不是给旧 CLI 加个 `--json` 就完事。是把"使用者会读报错、会手动调试、会读文档"这套人类假设**整个倒过来**重做接口。Vercel 把它推到极致：CLI 转零依赖自更新签名二进制、Sandbox 内跑 Docker、甚至造了 Zero 语言让编译器吐 JSON 诊断给 agent 修。详见 `references/vercel-case-study.md`。

## 何时用本技能

- 设计 / 重写一个会被 AI agent 调用的 CLI
- 评审一个 CLI 是否"agent 友好"
- 纠结：要不要做 MCP server，还是把 CLI 做好就够了
- 决定输出格式、错误结构、退出码、flag、打包方式
- 给现有工具加 agent 安全护栏（dry-run、输入校验、幂等）

不适用：纯人机交互的本地工具（如个人 dotfiles 脚本），或决策已被 lint/schema 机械约束的场景。

## 十二条原则（速查）

| # | 原则 | 一句话 |
|---|------|--------|
| 1 | 机器输出是默认，不是选项 | `--json` 结构化信封；TTY 给人看，管道给机器 |
| 2 | stdout/stderr 分流 | 数据走 stdout，诊断/日志/错误走 stderr，管道才干净 |
| 3 | 接收原始 payload | 允许直接传与 API schema 同构的 JSON，LLM 零翻译损失 |
| 4 | 错误要可执行 | 退出码 + 稳定错误码 + message + 修复命令 + 重试提示 |
| 5 | 自描述、可发现 | `--help`、schema introspection、`explain CODE`，CLI 是"此刻 API 接受什么"的唯一真相源 |
| 6 | 默认非交互 | 每个提示都有 flag 绕过；env var 认证，无浏览器登录 |
| 7 | 零依赖、自包含 | 单一签名二进制，快启动、可信、沙箱里无依赖链惊喜 |
| 8 | 可组合（Unix） | 可 pipe、读 stdin、NDJSON 流式分页 |
| 9 | 自治护栏 | `--dry-run`、幂等键、输入加固、响应净化防注入 |
| 10 | 省 token | 字段裁剪、分页、简洁输出，别撑爆上下文窗口 |
| 11 | 确定性优先 | 稳定输出契约 + 版本化 schema，agent 要可预测胜过聪明 |
| 12 | 一核多面 | CLI / MCP / SDK / env var 共享同一核心能力 |

## 原则展开（关键的几条）

**1 + 2 双形态输出。** 检测 TTY：交互终端给人类友好输出，非 TTY（被管道/agent 调用）默认结构化。或显式 `--json`。结构化信封要稳定：`{ "ok": bool, "data": ..., "error": ... }`。数据只走 stdout，这样 `cmd --json | jq` 不会被日志污染。

**4 可执行错误。** 反例：`Error: something went wrong`（exit 1）。正例：
```json
{"ok": false, "error": {
  "code": "AUTH_004",
  "message": "Token expired",
  "fix": "run `tool auth login`",
  "retryable": false
}}
```
错误码要**稳定**（agent 靠它精确匹配，而不是解析自然语言），并配 `tool explain AUTH_004` 给结构化解释——别让 agent 去爬外部文档。

**5 自描述。** `--help` 是 agent 的发现入口（这也是"CLI 是新 MCP"论点的核心：现成 CLI 自带 `--help`、自带认证/分页/重试，零集成负担）。更进一步：内置 schema introspection 命令、随二进制版本对齐的用法指引（Vercel Zero 的 `zero skills`），解决"外部文档与实际版本不同步"。

**6 非交互默认。** agent 跑在 headless 环境，任何 `Are you sure? [y/N]` 都会让它卡死。规则：**每个交互提示必须有 flag 旁路**（`--yes` / `--force`），凭证走环境变量。

**7 零依赖二进制。** 动机：agent 在临时沙箱里反复拉起工具，依赖链 = 不可预测 + 慢 + 攻击面。单一**代码签名**二进制可验证来源、快启动、跨平台。这正是 Vercel CLI 改造的方向。

**9 自治护栏。** agent 会幻觉输入——"build like it"。校验并拒绝路径穿越、控制字符、注入；变更操作给 `--dry-run`；副作用操作用幂等键（同键重试不重复执行）；返回数据做净化，防止响应里夹带的 prompt injection 顺着喂进 agent。**若工具会执行 agent 产出的代码/命令**，输入校验只是第一层——隔离要做到 **VM 级（trust-domain microVM）**，而非容器级共享内核：默认假设"agent 生成的代码不可信"。这正是 Vercel Sandbox 的核心论点（详见案例）。

## CLI vs MCP（常见决策）

| 维度 | 做好 CLI | 写 MCP server |
|------|---------|--------------|
| 集成成本 | 零（agent 直接 shell out） | 每个集成建专用 server |
| 可组合 | Unix pipe 天然 | 协议内组合较弱 |
| 发现 | `--help` 自带 | 需 schema 定义 |
| 权限/审计 | 复用系统权限 + shell history | 另建 |
| 何时选 MCP | 需要持久连接、结构化双向流、富类型协商时 |

经验法则：**先把 CLI 做成 agent-first，多数场景就够了；MCP 留给真正需要有状态协议的场景。** 一核多面（原则 12）让两者共享同一底层。

## 反模式

- `200-with-error-body`：永远退出 0，把错误塞进正文 → agent 以为成功
- 人类输出和机器输出混在 stdout
- 报错只有散文，没有稳定码，没有修复建议
- 默认交互、没有 `--yes` 旁路 → headless 卡死
- 输出不稳定（随机顺序、带时间戳/颜色码污染 JSON）
- 信任 agent 输入不校验
- 文档在外部网站，和二进制版本漂移

## 自检清单

- [ ] 非 TTY 下默认结构化输出？`--json` 存在？
- [ ] 数据→stdout，日志/错误→stderr？
- [ ] 失败退出码非 0，且错误带 code+message+fix+retryable？
- [ ] 错误码稳定且有 `explain`？
- [ ] 每个交互提示都有 flag 旁路？env var 认证？
- [ ] 变更操作有 `--dry-run` / 幂等？
- [ ] 输入做了加固校验？
- [ ] 输出契约稳定、版本化、省 token？
- [ ] `--help` / schema 自描述完整？
- [ ] 打包尽量零依赖、可信？

## 来源

调研来源与 Vercel 案例细节见 `references/vercel-case-study.md` 与 `references/sources.md`。
