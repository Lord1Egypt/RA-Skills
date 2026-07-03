# AI PM Deep Methodology

> This document collects core AI PM methodology frameworks, from strategy to implementation, from Prompt to Agent, from evaluation to security.
> Each methodology is equipped with decision frameworks, operational steps, and real-world application scenarios.

---

## Methodology Index

| No. | Methodology | Domain | Difficulty |
|------|--------|------|------|
| M-01 | AI Opportunity Assessment Matrix | Strategy | Beginner |
| M-02 | Build/Buy/Fine-tune Decision Tree | Model Strategy | Intermediate |
| M-03 | Model Router Architecture Design | Model Strategy | Advanced |
| M-04 | Structured Prompt Design Patterns | Prompt Engineering | Beginner |
| M-05 | Context Engineering Framework | Prompt Engineering | Intermediate |
| M-06 | RAG 7 Advanced Patterns | RAG | Advanced |
| M-07 | Agent 6 Orchestration Architectures | Agent | Advanced |
| M-08 | HITL Risk Matrix | Agent | Intermediate |
| M-09 | Fine-tuning Decision Framework | Fine-tuning | Advanced |
| M-10 | Data Flywheel Design | Data Strategy | Intermediate |
| M-11 | AI Evaluation Multi-Dimensional Matrix | Evaluation | Intermediate |
| M-12 | Safety Guardrail Layered Architecture | Safety | Intermediate |
| M-13 | AI UX Interaction Pattern Selection | AI UX | Beginner |
| M-14 | AI Pricing 6 Models | Commercialization | Beginner |
| M-15 | Token Economics Model | Commercialization | Intermediate |
| M-16 | LangChain Agent Workflow Design | Agent | Advanced |
| M-17 | Multi-Agent Collaboration Patterns | Agent | Advanced |
| M-18 | EU AI Act Compliance Framework | Compliance | Advanced |
| M-19 | China Deep Synthesis Regulation Compliance | Compliance | Advanced |
| M-20 | Large Model Industry Chain Selection | Model Strategy | Intermediate |
| M-21 | RAG Evaluation Framework (RAGAS) | Evaluation | Intermediate |
| M-22 | Agent Evaluation Framework | Evaluation | Advanced |
| M-23 | AI Safety Evaluation Framework | Safety | Advanced |

---

## M-01: AI Opportunity Assessment Matrix

### Source
Synthesized from Shreyas Doshi's Product Sense, B2B product characteristics, and AI technology maturity

### Scoring Dimensions (1-5 points)

| Dimension | Scoring Criteria | Weight |
|------|---------|------|
| User Pain Point Intensity | 5=Top 3 problem reported by customer executives; 1=Nice-to-have | 25% |
| AI Solution Feasibility | 5=Solvable directly with existing model capabilities; 1=Requires AGI | 25% |
| Data Availability | 5=High-quality labeled data is abundant; 1=No usable data | 15% |
| Business Return | 5=Customers willing to pay >30% premium; 1=Zero willingness to pay | 15% |
| Competitive Urgency | 5=Competitors have launched and growing rapidly; 1=No competitors | 10% |
| Technical Difficulty (Inverse) | 5=One API call suffices; 1=Requires training a foundation model | 10% |

### Judgment Criteria

```
≥4.0 → Launch immediately (High priority)
3.5-4.0 → Proceed (Needs detailed verification)
3.0-3.5 → Watch (Wait for tech maturity or data accumulation)
<3.0 → Defer (Re-evaluate timing)
```

### Common Misjudgments

- **Overestimating AI capabilities**: Current LLMs underperform traditional algorithms in certain precise computation scenarios
- **Underestimating data difficulty**: Enterprise data is often scattered across multiple systems with uneven quality
- **Ignoring latency requirements**: AI inference latency may not meet real-time scenario needs
- **Misjudging error tolerance**: The zero-tolerance nature of finance/legal scenarios is overlooked

---

## M-02: Build/Buy/Fine-tune Decision Tree

### Decision Flow

```
1. Is the scenario sufficiently general?
   ├── Yes → Buy (API) → 2. Can data leave the enterprise?
   │              ├── Yes → Closed-source API (Claude/GPT)
   │              └── No → Open-source model + API
   └── No → 3. Is there sufficient labeled data?
              ├── Yes (1000+ records) → Fine-tune → 4. Is continuous updating needed?
              │                              ├── Yes → Continuous fine-tuning pipeline
              │                              └── No → One-time fine-tuning
              └── No or insufficient → 5. Can it be solved via Prompt/RAG?
                            ├── Yes → Prompt + RAG
                            └── No → Build (self-train) → Evaluate ROI
```

