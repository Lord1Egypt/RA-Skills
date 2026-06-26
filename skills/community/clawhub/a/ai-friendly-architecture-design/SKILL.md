---
name: ai-friendly-architecture-design
description: Use when system needs to handle AI uncertainty, Agent types must be selected, APIs will be consumed by AI, or architecture must support probabilistic outputs and dynamic planning
license: Apache-2.0
---

# AI Friendly Architecture Design

## Overview

AI Friendly architecture enables traditional systems to handle AI's inherent **uncertainty** through three paradigm shifts: deterministic→probabilistic, structured→semantic, and static→dynamic. This skill guides agents to apply these principles correctly and avoid common anti-patterns.

**Core principle:** Use appropriate architecture for the problem—don't over-engineer with AI when traditional solutions suffice.

## When to Use

**Use when:**
- Designing systems that incorporate LLM/AI capabilities
- Evaluating whether to use AI Friendly architecture vs traditional architecture
- Designing Agent-based systems (ReAct, Plan, Multi-Agent)
- Creating APIs that will be consumed by AI Agents
- Building context engineering pipelines for AI applications

**Do NOT use when:**
- Building simple CRUD applications with no AI requirements
- Creating AI Workflow applications that only call pre-built Agents as APIs
- The system only needs deterministic, rule-based logic

## The Three Paradigm Shifts

### 1. Deterministic → Probabilistic

**Traditional:** Output follows `y=f(x)` mapping—binary success/failure.

**AI Friendly:** Output emerges from model + prompt + context + environment. Design goal: converge probabilistic output to an acceptable "safe interval" through RAG, prompt engineering, and evaluation mechanisms.

**Design implication:** Don't expect exact schema compliance from AI outputs. Build validation and fallback mechanisms.

### 2. Structured → Semantic

**Traditional:** Input must match predefined Schema exactly (JSON field types). System boundary is a rigid wall.

**AI Friendly:** System understands natural language and unstructured data. Responds based on **intent**, not format. System boundary becomes an elastic membrane.

**Design implication:** Design interfaces that accept flexible inputs and translate intent to actions.

### 3. Static → Dynamic

**Traditional:** Execution paths defined by hardcoded if-else logic or rules. Behavior is enumerable and verifiable.

**AI Friendly:** System makes decisions based on models, can reason about current state, decompose tasks, and respond to unknown changes without human intervention.

**Design implication:** Shift from "rules" to "planning"—grant systems autonomy for intelligent task orchestration.

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    Quality & Stability Layer                 │
│         (AI Observability, Evaluation, Security)            │
├─────────────────────────────────────────────────────────────┤
│                      Application Layer                       │
│    ┌──────────┐  ┌──────────┐  ┌──────────────────────┐    │
│    │  Agent   │  │  Intent  │  │      Session         │    │
│    │  Layer   │  │  Layer   │  │      Layer           │    │
│    └──────────┘  └──────────┘  └──────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│                    Capability Layer                          │
│         (MCP, RAG, Function Calling)                        │
├─────────────────────────────────────────────────────────────┤
│                   Foundation Layer                           │
│    ┌──────────┐  ┌──────────┐  ┌──────────────────────┐    │
│    │  Model   │  │ Knowledge│  │   Tool Management    │    │
│    │Management│  │Management│  │                      │    │
│    └──────────┘  └──────────┘  └──────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Foundation Layer

- **Model Management:** Unified API (OpenAI protocol) for multiple LLM providers
- **Knowledge Management:** Vector storage and retrieval for different knowledge sources
- **Tool Management:** MCP protocol for tool integration, Computer Use skills

#### Model Management Details

**Provider Selection:**

| Factor | Consideration |
|--------|--------------|
| Latency requirements | Regional providers vs global (OpenAI, Anthropic) |
| Cost | Per-token pricing, batch discounts, small model for simple tasks |
| Data privacy | On-premise (Ollama, vLLM) vs cloud API |
| Capability | Task-specific: code (Codex), vision (GPT-4V), reasoning (Claude) |

