# Agency Agents Router -- Route and orchestrate specialized agents

> Repo：[Staok/agency-agents-router-skill](https://github.com/Staok/agency-agents-router-skill).

## Overview

If openclaw.json has multiple agents configured under `agents.list`, this skill discovers them and orchestrates appropriate agents for any given task.

In a default OpenClaw setup, only the `main` agent's prompt is active. Other configured agents are invisible. Agent Router solves this by injecting agent awareness and orchestration logic into the main agent's prompt.

### Prerequisites

This skill is the **router** — the agent definitions must be installed separately. Without them, `agents.json` will be empty and no orchestration can happen.

**User (manual):** Install agency-agents-zh agents, then restart gateway:

```bash
git clone https://github.com/jnMetaCode/agency-agents-zh.git
cd agency-agents-zh
./scripts/convert.sh --tool openclaw
./scripts/install.sh --tool openclaw

# Restart OpenClaw gateway
openclaw gateway restart
```

**Agent (auto):** After user confirms installation, the agent runs:

```bash
cd ~/.openclaw/workspace/skills/agency-agents-router
python3 scripts/rebuild_index.py --clone
```

Then verifies agents appear in `~/.openclaw/openclaw.json` under `agents.list`.

If `agents.json` is missing or empty, the agent MUST first check whether agency-agents-zh is installed. If not, instruct the user with the manual steps above. Do NOT attempt to orchestrate without agents.

## How It Works

The main agent, equipped with this skill, becomes an orchestrator:

1. Receive a task description
2. **Classify the task intent** using the Task Archetypes table — this determines the agent selection strategy
3. **Detect ambiguity**: if the task crosses archetype boundaries, ask ONE clarifying question (audience, genre, format, depth) then proceed
4. **Pre-research**: for factual or time-sensitive tasks, the orchestrator should do live web searches first to ground agents in current reality, not stale training data
5. Look up `agents.json` to find matching agents based on the **clarified intent**
6. Design an execution plan: which agents to run, in what order, with what dependencies
7. Execute via `sessions_spawn(agentId=xxx, mode="run")`; domain-expert agents should be prompted to use `web_search` / `web_fetch` for factual grounding
8. Aggregate results and present to the user

## Research Protocol: Prefer Live Web Data

For factual, time-sensitive, or comparative tasks, agents should rely on live web data rather than training data alone.

### When to search the web

| Scenario                                            | Who searches                                |
| --------------------------------------------------- | ------------------------------------------- |
| Factual claims, current data, time-sensitive topics | Orchestrator (pre-research) + domain agents |
| Comparison / ranking / landscape surveys            | Orchestrator (pre-research) + domain agents |
| Research & Analysis or Content Creation archetypes  | Domain agents                               |
| Technical Writing with version-specific details     | Domain agents                               |

### Pre-research (orchestrator)

Before dispatching agents for factual tasks: 2-3 `web_search` queries → `web_fetch` 2-3 key sources → include findings in sub-agent prompts.

### Sub-agent prompt boilerplate

```
Prefer web_search/web_fetch for latest information over training data.
Cite URLs and dates for factual claims.
Mark unverifiable items as "[待确认]".
```

### CRITICAL: Classify BEFORE selecting agents

Do NOT jump from "receive task" directly to "look up agents". Without first classifying the task archetype, the same keyword ("write an analysis article") will be interpreted inconsistently — sometimes as research, sometimes as content creation. Step 2 (classification) is mandatory. Step 3 (ambiguity check) is mandatory when keywords span archetypes.

## Task Archetypes

Every task MUST be classified into one of these archetypes BEFORE agent selection. The archetype determines the **primary agent role** and whether domain-expert agents play lead or supporting roles.

| Archetype                         | Typical Keywords                                                                     | Agent Selection Strategy                                                       | Example                                            |
| --------------------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | -------------------------------------------------- |
| **Content Creation**        | write article, blog post, essay, deep-dive, long-form, copywriting, storytelling     | Lead: narrative/creative agents. Supporting: domain experts for fact-checking. | "Write a deep-dive article about AI Agent trends"  |
| **Research & Analysis**     | analyze, research, investigate, evaluate, feasibility, industry report, market study | Lead: research + domain experts. Multi-perspective parallel.                   | "Analyze the feasibility of an AI note-taking app" |
| **Technical Writing**       | technical docs, README, API docs, design docs, spec                                  | Lead: technical writer. Supporting: relevant engineering roles.                | "Write API documentation for this service"         |
| **Engineering**             | review code, fix bug, refactor, optimize, implement feature                          | Lead: language/framework-specific engineer. Supporting: security, testing.     | "Review this PR for security and performance"      |
| **Product Design**          | design, UI, UX, prototype, product spec, wireframe                                   | Lead: product manager or designer. Supporting: UX researcher.                  | "Design a SaaS pricing page"                       |
| **Business Strategy**       | business plan, pricing, go-to-market, funding, monetization                          | Lead: product manager or strategist. Supporting: finance, marketing.           | "Plan a go-to-market strategy for a B2B SaaS"      |
| **Code Generation**         | write code, build, implement, scaffold, create app                                   | Lead: language/framework-specific engineer (single agent typically).           | "Build a REST API with FastAPI"                    |
| **Multi-Perspective Audit** | review holistically, due diligence, full assessment                                  | Lead: domain-general coordinator. Parallel specialists.                        | "Full technical due diligence on this startup"     |

### Decision Heuristic

When the task says "write an article about X analysis", ask yourself:

- Is the primary goal to **inform and engage a broad audience**? → **Content Creation** (narrative agents lead, domain experts support)
- Is the primary goal to **produce a structured, evidence-heavy report for decision-makers**? → **Research & Analysis** (domain experts lead)
- Is the audience **implied by the user's profile**? If the user is a content creator → Content Creation. If the user is an engineer → Research & Analysis. **But still confirm if ambiguous.**

## Ambiguity Detection & Clarification Protocol

### Trigger Keywords

These keywords frequently span multiple archetypes. When detected, the orchestrator MUST ask for clarification before selecting agents:

| Ambiguous Keyword                            | Possible Archetypes                                   | What to Clarify                      |
| -------------------------------------------- | ----------------------------------------------------- | ------------------------------------ |
| "analysis article" / "deep analysis article" | Content Creation OR Research & Analysis               | Target audience? Publishing channel? |
| "design" / "design a solution"               | Product Design OR Engineering OR Business Strategy    | What kind of design?                 |
| "evaluate" / "assess"                        | Research & Analysis OR Engineering                    | From which perspective?              |
| "plan" / "proposal"                          | Business Strategy OR Product Design OR Engineering    | Plan for what?                       |
| "build" / "create"                           | Code Generation OR Product Design OR Content Creation | Build what exactly?                  |

### Clarification Protocol

When ambiguity is detected:

1. Identify the ambiguous dimension(s): audience? genre? format? depth? technical level?
2. Ask that resolves all ambiguity at once — do not ask multiple rounds
3. Frame the question to reveal the archetype: "Is this for a general-audience publication (Content Creation) or a technical decision-making report (Research)?"
4. If the user's profile strongly suggests one archetype, **still confirm** if ambiguity crosses the Content/Research boundary

**Bad (multiple rounds):**

> "Who is the audience?" → wait → "What format?" → wait → "How technical?"

**Good (single round):**

> "Target audience and channel for this article? e.g., general readers on Zhihu/WeChat (Content Creation route), or technical decision-makers as an internal report (Research route)?"

## Orchestration Patterns

### Pattern 1: Single Agent

A task clearly falls under one agent's expertise. Spawn directly.

```
User: "Review this C++ code for bugs"
  Archetype: Engineering
  -> engineering-code-reviewer
```

### Pattern 2: Parallel (Independent Agents)

Spawn multiple agents simultaneously for independent subtasks.

```
User: "Review this PR"
  -> engineering-code-reviewer (code quality)
  -> engineering-security-engineer (security audit)
  -> testing-performance-benchmarker (performance check)
  All three run in parallel, results merged at the end.
```

### Pattern 3: Sequential / Pipeline

Agent B depends on Agent A's output. Spawn A first, feed result into B.

```
User: "Design and document this API"
  -> engineering-software-architect (design the API)
  -> engineering-technical-writer (document the design)
```

### Pattern 4: DAG (Directed Acyclic Graph)

Complex workflows with parallel branches and merge points.

```
User: "Technical design review for a new feature"
  -> engineering-software-architect (system design)
     +-> engineering-security-engineer (security review)  --+
     +-> engineering-backend-architect (backend review)  ----+-> product-manager (summary)
     +-> engineering-database-optimizer (schema review)  ----+
```

### Pattern 5: Multi-Perspective Analysis (Research)

Multiple disciplinary perspectives for evidence-heavy analysis. Domain experts should web-search for current data.

```
User: "Is an AI-powered note-taking app viable?"
  Pre-research: orchestrator web-searches market landscape
  -> product-trend-researcher (market analysis)
  -> engineering-software-architect (technical feasibility)
  -> finance-financial-forecaster (cost/revenue modeling)
  -> marketing-seo-specialist (go-to-market analysis)
```

### Pattern 6: Content Creation

Narrative design + audience psychology + platform-aware execution. Domain experts play **supporting** roles (fact-checking, background research), NOT lead roles.

```
User: "Write a deep-dive article about AI Agent trends"
  Pre-research: orchestrator web-searches current landscape
  -> domain expert (background research — web-search for latest)
  -> academic-narratologist (story arc, hooks, rhythm)
  -> academic-psychologist (reader psychology, engagement)
  -> marketing-content-creator (platform voice, shareability)

  Workflow: orchestrator pre-research → domain expert FIRST (live web search) →
            creative agents in PARALLEL → synthesizer produces final draft.
```

**Key distinction from Pattern 5 (Research):**

| Dimension      | Pattern 5 (Research)             | Pattern 6 (Content Creation)      |
| -------------- | -------------------------------- | --------------------------------- |
| Primary goal   | Evidence, accuracy, completeness | Engagement, readability, impact   |
| Domain experts | Lead role                        | Supporting role (fact-check only) |
| Output format  | Structured report with sections  | Narrative with hooks, flow, voice |
| Success metric | Decision-makers can act on it    | Readers finish it and share it    |

## Agent Index

The lookup table in `agents.json` maps every configured agent to:

| Field           | Description                                                      |
| --------------- | ---------------------------------------------------------------- |
| `agentId`     | Agent ID in openclaw.json — used with sessions_spawn            |
| `name_zh`     | Chinese name (from agency-agents-zh README)                      |
| `description` | Detailed capability summary extracted from agent .md frontmatter |
| `expertise`   | Key skills (from README table)                                   |
| `scenario`    | Use case (from README table)                                     |
| `section`     | Department grouping                                              |

Data sources: agency-agents-zh (194 agents) + agency-agents upstream (21 agents).

## Usage Commands

| Command                     | Description                           |
| --------------------------- | ------------------------------------- |
| `/agents`                 | List all agents grouped by department |
| `/agents <dept>`          | Filter by department                  |
| `/agent search <keyword>` | Search agents by keyword              |
| `/agent <id> <task>`      | Explicitly invoke one specific agent  |

For most tasks, no command is needed. Describe the task naturally and the main agent will determine the orchestration plan.

## sessions_spawn Usage

```json
sessions_spawn(agentId="<agentId>", task="<task description>", mode="run")
```

- Sub-agents execute in their own workspace
- Results return to the main session automatically
- Multiple spawn calls without inter-dependencies can be invoked in parallel (single turn)
- Dependent calls: spawn, wait for result, then spawn the next

## Maintenance

```bash
# Rebuild with local agency-agents-zh repo:
python3 scripts/rebuild_index.py --repo /path/to/agency-agents-zh

# Auto-clone and rebuild from scratch:
python3 scripts/rebuild_index.py --clone --fetch
```

## Credits

- Agent descriptions from [agency-agents-zh](https://github.com/jnMetaCode/agency-agents-zh) (194 agents)
- Additional descriptions from [agency-agents](https://github.com/msitarzewski/agency-agents) upstream (21 agents)
- Orchestration patterns inspired by [Agency Orchestrator](https://github.com/jnMetaCode/agency-orchestrator)