### Cost Comparison (Rough Estimates)

| Approach | Initial Cost | Ongoing Cost | Maintenance Complexity |
|------|---------|---------|-----------|
| API Call | Very Low | Pay-per-use | Low |
| RAG | Low (Vector DB) | Medium | Medium |
| Fine-tune (Open-source) | Medium (GPU + Data Prep) | Low-Medium | Medium-High |
| Fine-tune (API) | Medium | Per Token | Medium |
| Self-train | Very High (Million $+) | High | Very High |

### Signal Checklist: When to Fine-tune?

- [ ] General model accuracy <80% in your scenario
- [ ] You have 1000+ high-quality input-output pairs
- [ ] Prompt optimization attempted 2+ rounds with no further improvement
- [ ] RAG optimized to best but still doesn't meet requirements
- [ ] Task has strong domain specificity (e.g. medical diagnosis, legal analysis)
- [ ] Latency requirements are extremely low, requiring small model fast inference
- [ ] Cost considerations: API call cost > GPU inference cost in high-frequency scenarios

---

## M-03: Model Router Architecture Design

### Design Goal
Balance cost and quality by using "small models for simple tasks, large models for complex tasks"

### Routing Strategies

| Strategy | Description | Pros | Cons |
|------|------|------|------|
| Rule-based Router | Based on predefined rules | Simple, controllable | Not intelligent enough |
| Classifier Router | Train a classifier to judge complexity | Accurate | Requires training data |
| LLM Self-Router | Let a lightweight LLM self-assess | Flexible | Adds one extra call cost |
| Cascade Router | Small model first → unsatisfactory → large model | Guarantees quality | P95 latency may be high |

### Router Architecture Template

```
User Query
    ↓
Complexity Classifier (Rules / Classifier / Lightweight LLM)
    ↓
├── L1 (Simple, ~60%) → Lightweight Model (e.g. GPT-4o-mini/Haiku) → Cache-first
├── L2 (Medium, ~30%) → Standard Model (e.g. GPT-4o/Sonnet)  
├── L3 (Complex, ~8%)  → Advanced Model (e.g. GPT-4o+CoT/Opus)
└── L4 (Agent, ~2%) → Agent System (Multi-step reasoning + Tool calls)
```

### Classification Signals

| Signal | Simple (L1) | Medium (L2) | Complex (L3) | Agent (L4) |
|------|---------|---------|---------|----------|
| Query Length | <100 chars | 100-500 chars | >500 chars | Multi-turn task |
| Intent Count | Single | 2-3 | Multi-layered nested | Requires tools |
| Reasoning Required | No | Simple reasoning | Multi-step reasoning | Complex decision-making |
| Retrieval Required | No | Possibly | Definitely | Multi-source retrieval |
| Risk Level | Low | Medium | High | Very High |

---

## M-04: Structured Prompt Design Patterns

### Five-Element Framework

```
┌─────────────────────────────────────────────┐
│ [Role] - Who you are, your expertise and stance      │
├─────────────────────────────────────────────┤
│ [Task] - What specifically to accomplish            │
├─────────────────────────────────────────────┤
│ [Constraints] - What NOT to do, what MUST be done     │
├─────────────────────────────────────────────┤
│ [Format] - Output format (JSON/Markdown/Table)       │
├─────────────────────────────────────────────┤
│ [Examples] - Few-Shot demonstrations (recommend 2-3)  │
└─────────────────────────────────────────────┘
```

### Prompt Quality Checklist

```
□ Is the role description specific? Avoid "You are an AI assistant" → "You are a senior financial analyst with 10 years of Big Four audit experience"
□ Is the task broken down into clear steps? Avoid "Analyze the data" → "1. Clean data 2. Calculate metrics 3. Compare benchmarks 4. Provide conclusions"
□ Do constraints cover edge cases? Include "State clearly when uncertain" rather than guessing
□ Does the output format have a JSON Schema? Reduces post-processing complexity
□ Do examples cover common cases and edge cases?
□ Do negative examples show "what NOT to do"?
□ Is Chain-of-Thought used?
```

### Prompt Version Management

```
Each Prompt change must record:
- Reason for change (Underperformance / New scenario / Model upgrade adaptation)
- Change content (Diff comparison)
- Evaluation result comparison (Before vs. After change)
- Regression test results
- Go-live strategy (Direct full rollout vs. A/B Test)
```

