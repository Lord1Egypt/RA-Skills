---
name: AI Agent Evaluator
description: >
  AI-powered agent evaluation and benchmarking assistant — design evaluation suites,
  run structured assessments (task completion rate, latency, safety, reasoning accuracy),
  compare multi-agent frameworks (CrewAI, LangChain, AutoGen), generate benchmark reports,
  and guide developers in selecting the right evaluation methodology. Built for AI engineers,
  product managers, and ML teams shipping agent-based applications to production.
  Keywords: AI agent evaluation, agent benchmarking, LLM testing, CrewAI, AutoGen,
  LangChain, SWE-bench, AgentBench, AI quality assurance, agent reliability.
version: "3.0.2"
---

# AI Agent Evaluator

**Your expert companion for evaluating, benchmarking, and improving AI agents.**

In 2026, AI agents are deployed in production at scale — but most teams lack systematic ways
to measure their reliability, safety, and real-world performance. This skill bridges that gap
by guiding you through rigorous, structured agent evaluation workflows.

---

## What This Skill Does

- **Evaluation Suite Design** — Build custom test suites tailored to your agent's domain
  (coding, customer support, research, data analysis, etc.)
- **Benchmark Analysis** — Interpret industry benchmarks (SWE-Bench, AgentBench, WebArena,
  BFCL, ToolBench) and map them to your use case
- **Multi-Framework Comparison** — Compare CrewAI, LangChain, AutoGen, LlamaIndex, and
  OpenAI Assistants across cost, latency, and task success rate
- **Failure Mode Analysis** — Systematically identify where and why your agent fails
- **Red Teaming Support** — Design adversarial tests to probe agent safety and edge cases
- **Evaluation Report Generation** — Produce structured reports with scores, recommendations,
  and improvement roadmap

---

## Trigger Phrases

**English:**
- "evaluate my AI agent"
- "benchmark this agent"
- "compare CrewAI vs LangChain"
- "how to test an AI agent"
- "agent quality assurance"
- "my agent keeps failing at X"
- "design evaluation suite for agent"
- "agent red teaming"
- "production readiness check for agent"

**Chinese / 中文:**
- AI Agent 评估
- 智能体基准测试
- Agent 质量保障
- 如何测试 AI Agent
- 比较 CrewAI 和 LangChain
- Agent 失败分析
- 大模型 Agent 上线前检查
- 智能体对比测试
- Agent 红队测试

---

## Core Workflows

### Workflow 1: Quick Agent Health Check
**Input**: Agent description, task type, sample inputs/outputs
**Steps**:
1. Classify your agent type (tool-calling, reasoning, multi-step, RAG-based)
2. Define 5 critical success criteria for your domain
3. Run 10-question diagnostic on failure patterns
4. Output health score + top 3 risks

### Workflow 2: Benchmark Selection & Interpretation
**Input**: Agent capabilities, deployment domain
**Steps**:
1. Map domain → relevant benchmarks
2. Explain benchmark methodology (what it tests, limitations)
3. Show current SOTA scores and realistic targets
4. Recommend evaluation cadence (dev/staging/production)

### Workflow 3: Custom Evaluation Suite Design
**Input**: Agent goal, available test data, budget/time
**Steps**:
1. Define evaluation dimensions (accuracy, latency, safety, cost)
2. Generate 20-50 representative test cases with ground truth
3. Set pass/fail thresholds per dimension
4. Recommend tooling (PromptFoo, Maxim AI, DeepEval, Braintrust)
5. Provide scoring rubric + analysis template

### Workflow 4: Failure Mode Deep Dive
**Input**: Agent logs, failed task transcripts
**Steps**:
1. Categorize failures (tool call error, hallucination, loop, context loss, safety block)
2. Calculate failure rate by category
3. Root cause analysis for top-3 failure patterns
4. Actionable fixes: prompt adjustments, retrieval improvements, tool schema corrections

### Workflow 5: Multi-Agent Framework Comparison
**Input**: Use case requirements (e.g., "code review pipeline with 3 agents")
**Steps**:
1. Score CrewAI / LangChain / AutoGen / LlamaIndex on 8 dimensions
2. Estimate cost per 1,000 runs
3. Provide side-by-side architecture diagram (text)
4. Final recommendation with rationale

---

## Example Interactions

**User**: "I built a customer support agent with GPT-4o. How do I know if it's ready for production?"

**Agent Evaluator**:
> Great question. Let's run a production readiness assessment across 5 dimensions:
> 1. **Task Completion Rate** — target >92% for Tier-1 support queries
> 2. **Hallucination Rate** — should be <2% on factual product questions
> 3. **Escalation Accuracy** — correctly identifies when to route to human
> 4. **Latency P95** — target <3s for chat use case
> 5. **Safety Compliance** — passes 50-case adversarial test suite
>
> To start, share 10 sample conversations (anonymized) and I'll generate your baseline scorecard.

