---
type: reference
audience: skill-self
---

# 环境自动探测与适配

> 本文件在 Skill 激活、或用户问"在这里怎么用 Quill"时加载。
> Quill 不假设运行环境；激活时先自动探测当前 harness / agent 环境，再按其特征适配——这是自动探测功能，不是手动配置。
> 除主流 harness 外，**仅在技术上有真实需要时**才探测 CC Switch（见下"CC Switch"段）。

## 为什么自动探测

不同 harness 的 skill 安装路径、文件读写工具、frontmatter 约定、CLI 可用性都不同。
硬编码任一环境都会在别处失效。因此 Quill 激活时先"问清自己在哪"，再决定怎么动手。
所有探测都由模型读取环境得出，不跑脚本。

## 探测信号

综合判断当前环境（单一信号不足以下结论，至少两处印证）：

| 信号 | 探法 | 指向 |
|------|------|------|
| 环境变量 | 读 `$env:DSH_*`、`$env:CODEX_*`、`$env:CLAUDE_*` 等 | DSH / Codex / Claude |
| 配置目录 | 查 `~/.agents/skills/`、`~/.claude/skills/`、`.opencode/`、`~/.config/opencode/` | Codex / Claude Code / OpenCode |
| 工作目录特征 | 是否在 Obsidian Vault（含 `00-Inbox` `04-归档` 等 PARA 目录、`.obsidian/`） | Obsidian Agent Client |
| 可用工具 | 是否有 `obsidian` CLI、文件工具名（read/write/edit）、`present` 工具 | Obsidian Agent Client / DSH / 通用 |
| 上下文提示 | 系统提示里的 harness 自称、AGENTS.md / CLAUDE.md 是否在仓 | 各 harness |
| CC Switch（按需） | 只查 `~/.cc-switch/skills/` 是否存在、符号链接指向何处 | 由 CC Switch 托管配置与 skill 符号链接 |

## 适配要点

确定环境后，按其特征调整 Quill 的执行方式：

- **Codex（`~/.agents/skills/quill/`）**：用其文件工具读写；遵循仓内 AGENTS.md；skill 由 Codex 按 description 自动触发。
- **Claude Code（`~/.claude/skills/quill/`）**：同上，遵循 CLAUDE.md；frontmatter `description` 是触发主机制。
- **OpenCode（`.opencode/skills/quill/` 项目级，或 `~/.config/opencode/skills/quill/` 全局）**：项目级优先；按 OpenCode 的 skill 加载语义。
- **Obsidian Agent Client（ACP）**：在 Vault 内工作；优先用 `obsidian` CLI（前提：Obsidian 桌面应用在运行）；遵循 Vault 的 PARA / frontmatter / 双链 / 脚注约定；文章落 `40-Writing/`。
- **DSH（DeepSeek Harness）**：用 `read` / `write` / `edit`、`present` 声明交付；`write` 在某些工作区可能受限（如 EISDIR），改用 PowerShell `Set-Content -Encoding utf8NoBOM` 落盘。
- **CC Switch 托管（`~/.cc-switch/` 存在）**：CC Switch 是管理 Claude Code / Codex / Gemini CLI / OpenCode / OpenClaw / Hermes 等多 CLI 的桌面层，把 skill 从 `~/.cc-switch/skills/quill/` 符号链接进各 app。技术上的真实需要是：**当要修改 Quill skill 本身时**，改 `~/.cc-switch/skills/quill/` 源文件，勿改各 app 下的链接副本（否则切换 provider 后可能丢失）；安装/更新 Quill 走 CC Switch 的 Skills 面板（GitHub/ZIP 一键安装，双向同步）。只碰 `skills/` 这个目录——`cc-switch.db` 与 `settings.json` 是 provider 配置，可能存着 API key，**不读**；确实需要看再问用户。provider 切换对写作任务无直接影响，仅在维护 skill 时关心。
- **其他 / 不确定**：用最通用的文件读写方式；列候选环境请用户确认。

## 通用不变量（任何环境都遵守）

- 模型驱动，不依赖脚本（无 `.mjs`）。
- 读取 > 建议 > 手动修改；重大改动需人工确认。
- 禁止批量改库（Obsidian 知识库红线：禁止脚本批量修改笔记）。
- frontmatter 英文键名；文章单文件 + 四文件资产结构。

## 探测结果记录

激活探测后，用一句话向用户确认环境与适配方式，例如：

> 检测到环境：Obsidian Agent Client（Vault 内，obsidian CLI 可用）。Quill 将在 40-Writing/ 下建项目，遵循 PARA 与脚注溯源。

若探测不确定，列出候选环境并请用户确认，不要默认假设。

## 参考

- CC Switch 官方仓库：https://github.com/farion1231/cc-switch （数据存储见其 FAQ；最小侵入原则：卸载后 CLI 仍可用）