**Failover Strategy:**
1. Primary model → fallback model → rules-based fallback
2. Circuit breaker pattern: after N failures, skip model for cooldown period
3. Graceful degradation: reduce output quality rather than fail completely

**Cost Optimization:**
- Model tiering: small model for classification, large model for reasoning
- Caching: cache deterministic or near-duplicate queries
- Batching: group non-urgent requests for batch API pricing
- Prompt optimization: shorter prompts = fewer tokens = lower cost

### Agent Layer

> **Reference:** The ReAct pattern is from the paper [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) (Yao et al., 2022).

Three Agent types for different scenarios (this is one common taxonomy—other frameworks may use different classifications):

| Agent Type | Capability | Use Case |
|------------|------------|----------|
| **BaseAgent** | Fixed workflow, no dynamic planning | Simple chatbots, AI Workflows |
| **ReActAgent** | Thought→Action→Observation loop | Rational tasks with tool use |
| **PlanAgent** | Global planning + ReAct execution | Complex tasks requiring strategy |

> **Note:** "PlanAgent" is a common architectural pattern but not a standardized term—different frameworks may name it differently.

**ReAct + Plan Combination:**
- Plan produces global strategy (use templates for quality)
- ReAct executes domain-specific reasoning
- Together they handle both strategic and tactical problems

### Intent Layer

Required only for multi-intent scenarios. Handles:
- **Parallel intents:** Multiple independent intents in one query
- **Sequential intents:** Intent B depends on Intent A result
- **Logical intents:** Intents with logical relationships

Also performs query rewriting and expansion for intent optimization.

### Session Layer

Manages conversation state and user context. Feeds data into Context Engineering.

**Responsibilities:**
- Session lifecycle: creation, timeout, cleanup
- State persistence: save/load conversation state across sessions
- User context binding: associate session with user profile, preferences

**What it does NOT do:**
- Memory management strategies → see Context Engineering
- RAG retrieval → see Capability Layer
- Model selection → see Foundation Layer

Session Layer provides the **data**; Context Engineering decides **how to use it**.

## Multi-Agent Patterns

Three coordination patterns:

| Pattern | Decision Point | Use Case |
|---------|----------------|----------|
| **Centralized** | Single coordinator agent | Clear task decomposition |
| **Decentralized** | Peer-to-peer negotiation | Collaborative problem-solving |
| **Hybrid** | Mixed coordination | Complex domains with sub-domains |

**MOE (Mixture of Experts) Pattern:**
- Each domain has specialized Agent (product, order, inventory, etc.)
- Central Agent performs intent recognition and task distribution
- Domain Agents execute with ReAct + Plan capabilities

## AI Friendly API Design

### Tool Atomicity
Split interfaces into atomic tools matching Agent reasoning patterns:
```
❌ getProductWithInventoryAndPricing(id)
✅ getProduct(id)
✅ getInventory(productId)
✅ getPricing(productId)
```

### Parameter Design
Human-readable names, flat KV structure, core parameters only:
```json
// ❌ Bad: Nested, complex
{"product": {"identifiers": {"sku_id": "123"}, "filters": {"status": "active"}}}

// ✅ Good: Flat, clear
{"sku_id": "123", "status": "active"}
```

### Error Handling
- **Expected errors:** Short descriptions for Agent reasoning
- **Unexpected errors:** Stack traces for error diagnosis

## Context Engineering

### Beyond Prompt Engineering

Context Engineering selects, organizes, and compresses information optimally within context windows. It is more impactful than model selection for production systems.

### Core Techniques

#### 1. Historical Case Library (Illustrative: ~8% accuracy improvement)

