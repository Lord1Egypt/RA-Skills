---
name: agent-architecture-audit
description: "Audit agent system architecture across 12 layers for wrapper regression, memory pollution, tool discipline failures, and hidden fix loops. Use when diagnosing agent structural issues, detecting regressions, or producing severity-ranked discovery reports."
metadata:
  origin: ECC agent-architecture-audit
---

# Agent Architecture Audit �?12 层架构审�?
诊断 Agent 系统中隐藏故障的审计工作流�?
## 触发条件

**必须使用**�?- Agent 行为退化（"Agent 变差�?�?工具不稳�?�?- 模型�?playground 正常，但�?wrapper 中失�?- 添加�?prompt �?工具定义/记忆系统后，现有行为退�?- 调试 Agent 行为超过 15 分钟未找到根�?- 发布 Agent 应用�?
**不适用**�?- 通用代码调试 �?�?`agent-introspection-debugging`
- 代码审查 �?�?`code-review`
- 安全扫描 �?�?`security-and-hardening`
- 性能基准测试 �?�?`performance-optimization`

## 12 层架构栈

每个 Agent 系统都有这些层。任何一层都可能损坏答案�?
| # | �?| 可能的问�?|
|---|-----|-----------|
| 1 | **System prompt** | 指令冲突、指令膨胀 |
| 2 | **Session history** | 旧上下文注入到新轮次 |
| 3 | **Long-term memory** | 跨会话污染、旧话题出现在新对话 |
| 4 | **Distillation** | 压缩产物作为伪事实重新进�?|
| 5 | **Active recall** | 冗余重摘要层浪费上下�?|
| 6 | **Tool selection** | 错误工具路由、模型跳过必需工具 |
| 7 | **Tool execution** | 幻觉执行——声称调用但未实际执�?|
| 8 | **Tool interpretation** | 误读或忽略工具输�?|
| 9 | **Answer shaping** | 最终响应格式损�?|
| 10 | **Platform rendering** | 传输层变异（UI/API/CLI 变异有效答案�?|
| 11 | **Hidden repair loops** | 静默 fallback/retry agent 运行第二�?LLM 调用 |
| 12 | **Persistence** | 过期状态或缓存产物作为实时证据重用 |

## 5 种常见失败模�?
### 1. Wrapper 回归

基础模型产生正确答案，但 wrapper 层使其变差�?
**症状**�?- 模型�?playground 或直�?API 调用中正常，�?Agent 中失�?- 添加�?prompt 层后，现有行为退�?- Agent 听起来自信但自信地错�?- "之前还能用，更新后就不行�?

### 2. 记忆污染

旧话题通过 history、memory retrieval �?distillation 泄漏到新对话�?
**症状**�?- Agent 提起不相关的过去话题
- 用户纠正不持久（旧记忆覆盖新的）
- 同会话产物作为伪事实重新进入
- 记忆无限增长，降低响应质�?
### 3. 工具纪律失败

工具�?prompt 中声明但未在代码中强制执行。模型跳过或幻觉执行�?
**症状**�?- Prompt �?必须用工�?X"，但模型不调用就回答
- 工具结果看起来正确但从未实际执行
- 不同工具争夺同一职责
- 模型不该用工具时用了，该用时跳过�?
### 4. 渲染/传输损坏

Agent 内部答案正确，但平台层在传递时变异�?
**症状**�?- 日志显示正确答案，用户看到损坏输�?- Markdown 渲染、JSON 解析或流式传输片段损坏有效响�?- 隐藏 fallback agent 在传递前静默替换答案
- 终端�?UI 输出不同

### 5. 隐藏 Agent �?
静默修复、重试、摘要或召回 agent 在没有明确契约的情况下运行�?
**症状**�?- 输出在内部生成和用户传递之间变�?- "自动修复"循环运行用户不知道的第二�?LLM 调用
- 多个 agent 在没有协调的情况下修改同一输出
- 答案被不可见�?平滑"�?纠正"

## 审计工作�?
### Phase 1: Scope（范围）

定义审计目标�?
- **目标系统** �?哪个 Agent 应用�?- **入口�?* �?用户如何交互�?- **模型�?* �?哪些 LLM 和提供商�?- **症状** �?用户报告什么？
- **时间窗口** �?何时开始？
- **要审计的�?* �?12 层中哪些适用�?
### Phase 2: Evidence Collection（证据收集）

从代码库收集证据�?
- **源代�?* �?Agent 循环、工具路由、记忆准入、prompt 组装
- **日志** �?历史会话追踪、工具调用记�?- **配置** �?prompt 模板、工�?schema、提供商设置
- **记忆文件** �?SOP、知识库、会话归�?
搜索反模式：

