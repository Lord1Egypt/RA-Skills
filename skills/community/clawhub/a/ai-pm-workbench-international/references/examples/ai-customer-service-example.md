# AI Intelligent Customer Service Complete Case Study

> This case study demonstrates how to design an enterprise-grade AI intelligent customer service product from 0 to 1.
> Covers the full process: AI Strategy → Model Selection → RAG Design → Agent → Prompt → AI UX → Evaluation → Security → Pricing.

---

## Case Background

### Product Overview
"SmartCS" — An AI-powered intelligent customer service platform for mid-to-large enterprises, built on LLM+RAG+Agent technology, enabling the intelligent upgrade of customer service.

### Target Customers
- Enterprise size: 200-5000 employees, with a dedicated customer service team
- Typical industries: Retail e-commerce, FinTech, SaaS services, Logistics
- Average monthly ticket volume: 5,000-100,000+
- Current pain points: High labor costs for human agents, slow response times, difficulty in knowledge transfer, high QA costs

---

## Phase 0: AI Opportunity Assessment

### Scoring Results

| Dimension | Score | Weight | Weighted | Basis |
|------|------|------|------|------|
| User Pain Point Intensity | 5 | 25% | 1.25 | Customer service costs account for 3-8% of revenue; human agents earn 5K-8K/month, recruitment is difficult |
| AI Feasibility | 4 | 25% | 1.00 | LLM+RAG can already resolve 70%+ of standard inquiries |
| Data Availability | 4 | 15% | 0.60 | Enterprises have historical tickets, knowledge bases, SOP documents |
| Business Return | 5 | 15% | 0.75 | Customers are willing to pay to reduce CS costs; ROI is clearly quantifiable |
| Competitive Urgency | 4 | 10% | 0.40 | Multiple competitors have launched AI customer service, but experience quality varies |
| Technical Difficulty (inverse) | 3 | 10% | 0.30 | Requires RAG+Agent, not a simple API call |
| **Total Score** | | | **4.30** | ✅ Launch immediately |

### Task Characteristics Analysis

| Characteristic | Assessment | AI Suitability |
|------|------|---------|
| Task Repetitiveness | High (60-70% of tickets are common questions) | ⭐⭐⭐⭐⭐ |
| Error Tolerance | Medium (incorrect CS answers can be escalated to human) | ⭐⭐⭐⭐ |
| Creativity Required | Low-Medium (standard answers + moderate empathy) | ⭐⭐⭐⭐ |
| Determinism Required | High (policies/processes must not be wrong) | ⭐⭐⭐ |

---

## Phase 1: Model Selection

### Selection Decisions

| Decision | Choice | Rationale |
|------|------|------|
| Build/Buy/Fine-tune | Buy API + RAG | The use case is relatively general; no need for self-training |
| Primary Model | Claude Sonnet 4 | Balances quality, cost, and latency |
| Complex Case Model | Claude Opus 4 | Complex complaints, multi-intent reasoning |
| Simple Case Model | Claude Haiku 4.5 | Simple FAQ, intent recognition |
| Routing Strategy | Classifier-based routing | Train an intent complexity classifier |
| Context Window | 128K tokens (Sonnet) | Supports long knowledge base documents + long conversation history |
| Chinese Capability | Native multilingual | Directly applicable to Chinese CS scenarios |

### Model Routing Architecture

```
User Query
    ↓
Intent Classifier (BERT fine-tuned)
    ↓
├── FAQ/Greeting (~50%) → Claude Haiku + Cache → <500ms
├── Standard Questions (~35%) → Claude Sonnet + RAG → <2s  
├── Complex Questions (~12%) → Claude Sonnet + Agent + RAG → <5s
└── Complaints/Sensitive (~3%)  → Claude Opus + Human Review → <8s
```

### Token Cost Estimation (Standardized per 1,000 Tickets)

| Scenario | Share | Input | Output | Unit Cost (Sonnet) | Cost per 1K Tickets |
|------|------|-------|--------|-----------------|-----------|
| FAQ Simple | 50% | 500 | 200 | $0.003 | $1.50 |
| Standard Q&A | 35% | 2000 | 500 | $0.012 | $4.20 |
| Complex Issues | 12% | 5000 | 1000 | $0.030 | $3.60 |
| Complaint Handling | 3% | 8000 | 1500 | $0.045 (Opus) | $1.35 |
| **Total** | | | | | **$10.65/1K Tickets** |

Comparison: Human agents handling 1,000 tickets costs approximately $500-800; AI cost is only 1.5-2% of human cost.

---

## Phase 2: RAG Design