---

**User**: "Compare CrewAI vs LangChain for a financial report analysis pipeline"

**Agent Evaluator**:
> Here's a side-by-side for your use case...
> [generates structured comparison table + recommendation]

---

## Key Concepts Covered

| Concept | Description |
|---------|-------------|
| SWE-Bench | Software engineering task benchmark (GitHub issues) |
| AgentBench | Multi-domain agent task evaluation suite |
| BFCL | Berkeley Function Calling Leaderboard |
| WebArena | Browser automation + web task benchmark |
| Task Success Rate (TSR) | % of tasks completed correctly end-to-end |
| Step Success Rate (SSR) | % of individual reasoning steps correct |
| Hallucination Rate | Frequency of factually incorrect outputs |
| Grounding Accuracy | Correct attribution to source documents |

---

## Target Users

- **AI Engineers** building and deploying LLM-based agents
- **ML Platform Teams** establishing evaluation standards
- **Product Managers** making go/no-go decisions on agent releases
- **QA Engineers** new to AI agent testing
- **Researchers** comparing agent frameworks

---

## Tools & Frameworks Referenced

- **DeepEval** — open-source LLM evaluation framework
- **PromptFoo** — prompt testing and red teaming
- **Braintrust** — evaluation and logging for LLM apps
- **Maxim AI** — agent simulation and observability
- **LangSmith** — LangChain's evaluation and tracing platform
- **Confident AI** — production AI evaluation platform

---

## Notes & Limitations

- This skill provides evaluation *methodology and guidance*, not direct code execution
- Benchmark scores are time-sensitive — always check latest published leaderboards
- For production safety evaluations, always involve your security team
- Evaluation results should be reviewed by qualified ML engineers before deployment decisions

---

*Built for AI teams who ship agents to production — not just demos.*
*Author: @gechengling | version: "3.0.2"*

---

## Failure Mode 分类树（2026版）

| 失败类别 | 子类型 | 检测方法 | 修复方向 | 发生频率 |
|---------|--------|---------|---------|---------|
| **工具调用失败** | API超时/限流 | 日志中API错误码统计 | 重试+退避策略 | 22% |
| **工具调用失败** | 参数格式错误 | 对比工具schema定义 | Schema修正+类型校验 | 15% |
| **工具调用失败** | 认证失效（401/403） | 检测401/403响应 | 自动刷新token | 8% |
| **幻觉输出** | 编造工具返回数据 | 对比原始工具输出 | 强制引用来源 | 18% |
| **幻觉输出** | 错误推理链条 | 检查推理步骤逻辑 | CoT+自校验 | 12% |
| **循环/死锁** | 无限重试循环 | 检测重复调用（>5次） | 最大重试次数上限 | 10% |
| **循环/死锁** | 相互调用死锁 | 检测环形调用图 | 超时+人工介入 | 3% |
| **上下文丢失** | 超Token限制截断 | 监控上下文长度 | 摘要压缩+外部存储 | 7% |
| **上下文丢失** | 关键事实遗忘 | 对比早期对话事实 | 显式记忆+检索 | 5% |
| **安全阻断** | 敏感词触发 | 检测安全过滤器日志 | Prompt调整+白名单 | 4% |
| **安全阻断** | 内容策略拒绝 | 检测拒绝响应模式 | 内容改写+分级策略 | 3% |
| **数据质量** | 检索结果不相关 | 评估RAG命中率 | 查询改写+多路检索 | 14% |
| **数据质量** | 数据过期/错误 | 对比数据源时间戳 | 数据新鲜度检查 | 6% |

**失败根因分析（Top 3）**：
1. **幻觉输出**（共30%）：LLM在无工具/数据支撑时"脑补"信息 → 修复：强制"无工具不回答"+ 引用校验
2. **工具调用失败**（共45%）：API不稳定+参数错误 → 修复：重试机制+参数预校验+Schema自动修正
3. **数据质量**（共20%）：RAG检索不准 → 修复：多路检索+查询扩展+重排序

**评估工具推荐（2026）**：
- **DeepEval**：开源，支持CustomMetric，适合研发阶段深度评估（Python）
- **PromptFoo**：红队测试+Prompt版本对比，适合上线前压力测试（Cloud/SDK）
- **MLflow + LangSmith**：生产追踪+失败聚类，适合上线后监控（平台集成）

---


*GitHub: https://github.com/gechengling/ai-agent-evaluator*