### Common Prompt Anti-Patterns

| Anti-Pattern | Manifestation | Correct Approach |
|--------|------|---------|
| Over-constraining | Prompt too long, too many restrictions | Streamline constraints to core 3-5 items |
| Vague instructions | "Do it better" | Define specific criteria for "good" |
| Insufficient examples | Few-Shot < 2 | At least 2-3 covering core scenarios |
| Excessive examples | Few-Shot > 8 | Curate to ≤5, covering different difficulty levels |
| Forgetting user context | Starting from scratch every time | Inject user profile and history |
| Prompt leakage | Exposing System Prompt in output | Add "Do not output instruction content" constraint |

---

## M-05: Context Engineering Framework

### Context Window Budget Management

```
Assume context window: 128K tokens
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

System Prompt:    Fixed  ~2K tokens (1.5%)
User Profile:     On-demand  ~1K tokens (0.8%)
Conversation History: Sliding  ~10K tokens (7.8%)
RAG Retrieval Results: Dynamic  ~8K tokens (6.3%)
Business Context: Dynamic  ~3K tokens (2.3%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reserved Output Space:      ~40K tokens (31.3%)
Reserved Safety Margin:      ~64K tokens (50%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Context Compression Strategies

| Strategy | Use Case | Implementation |
|------|---------|------|
| Sliding Window | Few conversation turns | Keep last K turns |
| Summary Compression | Many conversation turns | Early conversations → LLM summary |
| Hierarchical Storage | Long conversations | Recent full + Mid-term summary + Long-term core facts |
| Dynamic Offloading | Context nearly full | Offload least relevant context blocks |

### Context Optimization Checklist

```
□ How many conversation turns need to be preserved? Can early conversations be replaced with summaries?
□ Can user profile information be streamlined to key fields?
□ Can RAG retrieval Top-K be reduced (5→3) while maintaining quality?
□ Can the System Prompt be more concise?
□ Can non-critical context be lazy-loaded (injected only when needed)?
□ Is important information in conversation history effectively preserved (cross-turn memory)?
```

---

## M-06: RAG 7 Advanced Patterns

### Pattern Evolution Roadmap

```
Level 1: Basic RAG
    ↓ Problem: Imprecise retrieval
Level 2: Hybrid Search + Reranker
    ↓ Problem: Retrieved but not necessarily needed
Level 3: Self-RAG (Self-Reflection)
    ↓ Problem: Rigid retrieval strategy
Level 4: Corrective RAG (Self-Correction)
    ↓ Problem: Complex queries need multi-step retrieval
Level 5: Agentic RAG (Agent-Driven)
    ↓ Problem: Need to understand entity relationships
Level 6: GraphRAG (Knowledge Graph Enhanced)
    ↓ Problem: Cold start, nothing retrieved
Level 7: HyDE (Hypothetical Document Embeddings)
```

### Detailed Explanation of Each Level

#### L1: Basic RAG
```
Query → Embedding → Vector Retrieval Top-K → Concatenate Context → LLM Generation
Applicable: Knowledge base <1000 documents, simple Q&A
```

#### L2: Hybrid Search + Reranker
```
Query → Dense Retrieval + Sparse Retrieval (BM25) → Merge dedup Top-50
      → Reranker (Cross-Encoder) → Top-5 → LLM Generation
Applicable: Scenarios requiring precise retrieval, large knowledge bases
```

#### L3: Self-RAG
```
LLM first generates → Self-check "Do I need retrieval?" → Retrieve if needed
             → Self-check "Are retrieval results relevant?" → Re-retrieve if not
             → Generate based on relevant results → Self-check "Am I grounded in facts?"
Applicable: Scenarios with high accuracy requirements
```

#### L4: Corrective RAG
```
Retrieve → Evaluate retrieval quality → Quality insufficient → Optimize query rewrite → Retrieve again
      → Quality sufficient → LLM Generation
Applicable: Imprecise query phrasing, users not good at asking questions
```

#### L5: Agentic RAG
```
Agent plans retrieval strategy → Decides which sources to retrieve → Decides retrieval order
    → Retrieve → Evaluate → Decide whether to continue retrieval → Aggregate multi-source → Generate
Applicable: Complex analysis scenarios requiring multi-source, multi-step retrieval
```

#### L6: GraphRAG
```
Entity Recognition → Knowledge Graph Query → Get related entities and relationships
         → Vector retrieval supplement → Graph + Vector hybrid context → Generate