```bash
# 工具要求仅在 prompt 文本中表达（未在代码中强制）
rg "must.*tool|必须.*工具|required.*call" --type md

# 工具执行无验�?rg "tool_call|toolCall|tool_use" --type py --type ts

# �?Agent 循环外的隐藏 LLM 调用
rg "completion|chat\.create|messages\.create|llm\.invoke"

# 记忆准入无用户纠正优�?rg "memory.*admit|long.*term.*update|persist.*memory" --type py --type ts

# 运行额外 LLM 调用�?fallback 循环
rg "fallback|retry.*llm|repair.*prompt|re-?prompt" --type py --type ts

# 静默输出变异
rg "mutate|rewrite.*response|transform.*output|shap" --type py --type ts
```

### Phase 3: Failure Mapping（失败映射）

对每个发现，记录�?
- **症状** �?用户看到什�?- **机制** �?wrapper 如何导致
- **源层** �?12 层中的哪一�?- **根因** �?最深层原因
- **证据** �?file:line �?log:row 引用
- **置信�?* �?0.0 �?1.0

### Phase 4: Fix Strategy（修复策略）

默认修复顺序（代码优先，�?prompt 优先）：

1. **代码门控工具要求** �?在代码中强制，不仅在 prompt 文本
2. **移除或收窄隐藏修�?agent** �?�?fallback 明确带契�?3. **减少上下文重�?* �?同一信息通过 prompt + history + memory + distillation
4. **收紧记忆准入** �?用户纠正 > Agent 断言
5. **收紧 distillation 触发** �?不压缩不应压缩的内容
6. **减少渲染变异** �?直通，不转�?7. **转换为类型化 JSON 信封** �?结构化内部流，非自由文本

## 严重度模�?
| 级别 | 含义 | 行动 |
|------|------|------|
| `critical` | Agent 可以自信地产生错误的操作行为 | 下次发布前修�?|
| `high` | Agent 经常降低正确性或稳定�?| �?sprint 修复 |
| `medium` | 正确性通常存活但输出脆弱或浪费 | 计划下一周期 |
| `low` | 主要是外观或可维护性问�?| Backlog |

## 输出格式

按此顺序呈现发现�?
1. **严重度排序的发现**（最严重优先�?2. **架构诊断**（哪层损坏了什么，为什么）
3. **排序修复计划**（代码优先，�?prompt 优先�?
不要以赞美或摘要开头。如果系统坏了，直接说�?
## 7 个快速诊断问�?
| # | 问题 | 如果�?�?|
|---|------|----------|
| 1 | 模型能跳过必需工具仍然回答吗？ | 工具未代码门�?|
| 2 | 旧对话内容出现在新轮次吗�?| 记忆污染 |
| 3 | 同一信息�?system prompt AND memory AND history 中？ | 上下文重�?|
| 4 | 平台在传递前运行第二�?LLM 调用吗？ | 隐藏修复循环 |
| 5 | 输出在内部生成和用户传递之间不同吗�?| 渲染损坏 |
| 6 | "必须用工�?X" 规则仅在 prompt 文本中？ | 工具纪律失败 |
| 7 | Agent 自己的独白能成为持久记忆吗？ | 记忆中毒 |

## 报告 Schema

审计应产出结构化报告�?
```json
{
  "schema_version": "agent-architecture-audit.report.v1",
  "executive_verdict": {
    "overall_health": "high_risk | moderate | healthy",
    "primary_failure_mode": "string",
    "most_urgent_fix": "string"
  },
  "scope": {
    "target_name": "string",
    "model_stack": ["string"],
    "layers_to_audit": ["string"]
  },
  "findings": [
    {
      "severity": "critical | high | medium | low",
      "title": "string",
      "mechanism": "string",
      "source_layer": "string (1-12)",
      "root_cause": "string",
      "evidence_refs": ["file:line"],
      "confidence": 0.0,
      "recommended_fix": "string"
    }
  ],
  "ordered_fix_plan": [
    {
      "order": 1,
      "goal": "string",
      "why_now": "string",
      "expected_effect": "string"
    }
  ]
}
```

## 与现有技能的关系

| 技�?| 用�?| 关系 |
|------|------|------|
| `agent-introspection-debugging` | 运行时调试（工具循环、上下文漂移�?| 互补：本技能管架构级审�?|
| `error-classifier` | 错误分类 + 重试策略 | 互补：本技能管架构视角 |
| `code-review` | 代码级审�?| 本技能更高层（架构级�?|

## 反模�?
- 在证�?wrapper 层回归前，不要责怪模�?- 不要在没有显示污染路径的情况下责怪记�?- 不要让干净的当前状态抹去脏的历史事�?- 不要�?Markdown 文本视为可信的内部协�?- 不要接受"必须用工�?仅在 prompt 文本中而代码从未强�?- 保持发现直接、证据支持、严重度排序

---

*12 层架构审计：系统化诊�?Agent 系统的隐藏故障�?
