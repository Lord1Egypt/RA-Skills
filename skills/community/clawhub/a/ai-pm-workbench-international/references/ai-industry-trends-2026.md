
## 2026 AI Industry Top 10 Trends

| # | Trend | Core Description | Implications for AI PMs |
|---|------|---------|-------------|
| 1 | **Crossing the Pilot Trap** | From PoC to production, 88% adoption → only 6% high-performing | Focus on quantifiable business value |
| 2 | **Agent Workforce Moment** | AI Agents from "assistant" to "colleague" | Design human-machine collaboration workflows, not replacement |
| 3 | **Decision Trajectories** | Focus on how AI affects decision chains, not single-point outputs | Design decision traceability |
| 4 | **Efficiency Singularity** | Inference costs dropping off a cliff, unlocking new scenarios | Re-evaluate scenarios previously deemed "too expensive" |
| 5 | **Multimodal as Standard** | Text → Image → Video → 3D, multimodality becomes baseline capability | Product design considers multimodal interaction |
| 6 | **AI Security Firewall** | AI security from "nice-to-have" to "must-have" | Compliance-first, security-by-design |
| 7 | **SaaS Giants Counterattack** | Salesforce / Microsoft / Oracle going all-in on AI | Vertical scenarios are startup opportunities |
| 8 | **Google Awakens** | Gemini + DeepMind + Google ecosystem integration | Pay attention to Google AI ecosystem |
| 9 | **Productivity Paradox Ends** | AI from "potentially useful" to "actually useful" | Prove AI's ROI with data |
| 10 | **Open-Source / Closed-Source Balance** | Open-source catching up to closed-source, gap narrowing to 6-12 months | Architecture design supports model switching |

---

> Each phase follows a unified structure: **Inputs → Core Process → Methodology → Outputs → Quality Standards → PM Checklist**

---

### Phase 1: AI Strategy & Opportunity Identification

**Role: AI Strategist**

> "First ask whether AI should be used, then ask how to use AI."

#### 1.1 AI Opportunity Assessment Framework

##### Is This an AI Problem? (4-Question Judgment Method)

```
Q1: What type of intelligence does the task require?
    ├── Pattern recognition / Classification → AI strength
    ├── Content generation / Transformation → AI strength
    ├── Precise mathematical computation → AI weakness (needs tool assistance)
    ├── Deterministic business logic → Traditional software is better
    └── Requires 100% accuracy → AI not suitable (unless with HITL)

Q2: What is the error tolerance?
    ├── Zero tolerance (medical diagnosis / legal judgment) → AI assist only, human final decision
    ├── Low tolerance (financial reports / compliance) → AI + RAG + Human review
    ├── Medium tolerance (customer service / content recommendation) → AI-led + spot-check review
    └── High tolerance (creative generation / drafts) → AI autonomous

Q3: Is data / knowledge available?
    ├── Structured knowledge base available → RAG feasible
    ├── Large amount of labeled data → Fine-tuning feasible
    ├── Only a few examples → Few-shot Prompt
    └── No data at all → Use the most powerful general model + human judgment

Q4: Are users ready to accept AI?
    ├── Users willing to accept AI assistance → Proceed
    ├── Users don't trust AI → Build trust with low-risk features first
    └── Users resist AI → First build internal tools to validate value
```

##### AI Value Assessment Matrix

| Dimension | Score (1-5) | Weight | Weighted Score |
|------|----------|------|--------|
| User Pain Point Intensity | | 25% | |
| AI Solution Feasibility | | 25% | |
| Data Availability | | 15% | |
| Business Return | | 15% | |
| Competitive Urgency | | 10% | |
| Technical Implementation Difficulty (inverse) | | 10% | |

**Total Score ≥ 3.5 → High Priority; 2.5-3.5 → Medium Priority; < 2.5 → Watch / Abandon**

#### 1.2 AI Product Type Decision Tree

```
What is your AI product?
├── AI-Native (the product itself IS AI)
│   ├── Model Layer → Provide API/model services → You are an AI Builder PM
│   └── Application Layer → Standalone AI application → You are an AI Experience PM
├── AI-Enhanced (add AI features to existing product)
│   └── Embed AI into existing workflows → You are an AI Experience PM
└── AI-Infrastructure (AI infrastructure)
    └── Tools / Platforms / Middleware → You are an AI Builder PM
```

#### 1.3 AI Market Competitive Analysis Framework

**AI Competitive Analysis Special Dimensions:**

| Traditional Dimensions | AI-Specific Dimensions |
|---------|-----------|
| Feature comparison | **Model capability comparison** (What underlying model? Fine-tuned?) |
| Price comparison | **Inference cost estimation** (Cost per interaction? Who is subsidizing?) |
| User experience | **AI UX patterns** (Chat vs Copilot vs Agent vs Embedded) |
| Market share | **Data flywheel stage** (How much user interaction data is there?) || Technical Architecture | **Model Strategy** (Self-developed vs API wrapper vs Fine-tuning vs RAG) |

**AI Competitive Moat Assessment (Hamilton Helmer 7 Powers — AI-Adapted Version):**

| Power | Manifestation in AI Products | Sustainability |
|------|--------------|---------|
| **Data Network Effects** | More users → More interaction data → Better AI → More users | ⭐⭐⭐⭐⭐ |
| **Switching Costs** | Once AI learns user preferences, cost of switching to competitors | ⭐⭐⭐⭐ |
| **Economies of Scale** | Inference costs drop with scale (model optimization / volume discounts) | ⭐⭐⭐ |
| **Cornered Resources** | Proprietary training data / domain experts / regulatory licenses | ⭐⭐⭐⭐ |
| **Counter-Positioning** | AI Native challenges traditional software cost structures | ⭐⭐⭐ |
| **Brand** | Reputation for accuracy / safety record / enterprise trust | ⭐⭐⭐ |
| **Process Power** | Accumulated Prompt Engineering / evaluation systems / safety experience | ⭐⭐ |

#### 1.4 AI Product Strategy Framework

