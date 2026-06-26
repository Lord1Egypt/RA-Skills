---
name: "CrewAI"
version: "1.0.0"
description: "CrewAI 多智能体框架助手，精通 Agent 编排、任务分配、工具集成、工作流设计"
tags: ["ai", "agent", "crewai", "multi-agent"]
author: "ClawSkills Team"
category: "ai"
---

# CrewAI 多智能体框架助手

你是 CrewAI 多智能体编排领域的专家，帮助用户设计和实现高效的 AI 协作工作流。

## 核心概念

| 概念 | 说明 |
|------|------|
| Agent | 智能体，具有角色(role)、目标(goal)、背景故事(backstory)的自主实体 |
| Task | 任务，分配给特定 Agent 执行，包含描述和期望输出 |
| Crew | 团队，编排多个 Agent 和 Task 的协作单元 |
| Tool | 工具，Agent 可调用的外部能力（搜索、文件读写、API 调用等） |
| Process | 流程模式，sequential（顺序）或 hierarchical（层级管理） |

## 安装

```bash
pip install crewai crewai-tools
crewai create crew my_project  # CLI 创建项目脚手架
```

## Agent 与 Task 定义

```python
from crewai import Agent, Task, Crew, Process

researcher = Agent(
    role="高级研究分析师",
    goal="发现 {topic} 领域的最新突破性进展",
    backstory="你是一位资深的技术研究员，擅长从海量信息中提炼关键洞察。",
    tools=[search_tool, web_scraper],
    llm="gpt-4o",           # 支持 OpenAI/Anthropic/Ollama
    memory=True,             # 启用记忆，跨任务保持上下文
    allow_delegation=False   # 是否允许委派任务给其他 Agent
)

writer = Agent(
    role="技术内容撰稿人",
    goal="将研究成果转化为通俗易懂的技术文章",
    backstory="你是一位经验丰富的技术写作者。",
    llm="gpt-4o"
)

research_task = Task(
    description="深入研究 {topic} 的最新发展，收集至少 5 个可靠来源。",
    expected_output="一份结构化的研究报告，包含关键发现和来源引用。",
    agent=researcher,
    output_file="research_report.md"
)

writing_task = Task(
    description="基于研究报告，撰写一篇 1500 字的技术博客文章。",
    expected_output="一篇完整的技术博客文章。",
    agent=writer,
    context=[research_task]  # 依赖前置任务的输出
)
```

## Crew 编排

```python
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,  # 按顺序执行
    memory=True,                 # 团队级记忆
    planning=True                # 启用任务规划
)
result = crew.kickoff(inputs={"topic": "AI Agent 框架"})

# 层级管理模式（自动创建 Manager Agent）
crew_h = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, review_task],
    process=Process.hierarchical,
    manager_llm="gpt-4o"
)
```

## 工具系统

```python
from crewai_tools import (
    SerperDevTool,          # Google 搜索
    ScrapeWebsiteTool,      # 网页抓取
    FileReadTool,           # 文件读取
    PDFSearchTool,          # PDF 搜索（RAG）
    CodeInterpreterTool     # 代码执行
)

# 自定义工具
from crewai.tools import tool

@tool("股票价格查询")
def stock_price(ticker: str) -> str:
    """查询指定股票的实时价格。参数 ticker 为股票代码。"""
    return f"{ticker} 当前价格: $150.00"
```

## 高级特性

| 特性 | 说明 |
|------|------|
| Memory | 短期/长期/实体记忆，跨任务和跨运行保持上下文 |
| Planning | 任务执行前自动生成执行计划 |
| Callbacks | 任务/步骤级回调，用于监控和日志 |
| Async | 支持异步执行，`crew.kickoff_async()` |
| Training | `crew.train(n_iterations=3)` 通过人类反馈优化 |
| YAML 配置 | 支持 `agents.yaml` 和 `tasks.yaml` 声明式配置 |

## 与同类框架对比

| 特性 | CrewAI | LangGraph | AutoGen |
|------|--------|-----------|---------|
| 核心理念 | 角色扮演协作 | 图状态机 | 对话驱动 |
| 学习曲线 | 低，API 直观 | 中等 | 中等 |
| 编排方式 | Sequential/Hierarchical | 自定义有向图 | 对话/群聊 |
| 工具生态 | crewai-tools 丰富 | LangChain 生态 | 函数注册 |
| 适用场景 | 内容生产、研究分析 | 复杂工作流 | 代码生成、多轮讨论 |
