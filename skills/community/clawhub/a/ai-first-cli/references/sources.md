# 调研来源

## Vercel 一手 / 案例
- Rauch 推文（背景源）: https://x.com/rauchg/status/2060443982342357032
- Docker in Vercel Sandbox changelog: https://vercel.com/changelog/run-docker-containers-inside-vercel-sandbox
- Zero-config backends on Vercel AI Cloud: https://vercel.com/blog/zero-config-backends-on-vercel-ai-cloud
- Vercel CLI docs: https://vercel.com/docs/cli
- Vercel Sandbox concepts: https://vercel.com/docs/vercel-sandbox/concepts
- Zero 语言仓库: https://github.com/vercel-labs/zero
- Zero 报道 (MarkTechPost): https://www.marktechpost.com/2026/05/17/vercel-labs-introduces-zero-a-systems-programming-language-designed-so-ai-agents-can-read-repair-and-ship-native-programs/
- Zero 解读 (Firethering): https://firethering.com/vercel-zero-programming-language-ai-agents/

## 深度调研补充一手源（3-0 对抗式验证确认）
- Native binaries for Vercel CLI: https://vercel.com/changelog/experimental-native-binaries-for-vercel-cli
- Vercel CLI for marketplace integrations, optimized for agents: https://vercel.com/changelog/vercel-cli-for-marketplace-integrations-optimized-for-agents
- Vercel Agent docs: https://vercel.com/docs/agent
- Agentic infrastructure (blog): https://vercel.com/blog/agentic-infrastructure
- Security boundaries in agentic architectures: https://vercel.com/blog/security-boundaries-in-agentic-architectures
- Vercel Sandbox GA: https://vercel.com/blog/vercel-sandbox-is-now-generally-available
- The AI Cloud — unified platform: https://vercel.com/blog/the-ai-cloud-a-unified-platform-for-ai-workloads
- Introducing Vercel MCP: https://vercel.com/blog/introducing-vercel-mcp-connect-vercel-to-your-ai-tools
- AI SDK 6: https://vercel.com/blog/ai-sdk-6
- mcp-to-ai-sdk: https://vercel.com/blog/generate-static-ai-sdk-tools-from-mcp-servers-with-mcp-to-ai-sdk
- Vercel MCP docs: https://vercel.com/docs/agent-resources/vercel-mcp
- AI SDK MCP tools: https://ai-sdk.dev/docs/ai-sdk-core/mcp-tools
- vercel-labs/vercel-openclaw: https://github.com/vercel-labs/vercel-openclaw
- Claude Agent SDK on Vercel Sandbox: https://vercel.com/kb/guide/using-vercel-sandbox-claude-agent-sdk
- AI Gateway coding agents: https://vercel.com/docs/ai-gateway/coding-agents

## 调研可信度与偏差（必读）
- **样本偏差**：6 角度 / 26 源 / 109 声明 / 25 条经 3-vote 对抗验证 → 24 confirmed, 1 killed。但确认的源**几乎全是 Vercel 一方**，只能证"宣称且内部一致"，不能证"生产实效"。
- **被驳回（勿采信）**：「Sandbox 单 API 调用克隆/启动数百万 agent」— 1-2 未过，营销夸张。
- **证据偏弱**：OpenClaw/Claude Code "大规模嵌入 Vercel agentic 基础设施" — 仓库与集成路径为实，规模叙事缺独立佐证，按"方向成立、规模待证"处理。
- 第三方批评源（truefoundry / qovery / northflank）质量为 blog 级，未作为事实依据。

## AI-first CLI 设计原则（横向）
- You Need to Rewrite Your CLI for AI Agents (Justin Poehnelt): https://justin.poehnelt.com/posts/rewrite-your-cli-for-ai-agents/
- Why CLI is the New MCP for AI Agents (OneUptime): https://oneuptime.com/blog/post/2026-02-03-cli-is-the-new-mcp/view
- better-cli — SKILL.md for AI-friendly CLIs (yogin16): https://github.com/yogin16/better-cli
- Writing CLI Tools That AI Agents Actually Want to Use (dev.to): https://dev.to/uenyioha/writing-cli-tools-that-ai-agents-actually-want-to-use-39no
- Designing CLI Tools for AI Agents — Lessons from Memori: https://archit15singh.github.io/posts/2026-02-28-designing-cli-tools-for-ai-agents/
- MCP vs CLI vs CLI+Skills (Medium): https://medium.com/@akshaychame2/mcp-vs-cli-vs-cli-skills-trade-offs-use-cases-and-best-practices-49b9cfd7a556

## 原则映射（哪条来自哪里）
- 双形态输出 / stdout-stderr 分流 / 可执行错误 / 非交互默认 → better-cli 五大基石
- 原始 payload / schema introspection / 输入加固 / dry-run / 响应净化 / env 认证 / 多面暴露 → Poehnelt "Rewrite your CLI"
- 可组合 / 现成工具 / 自描述 / 零集成负担 / 权限复用 → "CLI is the new MCP"
- 稳定错误码 / typed repair / 版本对齐指引 / 零依赖二进制 → Vercel Zero + Vercel CLI native binary
- 幂等键 → API idempotency 通用实践 (Stripe/Shopify/AWS)