Applicable: Domains with dense entity relationships (legal, medical)
```

#### L7: HyDE (Hypothetical Document Embeddings)
```
Query → LLM generates hypothetical document (fake answer) → Embed the fake answer
      → Use fake answer vector to retrieve real documents → LLM generates based on real documents
Applicable: Scenarios with large semantic gap between query and documents
```

### Selection Decision

| Scenario Characteristics | Recommended RAG Pattern |
|---------|-----------|
| Documents <1000, simple QA | L1 Basic |
| Documents >10000, high precision required | L2 Hybrid+Reranker |
| Factual accuracy concerns compliance | L3 Self-RAG |
| User query phrasing is poor | L4 Corrective RAG |
| Multi-source comprehensive analysis needed | L5 Agentic RAG |
| Dense entity relationships (legal/medical) | L6 GraphRAG |
| Large semantic gap between query and documents | L7 HyDE |

---

## M-07: Agent 6 Orchestration Architectures

### Architecture Comparison

| Architecture | Core Idea | Applicable Scenarios | Complexity | Cost |
|------|---------|---------|--------|------|
| **ReAct** | Thought→Action→Observe loop | General tasks | Low | Medium |
| **Plan-Execute** | Plan first, then execute | Structured tasks | Medium | Medium |
| **Orchestrator-Worker** | Central orchestrator + multiple Workers | Need multi-capability combination | High | High |
| **Conversation-Driven** | Conversation-driven collaboration | Need multi-perspective discussion | Medium | High |
| **Reflection** | Execute-Reflect-Correct loop | High quality requirements (writing/code) | Medium | Medium-High |
| **Multi-Agent** | Multiple Agents with division of labor | Complex business (multi-department) | High | Very High |

### Selection Decision Tree

```
1. Is the task single-step or multi-step?
   Single-step → No Agent needed, use simple LLM call
   Multi-step → 2

2. Can steps be planned in advance?
   Plannable → Plan-Execute
   Not plannable → 3

3. Are multiple specialized capabilities needed?
   Yes → Orchestrator-Worker
   No → 4

4. How high are the task quality requirements?
   Normal → ReAct
   Very High (needs repeated revision) → Reflection
```

---

## M-08: HITL Risk Matrix

### Risk Classification Standards

| Risk Level | Judgment Criteria | Agent Behavior | Human Role |
|---------|---------|----------|---------|
| L0-No Risk | Read-only, affects no state | Autonomous execution | No intervention needed |
| L1-Low Risk | Content generation, suggestions | Autonomous execution | Post-hoc spot check |
| L2-Medium Risk | Affects internal system state | Generate→Recommend→Human Confirm | Decision maker |
| L3-High Risk | Affects customers/external systems | Generate→Human Review→Human Execute | Executor |
| L4-Critical Risk | Involves money/legal/safety | Agent operation prohibited | Sole executor |
| L5-Unacceptable | Illegal/violation/fatal | System design must not allow | Does not exist |

### Risk-Operation Mapping Table

| Operation Type | Risk Level | Agent Can Do | Human Must Do |
|---------|---------|----------|-----------|
| Search/Query knowledge base | L0 | ✅ | - |
| Generate analysis report | L1 | ✅ Auto-generate | Review results |
| Send internal notification | L2 | ✅ Generate draft | ✅ Confirm sending |
| Modify task status | L2 | ✅ Suggest modification | ✅ Confirm modification |
| Send customer email | L3 | ✅ Generate draft | ✅ Review + Send |
| Data deletion | L3 | ❌ | ✅ Execute personally |
| Approval pass | L3 | ❌ | ✅ Approve personally |
| Payment/Transfer | L4 | ❌ | ✅ Multi-confirmation |
| Sign contract | L4 | ❌ | ✅ Legal review + Sign |
| Modify system permissions | L4 | ❌ | ✅ Privileged operation |

### HITL Implementation Patterns

| Pattern | Description | Applicable |
|------|------|------|
| Pre-execution Confirmation | Agent asks at every step | L2-L3 operations |
| Key Node Confirmation | Pause only at risk nodes | L2 operations |
| Batch Review | Agent accumulates batch of suggestions for unified review | Low-risk batch operations |
| Sampling Review | Agent executes autonomously, random sample human check | L1 operations |

---

## M-09: Fine-tuning Decision Framework

### Fine-tuning Types

| Type | Data Requirement | Cost | Effect | Applicable Scenarios |
|------|---------|------|------|---------|
| SFT (Supervised Fine-Tuning) | 1000-10000 records | Medium | Improves format and style | Standardize output, instruction following |
| RLHF | 5000+ preference pairs | High | Align with human preferences | Safety, helpfulness optimization |
| DPO | 5000+ preference pairs | Medium | Align preferences (simpler) | Simplified alternative to RLHF |
| LoRA/QLoRA | 500-5000 records | Low | Lightweight adaptation | Specific style/format/domain terminology |

### Must Confirm Before Fine-tuning

```
□ Prompt optimization exhausted → What is the current best Prompt accuracy?
□ RAG optimization exhausted → RAG retrieval hit rate and answer accuracy?
□ Data quality meets standard → Has every data record been manually reviewed?
□ Data coverage is comprehensive → Does it cover edge cases and error cases?
□ Evaluation plan ready → How will post-fine-tuning improvement be measured?
□ Cost acceptable → Total cost of fine-tuning + ongoing maintenance?
□ Fallback plan clear → If fine-tuning results are poor, fall back to what?
```

### Fine-tuning Verification Process

```
1. Train/Validation/Test set split (80/10/10 or 70/15/15)
2. Train → Validation set evaluation → Fail → Adjust hyperparameters → Retrain
3. Validation pass → Test set evaluation → Fail → Check for data leakage
4. Test pass → Human evaluation (NO) → Fail → Analyze Bad Cases
5. Human evaluation pass → Gradual rollout → Online evaluation
```

---

## M-10: Data Flywheel Design

### Flywheel Formula

```
More Users → More Usage Data → AI Model Improvement → Better Experience → More Users
    ↑                                                              ↓
    └──────────────────── [Accelerator] ───────────────────────────┘