### Knowledge Base Design

| Knowledge Source | Document Type | Quantity (Example) | Update Frequency | Priority |
|--------|---------|-----------|---------|--------|
| Product FAQ | Structured QA pairs | 5,000+ | Weekly | ⭐⭐⭐⭐⭐ |
| Product Help Docs | Technical docs / User manuals | 200+ articles | Per release | ⭐⭐⭐⭐ |
| Policies / Agreements | Refund / Privacy / Terms of Service | 50+ articles | Per policy change | ⭐⭐⭐⭐ |
| SOP Documents | Standard Operating Procedure docs | 100+ articles | Monthly | ⭐⭐⭐ |
| Historical High-Quality Tickets | Human agent conversations | 10,000+ | Continuous | ⭐⭐⭐ |

### Chunking Strategy

| Document Type | Chunking Method | Chunk Size | Overlap | Rationale |
|---------|---------|---------|------|------|
| FAQ | By QA pair | 1 QA/chunk | 0% | Each QA is self-contained |
| Help Docs | By paragraph + heading hierarchy | 1024 tokens | 20% | Preserve heading context |
| Policy Clauses | By clause number | 512 tokens | 10% | Clauses are independent but need to be linked |
| Historical Tickets | By full conversation | 2048 tokens | 0% | Maintain conversation integrity |

### Retrieval Architecture

```
User Query
    ↓
Query Rewriting (handles colloquialisms, polysemy, typos)
    ↓
Parallel Retrieval:
├── Dense Retrieval (bge-large-zh-v1.5, Top-30)
└── Sparse Retrieval (BM25, Top-30)
    ↓
Merge & Dedup → Top-50
    ↓
Cohere Rerank v3 → Top-5
    ↓
Relevance Filtering (score > 0.6)
    ↓
Context Assembly → LLM Generation
```

### Retrieval Parameters

| Parameter | Value | Rationale |
|------|-----|------|
| Initial Recall Count | Top-50 | Ensure recall coverage |
| Post-Rerank Count | Top-5 | Efficient use of context window |
| Similarity Threshold | 0.6 | Balance recall and precision |
| Hybrid Weighting | Dense 0.7 / BM25 0.3 | Dense as primary, BM25 assists with exact matching |

### Embedding Model

| Decision | Choice | Rationale |
|------|------|------|
| Model | bge-large-zh-v1.5 | One of the best for Chinese retrieval benchmarks |
| Dimensions | 1024 | |
| Max Input | 512 tokens | |
| Local Deployment | Yes | Data stays within the enterprise |

---

## Phase 3: Agent Design

### Agent Architecture (Plan-Execute Pattern)

```
User Query → Agent Planner
    ↓
Create Execution Plan:
├── Step 1: Identify user identity and intent
├── Step 2: Retrieve relevant knowledge base
├── Step 3: If order/member info is needed → Call business API tools
├── Step 4: Comprehensive analysis, generate response
├── Step 5: (Optional) If refund/complaint involved → Generate suggestion → HITL Confirmation
└── Step 6: Log ticket, update statistics
```

### Tools Definition

| Tool ID | Tool Name | Function | Risk Level | HITL |
|--------|---------|------|---------|------|
| T01 | search_knowledge_base | Search knowledge base | L0 | Not required |
| T02 | query_order | Query order information | L0 | Not required |
| T03 | query_member | Query member information | L0 | Not required |
| T04 | query_ticket | Query historical tickets | L0 | Not required |
| T05 | create_ticket | Create ticket | L1 | Post-hoc spot check |
| T06 | update_ticket | Update ticket status | L2 | Confirmation |
| T07 | send_notification | Send notification (SMS/Email/Push) | L2 | Confirmation |
| T08 | process_refund | Initiate refund | L3 | Mandatory Confirmation |
| T09 | modify_member_level | Modify membership tier | L3 | Mandatory Confirmation |
| T10 | escalate_to_human | Escalate to human agent | N/A | Automatic |

### HITL Matrix

| Operation | Risk Level | Agent Behavior | Human Role |
|------|---------|----------|---------|
| Answer FAQ | L0 | Autonomous response | Post-hoc spot check |
| Query Order/Member | L0 | Autonomous query | Log audit |
| Create Ticket | L1 | Auto-create | Post-hoc review |
| Modify Ticket Status | L2 | Suggest → Confirm | Review & Confirm |
| Send Notification | L2 | Generate draft → Confirm | Confirm & Send |
| Initiate Refund | L3 | Generate application → Human approval | Approve & Execute |
| Modify Member Tier | L3 | Suggest → CS Manager approval | Approve & Execute |
| Issue Coupon | L2 | Suggest issuance (within limit) | Approval for exceeding limit |
| Sensitive Complaint | L3 | Flag + Escalate to human | Manual handling |

