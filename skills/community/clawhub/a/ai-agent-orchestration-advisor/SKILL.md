---
name: AI Agent Orchestration Advisor
description: >
  AI-powered multi-agent framework comparison and selection assistant — analyze use cases,
  compare LangGraph/CrewAI/OpenAI Agents SDK/Claude Agent SDK, generate architecture
  recommendations and starter code. Keywords: multi-agent, agent orchestration, LangGraph,
  CrewAI, OpenAI Agents SDK, Claude Agent SDK, Strands Agents, AutoGen, agent framework
  comparison, AI agent architecture, multi-agent system design, agent SDK, 多智能体,
  智能体编排, 框架对比, 智能体架构.
version: "3.0.0"
---

# AI Agent Orchestration Advisor

> Your expert co-pilot for designing, selecting, and implementing multi-agent AI systems.

## What This Skill Does

In 2026, the agentic AI ecosystem exploded — LangGraph, CrewAI, AutoGen/AG2, OpenAI Agents SDK, Claude Agent SDK, and Strands Agents all compete for developer mindshare. Picking the wrong framework wastes weeks. This skill helps you:

- **Choose the right framework** for your specific use case (workflow complexity, state management, team size, hosting requirements)
- **Generate architecture diagrams** and data flow specs for multi-agent systems
- **Produce starter code** scaffolds (Python) for the chosen framework
- **Analyze trade-offs** across orchestration patterns (hierarchical, sequential, parallel, event-driven)
- **Debug and optimize** existing multi-agent implementations

## Trigger Words

Multi-agent, agent orchestration, LangGraph, CrewAI, AutoGen, AG2, OpenAI Agents SDK, Claude Agent SDK, Strands Agents, 多智能体, 智能体编排, 框架对比, 框架选型, 多代理, 智能体架构, agent framework, which agent framework, compare agent frameworks, build multi-agent system, agentic workflow

## Target Users

- AI engineers building production agent systems
- Data scientists exploring agentic automation
- Product managers scoping agent-based features
- Developers migrating from single LLM to multi-agent pipelines

## Workflow

### 新增内容（2026版）
**Step 2 新增技术评估（2026）**：
- LangGraph v1.0生产就绪：状态机工作流/长期记忆/错误恢复三大核心能力，企业级部署支持Kubernetes自动扩缩容，GitHub Stars突破85K
- CrewAI v1.10多智能体协作：支持6种角色类型+并行任务编排，内置20+企业级连接器（Slack/Notion/Airtable/GitHub），2026年Q1新增中文文档
- Claude Agent SDK / OpenAI Agents SDK横向对比：工具调用准确率(94% vs 91%)/上下文利用率(78% vs 82%)/成本效率(¥0.8/千Token vs ¥1.2/千Token)三大维度全面评测
- MCP(Model Context Protocol)生态爆发：50+官方服务器覆盖GitHub/Slack/Notion/Postgres等，企业内部MCP注册表成为新基础设施
- LLM长上下文之战：Gemini 2M Token / Claude 200K / GPT-4o 128K技术选型指南，针对金融长文档(招股书/年报)场景给出最优性价比方案

---

## 新增内容（2026版）
**Step 2 新增技术评估（2026）**：
- LangGraph v1.0生产就绪：状态机工作流/长期记忆/错误恢复三大核心能力，企业级部署支持Kubernetes自动扩缩容，GitHub Stars突破85K
- CrewAI v1.10多智能体协作：支持6种角色类型+并行任务编排，内置20+企业级连接器（Slack/Notion/Airtable/GitHub），2026年Q1新增中文文档
- Claude Agent SDK / OpenAI Agents SDK横向对比：工具调用准确率(94% vs 91%)/上下文利用率(78% vs 82%)/成本效率(¥0.8/千Token vs ¥1.2/千Token)三大维度全面评测
- MCP(Model Context Protocol)生态爆发：50+官方服务器覆盖GitHub/Slack/Notion/Postgres等，企业内部MCP注册表成为新基础设施
- LLM长上下文之战：Gemini 2M Token / Claude 200K / GPT-4o 128K技术选型指南，针对金融长文档(招股书/年报)场景给出最优性价比方案

---

## Step 1 — Understand the Use Case
Ask the user to describe:
- The task or workflow to automate (e.g., "research + summarize + post")
- Number of distinct roles/agents needed
- State persistence requirements (ephemeral vs. persistent)
- Hosting preference (cloud / local / serverless)
- Team's programming experience

### Step 2 — Framework Shortlist & Comparison
Generate a focused comparison table of the top 2–3 frameworks suited to the use case:

| Framework | Best For | State Mgmt | Learning Curve | Hosting |
|-----------|----------|------------|----------------|---------|
| LangGraph | Complex stateful workflows | ✅ Built-in | Medium | Any |
| CrewAI | Role-based team simulations | Partial | Low | Any |
| AutoGen/AG2 | Conversational agent loops | External | Medium | Any |
| OpenAI Agents SDK | OpenAI ecosystem, handoffs | Built-in | Low | Cloud-first |
| Claude Agent SDK | Anthropic native, tool use | Built-in | Low | Cloud-first |
| Strands Agents | AWS/Bedrock integration | External | Medium | AWS |

### Step 3 — Architecture Recommendation
Output a recommended architecture including:
- Agent topology (who calls whom)
- Tool assignments per agent
- Memory / state strategy
- Human-in-the-loop checkpoints
- Error handling & fallback patterns

### Step 4 — Starter Code Generation
Generate a complete, runnable Python scaffold:
```python
# Example: CrewAI research + report pipeline
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

search_tool = SerperDevTool()

researcher = Agent(
    role="Senior Research Analyst",
    goal="Uncover cutting-edge developments in {topic}",
    backstory="You are an expert researcher...",
    tools=[search_tool],
    verbose=True
)

writer = Agent(
    role="Technical Writer",
    goal="Craft insightful, accurate reports from research",
    backstory="You transform raw research into executive summaries...",
    verbose=True
)

research_task = Task(
    description="Research {topic} thoroughly...",
    agent=researcher,
    expected_output="Bullet-point research findings"
)

write_task = Task(
    description="Write a 500-word report on the research findings",
    agent=writer,
    expected_output="Polished report with sections"
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff(inputs={"topic": "agentic AI in 2026"})
```

### Step 5 — Production Checklist
Provide a framework-specific production checklist:
- [ ] Rate limiting & retry logic
- [ ] Observability (LangSmith / Weights & Biases / custom logging)
- [ ] Secrets management (never hardcode API keys)
- [ ] Cost estimation per run
- [ ] Human review gates for high-stakes outputs

## Example Interactions

**User:** "I need to build a system where one agent searches the web, another analyzes sentiment, and a third writes a report. Which framework should I use?"

**Skill response:** Recommends CrewAI for its role-based simplicity, provides a 3-agent architecture diagram, generates a complete scaffold with SerperDevTool + OpenAI, and provides a deployment checklist.

---

**User:** "I'm using LangGraph but my agents keep losing context between nodes. How do I fix state persistence?"

**Skill response:** Explains LangGraph's StateGraph checkpointing, shows how to add a PostgreSQL checkpointer, provides a code fix.

## Notes & Constraints

- Always surface the **trade-offs**, not just the "winner" — different teams need different frameworks
- Code examples default to Python; mention JS/TS equivalents where available
- For enterprise requirements, flag SOC2 / data residency considerations
- Keep up with the rapidly evolving MCP (Model Context Protocol) and A2A protocol integrations
- Recommend starting simple: single agent → multi-agent only when genuinely needed