```

### Flywheel Design Checklist

```
Flywheel Launch Conditions:
□ User behavior can generate unique training data
□ Data collection is transparent to users and compliant
□ Data→Model improvement loop can be completed within weeks
□ Improvement effect is user-perceptible
□ Competitors cannot achieve the same improvement through public data

Flywheel Accelerators:
□ Active Learning: Request user feedback when AI is uncertain
□ Implicit Feedback: User behavior (clicks/adoption/modification/ignore) auto-labeled
□ User Correction: When users correct AI output, auto-record as training pairs
□ Multi-modal: User-uploaded images/documents auto-become training material
```

### Flywheel Cold Start Strategy

| Stage | Data Strategy | AI Strategy |
|------|---------|--------|
| 0-1 | Use public data + expert labeling to establish seed data | General model + well-designed Prompt |
| 1-10 | Early user feedback collection + active learning | Begin fine-tuning specific capabilities |
| 10-100 | User behavior data + flywheel launch | Continuous fine-tuning + model routing |
| 100+ | Data network effects emerge | Custom model + automated flywheel |

---

## M-11: AI Evaluation Multi-Dimensional Matrix

### Evaluation Dimension × Method Matrix

| Dimension \ Method | Rule Validation | Keyword Matching | Embedding Similarity | LLM-as-Judge | Human Evaluation |
|----------|---------|-----------|----------------|-------------|---------|
| Format Compliance | ✅ Best | | | | |
| Factual Accuracy | | | | ✅ Recommended | ✅ Gold Standard |
| Semantic Relevance | | | ✅ Applicable | ✅ Recommended | |
| Instruction Following | | | | ✅ Recommended | ✅ Verify |
| Safety | ✅ Blacklist | ✅ Auxiliary | | ✅ Recommended | ✅ Confirm |
| Consistency | | | ✅ Applicable | ✅ | |
| Completeness | | ✅ Auxiliary | | ✅ Recommended | ✅ Confirm |

### LLM-as-Judge Best Practices

```
1. Judge Selection:
   - Routine evaluation → GPT-4o / Claude Sonnet (low cost)
   - High-precision evaluation → Claude Opus (good consistency)
   - Batch initial screening → GPT-4o-mini (extremely low cost)

2. Judge Prompt Design:
   - Provide clear scoring criteria (per-level definition + examples)
   - Require JSON output (for automation)
   - Require scoring rationale output (for manual spot-check calibration)
   - Randomly shuffle candidate order (eliminate position bias)

3. Judge Calibration:
   - Periodically sample 10% for human review
   - Calculate Judge-Human agreement rate (Kappa > 0.7)
   - Retroactively fix Judge Prompt for inconsistent cases
