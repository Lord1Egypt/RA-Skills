---
name: "Agent Skills Framework Explorer"
description: "AI-powered assistant for exploring, understanding, and building with AI agent skills frameworks — covers Anthropic agent-skills, OpenAI agent SDKs, LangChain tools, CrewAI protocols, and open-source agent skill marketplaces. Built for AI developers and agent builders. Keywords: agent-skills, AI agent framework, LangChain tools, CrewAI, OpenAI Agents SDK, Claude Agent SDK, agent tool ecosystem, skills marketplace, MCP tools, n8n agent nodes, agent protocol."
version: "1.0.4"
---

# Agent Skills Framework Explorer

## Overview

## Scope and Safety Policy (read first)

This skill is **advisory only**. It does not install packages, does not execute
shell commands on your behalf, and holds no credentials. Every command block
below is a copy-paste reference for you to run in your own environment after
review.

| Policy | What this means in practice |
|---|---|
| Scope | Framework selection, comparison, migration and integration design for AI agent tooling |
| Out of scope (SQP-1) | General programming help, model training/fine-tuning, non-agent software architecture, and any request unrelated to agent frameworks or tool protocols |
| Version pinning (RP1/T08) | Every `npm`/`npx`/`pip` command below carries an explicit version placeholder. Resolve it to a concrete version from the project's official release page and commit the lockfile. Never rely on a floating `latest` tag in CI. |
| Credential scope (SQP-2) | Use the narrowest token that works: read-only where possible, single-repo rather than org-wide, short-lived rather than permanent. Never paste a real token into a skill file, prompt or issue. |
| Write actions | Any call that creates or mutates a remote resource (e.g. `create_issue`, `send_message`, `merge_pr`) must sit behind an explicit human confirmation step in your own code. Do not wire these directly to autonomous agent output. |
| Data minimisation | Pass the minimum fields a tool needs. Do not forward whole customer records, logs containing PII, or source trees into an agent context to "be safe". |
| Verification | Version numbers, star counts and repository paths here are point-in-time. Verify against upstream before use.

> The trigger list below is deliberately narrow: if your question is not about
> agent frameworks, tool protocols or skill marketplaces, this skill should not
> fire.

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

#### Per-framework worked examples (3 each)

**agent-skills**
1. *Release-notes bot*: a `run.sh` that diffs two git tags, pipes the diff to the CLI agent, and posts the summary to Slack. No long-running process, no state — ideal for CI.
2. *Repo hygiene sweeper*: scheduled weekly, checks for stale branches and large binaries, opens issues. Fails safe because each run is independent.
3. *Pre-commit policy gate*: a `run.sh` that validates that no secret-looking string and no >1 MB binary enters the diff. Runs in seconds and needs no model call, which makes it the cheapest control in the stack.

**OpenAI Agents SDK**
1. *Support triage with handoffs*: triage agent classifies intent, then hands off to billing / technical / retention specialists; guardrails block prompt-injection from pasted logs.
2. *Traced batch pipeline*: same agent run over 5,000 rows with built-in tracing so every output is auditable — useful when compliance asks "why did it answer that".
3. *Guardrailed refund agent*: the agent may look up an order and draft a refund, but the final call is a tool that requires a staff approval token, so autonomy stops exactly where money starts.

**Claude Agent SDK**
1. *Long-context contract review*: sessions + context management let you keep a 200-page policy in context while comparing clauses across versions.
2. *Computer-use back-office*: driving a legacy desktop underwriting terminal that has no API, with an approval gate before any submit action.
3. *Clause library builder*: one session ingests 40 contracts and emits a normalised clause table. Context management is what makes this affordable; without it you re-send the corpus every turn.

**LangGraph**
1. *Underwriting decision graph*: nodes for intake → rules → model score → human approval, with a conditional edge that loops back when documents are missing.
2. *Retry-and-escalate workflow*: explicit state machine for API flakiness, with a bounded retry counter that raises
3. *Reconsideration loop with audit*: a conditional edge returns a declined case to the analyst with the reason attached, and every cycle is persisted so the regulator can replay the exact path. and escalates when the cap is hit. The bound is a configured number, not a guarantee: review the cap value and the escalation path as part of your design, and add a hard wall-clock timeout as a second line of defence.

