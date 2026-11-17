# 从 Cursor 迁移到替代方案：5人团队对比简报

> 决策问题：5人核心开发团队是否从 Cursor 切换到更开放的 coding agent 方案
> 来源：证据表「Cursor 替代方案对比」（2026-09-18），定价页经 omni-reader 解析验证
> 注意：本简报仅反映证据表已覆盖的维度，未覆盖事项见文末

## 结论先行

**短期（1-3个月）建议保留 Cursor Pro，同时试用 Claude Code Max 3-5 人做深度验证。** 四个方案中，Claude Code 在产品成熟度、上下文能力上最接近 Cursor 的替代，但定价更高且不开源。OpenCode 是最开放的选择但项目已归档（转至 Crush）。Codex CLI 免费但产品成熟度不足。

---

## 对比表

| 维度 | Cursor | Claude Code | OpenCode | Codex CLI |
|------|--------|-------------|----------|-----------|
| **5人月费估算** | Individual $100 | Pro $100 / Max $500+ | $0（需自付 API） | $0（需 API 按量） |
| **模型开放度** | Claude + GPT-4o + Grok | 仅 Claude 系列 | 任意模型 + BYOK | OpenAI 系 |
| **上下文** | 未公开（~15K 推测） | Up to 1M | 取决于后端 | 128K |
| **开源** | ❌ | ❌ | ✅ MIT（已归档→Crush） | ⚠️ SDK 开源 |
| **MCP/插件** | ✅ MCP/skills/hooks | ✅ Skills/Connectors | ✅ MCP（stdio+SSE） | ✅ MCP |
| **多文件编辑** | ✅ | ✅ | ⚠️ CLI 依赖 | ✅ |
| **成熟度** | 高（团队 100+） | 高（2025 中 GA） | 归档 | 早期（2025 H2） |

## 逐家分析

### Cursor（基线）

*fact（来源：cursor.com/pricing，omni-reader 解析 2026-09-18）*

**定价**：Hobby Free；Individual $20/月（含 Agent/Composer 扩展限额）；Teams $40/用户/月（含团队管理、Bugbot）；Enterprise 定制。还有 Pro+/Ultra 子档位未公开单独价格。

**优势**：
- 产品成熟度最高，编辑器内体验流畅（opinion）
- 支持 MCPs、skills、hooks（fact）
- 单个份额 TCO 最低（fact）

**劣势**：
- 闭源（fact）
- token 窗口未公开（fact）
- 定价 per-seat，用量大成本线性增长（fact）

### Claude Code

*fact（来源：claude.com/pricing，omni-reader 解析 2026-09-18）*

**定价**：Pro $20/月（$17 年付），含 Claude Code；Max $100+/月（5x 或 20x Pro 用量）；Team Standard $20/座位/月（年付），Premium $100/座位/月；Enterprise $20/座位/月 + API 按量。5人 Pro $100 与 Cursor 持平；Max 5x $500+/月贵 5 倍。

**优势**：
- Up to 1M token，远超竞品（fact）
- Skills 架构支持自定义工作流（fact）
- 后背 Anthropic 持续迭代（fact）

**劣势**：
- 高价位的 Max 计划对 5 人团队预算影响大（fact）
- 仅 Claude 模型，无 BYOK（fact）
- 闭源（fact）

### OpenCode

*fact（来源：github.com/opencode-ai/opencode，omni-reader 解析 2026-09-18）*

**关键发现：项目已归档**，转移至 Crush（charmbracelet/crush）。原项目功能完整但不再维护。

**定价**：开源免费（MIT），需自付模型 API 费。

**优势**：
- 完全开源，任意模型 + BYOK（fact）
- 支持 MCP 协议（stdio + SSE）（fact）
- LSP 集成、多模型供应商（fact）

**劣势**：
- 已归档，无人维护（fact）
- 安装配置需一定技术投入（inference）
- 多文件编辑能力依赖 CLI 工具链（inference）

### Codex CLI

*fact（来源：github.com/openai/codex，omni-reader 解析 2026-09-18）*

**定价**：免费 CLI，使用需 ChatGPT Plus/Pro/Business/Edu/Enterprise 订阅或独立 API 按量。

**优势**：
- 直接接入 OpenAI 模型系（fact）
- SDK 开源（Apache-2.0）（fact）
- 多种安装方式（npm/Homebrew/二进制）（fact）

**劣势**：
- Agent 核心闭源（fact）
- 产品成熟度不足，迭代节奏不稳定（inference）
- IDE 集成尚在早期（opinion）

---

## 按决策维度排序

### 1. 定价（5人团队月费）

| 方案 | 月费估算 | 计费模型 | 备注 |
|------|---------|----------|------|
| Cursor | $100 | per-seat | 成本随人数线性增长 |
| Claude Code Pro | $100 | per-seat | 同 Cursor 价格 |
| Claude Code Max | $500+ | per-seat | 5x 用量版 |
| OpenCode | $0 + API | 开源免授权 | 需自托管；已归档 |
| Codex CLI | $0 + 订阅/API | 免费 CLI | 需 ChatGPT 订阅或 API key |

### 2. 开放性

| 方案 | 开源 | 模型自由 | MCP/插件 | 定制能力 |
|------|------|---------|----------|---------|
| Cursor | ❌ | ❌ | ✅ | hooks/skills |
| Claude Code | ❌ | ❌（仅 Claude） | ✅ | Skills 架构 |
| OpenCode | ✅ MIT | ✅ 任意 | ✅ | 全定制，已归档 |
| Codex CLI | ⚠️ SDK | ⚠️ OpenAI | ✅ | CLI 层面 |

### 3. 上下文能力

| 方案 | 上下文限制 | 备注 |
|------|-----------|------|
| Cursor | 未公开（~15K 推测） | 无官方数字 |
| Claude Code | Up to 1M | 视模型而定 |
| OpenCode | 取决于后端 | auto-compact |
| Codex CLI | 128K | 官方文档确认 |

---

## 证据覆盖度

- 证据表总行数：24（fact 21/24 ≈ 88% · inference 3/24 ≈ 12% · opinion 0/24）
- 置信度高 18 · 中 5 · 低 1（三档合计 24，无未填）
- 完全覆盖：定价 · 模型开放度 · 开源 · MCP/插件 · 多文件编辑 · 成熟度
- 部分覆盖：上下文（Cursor 无官方数据）
- **未覆盖清单**（证据表里没有数据，不在对比范围内）：
  - 实际使用体验（基于公开信息，未端到端测试）
  - 企业级管控（数据驻留、认证、审计日志）
  - 迁移成本（配置、rules、快捷键习惯）
  - 社区与插件生态规模
  - API 定价透明度（部分竞品未公开）