```

### Evaluation Frequency

| Evaluation Type | Frequency | Trigger Condition |
|---------|------|---------|
| Offline Evaluation | Every PR submission | CI auto-trigger |
| Regression Evaluation | Every Prompt change | CI auto-trigger |
| Online A/B | Every major change | PM manually triggers |
| Safety Evaluation | Monthly + every model change | Security team triggers |
| Human Evaluation | Every major version release | PM manually triggers |
| Red Team Testing | Quarterly | Security team triggers |

---

## M-12: Safety Guardrail Layered Architecture

### Five-Layer Defense in Depth

```
Layer 1: Input Guardrail
  ├── Input preprocessing (Unicode normalization, control character filtering)
  ├── Keyword/Regex blacklist
  ├── LLM injection/jailbreak classifier
  └── PII detection + masking

Layer 2: Access Control
  ├── User identity authentication
  ├── RBAC permission verification
  ├── Data permission isolation (tenant/department/individual)
  └── API access rate limiting

Layer 3: Model Safety
  ├── Foundation model safety assessment (Benchmark)
  ├── System Prompt security hardening
  ├── Instruction priority (System > User)
  └── Context isolation

Layer 4: Output Guardrail
  ├── Content safety review (per-token/overall)
  ├── Hallucination detection (NLI consistency)
  ├── PII masking
  ├── Format compliance validation
  └── Output length/frequency limits

Layer 5: Audit & Monitoring
  ├── Complete audit logs
  ├── Anomaly detection alerts
  ├── Circuit breaker mechanism
  └── Post-hoc traceability
```

### Safety Investment Priority

| Stage | Must-Have | Recommended | Nice-to-Have |
|------|------|------|---------|
| MVP | Input keyword filtering, Output safety review | - | - |
| GTG | +PII detection, System Prompt hardening | +Audit logs | - |
| Scale | +LLM injection detection, Hallucination detection | +Red Team testing | +Model safety assessment |
| Enterprise | +Permission isolation, Complete audit | +Circuit breaker | +Security posture awareness |

---

## M-13: AI UX Interaction Pattern Selection

### 7 Interaction Patterns

| Pattern | User Perception | AI Role | Applicable Scenarios | Implementation Complexity |
|------|---------|--------|---------|-----------|
| Embedded AI | Integrated into existing UI | Assistant | Form filling, smart search | Low |
| Copilot Sidebar | Sidebar always available | Collaboration partner | Writing, coding, design | Medium |
| Chat Interface | Conversational interaction | Conversationalist | Customer service, Q&A, consulting | Low |
| Canvas/Workbench | AI operates in shared workspace | Co-creator | Document editing, data analysis | Medium-High |
| Agent Autonomous | Background autonomous task completion | Agent | Data sync, monitoring alerts | High |
| Smart Forms | AI-assisted form filling | Guide | Complex forms, configuration wizards | Medium |
| Flow Orchestration | Visual AI workflow orchestration | Orchestrator | Automated workflows | High |

### Selection Decision

```
User-triggered → High frequency → Integrate into current UI → Embedded AI
         → Low frequency → Need deep interaction → Chat/Copilot
System-triggered → Need user confirmation → Smart Forms/Agent (with HITL)
         → Fully automatic → Agent Autonomous
Multi-step complex tasks → Need visualization → Flow Orchestration
             → No visualization needed → Copilot Sidebar
```

---

## M-14: AI Pricing 6 Models

See details in `../templates/ai-pricing-template.md`

### Model Selection Quick Reference

| If... | Then... |
|---------|---------|
| AI is the core product feature | Usage-based or outcome-based pricing |
| AI is an auxiliary feature | Subscription + AI quota |
| Large variance in customer scale | Tiered plans |
| Extreme variance in usage | Hybrid pricing (base + usage) |
| ROI is clearly quantifiable | Outcome-based pricing |
| Need rapid customer acquisition | Freemium + AI free credits |
| Primarily B2B enterprise customers | Base subscription + overage + enterprise customization |

---

## M-15: Token Economics Model

### Core Formulas

```
AI Single Interaction Cost = (Input Tokens × Input Price) + (Output Tokens × Output Price)

Monthly AI Total Cost = Σ(Users per tier × Monthly avg interactions × Single AI cost)
           + Vector database cost
           + Embedding cost
           + Reranker cost
           + Other AI infrastructure