### Memory Design

| Memory Type | Content | Implementation |
|---------|------|------|
| Short-term Memory | Current conversation context | Context window, last 20 turns |
| Episodic Memory | Summary of user's historical interactions | Vector DB storing key interaction summaries |
| Semantic Memory | User preferences / habits / tags | Structured user profile storage |
| Working Memory | Current task state | Agent state machine storage |

---

## Phase 4: Prompt Design

### System Prompt

```
You are SmartCS intelligent customer service assistant. Your responsibility is to provide accurate, professional, and friendly customer service to users.

# Your Capabilities
- Answer product usage questions (based on knowledge base)
- Query order, logistics, and member information (via tools)
- Handle common after-sales issues (returns, exchanges, refund policy inquiries)
- Create and update service tickets
- Seamlessly escalate to human agents when unable to handle

# Your Constraints
- Only answer based on knowledge base documents and real data returned by the system
- If information is not in the knowledge base, honestly tell the user "I need to look up more information for you"
- For sensitive operations involving refunds, compensation, etc., must explicitly inform the user "I will help you submit the application, which will be reviewed and processed by a customer service colleague"
- Never disclose other users' information
- Express uncertainty clearly when unsure; do not guess

# Your Working Approach
1. Identify user identity and intent
2. Retrieve relevant knowledge base and user data
3. If multi-step operations are required, create an execution plan
4. Execute step by step, observe results
5. Respond to users in natural, warm language
6. After each response, assess whether escalation to human is needed

# Response Format
- Brief empathy first, then provide the answer
- For step-by-step questions, use numbered lists
- For policy-related questions, cite specific clauses
- For sensitive operations, explain the subsequent process
```

### Context Assembly

```
┌─────────────────────────────────┐
│ System Prompt (~1.5K tokens)    │
├─────────────────────────────────┤
│ User Profile (~300 tokens)      │ ← VIP tier / Historical ticket count / Preferred language
├─────────────────────────────────┤
│ User Recent Tickets (~1K tokens)│ ← Summary of last 3 tickets
├─────────────────────────────────┤
│ RAG Retrieval Results (~5K tokens)│ ← Top-5 document chunks
├─────────────────────────────────┤
│ Conversation History (~3K tokens)│ ← Last 10 turns
├─────────────────────────────────┤
│ Tool Call Results (~2K tokens)  │ ← Order/Member API returns
├─────────────────────────────────┤
│ User Current Input               │
└─────────────────────────────────┘
```

### Few-Shot Examples

#### Example 1: Simple FAQ
**User:** "What is the return process?"

**AI:** "Hello! Our return process is very simple, just 3 steps:
1. Click 'Apply for Return' in 'My Orders' and select the return reason
2. After approval, you will receive the return address and shipping instructions (approval is usually completed within 1 business day)
3. Once we receive the return and confirm it's correct, the refund will be issued to your original payment method within 3-5 business days

Tip: Please apply for a return within 7 days of receiving the item. Any other questions?"

#### Example 2: Requires Query Tool
**User:** "Has the earphones I bought the day before yesterday been shipped? The order number is probably ORD123456"

**AI:** "Sure, let me check the status of order ORD123456 for you..."

[Call query_order tool]
[Return: Shipped, tracking number SF1234567890, dispatched from Shenzhen on 2026-06-06 15:30]

"Found it! Your order was shipped from Shenzhen on the afternoon of June 6th, tracking number SF1234567890 (SF Express), currently in transit.

Generally, after shipping from Shenzhen, delivery within the province takes 1-2 days. Would you like me to track the logistics details for you?"

#### Example 3: Requires Escalation to Human
**User:** "Your product quality is terrible! It broke after just three days of use. I want a refund and I want to file a complaint!"

**AI:** "I'm very sorry for such an unpleasant experience. I can understand how you feel.

This issue is quite complex. To provide you with the best solution, let me transfer you to our senior customer service specialist, okay? They will prioritize your case, and the expected wait time is no more than 3 minutes.

Before the transfer, I've already recorded the following information for you:
- Order Number: ORD123456
- Issue: Product quality problem, malfunction within three days
- Request: Refund + Complaint

Would you mind waiting a moment?"

---

## Phase 5: AI UX Design

### Interaction Mode Selection

