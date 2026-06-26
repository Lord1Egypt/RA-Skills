---
name: "Agent Skills Framework Explorer"
description: "AI-powered assistant for exploring, understanding, and building with AI agent skills frameworks — covers Anthropic agent-skills, OpenAI agent SDKs, LangChain tools, CrewAI protocols, and open-source agent skill marketplaces. Built for AI developers and agent builders. Keywords: agent-skills, AI agent framework, LangChain tools, CrewAI, OpenAI Agents SDK, Claude Agent SDK, agent tool ecosystem, skills marketplace, MCP tools, n8n agent nodes, agent protocol."
version: "1.0.0"
---

# Agent Skills Framework Explorer

## Overview

A comprehensive guide and assistant for navigating the rapidly evolving AI agent skills framework ecosystem. Whether you're exploring addyosmani/agent-skills (40K+ stars), building with Anthropic's Claude Agent SDK, designing multi-agent pipelines with CrewAI/LangGraph, or connecting tools via MCP protocol — this skill helps you understand, compare, and implement the right framework for your use case.

## Triggers

- "compare agent frameworks"
- "how to use agent-skills"
- "build a multi-agent pipeline with [framework]"
- "what is MCP protocol"
- "CrewAI vs LangGraph vs OpenAI Agents SDK"
- "find tools for my agent"
- "agent framework comparison"
- "MCP server setup"
- "AI Agent工具框架对比"
- "多智能体框架选型"

## Workflow

### Step 1: Identify the User's Goal

Determine the primary use case:
- **Framework selection**: Comparing options for a new project
- **Tool integration**: Adding capabilities to an existing agent
- **Multi-agent design**: Orchestrating multiple specialized agents
- **Skills marketplace**: Finding pre-built agent capabilities
- **Protocol understanding**: Learning MCP, Agent Protocol, or other standards
- **Migration**: Moving from one framework to another

### Step 2: Framework Deep Dive

Provide structured comparison and guidance for the relevant framework:

#### Anthropic agent-skills (addyosmani/agent-skills)
- **What it is**: Shell-based skill framework for CLI agents, Claude Code, and GitHub Actions
- **Key concepts**: `skill.yaml` metadata, bash/python/shell execution, skill chaining
- **Use when**: Building CLI tools, automation scripts, developer-facing agents
- **Ecosystem**: 40K+ stars, active community, skill registry at agent-skills.dev
- **Example skill structure**:
  ```
  skill.yaml  (name, triggers, description, tools)
  run.sh     (main execution script)
  references/ (docs, examples)
  ```

#### OpenAI Agents SDK
- **What it is**: Official Python SDK for building multi-agent systems
- **Key concepts**: Handoffs, tracing, guardrails, function calling
- **Use when**: Building customer-facing agents on OpenAI models
- **Best for**: Product teams needing production-ready agents with built-in observability

#### Claude Agent SDK (Anthropic)
- **What it is**: SDK for building Claude-powered agents with tool use
- **Key concepts**: Tools, sessions, context management, computer use
- **Use when**: Deep Claude integration, computer-use agents, complex tool chains

#### LangGraph (LangChain)
- **What it is**: Graph-based framework for cyclical agent workflows
- **Key concepts**: Nodes, edges, state machines, human-in-the-loop
- **Use when**: Complex workflows with branching, loops, and multi-agent coordination

#### CrewAI
- **What it is**: Role-based multi-agent framework
- **Key concepts**: Agents with roles/goals/backstory, task delegation, crew orchestration
- **Use when**: Team-based AI workflows (e.g., research crew, writing crew)
- **Best for**: Business users who want multi-agent without deep coding

#### MCP (Model Context Protocol)
- **What it is**: Open protocol for connecting AI models to external tools
- **Key concepts**: Servers, clients, resources, prompts, tools
- **Ecosystem**: 50+ official and community servers (GitHub, Slack, Postgres, etc.)
- **Use when**: Connecting agents to real-world data and services
- **Reference**: https://modelcontextprotocol.io

### Step 3: Hands-On Implementation

For each framework, provide starter code and best practices:

#### Setting up agent-skills
```bash
# Clone the framework
git clone https://github.com/addyosmani/agent-skills

# Register a new skill
cd agent-skills/skills
npx create-skill my-skill

# skill.yaml example
name: my-skill
triggers:
  - "run my task"
  - "execute my workflow"
description: "A custom agent skill"
tools:
  - bash
  - filesystem
execute: ./run.sh
```