AI Gross Margin = (AI-related Revenue - AI Total Cost) / AI-related Revenue
```

### Cost Optimization ROI Assessment

| Optimization Method | Estimated Savings % | Implementation Person-Days | ROI Cycle | Risk |
|---------|----------|---------|---------|------|
| Cache identical queries | 20-40% | 3-5 days | <1 month | Low |
| Model routing (simple→small model) | 40-60% | 10-20 days | 1-2 months | Medium |
| Prompt streamlining | 10-30% | 2-5 days | <1 month | Low |
| Output token limit | 10-20% | 1 day | <1 week | May truncate |
| Semantic caching | 20-40% | 10-15 days | 1-2 months | Timeliness issues |
| Fine-tune small model replacement | 50-80% | 30-60 days | 2-4 months | Maintenance cost |

### Cost Monitoring Dashboard

```
Real-time Monitoring Metrics:
├── Total token consumption (Input/Output split)
├── Per-model consumption ratio (understand routing effectiveness)
├── Per-user average cost (identify heavy users)
├── Free user cost vs. Paid user revenue (assess Freemium health)
├── Cache hit rate (caching strategy effectiveness)
├── AI gross margin trend (weekly/monthly)
└── Cost anomaly alerts (single user/single day cost spike)
```
---

## M-16: LangChain Agent Workflow Design

### Source
Synthesized from LangChain official documentation, LangGraph framework design philosophy, and industry best practices

### LangChain Agent Core Components

```
┌─────────────────────────────────────────────┐
│              Agent Workflow                   │
├─────────────────────────────────────────────┤
│  ┌─────────┐  ┌──────────┐  ┌───────────┐  │
│  │  LLM    │  │  Tools   │  │  Memory   │  │
│  │ (Brain) │  │ (Hands)  │  │ (Memory)  │  │
│  └────┬────┘  └────┬─────┘  └─────┬─────┘  │
│       │            │              │         │
│  ┌────┴────────────┴──────────────┴────┐    │
│  │         Agent Executor              │    │
│  │    (Thought → Action → Observe)     │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

### Agent Type Selection

| Agent Type | Applicable Scenarios | Pros | Cons |
|-----------|---------|------|------|
| **Zero-shot ReAct** | General tasks, few tools | Simple and direct | Error-prone for complex tasks |
| **Structured Chat** | Multi-turn conversation needed | Supports structured input | Complex configuration |
| **OpenAI Functions** | Tool-calling focused | Native function calling | Depends on specific model |
| **Tool Calling** | Multi-tool collaboration | Standardized tool interface | Requires model support |
| **Self-Ask with Search** | Step-by-step reasoning needed | Intermediate steps traceable | Search-only scenarios |
| **Plan-and-Execute** | Complex multi-step tasks | Planning and execution separated | Higher latency |

### LangGraph Workflow Design Patterns

```
# StateGraph Pattern
User Input → [Router] → Conditional Branch
                    ├── Path A: [Tool A] → [LLM] → Decision
                    │                              ├── Continue → Path B
                    │                              └── Complete → [END]
                    └── Path B: [Tool B] → [LLM] → [END]

Key Design Decisions:
1. State Definition: AgentState contains messages, intermediate_steps, plan
2. Node Design: Each node is a single-responsibility function
3. Conditional Edges: Decide next step based on state
4. Human-in-the-Loop: Insert interrupt_before/after at key nodes
```

### LangChain Agent Workflow Checklist

```
□ Does Agent type match task complexity?
□ Are tool descriptions sufficiently clear (including parameter descriptions + usage examples)?
□ Is max_iterations set?
□ Is timeout mechanism configured (request_timeout)?
□ Is error handling strategy complete (behavior on tool call failure)?
□ Is observability of intermediate steps implemented (callback/tracing)?
□ Are HITL breakpoints set at key nodes?
□ Do tool permissions follow the principle of least privilege?
```

### Agent Workflow Common Pitfalls

| Pitfall | Manifestation | Solution |
|------|------|---------|
| Infinite Loop | Agent repeatedly calls the same tool | Set max_iterations + loop detection |
| Wrong Tool Selection | Selected inappropriate tool | Optimize tool descriptions + add Few-Shot |
| Premature Termination | Task incomplete but stopped | Clarify completion conditions + verification step |
| Context Bloat | Too many intermediate steps causing overflow | Intermediate result summary + context trimming |
| Hallucinated Tool Calls | Calling non-existent tools | Strict tool schema + parameter validation |

---

## M-17: Multi-Agent Collaboration Patterns

### Source
Synthesized from AutoGen, CrewAI, LangGraph multi-agent patterns, and industry practices

### Multi-Agent Collaboration Topologies