| Decision | Choice | Rationale |
|------|------|------|
| AI Interaction Mode | Chat as primary + Copilot Sidebar (agent-facing) | Conversational is most natural for end users; sidebar assists agents |
| Streaming Output | Yes | Let users perceive that AI is working |
| Confidence Display | Show only for low confidence | Avoid excessive interference; only prompt when uncertain |
| Source Citation | Yes, expandable on click | Build trust |
| AI Identity Label | Clearly labeled "AI Assistant" | Avoid impersonating humans |

### Interaction State Design

| State | UI Display | User Action |
|------|--------|---------|
| Thinking | Typing animation + "Looking for answers..." | None (waiting) |
| Tool Calling | "Querying your order information..." | None (waiting) |
| Answer Output | Streaming text output | Reading |
| Low Confidence | Answer + ⚠️ "The above information may not be fully accurate" | Can click "Escalate to Human" |
| Confirmation Needed | Suggested action + "Confirm" button | Confirm / Modify / Cancel |
| Escalating to Human | "Transferring you now..." | Wait / Cancel |
| Escalated to Human | Conversation log + Transfer notice | Continue with human agent |
| Error | "Sorry, I encountered an issue" + Retry / Escalate to Human | Retry / Escalate to Human |

### Agent-Facing (Copilot Sidebar)

```
┌──────────────────┬──────────────────────┐
│ Conversation Area │ AI Copilot           │
│                  │                      │
│ [User]: Return... │ 💡 Suggested Reply:  │
│                  │ Per Return Policy     │
│                  │ Clause 3...          │
│                  │                      │
│ [Agent]:         │ 📋 Reference Ticket: │
│                  │ #1234 Similar Return │
│                  │ Case                 │
│                  │                      │
│                  │ ⚡ Quick Actions:    │
│                  │ [Initiate Refund]    │
│                  │ [Send Return Guide]  │
└──────────────────┴──────────────────────┘
```

---

## Phase 6: Evaluation Plan

### Golden Dataset

| Metric | Target Value |
|------|--------|
| Total Samples | 500+ |
| Common Scenarios (FAQ / Order Inquiry) | 60% |
| Edge Scenarios (Complex Complaints / Multi-Intent) | 20% |
| Adversarial Scenarios (Injection / Jailbreak) | 10% |
| Safety Scenarios (PII / Harmful Content) | 10% |

### Evaluation Metrics

| Dimension | Metric | Target | Measurement Method |
|------|------|--------|---------|
| Accuracy | Answer Correctness Rate | >90% | Golden Dataset + LLM-as-Judge |
| Faithfulness | RAGAS Faithfulness | >0.90 | Automated evaluation |
| Completeness | Information Coverage Rate | >85% | LLM-as-Judge |
| Safety | Harmful Output Rate | <0.1% | Safety test set |
| Latency | P95 Time-to-First-Token | <2s | Production monitoring |
| User Satisfaction | 👍 Ratio | >85% | Online feedback |

### Evaluation Pipeline

```
Every code/prompt change:
1. CI auto-runs Golden Dataset (500 items, ~10 min)
2. RAGAS metric check (Faithfulness > 0.90)
3. Safety test set check (0 harmful outputs)
4. Regression test (metrics must not drop by >3%)
5. Pass → 5% canary release → Observe for 1 day
6. Core metrics OK → Full rollout
```

---

## Phase 7: Security & Guardrails

### Security Architecture (Five-Layer Defense)

**Layer 1: Input Guardrails**
- Injection Detection: LLM classifier detects patterns like "ignore previous instructions"
- Jailbreak Detection: Detects role-playing, encoding bypasses
- PII Detection: Auto-masking of phone numbers / ID numbers / bank cards

**Layer 2: Access Control**
- Users can only query their own order/member information
- Agent tool permissions are tiered by role
- Strict tenant data isolation

**Layer 3: Model Security**
- System Prompt security hardening
- Strict separation of User Prompt and System Prompt
- Context data carries permission tags

**Layer 4: Output Guardrails**
- Content safety review (real-time per-token detection)
- Hallucination detection (claim-evidence consistency verification)
- PII masking
- Output format validation

**Layer 5: Audit & Monitoring**
- Complete logging of all AI interactions
- Anomaly detection (abnormal frequency / abnormal patterns)
- Circuit breaker: If safety rejection rate >5% within 10 minutes → Auto-switch to human-only mode

---

## Phase 8: Pricing Plan

### Pricing Model

| Tier | Price (CNY/month) | AI Ticket Quota | Agent Seats | Model Tier |
|------|------------|----------|-----------|---------|
| Starter | ¥2,999 | 2,000 | 5 | Haiku+Sonnet |
| Professional | ¥9,999 | 10,000 | 20 | Sonnet primary |
| Enterprise | ¥29,999 | 50,000 | Unlimited | Sonnet+Opus |
| Custom | On-demand | On-demand | On-demand | Customizable |