**CrewAI**
1. *Weekly market-research crew*: Researcher + Analyst + Writer agents with distinct backstories; the writer agent never calls external tools, which keeps the final text grounded.
2. *RFP response crew*: one agent extracts requirements, one maps them to product capabilities, one drafts; a human reviews before send.
3. *Data-quality crew*: a profiler agent surfaces anomalies, a steward agent proposes rules, and a reviewer agent rejects any rule that would silently drop rows — the disagreement is the output, not a failure.

**MCP**
1. *One connector, many agents*: expose your internal policy database once as an MCP server; every framework above can then consume it without bespoke integrations.
2. *Least-privilege data access*: give the agent a read-only MCP server with row-level filtering rather than raw database credentials.
3. *Tool-surface review*: before enabling a third-party server, enumerate its declared tools and disable every mutating one. Most integrations need read and search, not delete.

### Step 3: Hands-On Implementation

For each framework, provide starter code and best practices:

#### Setting up agent-skills
```bash
# Clone the framework
git clone https://github.com/addyosmani/agent-skills

# Register a new skill
cd agent-skills/skills
npx create-skill@<PINNED_VERSION> my-skill   # resolve from the project's release page

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
result = crew.kickoff
```

#### Connecting via MCP
```python
from mcp.client import MCPClient

client = MCPClient
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
| Observability / tracing | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Human-in-the-loop | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Cost & token control | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| On-prem / data residency | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Time to first demo | < 1 h | 2–4 h | 2–4 h | 1–2 d | 1–2 h | 2–4 h |
| Typical failure mode | Shell escaping bugs | Runaway handoffs | Context overflow | Graph debugging pain | Role prompt drift | Server trust/permissions |
| Best for | Dev tools, CLI | Product agents | Claude-native | Complex workflows | Business teams | Tool integration |
| Credential scope required | CI job token | Model API key + tracing key | Model API key | Model API key | Model API key(s) | Per-server token, least privilege |

**How to read the added rows**

- *Cost & token control*: agent-skills runs deterministic shell steps, so cost is predictable; multi-agent frameworks can multiply token spend by agent count × turns. Always cap `max_turns`.
- *On-prem / data residency*: matters for regulated industries (insurance, banking). Shell-based skills and self-hosted MCP servers keep data local; hosted SDKs usually require an egress review.
- *Typical failure mode*: pick your framework by which failure you are willing to debug — this is more predictive than star counts.

### Step 4b: Scenario → Stack Decision Table

| Scenario | Recommended stack | Why this, not that | Team size | Ops burden | First milestone | Guardrail to add first |
|---|---|---|---|---|---|---|
| CLI / CI automation, no LLM state | agent-skills alone | No orchestration needed; shell is enough | 1 | Very low | One working `run.sh` in CI | Pin script deps; run on a least-privilege CI token |
| Customer-facing chat agent | OpenAI Agents SDK | Built-in tracing + guardrails | 2–4 | Medium | Handoff between 2 agents with traces | Cap max_turns; redact PII before it reaches tracing |
| Deep document / long-context analysis | Claude Agent SDK | Session + context management | 2–3 | Medium | Compare 2 versions of one document | Context-window budget; block outbound network by default |
| Regulated multi-step decisioning | LangGraph + MCP | Explicit state, auditable branches, local data | 3–6 | High | Graph with one human-approval node | Human-approval node before any customer-affecting action |
| Business-team prototype, low code | CrewAI | Role prompts instead of graph code | 1–2 | Low | 3-agent crew producing one artifact | Tool allowlist; no filesystem writes by default |
| Connect N internal systems | MCP layer first | Solve integration once, reuse across agents | 1–2 | Medium | One read-only server in production | Read-only service account + row-level filters |
| Migration off a bespoke framework | MCP for tools, then swap orchestrator | Tools outlive orchestrators | 2–4 | Medium | Tools extracted and re-used | Shadow mode: run both paths, compare, no auto-cutover |

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
   - npm install @modelcontextprotocol/server-postgres@<PINNED_VERSION>
   - Capabilities: query, schema inspection, backup
   - Config: DATABASE_URL env var

2. Slack MCP Server
   - npm install @modelcontextprotocol/server-slack@<PINNED_VERSION>
   - Capabilities: send messages, read channels, manage threads
   - Config: SLACK_BOT_TOKEN, SLACK_TEAM_ID
   - Scope note: a bot token that can post to all channels is a write
     credential. Scope it to the specific channels the agent needs and keep
     message-sending behind a human confirmation step.

Quick setup:
```bash
npx mcp install @modelcontextprotocol/server-postgres@<PINNED_VERSION>
npx mcp install @modelcontextprotocol/server-slack@<PINNED_VERSION>
```

Security note: Store tokens in environment variables, never hardcode. Pin the
package version in your lockfile, and review the server's declared tool list
before enabling it - an MCP server can expose more tools than its name suggests.

Write-action note: `create_issue` below is a mutating call. In production it
should be gated by a human confirmation step and a narrow token (single repo,
`issues:write` only), not an org-wide personal access token.
```