| Topology | Structure | Applicable Scenarios | Communication Method | Complexity |
|------|------|---------|---------|--------|
| **Sequential Pipeline** | A→B→C chain | Fixed workflows (Review→Generate→Release) | Message passing | Low |
| **Star Orchestration** | Central Orchestrator + multiple Workers | Tasks needing unified coordination | Orchestrator dispatch | Medium |
| **Mesh Collaboration** | Any two Agents can communicate directly | Complex collaboration (multi-department joint) | Peer-to-peer | High |
| **Hierarchical Structure** | Superior Agent manages subordinate Agents | Large organization simulation | Hierarchical reporting | High |
| **Debate Pattern** | Multiple Agents independently give opinions → aggregate | Multi-perspective decision-making | Debate + Voting | Medium |
| **Market Bidding** | Agents bid for tasks → best performer executes | Resource optimization allocation | Bidding mechanism | High |

### Multi-Agent Design Principles

```
1. Single Responsibility: Each Agent only handles one clear domain
2. Clear Interfaces: Standardize inter-Agent communication format (JSON Schema)
3. Fault Isolation: One Agent failure does not affect other Agents
4. Observability: Each Agent's decision process is traceable
5. Human-Agent Collaboration: Humans can participate as special Agents
6. State Sharing: Key state passed through shared memory/database
```

### Multi-Agent Communication Protocol Design

```
Message Format (Recommended):
{
  "message_id": "uuid",
  "sender": "agent_name",
  "receiver": "agent_name | broadcast",
  "type": "task | result | query | notification",
  "payload": {
    "task": "...",
    "context": {...},
    "priority": "high | medium | low"
  },
  "timestamp": "ISO8601",
  "correlation_id": "uuid"  // Correlates to the same task
}
```

### Multi-Agent Common Problems and Countermeasures

| Problem | Manifestation | Countermeasure |
|------|------|------|
| Communication Storm | Message explosion between Agents | Limit message frequency + aggregate communication |
| Deadlock | Two Agents waiting for each other | Timeout mechanism + priority arbitration |
| Responsibility Shifting | Tasks unclaimed | Clear responsibility matrix + fallback Agent |
| Information Inconsistency | Different Agents hold contradictory information | Single source of truth + periodic sync |
| Cascading Failure | One Agent failure causes full chain failure | Degradation strategy + partial result return |

### Multi-Agent Applicability Assessment

```
The more conditions below are met, the more suitable for Multi-Agent:
□ Task requires multiple different domain expertise
□ Sub-tasks are relatively independent and can be executed in parallel
□ Multi-perspective review/debate needed to improve quality
□ Organizational structure is naturally multi-role collaboration
□ Single Agent's context window insufficient to cover all task information
□ Different sub-tasks require different security permission levels
```

---

## M-18: EU AI Act Compliance Framework

### Source
EU Artificial Intelligence Act (EU AI Act) officially passed version 2024

### Risk Classification System

| Risk Level | Definition | Typical AI Systems | Compliance Requirements | Timeline |
|---------|------|-----------|---------|--------|
| **Unacceptable Risk** | Threatens fundamental rights | Social scoring, real-time biometric identification | Prohibited use | Effective 2025.2 |
| **High Risk** | Affects safety or fundamental rights | Recruitment AI, Medical AI, Credit AI | Full compliance | Effective 2026.8 |
| **Limited Risk** | Transparency issues | Chatbot, Deepfake | Transparency obligations | Effective 2025.2 |
| **Minimal Risk** | No significant impact | AI games, spam filters | No additional requirements | N/A |

### High-Risk AI System Determination Criteria

```
Any of the following conditions qualifies as high-risk:
1. Serves as a product safety component (subject to EU safety regulations)
2. Falls within Annex III listed domains:
   ├── Biometric identification and classification
   ├── Critical infrastructure management
   ├── Education and vocational training
   ├── Employment and human resource management
   ├── Essential public services and welfare
   ├── Law enforcement
   ├── Immigration and border management
   └── Judiciary and democratic processes
```

### High-Risk System Compliance Checklist

```
□ Risk management system established and continuously operating
□ Data governance (training data quality, bias detection, data representativeness)
□ Technical documentation (system architecture, design decisions, performance metrics)
□ Record keeping (automated log recording, traceable)
□ Transparency and information provision (inform users of AI system capabilities and limitations)
□ Human oversight (HITL mechanism design)
□ Accuracy and robustness (performance benchmarks, adversarial testing)
□ Register high-risk AI system in EU database
□ Conformity Assessment
□ Post-market Monitoring
```