### Token Economics (Professional Plan)

| Metric | Value |
|------|---|
| Plan Monthly Fee | ¥9,999 |
| AI Monthly Interactions | 10,000 |
| Monthly Token Consumption | ~50M Input + ~10M Output |
| Monthly AI Inference Cost | ~¥2,500 |
| AI Gross Margin | ~75% |
| Other Costs (Servers / Labor / Ops) | ~¥3,000 |
| Overall Gross Margin | ~45% |

---

## Phase 9: Roadmap

### Now (This Quarter)
| Item | Goal | Dependency |
|------|------|------|
| Basic RAG Q&A Go Live | Cover 80% FAQ, accuracy >90% | Knowledge base preparation complete |
| Order/Member Query Agent | Auto-query, <3s response | Business system API integration |
| Smart Escalation to Human | Recognize 20+ escalation scenarios | Human CS system integration |

### Next (Next Quarter)
| Item | Goal | Dependency |
|------|------|------|
| Agent Copilot Sidebar | Improve agent efficiency by 30% | Agent workspace renovation |
| AI Proactive Service (Order anomaly alerts) | Proactive outreach rate >15% | Order system event integration |
| Multilingual Support (English first) | English answer accuracy >85% | English knowledge base + Embedding |

### Later (Long-term)
| Direction | What to Verify / Prepare |
|------|-----------------|
| AI Voice Customer Service | Speech recognition + synthesis + low latency |
| Fully Automated CS (AI-only) | Customer acceptance + AI accuracy meets targets |
| CS Agent Marketplace | Third-party Agent ecosystem |
---

## Phase 10: Compliance Considerations (Added in V1.1.0)

### EU AI Act Compliance Assessment

According to the EU AI Act risk classification, SmartCS falls under the **Limited Risk** category (Chatbot + Automated decision support), and must meet the following compliance requirements:

| Compliance Requirement | Status | Implementation Plan |
|---------|------|---------|
| Transparency Obligation | ✅ Implemented | AI identity label + "AI Assistant" clearly marked |
| Synthetic Content Labeling | ⚠️ Needs Supplement | Add explicit + implicit labeling for deep-synthetic content |
| Human Oversight | ✅ Implemented | HITL mechanism covers L2-L4 operations |
| User Right to Know | ✅ Implemented | First conversation informs user of AI identity and capability boundaries |
| Data Governance | ⚠️ Needs Supplement | Training data source logging + bias detection |

### China Deep Synthesis Regulation Compliance

| Compliance Requirement | Status | Implementation Plan |
|---------|------|---------|
| Algorithm Filing | ⚠️ To Complete | Generative AI service algorithm filing |
| Synthesis Labeling | ⚠️ Needs Supplement | Embed explicit + implicit labels in all AI-generated content |
| X-DeepSynth Response Header | ⚠️ Needs Supplement | Add synthesis labeling header to API responses |
| Content Moderation | ✅ Implemented | Five-layer security guardrails |
| User Real-Name Verification | ⚠️ Needs Supplement | Integrate phone number real-name authentication |
| Log Retention | ⚠️ Needs Supplement | Conversation log retention ≥ 6 months |

### Compliance Implementation Roadmap

| Phase | Timeline | Item |
|------|------|------|
| Short-term | Within 1 month | Add X-DeepSynth response header + synthesis labeling |
| Mid-term | Within 3 months | Complete algorithm filing + user real-name integration |
| Long-term | Within 6 months | Establish EU AI Act compliance documentation system + log retention system |

### Model Selection Compliance Considerations

| Consideration | Recommended Approach | Rationale |
|------|---------|------|
| Data Cross-Border | Domestic clients use domestic models (Qwen/DeepSeek) | Meet data localization requirements |
| Model Transparency | Prioritize models providing Model Cards | Meet EU AI Act transparency |
| Vendor Lock-in | Maintain at least 2 model suppliers | Reduce single-supplier risk |
| Open-Source Backup | Maintain open-source model deployment capability | Prepare for API service interruptions |

### Copyright Notice & Disclaimer

This case study (SmartCS AI Intelligent Customer Service) is a teaching example for the AI PM Workbench, intended for learning and reference only. Actual product design should be adapted to specific business scenarios, regulatory requirements, and organizational capabilities. The technical proposals and regulatory interpretations referenced herein may change due to policy updates or technological iteration.