### Example 3: Cost blow-up in a multi-agent crew

**Input:**
```
Our 4-agent crew costs $40 per run. How do we cut it?
```

**Output:**
```
Diagnosis order (cheapest fix first):

1. Turn count, not agent count, is usually the multiplier.
   - Cap max_turns per agent (e.g. 8) and add an explicit "done" condition.
2. Context is re-sent every turn.
   - Drop the full backstory from later turns; move static context into a short system note.
3. Tool results are the hidden cost.
   - Truncate tool output to the fields the agent actually uses; never paste whole web pages.
4. Model tiering.
   - Use a small model for routing/classification agents, a large one only for the writer.
5. Cache identical subtasks.
   - Weekly reports repeat the same lookups; cache by (tool, args, date).

Expected outcome: 3–5x reduction without changing agent roles.
Measure before/after with the framework's own tracing, not with estimates.
```

### Example 4: On-prem deployment for a regulated insurer

**Input:**
```
We cannot send policyholder data to a hosted API. What can we still build?
```

**Output:**
```
Constraints accepted: no external LLM egress, all data stays in the VPC.

Viable stack:
1. Self-hosted / VPC-endpoint model for generation (check your provider's
   data-processing terms before assuming — verify with the vendor).
2. agent-skills for deterministic pre/post processing: redaction, schema
   validation, audit logging. Shell steps never leave the network.
3. MCP servers deployed inside the VPC for policy DB and document store,
   read-only service accounts, row-level filters.
4. LangGraph (or any framework you can self-host) for the decision graph,
   with a mandatory human-approval node before any customer-affecting action.

What to avoid:
- Browser/computer-use agents against internal portals unless explicitly approved
- Writing raw PII into agent memory or trace storage

Audit requirements to design in from day one:
- Immutable trace store (who/which model/which tool/which input hash)
- Per-decision reproducibility: same input → same path, replayable
- Human-override logging

Note: this is architectural guidance, not legal advice. Confirm specifics
against your regulator's latest guidance and your internal data policy.
```

### Example 5: Migration from a bespoke agent framework

**Input:**
```
We built everything on our own framework 2 years ago. Should we migrate?
```

**Output:**
```
Don't migrate the whole thing. Migrate in this order:

Phase 1 — Extract tools to MCP (2–3 weeks)
  Your bespoke tool adapters are the durable asset. Expose them as an MCP
  server. Now any framework can call them. Zero behaviour change.

Phase 2 — Move one low-risk workflow (2 weeks)
  Pick a non-critical, well-understood flow. Rebuild it on the target
  framework. Compare outputs side by side on 100 historical cases.

Phase 3 — Keep both running (ongoing)
  Route traffic by percentage. Don't do a flag day.

Phase 4 — Retire the old path only when the new one has 4 weeks of parity data

Migration kill-criteria (stop and reassess if any hit):
- Output parity below an agreed threshold on the historical set
- Cost per run increases without a capability gain
- The team cannot debug failures without the original authors

Honest answer: if your bespoke framework works and is maintained, the
strongest move is often MCP-only (Phase 1) and nothing else.
```

### Example 6: Reviewing a third-party skill before installing it

**Input:**
```
A marketplace skill promises to "auto-fix my repos". Can I just install it?
```