*Based on production AI Review system results. See [Real-World Impact](#real-world-impact) section.

Store past successful cases with their decision reasoning. Retrieve similar cases via vector search to guide current decisions.

- **When to use:** Tasks with recurring patterns (code review, customer support, troubleshooting)
- **Implementation:** Embed past cases → vector store → similarity search → inject top-K into context
- **Key:** Include both the case AND the reasoning, not just the result

#### 2. Hybrid Decision-Making (Illustrative: ~10%+ accuracy improvement)

*Based on production CogentAI system results. See [Real-World Impact](#real-world-impact) section.

Multiple models vote with confidence scores. Use when single-model accuracy is insufficient.

- **When to use:** High-stakes decisions, compliance checks, medical/financial analysis
- **Implementation:** Run 2-3 models in parallel → collect outputs → weighted voting based on domain confidence
- **Key:** Assign domain-specific confidence weights, not uniform voting

#### 3. Memory Management

| Type | Scope | Implementation | Use Case |
|------|-------|---------------|----------|
| Long-term memory | Cross-session | Persistent store (DB/vector) | User preferences, history |
| Short-term memory | Current session | In-context window | Current task context |
| Working memory | Current step | Scratchpad pattern | Intermediate reasoning |

- **Summarization:** Periodically compress long-term memory to avoid context overflow
- **Relevance scoring:** Only inject relevant memories, not everything

#### 4. Advanced RAG

| Technique | When to Use | Trade-off |
|-----------|------------|-----------|
| Standard RAG | Simple Q&A over documents | Low complexity, moderate accuracy |
| GraphRAG | Entity relationships, knowledge graphs | Higher complexity, better associative retrieval |
| Dynamic context pruning | Long conversations, large knowledge bases | Reduces noise, may lose relevant context |
| Hybrid retrieval (dense + sparse) | Mixed structured/unstructured data | Best recall, more infrastructure |

### Decision Guide

```
Is the task pattern-recurring?
├─ Yes → Build historical case library
└─ No → Is single-model accuracy sufficient?
    ├─ Yes → Standard RAG + memory management
    └─ No → Hybrid decision-making
        └─ Complex entity relationships?
            ├─ Yes → GraphRAG
            └─ No → Standard RAG + dynamic pruning
```

## Quick Reference: Decision Framework

### Decision Questions

| # | Question | If Yes | If No |
|---|----------|--------|-------|
| 1 | Is the task deterministic? | Traditional architecture (MVC/DDD) | → Q2 |
| 2 | Does it need language understanding? | → Q3 | Rules or traditional ML |
| 3 | Are there hard performance constraints (<100ms)? | Hybrid: AI offline + rules online, caching | → Q4 |
| 4 | Are there strict cost constraints? | Hybrid: AI + rules, small models, caching | → Q5 |
| 5 | Does it need dynamic tool selection? | → Q6 | Single LLM call or AI Workflow |
| 6 | Does it need multi-step reasoning? | PlanAgent + ReActAgent | ReActAgent |
| 7 | Multiple domains? | Multi-Agent (MOE pattern) | Single Agent |

### Decision Criteria

**Q1: Is the task deterministic?**
- Yes: Input→output mapping is fixed, no natural language understanding needed
- No: Task requires understanding intent, context, or unstructured data
- Examples:
  - Deterministic: Form validation, data transformation, CRUD operations
  - Non-deterministic: Customer support, content generation, recommendation

**Q2: Does it need language understanding?**
- Yes: Task involves natural language input/output, requires semantic understanding
- No: Task can be solved with rules, traditional ML, or simple pattern matching
- Examples:
  - Needs understanding: Chatbots, content analysis, query interpretation
  - Rules/ML: Fraud detection (features), image classification (CNN)

**Q3: Are there hard performance constraints?**
- Yes: Response time <100ms, real-time requirements, SLA commitments
- No: Batch processing, async operations, acceptable delays
- Hybrid approach: AI for offline training/analysis, rules for online decisions

**Q4: Are there strict cost constraints?**
- Yes: Limited budget, high volume, cost-sensitive application
- No: Budget allows for AI infrastructure, low volume
- Hybrid approach: AI for high-value decisions, rules for routine tasks

**Q5: Does it need dynamic tool selection?**
- Yes: System must choose tools/APIs based on context at runtime
- No: Fixed workflow, predetermined tool sequence
- Examples:
  - Dynamic: Research agent, adaptive troubleshooting
  - Fixed: Data pipeline, report generation

**Q6: Does it need multi-step reasoning?**
- Yes: Task requires planning, decomposition, backtracking
- No: Single-step execution, direct action
- Examples:
  - Multi-step: Complex research, multi-domain problem solving
  - Single-step: Simple Q&A, data lookup

**Q7: Multiple domains?**
- Yes: System handles multiple specialized areas with different knowledge/tools
- No: Single domain, focused expertise
- Examples:
  - Multi-domain: Enterprise support (product, billing, technical)
  - Single-domain: Specialized medical diagnosis

**Constraint Strategy Table:**

| Constraint | Strategy | Example | Priority |
|-----------|----------|---------|----------|
| Latency <100ms | AI offline training + rules online, caching | Real-time recommendation | Hard |
| High volume (10M+/day) | Caching + small models + rules fallback | API gateway | Soft |
| Limited budget | Hybrid AI+rules, model tiering | Internal tools | Soft |
| Data privacy | On-premise models, data anonymization | Medical/financial | Hard |
| Performance + Cost | Small models + caching, reduce AI scope to high-ROI tasks | Budget real-time system | Hard > Soft |
| Performance + Privacy | On-premise small models + caching, accept lower accuracy | Hospital system | Hard > Hard |
| Cost + Privacy | On-premise small models, rules for low-value decisions | Internal medical tool | Soft < Hard |

**Rule:** Hard constraints (latency, privacy) beat soft constraints (cost, accuracy). When constraints conflict, optimize for the hard constraint first.

## Common Mistakes

| Mistake | Why Wrong | Fix |
|---------|-----------|-----|
| Using Multi-Agent for simple FAQ | Over-engineering, adds latency/cost | Use single Agent with knowledge base |
| Complex nested API for Agent tools | Agents can't parse deep structures | Atomic tools with flat parameters |
| Skipping Intent Layer for multi-intent queries | Agent can't distinguish user goals | Add Intent Layer with query rewriting |
| Using ReAct for deterministic tasks | Unnecessary reasoning overhead | Use BaseAgent or workflow |
| Ignoring Context Engineering | Poor model performance | Build case libraries, hybrid decisions |
| Ignoring performance constraints | AI inference latency breaks SLA | Use hybrid architecture, see Constraint Strategy Table |
| Ignoring cost constraints | Unsustainable AI spend at scale | Model tiering, caching, rules fallback |
| "To use AI" as architecture goal | No business value | Define specific problems AI solves |

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "Multi-Agent is always better" | Coordination overhead isn't justified for simple tasks |
| "ReAct can handle everything" | Deterministic tasks don't need dynamic reasoning |
| "AI Friendly API is too much work" | Atomic tools are easier to maintain and test |
| "Context Engineering is optional" | Memory and context are more important than model choice |
| "We need AI for everything" | Traditional architecture handles deterministic logic better |
| "Paradigm shifts are just theory" | They explain WHY the patterns work—skip them at your peril |
| "Context Engineering is just RAG" | Includes memory, hybrid decisions, case libraries beyond RAG |
| "Intent Layer is optional" | Required for multi-intent scenarios—Agent alone can't distinguish |
| "This only applies to LLM systems" | Principles apply to any AI system with uncertainty |

## Red Flags - STOP and Reconsider

- Adding AI without clear problem definition
- Using Agents where simple LLM calls suffice
- Complex nested APIs for Agent consumption
- Skipping evaluation and observability
- Ignoring the "when NOT to use" guidelines

## Real-World Impact

From production systems:
- **AI Review:** Illustrative results: 95.7% accuracy, 99.1% recall, 80%+ efficiency improvement
- **AI Q&A (CogentAI):** Illustrative results: 98%+ problem-solving accuracy, 80%+ efficiency improvement
- **Key success factors:** Proper architecture selection, Context Engineering, continuous evaluation

> Note: These metrics are illustrative examples from the source article, not independently verified measurements. Results will vary based on implementation quality, data, and domain.

## References

- [Article Summary](references/article-summary.md) (English)
- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) (Yao et al., 2022)
- [Skill Authoring Guide](https://github.com/GanJiaKouN16/Function-Point-Skill/blob/main/skill-authoring-guide.md)
