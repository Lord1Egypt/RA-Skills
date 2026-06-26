# RoundTable Skill v3.0 — 通用多 Agent 圆桌讨论引擎

[![Version](https://img.shields.io/badge/version-3.0.13-blue.svg)](https://github.com/Krislu1221/Claw-roundtable-skill)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)

## Overview / 概览

RoundTable simulates a real roundtable meeting: multiple AI Agents assume distinct expert personas and produce high-feasibility proposals through 5 rounds of progressive, structured discussion. Its core design goal is **to break single-Agent perspective blind spots** — one mind inevitably circles within its own cognitive frame; cross-validating ideas under pressure from multiple expert viewpoints is far more reliable than solitary reasoning.

> **概览**：RoundTable 模拟真实圆桌会议：多个 AI Agent 扮演不同专家角色，通过 5 轮渐进式讨论产出高可行性方案。核心目标是**打破单一 Agent 视角盲区**——一个大脑容易在自己的框架内打转；多视角交叉验证远比单一视角更可靠。

## Design Philosophy / 设计哲学

### Why RoundTable / 为什么需要 RoundTable

Single Agents have inherent limitations:

- **Narrow perspective** — No matter how deep one thinks, it cannot escape its own cognitive frame. A backend engineer will always reason like a backend engineer.
- **No adversarial check** — Without challenge, proposals become echo-chamber self-validation. The agent confirms its own assumptions and calls it "analysis."
- **Pseudo-depth** — Looks like thorough reasoning, but it is the same angle repeated with different wording. Real depth requires friction between opposing viewpoints.

RoundTable's structured adversarial design breaks this cycle through 5 mandatory rounds:

```text
R1 Independent → R2 Cross-Reference → R3 Forced Critique → R4 Debate & Revise → R5 Arbitrate
```

After 5 rounds, the system surfaces **15+ risks, 9+ defects**, and produces a plan that has been thoroughly stress-tested against diverse expert scrutiny.

> **为什么需要 RoundTable**：单一 Agent 存在天然局限——视角单一（无法跳出自身认知框架）、缺乏对抗检验（没有挑战的方案容易沦为回声室自证）、伪深度（看似全面实则同一角度反复展开）。RoundTable 通过结构化对抗设计打破这一循环：R1 独立提出 → R2 交叉引用 → R3 强制质疑 → R4 辩论修订 → R5 仲裁总结。5 轮后系统可暴露 15+ 风险、9+ 缺陷，产出经过充分压力测试的方案。

### Core Design Principles / 核心设计原则

1. **Real sub-Agent isolation** — Every utterance in every round is an independent `sessions_spawn`. Models and thought-chains are fully isolated; no shared context leaks between experts.
2. **Forced critique depth** — No vague hand-waving allowed. The critique round (R3) must produce exactly **5 risks + 3 defects**, each backed by concrete reasoning.
3. **Dynamic proposal evolution** — R4 is not a repeat of R1. Experts must show an explicit "Original → Revised + Reason" comparison table, proving their thinking evolved under challenge.
4. **Explicit disagreement arbitration** — The R5 Host cannot dodge conflicts. Every disputed point must receive a ruling with rationale, even when experts fundamentally disagree.
5. **Directly executable output** — Not "recommendations." The final deliverable is an 8-week task table with named owners, deliverables, and risk contingencies.

> **核心设计原则**：
>
> 1. **真实子 Agent 隔离**：每轮每句都是独立 `sessions_spawn`，模型与思维链完全隔离，避免专家之间共享上下文造成观点污染。
> 2. **强制质疑深度**：不允许模糊敷衍；R3 质疑轮硬性要求输出 5 个风险 + 3 个缺陷，并给出具体依据。
> 3. **方案动态演进**：R4 不能重复 R1，必须展示「原方案 → 修订方案 + 修订理由」对比表，证明观点在质疑后发生了真实变化。
> 4. **明确分歧仲裁**：R5 主持人不能回避冲突，必须对争议点逐条裁决并说明理由。
> 5. **直接可执行输出**：最终交付不是泛泛建议，而是带负责人、交付物、时间安排和风险预案的执行计划。

---

## 5 轮讨论流程

```text
R1 独立提案  →  R2 交叉引用  →  R3 深度质疑  →  R4 辩论修订  →  R5 主持人总结
      ↓              ↓              ↓              ↓              ↓
  3 位专家       引用彼此观点      5 风险 + 3 缺陷   回应质疑并修订     仲裁分歧并输出计划
  800-1200 字    800-1200 字       明确证据         1000-1500 字      1500-2000 字
```

| 轮次 | 主题 | 核心任务 | 硬性要求 |
| --- | --- | --- | --- |
| **R1** | 独立提案 | 每位专家从自身视角给出方案 | 至少 1 个对比表 + 5 个量化指标 |
| **R2** | 交叉引用 | 引用其他专家观点并补足盲区 | 至少 3 个引用标记 + 明确赞同/反对立场 |
| **R3** | 深度质疑 | 找出真实风险和缺陷 | **5 个风险** + **3 个缺陷**，每项都要有依据 |
| **R4** | 辩论修订 | 回应质疑并修订方案 | 必须提供「原方案 / 修订方案 / 修订理由」对比表 |
| **R5** | 主持总结 | 仲裁分歧并形成最终计划 | **8 周任务表** + 风险预案 + Top 3 风险 |

### 上下文传递机制

v2.0 的核心缺陷是 R2-R5 对前序轮次缺乏充分感知，导致每轮都像重新开始。v3.0 强制注入完整讨论历史：

- **R2**：注入全部 R1 专家发言，用于引用和交叉补充。
- **R3**：注入 R1 + R2 历史，确保质疑针对真实内容。
- **R4**：注入 R1-R3 历史，确保回应真实争议。
- **R5 主持人**：注入 R1-R4 完整历史，否则无法完成有效仲裁。

---

## 架构

```text
┌─────────────────────────────────────────────────────────┐
│                    RoundTable Engine                    │
├─────────────────────────────────────────────────────────┤
│  意图解析器        │  模型路由器       │  收敛控制器       │
│  MMR Intent        │  异构模型路由     │  防循环机制       │
├────────────────────┼──────────────────┼──────────────────┤
│  专家选择器        │  提示词构建器     │  通知模块         │
│  170+ 专家库       │  结构化模板       │  飞书/Lark        │
└─────────────────────────────────────────────────────────┘
```

### 1. 意图解析器：基于 MMR 的专家选择

不是简单关键词匹配，而是使用 **Maximal Marginal Relevance（MMR，最大边际相关性）**：

```text
score = λ × 相关性 − (1−λ) × 与已选专家的最大相似度
```

- λ 控制相关性与多样性的平衡，默认 0.7，更偏向覆盖不同视角。
- 避免“回音室效应”：3 位专家不能全部来自同一领域。
- 170+ 专家库覆盖工程、设计、产品、安全、性能、增长、DevOps、数据等方向。

### 2. 模型路由器：异构模型分配

不同专家角色使用不同模型，充分利用各模型优势：

| 专家角色 | 能力需求 | 推荐模型标签 |
| --- | --- | --- |
| 工程 / 架构 | 代码、逻辑、技术判断 | `code`、`technical`、`engineering` |
| 设计 / 创意 | 长上下文、创意表达 | `creative`、`long-context`、`design` |
| QA / 测试 | 均衡、快速、严谨 | `balanced`、`fast`、`general` |
| 产品 / 商业 | 中文表达、领域知识、业务判断 | `chinese`、`knowledge`、`product` |
| 主持总结 | 逻辑、裁决、归纳 | `logic`、`summary`、`decision`、`max` |

**三层路由策略：**

1. **用户显式配置**（最高优先级）：读取自定义 `local_models.json`。
2. **OpenClaw 官方 API**（推荐）：自动发现可用模型。
3. **单模型降级**（兜底）：由一个模型扮演全部角色。

ClawHub 合规要求：不扫描 `os.environ`，不读取 `apiKey` / `baseUrl` 等敏感字段；模型信息只来自公开配置文件。

### 3. 收敛控制器：防止无限循环

```text
R1 → R2 → R3 → R4 → R5
                    ↑
          语义分歧低于阈值 → 提前停止
          达到最大轮次 → 强制仲裁
```

- **语义重复检测**：连续 2 轮内容重合度超过 80% 时自动停止。
- **共识检测**：R4 后确认 3 个以上共识点时，加速进入 R5。
- **硬性上限**：最多 5 轮，防止 Token 爆炸。

### 4. 专家选择器：170+ 专家库

领域覆盖：

- **技术**：后端、前端、全栈、架构、DevOps、安全、DBA、算法、数据工程。
- **产品**：产品经理、增长、数据分析、UX、客户成功。
- **商业**：市场策略、品牌、销售、公关、商业分析。
- **设计**：交互、视觉、服务设计、设计系统。
- **管理**：项目经理、技术负责人、敏捷教练。

选择策略：MMR 算法 + 领域权重 + 用户强制指定。

### 5. 提示词构建器：结构化模板

每一轮都有独立的提示词框架（`prompts/framework.md`），不是自由发挥：

- **硬约束**：最低字数、表格要求、引用数量。
- **角色化内容**：不同专家角色使用对应行业模板。
- **历史注入**：将前序轮次内容加入当前轮提示词。

---

## 执行引擎

### 核心流程

```python
engine = RoundTableEngine(
    topic="智能客服技术方案",
    agents=["工程专家", "产品专家", "架构专家"],
    mode="pre-ac"  # pre-ac: 本地预分析；full: 完整模式
)
success = await engine.run()
```

### 容错机制

| 场景 | 处理策略 |
| --- | --- |
| 子 Agent 超时 | 最多重试 2 次，间隔 5 秒 |
| `sessions_spawn` 不可用 | 直接失败，不使用假数据兜底 |
| R5 主持人失败 | 从已有轮次中自动抽取总结 |
| 模型不可用 | 自动降级到 `FALLBACK_MODEL` |

### 输出内容

1. **JSON 报告**：`data/roundtable/{topic}.json`，结构化数据，便于机器读取。
2. **Markdown 报告**：人类可读版本，包含完整 5 轮讨论。
3. **飞书 / Lark 通知**（可选）：按轮次推送实时进度。
4. **聊天室模式**（可选）：将讨论广播到指定会话。

---

## v3.0 相比 v2.0 的改进

| 维度 | v2.0 | v3.0 |
| --- | --- | --- |
| **上下文传递** | R2-R5 缺少前序上下文 ❌ | **强制注入完整历史** ✅ |
| **质疑深度** | 泛泛而谈，约 3 个风险 | **硬性要求 5 个风险 + 3 个缺陷** |
| **方案演进** | R1-R4 内容容易重复 | **R4 必须给出修订对比表** |
| **分歧处理** | 没有明确仲裁 | **R5 主持人逐条裁决** |
| **输出质量** | 400-600 字，缺少表格 | **800-2000 字 + 强制表格** |
| **可执行性** | 约 50% | **90%+** |

### 基准测试数据（2026-03-19）

```text
主题：智能客服技术方案
参与专家：工程 / 产品 / 设计（3 位）
子 Agent 调用：15 次
识别风险：15 个
发现缺陷：9 个
修改建议：13 条
8 周计划：W1-W8，含每日工作量估算
分歧裁决：4 项，均有理由
总输出：约 8,500 字
```

---

## 适用场景

| ✅ 推荐使用 | ❌ 不推荐使用 |
| --- | --- |
| 技术方案评审：架构、技术选型、复杂实现路线 | 简单问答：直接问主 Agent 即可 |
| 产品立项：功能规划、MVP 边界、路线图 | 紧急决策：完整讨论通常需要 15-20 分钟 |
| 复杂决策：多因素权衡、跨角色冲突 | 代码生成：请使用 Auto-Coding 类技能 |
| 跨团队对齐：需要多视角共同校验 | 快速事实查询 |

---

## 使用策略

### 本地开发

使用 `local_models.json` 定义自定义模型阵容：

```json
{
  "engineering": "deepseek/deepseek-v4-flash",
  "design": "minimax/minimax-latest",
  "host": "deepseek/deepseek-v4-pro"
}
```

### ClawHub 公开模式

使用 `roundtable_config.yaml` 声明模型能力标签。只读取模型元数据，不访问 API Key、Base URL 或其它敏感配置。

---

## 文件路径

- `core/model_router.py`
- `core/intent_parser.py`
- `core/prompt_builder.py`
- `core/convergence.py`
- `prompts/framework.md`

---

## 🔒 数据处理透明度

本技能运行期间会处理以下数据：

| 行为 | 说明 | 用户控制 |
| --- | --- | --- |
| **模型配置读取** | 读取模型 ID、标签、优先级，用于异构路由 | ✅ 可通过参数覆盖 |
| **讨论历史注入** | R2-R5 注入前序轮次摘要，默认每轮截断到约 200 字符 | ✅ 截断限制暴露范围；用户控制讨论主题 |
| **报告持久化** | 保存 JSON 与 Markdown 讨论报告 | ✅ 可配置输出目录 |
| **聊天室广播** | 可选：将截断后的 Agent 输出（≤1000 字符）广播到独立会话 | ✅ 默认关闭（`enable_chat_room=False`） |

> ⚠️ **隐私提醒**：如果讨论包含敏感信息，报告文件、聊天室会话和轮次通知可能暴露主题名称、专家角色和部分讨论内容。处理保密议题时，请关闭聊天室和通知渠道。

**版本**：3.0.13  
**更新日期**：2026-05-26