**Wedge Strategy (recommended by a16z/O'Reilly):**

```
Traditional Path: Build platform → Find scenarios → Acquire users → Collect data
AI-Era Path: Find a pain point → AI solves it brilliantly → Earn trust → Capture proprietary data → Expand

Core Principles:
1. Start with one pain point for one "hero user"
2. Go narrow and deep, not broad and shallow
3. Simple AI tools are more trustworthy than complex Agents (let users trust AI's basic capabilities first)
4. Data is the moat, not the model (models will commoditize, proprietary data won't)
5. Don't compete with OpenAI/Anthropic at the model layer — differentiate at the application layer
```

**DHM Model (Gibson Biddle) — AI-Adapted Version:**

```
D - Delightful: Does the AI feature make users say "wow"?
H - Hard-to-copy: How long would it take competitors to replicate? (Data flywheel > Model selection)
M - Margin-enhancing: Is the inference cost structure healthy?

Scoring: 1-10 per dimension, the higher the product the better
Ideal: D>7 H>7 M>7 (e.g., Claude's Artifacts, Cursor's Tab completion)
Trap: High D, low H, low M → quickly copied by big players
```

#### Deliverables

1. **AI Opportunity Assessment Report** (including AI feasibility score + value assessment matrix)
2. **AI Competitive Analysis Report** (including model strategy reverse-engineering + data flywheel assessment)
3. **AI Product Strategy One-Pager** (including wedge strategy + DHM scoring)
4. **AI Product Roadmap** (Now/Next/Later + model dependency annotations)

---

### Stage 2: Data Strategy & Infrastructure

**Role: Data Strategist**

> "The ceiling of an AI product is not model capability, but data quality and data flywheel velocity."

#### 2.1 AI Data Landscape

```
Data types needed for AI products:

├── Training Data (if fine-tuning)
│   ├── Input-output pairs (SFT)
│   ├── Preference pairs (RLHF/DPO)
│   └── Quality requirements: high accuracy, diversity, bias-free
│
├── RAG Knowledge Base Data (if using RAG)
│   ├── Documents / knowledge bases / API docs
│   ├── Requirements: chunking strategy, metadata, permission tags
│   └── Quality requirements: accurate, up-to-date, complete
│
├── Evaluation Data (mandatory)
│   ├── Golden Dataset (evaluation benchmark)
│   ├── Requirements: cover various scenarios + edge cases
│   └── Quality requirements: representative of real distribution
│
├── User Interaction Data (data flywheel fuel)
│   ├── Implicit feedback: clicks / dwell time / adoption / edits / cancellations
│   ├── Explicit feedback: thumbs up / thumbs down / ratings / NPS
│   └── Used for: improving Prompts / optimizing RAG / identifying bad cases
│
└── Safety Data (if safety guardrails are needed)
    ├── Adversarial samples / jailbreak prompts
    └── Used for: training content safety classifiers
```

#### 2.2 Data Flywheel Design

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│  More users → More interaction data → Better AI → More users  │
│      ↑                                        ↓       │
│      └── Better UX ← More accurate AI ← Better data ──┘ │
│                                                      │
└──────────────────────────────────────────────────────┘

Flywheel Design Principles:
1. Every user interaction should produce data usable for improvement
2. Implicit feedback (behavior) >> Explicit feedback (ratings)
3. Bad cases are gold mines: every failure is an improvement opportunity
4. Data labeling embedded into product workflow (not a standalone outsourcing task)
5. Flywheel startup is the hardest: the first 100 high-quality interactions are the most critical
```

#### 2.3 Data Labeling Strategy

| Labeling Method | Quality | Cost | Speed | Applicability |
|---------|------|------|------|------|
| Domain Expert Labeling | ⭐⭐⭐⭐⭐ | Highest | Slowest | Golden Dataset, healthcare/legal |
| Crowdsourcing Platforms | ⭐⭐ | Low | Fast | Large-scale simple tasks |
| LLM Labeling + Human Review | ⭐⭐⭐⭐ | Medium | Fast | Data augmentation, initial screening |
| User Implicit Labeling | ⭐⭐⭐ | Very Low | Very Fast | Continuous data collection |
| Synthetic Data | ⭐⭐⭐ | Low | Fast | Expanding data diversity |

**Labeling Quality Control:**
- Inter-Annotator Agreement (IAA) ≥ 0.8
- 10% of samples double-labeled for quality control
- Labeling guidelines + examples + regular calibration meetings

#### 2.4 Data Quality Checklist

```
□ Accuracy: Does the data contain factual errors?
□ Completeness: Does it cover all required scenarios?
□ Consistency: Are identical inputs labeled consistently?
□ Timeliness: Is the data outdated? (Especially critical for RAG knowledge bases)
□ Diversity: Does it include edge cases / multiple expression styles?
□ Unbiasedness: Is there systematic bias against specific groups/scenarios?
□ Compliance: Is the data source legal? Does it involve PII?
□ Representativeness: Does the data distribution match real user distribution?
```

#### Deliverables

1. **Data Strategy Document** (including data requirements / data sources / data flywheel design)
2. **Data Labeling Specification** (including labeling guidelines / quality standards / QC process)
3. **Data Flywheel Monitoring Metrics** (interaction volume / feedback rate / bad case rate / data coverage)

---

### Stage 3: Model Selection & Architecture Decisions

**Role: AI Architecture Decision-Maker**

> "Choosing a model isn't about comparing benchmark scores — it's about matching the constraint set of capability, cost, latency, and compliance."

#### 3.1 Model Selection Decision Tree

```
Step 1: Can data leave the enterprise?
├── Yes → Step 2
└── No → Must deploy privately
          ├── General scenarios → Open-source models (Llama/Qwen/DeepSeek) + RAG
          └── Specialized scenarios (healthcare/legal/finance) → Open-source model + Fine-tuning

Step 2: Task complexity?
├── Simple (classification/extraction/basic summarization) → Small model (Haiku/Flash/fine-tuned 7B)
├── Medium (standard Q&A/content generation) → Medium model (Sonnet/GPT-4o)
└── Complex (multi-step reasoning/code/math) → Large model (Opus/GPT-4.1/o1)

Step 3: Latency requirements?
├── <500ms (real-time) → Smallest viable model + streaming output
├── 1-3s (near real-time) → Medium model + streaming output
└── Async/batch processing → Most powerful model

Step 4: Call volume?
├── Low frequency (<1K calls/day) → API is most economical
├── Medium frequency (1K-100K calls/day) → API primarily + semantic caching to cut 30%+
├── High frequency (>100K calls/day) → Evaluate break-even point for self-hosted inference
└── Ultra-high frequency (>1M calls/day) → Self-hosted inference + model quantization + continuous batching

Step 5: Task reusability?
├── Same task pattern recurring → Fine-tune small model (cost reduction 10-100x)
└── Tasks diverse and unpredictable → General-purpose large model API
```

#### 3.2 Mainstream Model Capability Matrix (2025-2026)

**Closed-source APIs:**

| Model | Best At | Context Window | Pricing (Input/Output $/M) | Applicable Scenarios |
|------|--------|----------|----------------------|---------|
| Claude Opus 4.5 | Complex reasoning, code, long documents | 200K | $5/$25 | Most complex B2B tasks |
| Claude Sonnet 4 | Balanced capability, code | 200K | $3/$15 | Default choice for most B2B scenarios |
| GPT-4.1 | Reasoning chains, math | 1M | $15/$60 | Scenarios requiring deep reasoning |
| GPT-4o | Multimodal, speed | 128K | $2.5/$10 | Multimodal + real-time scenarios |
| Gemini 2.5 Pro | Ultra-long context, search | 2M | $1.25/$10 | Ultra-long document/codebase analysis |
| Gemini Flash | Speed + cost | 1M | $0.075/$0.30 | High-throughput simple tasks |

**Open-source Models (for private deployment/fine-tuning):**

| Model | Parameters | Strongest Capability | Hardware Requirements (Inference) | Applicability |
|------|------|---------|--------------|------|
| Llama 4 | 8B/70B/405B | General-purpose, strong ecosystem | 8B=1 GPU / 70B=4 GPUs | English-primary |
| Qwen 3 | 7B/72B | Best for Chinese, multimodal | 7B=1 GPU / 72B=4 GPUs | Top choice for Chinese scenarios |
| DeepSeek V3/R1 | 671B (MoE) | Reasoning, Chinese, extreme cost-performance | MoE-optimized architecture | Cost-sensitive + strong reasoning |
| Mistral Large | 123B | Multilingual, speed | 4-8 GPUs | European market |

#### 3.3 Build vs Buy vs Fine-tune — Three-Path Decision

```
┌────────────────────────────────────────────────────┐
│                     Decision Tree                    │
│                                                    │
│ Is this a core differentiator?                      │
│   ├── Yes → BUILD (self-developed model)            │
│   │         Conditions: sufficient data + budget + ML team │
│   │         Cost: 7B ≈ $100K, 70B ≈ $1-5M           │
│   │         Timeline: 6-18 months                    │
│   │                                                   │
│   └── No → Do you have substantial proprietary data the model needs to learn? │
│             ├── Yes → FINE-TUNE (API or open-source model fine-tuning) │
│             │         Cost: $15 (LoRA small model) - $50K+              │
│             │         Timeline: 1-4 weeks                               │
│             │         Suitable for: changing style/format/domain terminology │
│             │                                                              │
│             └── No → BUY (use API directly)                               │
│                       Cost: pay-per-use                                   │
│                       Timeline: immediate                                 │
│                       Suitable for: most scenarios                        │
└────────────────────────────────────────────────────┘

2025 Industry Consensus: "Buy the substrates. Build the autonomy."
→ Purchase base models, build autonomous capability layer on top
```

#### 3.4 Model Routing Strategy (Multi-Model Architecture)

```
Advanced AI product architecture: not choosing one model, but routing across multiple models.

User Query → Classifier (complexity assessment) →
  ├── Simple (40%) → Small model (Haiku/Flash) → Low cost
  ├── Medium (40%) → Medium model (Sonnet/GPT-4o) → Balanced
  └── Complex (20%) → Large model (Opus/GPT-4.1) → High quality

Result: Cost reduced 40-60%, latency reduced 20-30%, quality roughly unchanged
```

#### Deliverables

1. **Model Selection Decision Report** (including decision tree path + comparison matrix + cost projection)
2. **Build/Buy/Fine-tune Recommendation** (including 2-3 year TCO estimate)
3. **Model Routing Architecture Design** (if applicable)

---

### Stage 4: Prompt & Context Engineering

**Role: Prompt Architect**

> "Prompt is the UI of AI products. Context Engineering is a deeper design layer than Prompt Engineering."

#### 4.1 Structured Prompt Design Pattern

```
┌─────────────────────────────────────────────┐
│ [System Prompt] — System-level role and capability definition │
│ Who you are | Your task | Your constraints | Your tone │
├─────────────────────────────────────────────┤
│ [Context] — Contextual information                    │
│ Current user info | Relevant data | Business rules | Scenario │
├─────────────────────────────────────────────┤
│ [Task] — Specific task instructions                  │
│ What to do | Steps | Format requirements             │
├─────────────────────────────────────────────┤
│ [Output Schema] — Output format constraints          │
│ JSON Schema | Field descriptions | Examples          │
├─────────────────────────────────────────────┤
│ [Few-Shot Examples] — Examples (strongly recommended) │
│ 2-5 high-quality input→output examples               │
├─────────────────────────────────────────────┤
│ [Constraints] — Prohibited actions                    │
│ Don't do X | Say "I don't know" if uncertain         │
└─────────────────────────────────────────────┘

Example: AI Legal Contract Review System Prompt
You are a senior corporate legal expert specializing in contract risk review.
Your review scope: sales contracts, service contracts, NDAs.
You must: cite specific clauses to point out risks, provide revision suggestions, label risk level (High/Medium/Low).
You must not: provide legal opinions (state "for reference only"), fabricate non-existent legal provisions.
Output format: JSON, containing risk_items array, each item with {clause, risk_level, description, suggestion}
```

#### 4.2 Advanced Prompt Techniques

| Technique | Principle | Applicable Scenarios | Effect |
|------|------|---------|------|
| **Chain-of-Thought** | Guide the model "let's think step by step" | Complex reasoning / math / multi-step analysis | Accuracy ↑15-30% |
| **Few-Shot** | Provide 2-5 high-quality input→output examples | Strict format requirements / domain-specific | Format adherence ↑50%+ |
| **Self-Consistency** | Multiple sampling + voting | Reasoning requiring high accuracy | Accuracy ↑5-10% |
| **ReAct** | Thought → Action → Observation loop | Tasks requiring tool calls | Essential for Agents |
| **Tree of Thoughts** | Explore multiple reasoning paths + evaluate and select | Complex planning / strategy | Planning-heavy scenarios |
| **Constitutional Prompting** | Embed principles within the Prompt | Content safety / value alignment | Safety refusal rate ↑ |

#### 4.3 Context Engineering

> Core question: "What information to give the model, in what structure, at what timing?"

**Context Window Budget Management (using 128K as example):**

```
Total Budget: 128K tokens

Allocation Strategy:
├── System Prompt: 2-5K tokens (role + rules + output format)
├── Conversation History: 10-20K tokens (recent conversations, summarize old ones)
├── RAG Retrieval Results: 20-40K tokens (most relevant documents + metadata)
├── User Current Query: 0.5-2K tokens
├── User Profile / Preferences: 2-5K tokens
├── Tool Definitions: 5-10K tokens (function definitions)
└── Reserved Buffer: ~20K tokens (for model thinking/generation)
```

**Context Window Pitfalls (Bigger ≠ Better!):**

| Pitfall | Manifestation | Mitigation |
|------|------|------|
| **Context Poisoning** | Earlier hallucinations are continuously cited and amplified | Periodic reset + source annotation |
| **Context Distraction** | Too much irrelevant information, model loses focus | Curate rather than dump |
| **Context Confusion** | Too many tools, calling the wrong tool | Keep tool count < 20 |
| **Context Conflict** | Contradictory information across multi-turn conversations (performance drop ~39%) | Conflict detection + clarification mechanism |

**Dynamic Context Assembly Strategy:**
- Load different System Prompts based on user role
- Choose different retrieval strategies based on current task type
- Personalize context based on user history (preferences / habits / level)
- Key information first: place the most important content in the first 2000 and last 500 tokens of the Prompt

#### 4.4 Prompt Version Management & A/B Testing

```
Prompt Engineering Best Practice = Manage Prompts like code

Process:
1. Version-control Prompts in Git (not tweaking in a database)
2. Every change has a Changelog (what changed, why, expected impact)
3. Evaluate new Prompt on Golden Dataset first (offline validation)
4. After passing evaluation, A/B test on 5% traffic (online validation)
5. Statistically significant (>95% confidence) + core metrics not degraded → full rollout
6. Keep old Prompt as rollback option

Metrics to monitor in A/B tests:
- Task completion rate (primary)
- User satisfaction / thumbs-up rate (secondary)
- Inference latency (must not degrade)
- Token cost (must not significantly increase)
- Safety refusal rate (must not degrade)
```

#### Deliverables

1. **System Prompt Design Document** (including role definition / constraints / format / examples)
2. **Context Assembly Strategy Document** (including window budget / dynamic assembly rules)
3. **Few-Shot Example Library** (categorized by scenario, continuously optimized)
4. **Prompt Version Management Specification** (Git integration + A/B testing process)

---

### Stage 5: RAG Design & Implementation

**Role: RAG Architect**

> "RAG is currently the most core and most mature architectural pattern for B2B AI products."

#### 5.1 RAG Standard Pipeline (5 Layers)

```
┌──────────────────────────────────────────────┐
│ 1. Document Ingestion                                  │
│    ├── Document parsing (PDF/Word/HTML/Markdown/image OCR) │
│    ├── Chunking: fixed-size / semantic / hierarchical   │
│    └── Metadata extraction (document name / date / author / permissions / tags) │
├──────────────────────────────────────────────┤
│ 2. Embedding                                        │
│    ├── Text → Vector (choose appropriate Embedding model) │
│    └── Store in vector database                          │
├──────────────────────────────────────────────┤
│ 3. Retrieval                                        │
│    ├── Hybrid search: BM25 (keyword) + Dense (semantic) │
│    ├── Reranking: Cross-encoder secondary ranking of recall results │
│    └── Filtering: by permissions / date / tags / metadata │
├──────────────────────────────────────────────┤
│ 4. Generation                                       │
│    ├── System Prompt + Retrieved Context + User Query → │
│    ├── LLM generates answer with citation annotations   │
│    └── Confidence output (inform user when uncertain)    │
├──────────────────────────────────────────────┤
│ 5. Evaluation & Iteration                            │
│    ├── RAGAS metrics (Faithfulness / Relevancy / Context Precision / Recall) │
│    ├── Bad Case analysis → Chunking strategy → Retrieval strategy → Iterate │
│    └── User feedback closed loop                        │
└──────────────────────────────────────────────┘
```

#### 5.2 RAG 7 Advanced Patterns (Latest 2025)

| Pattern | Mechanism | Latency | Accuracy | Best Scenario |
|------|------|------|--------|---------|
| **Basic RAG** | Vector retrieval + generation | Low | Medium | Rapid prototyping |
| **Hybrid Search + Reranker** | BM25 + Vector + Cross-encoder | Medium | High | **Default production starting point** |
| **Self-RAG** | Model self-reflection + judges whether retrieval is needed | Medium-High | High | Need to reduce hallucinations |
| **Corrective RAG** | Lightweight evaluator scores → use/discard/supplement | Medium-High | High | Unstable knowledge base quality |
| **Agentic RAG** | Dynamic reasoning + tool calling + multi-step retrieval | High | Very High | Complex multi-step autonomous tasks |
| **GraphRAG** | Knowledge graph + community summaries + hierarchical retrieval | Medium-High | Very High | 100K+ documents, cross-document relationships |
| **HyDE** | Generate hypothetical document first, then retrieve | Medium | High (fuzzy queries) | Domain-specific fuzzy queries |

#### 5.3 Key RAG Design Decisions

| Decision Point | Options | Recommendation | Rationale |
|--------|------|------|------|
| Chunking Strategy | Fixed / Semantic / Hierarchical | Semantic primary + Fixed secondary | Semantic chunking F1 ↑36% (legal docs) |
| Chunk Size | 256/512/1024/2048 | 512 primary, key paragraphs 1024 | Balance completeness and retrieval precision |
| Overlap Rate | 0%/10%/20% | 10-20% | Avoid cutting semantics at boundaries |
| Embedding Model | Various | Chinese → bge-large-zh; English → text-embedding-3-large | bge performs best for Chinese scenarios |
| Vector Database | Various | <1M vectors → pgvector; >1M → Milvus | Milvus has better distributed scaling |
| Top-K | 3/5/10/20 | Hybrid search 50 → Rerank to 5-10 | Reranker provides significant improvement |
| Reranker | Cohere/BGE/None | Must add Reranker | MRR improvement 20%+ |

#### 5.4 RAG vs Fine-tuning vs Long Context — Decision Framework

| Scenario | Recommended Approach | Reason |
|------|---------|------|
| Knowledge updates frequently | RAG | Fine-tuning obsolescence cost is high |
| Need explainability / source citations | RAG | Traceable to source documents |
| Need to mimic specific style / tone | Fine-tuning | More stable than Few-shot Prompt |
| Many domain terms / abbreviations | Fine-tuning | Learn term distribution |
| Documents < context window and rarely change | Long Context | Simplest, no extra infrastructure needed |
| **Most B2B scenarios** | **RAG + Fine-tuning** | 2025 industry consensus: hybrid is the default choice |

#### 5.5 RAG Evaluation Metrics (RAGAS Standard)

| Metric | What It Measures | Target |
|------|---------|------|
| **Faithfulness** | Whether generated answer comes entirely from retrieved content | >0.90 |
| **Answer Relevancy** | Whether the answer addresses the question | >0.85 |
| **Context Precision** | Proportion of retrieved content that is relevant | >0.85 |
| **Context Recall** | Proportion of relevant content that was retrieved | >0.90 |

#### Deliverables

1. **RAG Architecture Design Document** (including pipeline design / chunking strategy / retrieval strategy / vector database selection)
2. **Embedding Model Selection Report** (including Chinese/multilingual scenario comparison)
3. **RAG Evaluation Report Template** (including RAGAS metrics + Bad Case analysis)
4. **Knowledge Base Management Specification** (including document ingestion SOP / update frequency / quality checks)

---

---

### Stage 6: Agent & Multi-Agent Systems

**Role: Agent Architect**

> "Agent = LLM + Memory + Planning + Tools. Not every task needs an Agent."

#### 6.1 When to Use an Agent? (Decision Tree)

```
Is a simple LLM call sufficient?
├── Yes → Don't use an Agent! Simple calls are cheaper, lower latency, more controllable
│       Applicable: translation, summarization, classification, simple Q&A, content generation
│
└── No → Does it require multi-step operations?
         ├── Yes → Does it need flexible tool selection?
         │        ├── Yes → Use Agent
         │        └── No → Use fixed Pipeline
         └── No → Use simple LLM call

Agent's extra cost: multi-turn calls → latency ↑2-5x, Token consumption ↑3-10x
Agent's value: handling open-ended, complex tasks requiring multi-step reasoning and tool calls
```

#### 6.2 Agent Architecture Patterns

**Pattern 1: ReAct (Reasoning + Action)**
```
Thought → Action → Observation → Thought → ... → Final Answer
```

**Pattern 2: Plan-and-Execute**
```
Plan (create plan) → Execute Step 1 → ... → Summarize
Suitable for: clear objectives but complex steps, user can review plan before execution
```

**Pattern 3: Orchestrator-Worker**
```
Orchestrator → Worker A (search) + Worker B (analyze) + Worker C (write) → Integrate output
Suitable for: tasks decomposable into independent sub-tasks, parallel execution
```

**Pattern 4: Reflection Agent**
```
Execute → Self-evaluate → Identify issues → Revise → Re-evaluate
Accuracy improvement +10-20%, cost: extra 1-2 LLM call rounds
```

#### 6.3 Multi-Agent Orchestration Frameworks

| Framework | Programming Model | Strengths | Applicability |
|------|---------|------|------|
| **LangGraph** | Directed graph + state management | Flexible, controllable, large community | Production-grade Agent systems |
| **CrewAI** | Role-playing + sequential/hierarchical | Simple and intuitive, quick to start | Rapid prototyping |
| **AutoGen (Microsoft)** | Conversation-driven multi-agent | Academic background, supports HITL | Research + enterprise |
| **OpenAI Agents SDK** | Lightweight Agent + Handoff | Native integration, simple | OpenAI ecosystem |
| **Dify** | Visual + low-code | Chinese-friendly, drag-and-drop | Non-technical users |
| **Coze (ByteDance)** | Visual + plugin marketplace | Strong China ecosystem | AI Bot development |

#### 6.4 HITL Design (Mandatory for B2B Agent Compliance)

| Risk Level | Agent Behavior | Human Role | Example |
|---------|----------|---------|------|
| **Low Risk** | Agent executes autonomously | Post-hoc spot-check | Tags, summaries, formatting |
| **Medium Risk** | Agent generates → Human confirms | Confirm before execution | Notifications, status changes |
| **High Risk** | Agent suggests → Human executes | Human operates | Deletion, approval, publishing |
| **Not Allowed** | Agent operation prohibited | Human only | Payments, signing, permission changes |

#### 6.5 Agent Security & Sandboxing

```
Agent Security Layers:
├── Identity & Permissions: Principle of least privilege, short-lived credentials
├── Sandbox Isolation: gVisor / Kata Containers / Firecracker
├── Network Controls: Egress allowlisting, sensitive API interception
├── Tool Auditing: Signature verification, permission declarations
├── Runtime Monitoring: Anomaly behavior detection, resource limits
└── Emergency Circuit Breaker: One-click stop Agent execution
```

#### Deliverables

1. **Agent Architecture Design Document** (including architecture pattern / tool definitions / memory design / HITL matrix)
2. **Agent Tool API Specification** (function / input / output / permissions / error handling)
3. **Agent Security Design Document** (including sandbox strategy / permission model / circuit breaker mechanism)
4. **Agent Evaluation Plan** (task completion rate / tool call accuracy / HITL trigger rate)

---

### Stage 7: Model Fine-tuning & Adaptation

**Role: Model Optimizer**

> "Fine-tuning changes not knowledge, but style and format. New knowledge is injected via RAG."

#### 7.1 Fine-tuning Decision Framework

```
YES (Fine-tuning needed):
□ Model needs to output specific formats (JSON/tables/code templates) and Prompt is not stable enough
□ Specific tone / style / brand voice is needed
□ Many domain abbreviations / terms (Prompt can't fit them all)
□ Same task recurs frequently (fine-tune small model to replace large model, saving cost)

NO (Fine-tuning not needed):
□ Task requires latest knowledge → RAG is more suitable
□ Knowledge changes frequently → Fine-tuning can't keep up
□ Only a small number of examples (<100) → Few-shot Prompt is more practical
□ Using closed-source API and Prompt can solve it → Prompt optimization is cheaper
□ Need explainable source citations → RAG provides traceability
```

#### 7.2 Fine-tuning Method Comparison

| Method | Principle | Cost | Stability | Best Use |
|------|------|------|--------|---------|
| **SFT** | Input → Desired output pairs | Medium | ⭐⭐⭐⭐ | Format/style control |
| **RLHF** | Human feedback → Reward model → Reinforcement learning | Very High | ⭐⭐ | Value alignment |
| **DPO** | Direct preference pair comparison | Medium | ⭐⭐⭐⭐ | Good alignment, stable |
| **LoRA/QLoRA** | Train only a small number of parameters | Very Low (from $15) | ⭐⭐⭐⭐⭐ | Top choice for efficient fine-tuning |

**2025 Consensus: DPO + LoRA is the preferred combination for enterprise fine-tuning.**

#### 7.3 Fine-tuning Data Preparation

```
Minimum requirement: 100-500 high-quality examples
Recommended: 1000-5000 examples
Principle: 500 curated examples > 5000 noisy data points

Data Format (SFT):
{"messages": [
  {"role": "system", "content": "You are an expert in domain XX..."},
  {"role": "user", "content": "User input"},
  {"role": "assistant", "content": "Expected model output"}
]}

Data Construction Principles:
1. Diversity: Cover various scenarios, edge cases, expression styles
2. Consistency: Uniform labeling standards, conflicting data must be cleaned
3. Representativeness: Data distribution should match real user demand distribution
```

#### 7.4 GPU Requirements Estimation

| Model Size | Full Fine-tuning | LoRA/QLoRA |
|---------|-----------------|------------|
| 7B-8B | 4-8x A100 80GB | 1x A100/L40S || 13B | 8x A100 80GB | 1-2x A100 |
| 70B-72B | 32+ A100/H100 Cluster | 2-4x A100 |
| 405B | Large Cluster ($1M+) | 8x A100 |

#### Deliverables

1. **Fine-tuning Strategy Document** (including decision rationale / method selection / data strategy / cost estimation)
2. **Fine-tuning Data Preparation Specification** (including data format / quality standards / annotation guide)
3. **Fine-tuning Evaluation Plan** (including benchmark comparison / domain evaluation / regression testing)

---

### Phase 8: AI UX & Interaction Design

**Role: AI Experience Designer**

> "The best AI UX is when users don't even realize they're using AI."

#### 8.1 The 7 Major AI Interaction Patterns

| Pattern | Description | Best Scenario | Representative Product |
|------|------|---------|---------|
| **Embedded AI** | AI in the background, invisible to users | High-frequency, high-certainty | Google Search Ranking |
| **Copilot Sidebar** | Sidebar AI assistant | Assisted creation/analysis | GitHub Copilot |
| **Chat Dialogue** | Pure conversational interface | Exploratory tasks | ChatGPT |
| **Canvas** | AI + editable workspace | Content creation + iteration | Claude Artifacts |
| **Agent Autonomy** | Auto-complete multi-step tasks | Complex operations | Devin, AutoGPT |
| **Smart Forms** | Form → Prompt generation | Structured guidance | Resume builder |
| **Flowchart Orchestration** | Visual Agent orchestration | Workflow automation | n8n, Dify |

#### 8.2 AI UX Core Principles (10 Rules)

```
1. Progressive Trust — Start with low-risk features, gradually open up high-risk autonomy
2. Reversible — AI actions should be undoable with one click
3. Explainable — Let users know "why AI answered this way" (cite sources / reasoning steps)
4. Overridable — Users can manually take over or modify AI output at any time
5. Show Uncertainty — Display confidence levels when uncertain, don't pretend to be 100% certain
6. Streaming Output — Display token by token, letting users perceive AI is "thinking"
7. Give Users an Exit — Besides AI options, always provide manual operation paths
8. Empty State Guidance — Provide example prompts to reduce "don't know what to say" anxiety
9. Graceful Error Handling — Tell users "what happened + what to do" when errors occur
10. Context Visibility — Let users see what information AI is using to make decisions
```

#### 8.3 AI UX Anti-Patterns (10 Major Mistakes)

| # | Anti-Pattern | Correct Approach |
|---|--------|---------|
| 1 | **Everything is Chat** — Even simple tasks require dialogue | Use controls/buttons instead of unnecessary dialogue |
| 2 | **Pretending to be Human** — Creating trust traps | Clearly label "I am AI" |
| 3 | **Black-box Decisions** — Users have no idea what AI did | Show reasoning steps, cite sources |
| 4 | **No Exit Design** — Unsatisfied but can't operate manually | Always keep a manual path |
| 5 | **Excessive Anthropomorphism** — Simulating typing delay, "I'm thinking..." | Sincerity beats anthropomorphism, efficiency first |
| 6 | **All-or-Nothing Trust** — Either fully trust or fully distrust | Progressive trust, tiered by risk |
| 7 | **Pretending 100% Accuracy** — Using confidence to mask uncertainty | Use "possibly / suggest / reference" when uncertain |
| 8 | **Ignoring Wait Experience** — No feedback during reasoning | Streaming output + progress indicators |
| 9 | **Opaque Memory** — Users don't know what AI remembers | Provide a memory management panel |
| 10 | **Only Adding** — Adding AI everywhere | "AI-second, not AI-first" |

#### 8.4 GenUI (Generative UI — Cutting-Edge Concept)

```
Traditional AI: Text in → Text out
GenUI: Text in → Structured JSON → Real-time rendered UI components

Example:
User: "Compare the quotes from these 3 suppliers"
→ Generate comparison table JSON → Render as interactive comparison component (sortable / filterable / highlightable)

Tools: CopilotKit, LangChain + React streaming, C1 by Thesys
```

#### Deliverables

1. **AI UX Design Specification** (interaction pattern selection / principle declaration / anti-pattern checklist)
2. **AI Interaction Prototype** (HTML prototype: loading state / empty state / error state / result state / confidence display)
3. **AI User Trust Building Plan** (progressive trust roadmap)

---

### Phase 9: Evaluation System & Quality Assurance

**Role: AI Quality Assurance Expert**

> "Without evaluation, there is no AI product iteration. Evaluation is not a pre-launch checkpoint, but a continuous system."

#### 9.1 AI Evaluation vs Traditional Testing

| Dimension | Traditional Software Testing | AI Product Evaluation |
|------|------------|----------|
| Determinism | Given input → Deterministic output | Given input → Probabilistic output |
| Correctness | Clear binary judgment | Multi-dimensional degree judgment |
| Test Cases | Predefined, exhaustible | Open-ended, inexhaustible |
| Failure Modes | Explicit (errors / crashes) | Implicit (hallucinations / bias / omissions) |
| Regression Testing | Exact input/output matching | Statistical comparison (old vs new quality distribution) |

#### 9.2 Evaluation Dimension Matrix

| Dimension | What It Measures | Measurement Method | Target |
|------|---------|---------|------|
| **Accuracy** | Whether facts are correct | Golden Dataset comparison | >90% |
| **Relevance** | Whether it responds to user intent | Human scoring + semantic similarity | >85% |
| **Faithfulness** | Whether faithful to context (RAG) | RAGAS Faithfulness | >0.90 |
| **Completeness** | Whether all key information points are covered | Checklist coverage rate | >85% |
| **Safety** | Harmful content output rate | Red team testing + automated scanning | <0.1% |
| **Latency** | P50/P95/P99 | Automated monitoring | P95<3s |
| **Cost** | Token consumption per interaction | Automated statistics | Within budget |
| **Consistency** | Whether same intent with different expressions is consistent | Paraphrase test set | >90% |

#### 9.3 Golden Dataset Construction

```
Construction Process:
1. Sample from real user queries (not made up by PMs)
2. Coverage dimensions: Common scenarios (60%) + Edge cases (20%) + Adversarial cases (10%) + Safety tests (10%)
3. Quantity: At least 200 entries, recommended 500-1000 (statistically significant)
4. Annotation: Domain experts annotate standard answers + scoring rubric
5. Maintenance: Add new queries monthly (10-20 entries), retire outdated queries
```

#### 9.4 Evaluation Method Toolkit

| Method | Cost | Speed | Applicable |
|------|------|------|------|
| **Human Evaluation** | Highest | Slowest | Golden Dataset annotation, final decisions |
| **LLM-as-Judge** | Medium | Fast | Scaled daily evaluation (use strong model to judge weak model) |
| **Automated Metrics** (RAGAS/ROUGE) | Low | Fastest | Regression testing, quick screening |
| **A/B Testing** | High | Slow | Validating business impact |

**LLM-as-Judge Notes:**
- Use the strongest model as judge (accuracy ~81%)
- Add "Please explain your scoring" to improve transparency
- Periodically calibrate with human spot checks
- Different judge models have significant consistency differences

#### 9.5 Evaluation Pipeline

```
Evaluation process for every Prompt/model change:

Step 1: Offline Evaluation (must pass)
├── Run full Golden Dataset
├── RAGAS metrics must not degrade
├── Safety test set must show no new issues
└── Output comparison report (old vs new)

Step 2: Gradual Online Rollout (gradually increase traffic)
├── 5% → 10% → 25% traffic
├── Monitor core metrics
└── Statistically significant + metrics not degraded → continue rollout

Step 3: Full Rollout + Continuous Monitoring
├── 7×24 hour metric monitoring
├── Automatic Bad Case collection
└── Weekly evaluation report + iteration
```

#### Deliverables

1. **Evaluation System Design Document** (evaluation dimensions / method selection / metric definitions)
2. **Golden Dataset** (including answer standards + scoring rubric)
3. **Evaluation Pipeline Configuration** (offline evaluation + online monitoring dashboard)
4. **Weekly Evaluation Report Template**

---

### Phase 10: Safety Guardrails & Red Team Testing

**Role: AI Security Engineer**

> "AI safety is not a one-time check, but a continuous economic game (raising the cost of attacks)."

#### 10.1 AI-Specific Attack Surface

```
├── Input Layer: Prompt injection, Jailbreak, Base64/ROT13 encoding bypass, multilingual bypass
├── Output Layer: Hallucinations, harmful content, PII leakage, code injection
├── Data Layer: Knowledge base poisoning, malicious fine-tuning, membership inference attacks
└── System Layer: Agent tool abuse, privilege escalation, resource exhaustion
```

#### 10.2 Multi-Layer Safety Guardrails

```
Layer 1: Identity Authentication & Authorization (least privilege + short-lived tokens)
Layer 2: Input Guardrails (injection detection + jailbreak detection + PII filtering)
Layer 3: Output Guardrails (content safety classifier + hallucination detection + PII redaction)
Layer 4: Runtime Monitoring (anomaly detection + token consumption alerts + emergency circuit breaker)
Layer 5: Audit & Traceability (complete interaction logs + Agent invocation records)
```

#### 10.3 Red Team Testing

**Lessons from Microsoft's Red Teaming of 100+ Products:**
- Context awareness: Same model, different scenarios, different risks
- Simple attacks are most effective: Real attackers use Prompts, not gradients
- System-level thinking: The most effective attacks combine multiple techniques across the stack
- Dual-role testing: Malicious attacker AND well-intentioned accidental trigger
- Continuous posture: Offense-defense game, not a one-time check

**Cadence:** Full scope before major releases + Monthly focus areas + Continuous automated scanning + Regression after every model upgrade

#### 10.4 Safety Release 30-60-90 Day Plan

| Phase | Key Actions |
|------|---------|
| **Day 0-30** | Inventory Agents/tools; least privilege; sandboxing; emergency circuit breaker |
| **Day 31-60** | Tool signature verification; safety monitoring rules; HITL gating; targeted red team testing |
| **Day 61-90** | CI/CD security integration; comprehensive red team + fix + regression; security governance cadence |

#### Deliverables

1. **AI Security Design Document** (threat model / guardrail architecture / emergency response plan)
2. **Red Team Test Report Template** (test scope / findings / fix verification)
3. **Safety Release Checklist**
4. **Content Safety Classification Standards** (customized by deployment region)

---

### Phase 11: AI Observability & Production Operations

**Role: AI Operations Expert**

> "AI product launch is just the beginning; continuous observation and optimization is the norm."

#### 11.1 LLMOps Observability Panorama

```
Three Pillars:

Technical Metrics: Latency P50/P95/P99 | Throughput QPS | Token Consumption | Error Rate | Cache Hit Rate
Quality Metrics: Task Completion Rate | Like Rate | Hallucination Rate (sampled) | Safety Rejection Rate | RAGAS Trends
Business Metrics: User Retention | Feature Adoption Rate | Per-User Inference Cost | ROI (Value/Cost)
```

#### 11.2 Observability Tool Stack

| Tool | Core Capability | Applicable |
|------|---------|------|
| **LangSmith** | Prompt management + evaluation + tracing + monitoring | LangChain ecosystem |
| **Arize Phoenix** | LLM observability + drift detection | Open-source, OpenTelemetry-native |
| **Langfuse** | LLM tracing + metrics + Prompt management | Open-source alternative to LangSmith |
| **Weights & Biases** | Training tracking + Prompt management | Model training + products |
| **Datadog LLM** | Enterprise-grade monitoring | Enterprises already using Datadog |

#### 11.3 AI Product-Specific Degradation Patterns

```
1. Model Drift: Behavior changes after upstream model upgrade → Evaluate and compare after each model change
2. Data Drift: User query distribution changes → Monitor KL divergence, update Golden Dataset
3. Concept Drift: Same word changes meaning → Periodically sample and evaluate specific queries
4. Feedback Loop Degradation: AI output influences user behavior → influences AI again → Periodic calibration
```

#### 11.4 Cost Monitoring Dashboard

```
Core Metrics:
- Daily cost per user = Σ (function calls × Token cost)
- Free user cost ratio (>15% tighten restrictions)
- Top 10 high-cost users (investigate abuse)
- Per-interaction cost distribution P50/P95/P99

Alerts: Single user daily cost > 10x average | Free tier cost > 15% | API failure rate > 5%
```

#### Deliverables

1. **AI Observability Dashboard** (three-layer metrics: technical / quality / business)
2. **Alert Rule Configuration Document**
3. **Production Troubleshooting Manual**
4. **Cost Optimization Recommendation Report**

---

### Phase 12: AI Commercialization & Monetization

**Role: AI Commercialization Strategist**

> "AI product pricing is not per seat, but aligned with user value and inference cost."

#### 12.1 Why Is AI Pricing So Difficult?

```
Traditional SaaS marginal cost ≈ 0 → Per-seat pricing makes sense
AI product marginal cost ≠ 0 → Every call has real token cost

Problems:
- Simple query $0.001 vs complex multi-step chain $0.50+ (500x difference)
- Two users on the same seat could have 50x cost difference
- Per-seat pricing leads to profit inversion
```

#### 12.2 Six Major AI Pricing Models

| Model | Principle | Advantage | Disadvantage | Suitable For |
|------|------|------|------|------|
| **Per Token/Usage** | Pay as you go | Most precise cost alignment | User cost uncertainty | API products |
| **Hybrid (Base + Usage)** | Fixed monthly + overage per use | Predictable + flexible | Complex metering | **Most B2B AI SaaS** |
| **Per Outcome** | Pay per completed task | Directly aligned with user value | Complex attribution | Customer service / leads |
| **Tiered + AI Quota** | Each plan includes AI usage cap | Familiar to enterprise procurement | Power users may exceed | Enterprise SaaS |
| **Prepaid Consumption** | Token packages | Predictable revenue | Limits heavy user revenue | Early-stage products |
| **Free Trial + Paid** | Limited free quota | Lowers trial barrier | Free tier cost risk | PLG products |

**Recommendation: Hybrid model (base monthly fee + usage quota + overage metered billing)**

#### 12.3 Token Economics Core Metrics

| Metric | Formula | Healthy Benchmark |
|------|------|---------|
| **AI Gross Margin** | (AI Revenue - Inference Cost) / AI Revenue | >60% |
| **Cost Markup Rate** | Selling Price / Inference Cost | 1.3-3x |
| **Free Tier Cost Rate** | Free User Inference Cost / Total Inference Cost | <10% |
| **Monthly Cost Per User** | Monthly Total Inference Cost / Monthly Active Users | Continuously decreasing |

#### 12.4 Cost Optimization Strategies

| Strategy | Expected Savings | Implementation Difficulty |
|------|---------|---------|
| Semantic Caching | 20-35% | Medium |
| Model Routing | 40-60% | Medium-High |
| Prompt Compression | 15-25% | Low |
| Batch Processing | 20-40% | Low |
| Fine-tuned Small Model Replacing Large Model | 30-80% | High |

#### 12.5 Sequoia's Service-as-a-Software Paradigm

```
Traditional SaaS: Sell tools (per seat) → Market $650B
AI New Paradigm: Sell work outcomes (per result) → Potential market $10T

Traditional: "Pay us, we give you software tools"
AI Era: "Pay us, we directly complete the work"

→ AI PMs must think: Not "What AI features can I add?"
                       But "What work can AI complete for users?"
```

#### Deliverables

1. **AI Product Pricing Plan** (pricing model / plan design / usage strategy)
2. **Token Economics Model** (cost forecast / gross margin model / break-even analysis)
3. **Cost Optimization Roadmap**

---
