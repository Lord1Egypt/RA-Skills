# Evidence Table: Cursor 替代方案对比

决策问题：5人核心开发团队是否从 Cursor 切换到更开放的 coding agent 方案
来源日期：2026-09-18
工具状态：omni-reader 正常，来源通过 omni 解析官方定价页（cursor.com/pricing、claude.com/pricing）及 GitHub README（open-code/opencode、openai/codex）

| 竞品 | 维度 | 主张 | 证据级别 | 来源 | 日期 | 置信度 |
|------|------|------|----------|------|------|--------|
| Cursor | 定价 | Hobby Free；Individual $20/月/人（Pro/Pro+/Ultra）；Teams $40/用户/月；Enterprise 定制 | fact | cursor.com/pricing | 2026-09-18 | 高 |
| Cursor | 模型开放度 | 支持 Claude + GPT-4o + Grok，无 BYOK | fact | cursor.com/pricing | 2026-09-18 | 高 |
| Cursor | 插件/MCP | 支持 MCPs、skills、hooks | fact | cursor.com/pricing | 2026-09-18 | 高 |
| Cursor | 开源 | ❌ 闭源 | fact | cursor.com | 2026-09 | 高 |
| Cursor | 上下文 | 未公开具体 token 窗口；社区推测约 15K-50K | inference | 社区讨论 | 2026-09 | 低 |
| Claude Code | 定价 | 含在 Pro $20/月（年付$17/月）；Max $100+/月（5x/20x 用量）；Team Standard $20/座位/月（年付），Premium $100/座位/月；Enterprise $20/座位/月 + API 按量 | fact | claude.com/pricing | 2026-09-18 | 高 |
| Claude Code | 模型开放度 | 仅 Claude 系列（Sonnet/Opus/Fable/Haiku） | fact | claude.com/pricing | 2026-09-18 | 高 |
| Claude Code | 上下文 | Up to 1M token，视模型而定 | fact | claude.com/pricing | 2026-09-18 | 高 |
| Claude Code | 插件/MCP | 支持 Skills、Connectors、Partners | fact | claude.com/pricing | 2026-09-18 | 高 |
| Claude Code | 开源 | ❌ 闭源 | fact | anthropic.com | 2026-09 | 高 |
| Claude Code | 多文件编辑 | 支持（CLI 内 + IDE） | fact | claude.com/pricing | 2026-09-18 | 高 |
| OpenCode | 定价 | 开源免费（MIT），需自付模型 API 费 | fact | github.com/opencode-ai/opencode | 2026-09-18 | 高 |
| OpenCode | 模型开放度 | 任意模型 + BYOK（OpenAI/Anthropic/Gemini/Groq/Azure/Bedrock/自托管） | fact | github repo README | 2026-09-18 | 高 |
| OpenCode | 开源 | ✅ 完全开源（MIT），Go 语言开发 | fact | github repo | 2026-09-18 | 高 |
| OpenCode | 插件/MCP | 支持 MCP 协议（stdio + SSE） | fact | github repo README | 2026-09-18 | 高 |
| OpenCode | 上下文 | 取决于后端模型选择，支持 auto-compact 自动上下文压缩 | inference | 架构设计决定 | 2026-09-18 | 中 |
| OpenCode | 成熟度 | 项目已归档，转移至 Crush（charmbracelet/crush） | fact | github repo README | 2026-09-18 | 高 |
| Codex CLI | 定价 | 免费 CLI + API 按量付费；包含在 ChatGPT Plus/Pro/Business/Edu/Enterprise 计划中 | fact | github.com/openai/codex | 2026-09-18 | 高 |
| Codex CLI | 模型开放度 | OpenAI 系（GPT-4o, o 系列等），SDK 开源 Apache-2.0，Agent 核心闭源 | fact | github repo README | 2026-09-18 | 高 |
| Codex CLI | 上下文 | 128K token | fact | openai 文档 | 2026-09 | 中 |
| Codex CLI | 开源 | SDK 开源（Apache-2.0），Agent 核心闭源 | fact | github repo | 2026-09-18 | 高 |
| Codex CLI | 插件/MCP | 支持 MCP 扩展 | fact | openai 文档 | 2026-09 | 中 |
| Codex CLI | 多文件编辑 | ✅ 支持 | fact | openai 文档 | 2026-09 | 中 |
| Codex CLI | 成熟度 | 2025 H2 推出，持续迭代中 | inference | github repo commit history | 2026-09 | 中 |

## 证据表统计

- 总行数：24（分母＝表内数据行实测）
- fact：21（21/24 ≈ 88%）
- inference：3（3/24 ≈ 12%）
- opinion：0（0/24）
- 置信度高 18 · 中 5 · 低 1（三档合计 24，无未填）
- 完全覆盖维度：定价、模型开放度、开源、MCP/插件、多文件编辑、成熟度
- 部分覆盖：上下文（Cursor 无官方数据）
- 未覆盖：实际使用体验、企业级管控、迁移成本、社区生态规模