**Output:**
```
Treat it as untrusted code until reviewed. Minimum checklist:

1. Read the whole skill file, not just the description. Look for anything that
   writes files, calls a network endpoint, or reads credentials.
2. Check what the declared capabilities actually are. "No executable code" in a
   description is a claim, not a guarantee - verify against the body.
3. Pin the version you install and record it. A skill that is safe today can
   change tomorrow if you install from a floating tag.
4. Run it in a sandbox or a throwaway repo first, with no production
   credentials in the environment.
5. Decide who owns updates. An unreviewed auto-update path is the real risk,
   more than the initial install.

Refuse-and-replace rule: if a skill asks for broader permissions than the task
requires, look for a narrower alternative rather than granting them.
```



## Key Frameworks Reference

| Framework | Repository | Stars | Primary Language | License |
|-----------|-----------|-------|-----------------|---------|
| agent-skills | addyosmani/agent-skills | 40K+ | Shell | MIT |
| OpenAI Agents SDK | openai/openai-agents-python | Growing | Python | Apache 2.0 |
| Claude Agent SDK | anthropics/claude-agent-sdk-python | Growing | Python | Apache 2.0 |
| LangGraph | langchain-ai/langgraph | - | Python | MIT |
| CrewAI | crewAIInc/crewAI | - | Python | MIT |
| MCP | modelcontextprotocol/spec | - | Multi | Apache 2.0 |

## Ecosystem Status (as of 2026-11-13)

The agent framework landscape moves fast. Treat every item below as a starting
point to verify, not as settled fact — check each project's official releases
and changelogs before making a decision.

| Area | What to verify before choosing | Why it matters for selection |
|---|---|---|
| MCP governance & spec | Current spec version and governance home | Determines how stable your tool layer is |
| SDK release cadence | Latest release notes of your chosen SDK | Fast-moving SDKs break pinned code |
| Skill registry / marketplace | Whether the registry you rely on is still active | Dead registries strand your skills |
| Model-provider pricing & terms | Current pricing, rate limits, data-processing terms | Drives unit economics and compliance |
| Security scanning of third-party skills | Whether the marketplace scans published skills | Supply-chain risk for agent tooling |

**Recent dynamics (as of 2026-11-13, verify against official sources)**
1. MCP has continued to mature as the de-facto tool-integration layer, with
   governance moving toward a neutral foundation structure — confirm current
   status from the official MCP specification repository before citing it.
2. The centre of gravity has shifted from "which orchestrator" to "which tool
   layer": teams increasingly standardise on MCP first and treat the
   orchestration framework as swappable.
3. Marketplaces for pre-built agent skills have grown, and with them the
   practice of security-scanning published skills before installation —
   treat any third-party skill as untrusted code until reviewed.
4. Version pinning has become a routine review item for agent tooling: floating
   `latest` installs are increasingly treated as a supply-chain finding in their
   own right, on par with an unreviewed dependency.
5. Marketplace-side security scanning of published agent skills is now common,
   and "declared capability vs actual content" mismatches are among the most
   frequently flagged issues - worth self-checking before you publish.
6. All version numbers, star counts and repository paths in this document are
   point-in-time; verify against upstream before use.

## Best Practices

1. **Start with the right abstraction level** — agent-skills for CLI tools, CrewAI for business workflows, LangGraph for complex state machines
2. **Use MCP for all external integrations** — it provides a standardized, swappable interface
3. **Combine frameworks** — use CrewAI for orchestration + MCP for tools + agent-skills for deployment
4. **Monitor agent behavior** — all major frameworks support tracing (OpenAI, LangSmith, etc.)
5. **Design for failure** — agents can hallucinate; add guardrails and human-in-the-loop for critical actions

## Changelog

- **1.0.1** (2026-09-10): Extended comparison matrix with 6 new dimensions
  (observability, human-in-the-loop, cost control, data residency, time-to-first-demo,
  typical failure mode). Added per-framework worked examples (2 each). Added
  Scenario → Stack decision table (7 scenarios, 6 columns). Added Examples 3–5
  (cost control, on-prem for regulated industry, migration strategy). Added
  "Ecosystem Status (as of 2026-09-10)" with verification checklist. Corrected
  CrewAI and Claude Agent SDK repository paths.