#### Building with CrewAI
```python
from crewai import Agent, Task, Crew

researcher = Agent(
    role="Financial Analyst",
    goal="Research insurance market trends",
    backstory="Expert in insurance data analysis",
    tools=[...],
)

research_task = Task(
    description="Analyze Q1 2026 insurance market trends",
    agent=researcher,
)

crew = Crew(agents=[researcher], tasks=[research_task])
result = crew.kickoff()
```

#### Connecting via MCP
```python
from mcp.client import MCPClient

client = MCPClient()
# Connect to GitHub MCP server
await client.connect("github", token=os.getenv("GITHUB_TOKEN"))
# Use tools from the server
result = await client.call_tool("github", "create_issue", {
    "repo": "owner/repo",
    "title": "Agent-generated task",
})
```

### Step 4: Framework Comparison Matrix

| Criteria | agent-skills | OpenAI Agents SDK | Claude Agent SDK | LangGraph | CrewAI | MCP |
|----------|-------------|-------------------|-----------------|-----------|--------|-----|
| Multi-agent | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Ease of use | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Production-ready | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Customization | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Tool ecosystem | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Best for | Dev tools, CLI | Product agents | Claude-native | Complex workflows | Business teams | Tool integration |

### Step 5: Skill Discovery

Help users find pre-built skills for their needs:
1. Search agent-skills.dev registry by category
2. Find MCP servers for specific tools (database, API, etc.)
3. Discover CrewAI templates and Crew templates
4. Identify gaps where a custom skill should be built

## Input/Output Examples

### Example 1: Framework Selection

**Input:**
```
I want to build an AI agent that researches stock trends and writes a weekly report.
Which framework should I use?
```

**Output:**
```
Recommendation: CrewAI + MCP combination

Rationale:
- Research + writing = multi-role workflow → CrewAI's agent delegation shines
- Stock data requires external API tools → MCP for data connections
- Weekly automation → agent-skills for scheduling

Suggested stack:
1. CrewAI crew: Researcher agent (MCP-connected) + Writer agent
2. MCP servers: Financial data API, web search
3. agent-skills: Weekly trigger, report delivery

Implementation path:
Week 1: Set up CrewAI with 2 agents
Week 2: Add MCP financial data tools
Week 3: Deploy via agent-skills scheduler
```

### Example 2: MCP Server Selection

**Input:**
```
I need to connect my agent to PostgreSQL and Slack. Which MCP servers should I use?
```

**Output:**
```
Recommended MCP Servers:

1. PostgreSQL MCP Server
   - npm install @modelcontextprotocol/server-postgres
   - Capabilities: query, schema inspection, backup
   - Config: DATABASE_URL env var

2. Slack MCP Server
   - npm install @modelcontextprotocol/server-slack
   - Capabilities: send messages, read channels, manage threads
   - Config: SLACK_BOT_TOKEN, SLACK_TEAM_ID

Quick setup:
```bash
npx mcp install @modelcontextprotocol/server-postgres
npx mcp install @modelcontextprotocol/server-slack
```

Security note: Store tokens in environment variables, never hardcode.
```

## Key Frameworks Reference

| Framework | Repository | Stars | Primary Language | License |
|-----------|-----------|-------|-----------------|---------|
| agent-skills | addyosmani/agent-skills | 40K+ | Shell | MIT |
| OpenAI Agents SDK | openai/openai-agents-python | Growing | Python | Apache 2.0 |
| Claude Agent SDK | anthropics/anthropic-cookbook | - | Python | - |
| LangGraph | langchain-ai/langgraph | - | Python | MIT |
| CrewAI | crewAI同事/crewai | - | Python | MIT |
| MCP | modelcontextprotocol/spec | - | Multi | Apache 2.0 |

## Best Practices

1. **Start with the right abstraction level** — agent-skills for CLI tools, CrewAI for business workflows, LangGraph for complex state machines
2. **Use MCP for all external integrations** — it provides a standardized, swappable interface
3. **Combine frameworks** — use CrewAI for orchestration + MCP for tools + agent-skills for deployment
4. **Monitor agent behavior** — all major frameworks support tracing (OpenAI, LangSmith, etc.)
5. **Design for failure** — agents can hallucinate; add guardrails and human-in-the-loop for critical actions