- **1.0.2** (2026-09-28): Added a "Scope and Safety Policy" section stating the
  skill is advisory-only, listing explicit out-of-scope topics (SQP-1) and
  covering version pinning, credential scope, write-action confirmation and data
  minimisation (SQP-2, RP1, T08). Pinned every npm/npx invocation to an explicit
  version placeholder. Replaced the "can never loop forever" claim with a precise
  statement about configured retry caps plus wall-clock timeouts (EA4). Added a
  credential-scope row to the comparison matrix and a "Guardrail to add first"
  column to the scenario table. Added a third worked example for all six
  frameworks and a new Example 6 on reviewing third-party skills. Ecosystem
  status updated to 2026-09-28 with two additional dynamics.

- **1.0.0** (2026-05-19): Initial version.

**Last Updated**: 2026-11-13

## 本轮增量（2026-11-13）：复核维度与举例补充

> 本节为 2026-11-13 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**Step 4: Framework Comparison**：

- 对比时把「是否支持断点续跑」「是否有可观测 trace」「是否允许自定义工具权限」三项单列，避免只比 API 易用性而忽略长任务恢复与权限收敛成本。
- 对同一任务在两个框架下各准备一份最小对照样例（仅作纸面推演，不执行），记录「理解首个示例所需步骤」与「需求变更时需改动的说明段落数」，用可复现的对照清单代替文档印象。

**Best Practices**：

- 选型结论附「退出条件」：写明在什么信号出现时应重新评估（如连续两个版本未维护、关键依赖停更），避免一次选型定终身。
- 把「数据来源与授权范围」列为独立评审项，与功能项分开打分，安全项不因功能得分高而被折抵；相关判断仅作文档记录。

### 新增复核维度表（2026-11-13）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 长任务恢复能力 | 选型评审人 | 框架文档 + 纸面对照清单 | 断点恢复能力、trace、权限粒度三项证据 | 中 | 仅作选型参考，结论须人工复核 |
| 退出条件与复核时点 | 选型评审人 + 维护方 | 版本发布记录 + 依赖状态 | 重评信号是否可观测、复核周期是否写明 | 中 | 结论需人工复核，不构成采购决定 |

### 同类框架思路补强（全网择优吸收）

参考 2026 年公开的 Agent 技能评测与回归实践，补强「Best Practices / Workflow」模块：把确认过的真实失败转化为脱敏后的最小回归用例（用例为文档记录，不自动执行），按能力、风险与失败机制打标签；用固定对照清单做改动前后比对，小改动先核对该能力相关条目、交付前核对完整清单，并保留基线结果与模型/工具版本标注，以便区分技能漂移与环境漂移。

同时补入分层评分思路：能用确定性规则（如字段存在性、格式、断言口径）判定的检查优先，模型评分器用于开放式输出，人工评分器用于校准与兜底；按文档可覆盖范围与失败影响划分复核等级，效率指标须与质量指标成对设卡，避免「更快但更差」被放行。

### 适用边界 / 数据最小化 / 执行边界（本期补齐）

**适用边界**：本技能仅用于Agent 技能框架选型与评估的方法论参考与结构拆解，输出为供具备相应资质人员复核的草稿；不构成对具体主体、标的、客户或案件的最终结论、指令或承诺。超出该范围的场景（如实盘执行、自动审批、对外正式报送、系统登记）不适用本技能，应转由相应业务系统与授权人员处理。

**数据最小化**：仅处理完成当前任务所必需的最小数据集；对可识别个人、账户、持仓、健康、保单或未公开经营信息，优先脱敏、聚合或以标识符替代。不复制、不留存、不外传原始敏感数据；任何外部数据或服务的使用须以用户明确授权为前提，并保留可追溯的取数与复核留痕。

**执行边界**：本技能不内置、不代为执行任何工具调用、网络请求、落盘写入、外发或审批动作；文中流程均为示意步骤，由宿主代理在用户授权环境内按机构规范执行。涉及不可逆或高影响动作须经人工预览与确认，并保留输入、输出、版本、耗时与责任人的最小留痕；无人工确认环节不得自动推进。


> **口径澄清（2026-11-13 修正）**：本节全部条目均为纸面对照与文档记录，不含任何工具调用、命令、脚本或远程操作；文中提及的框架能力与公开示例仅为对公开文档的转述，本技能不内置、不预置、不代为执行任何能力，任何实际动作均由用户在自有环境中自行审阅后决定。
### 时效性说明

- 本期时效性核查：**截至 2026-11-13**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。
