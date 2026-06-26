# AI Engineering Interview — Competency Deep-Dive Guide

This file contains the detailed mental model, production context, interview questions, and rubric signals for each of the 10 AI Engineering competency domains. Read the relevant section when drilling, designing questions, or giving answer feedback.

---

## 1. LLM Fundamentals

### Mental Model
An LLM is a probability machine. Given a sequence of tokens, it predicts the next most likely token — repeatedly, until it generates an EOS token or hits the max length. Everything else (instructions, reasoning, context) is just shaping which tokens are likely.

**Key insight for SWEs:** Tokens ≠ words. "tokenization" is 2–3 tokens. This matters for cost, context window management, and multilingual failure modes.

### Production Scenarios
- A prompt that works perfectly in English fails in Vietnamese → likely a tokenization issue; the model was trained with far fewer Vietnamese tokens
- Costs spiked 300% after adding a feature → someone added a 4,000-token system prompt that runs on every call
- The model "forgets" instructions given early in a long conversation → lost-in-the-middle problem; position in context window matters

### Interview Questions
1. *(Screening)* "What's a context window and what do you do when your input exceeds it?"
2. *(Mid)* "A user sends a 50-page PDF to your chatbot. How does your system handle it?"
3. *(Senior)* "Explain temperature and top-p. When would you set temperature to 0 and why?"
4. *(Senior)* "What's the difference between a base model and an instruction-tuned model? When would you ever use a base model?"
5. *(Staff)* "You're selecting an LLM for a high-volume production feature. Walk me through your decision framework."

### Strong Signals
- Knows that input tokens cost less than output tokens on most APIs
- Understands that temperature=0 is not truly deterministic (it's greedy, not sampling)
- Can explain why multilingual tasks are harder even for large models
- Knows the lost-in-the-middle phenomenon and designs prompts to avoid it

### Weak Signals
- Thinks "context window" means how much the model can remember across conversations
- Thinks temperature=1 is always better for creativity (misses consistency trade-off)
- No intuition for token costs or context window limits

---

## 2. Prompt Engineering

### Mental Model
Prompts are code. They have inputs, outputs, edge cases, and bugs. Good prompt engineers write prompts like they write functions: with explicit contracts, tested against known inputs, version-controlled, and monitored in production.

**Key insight for SWEs:** The difference between a "prompt user" and a "prompt engineer" is: systematic testing, regression suites, and treating prompt changes like deploys.

### Production Scenarios
- A prompt that worked great in testing produces inconsistent JSON in production → needs explicit JSON mode + schema validation, not just "please respond in JSON"
- Adding a few-shot example accidentally causes the model to refuse certain valid requests → negative examples contaminate the pattern
- A user discovered that saying "ignore previous instructions" leaks the system prompt → prompt injection vulnerability in a B2B product

### Interview Questions
1. *(Screening)* "What's the difference between zero-shot and few-shot prompting? When does few-shot help?"
2. *(Mid)* "How do you test whether a prompt change improved or degraded output quality?"
3. *(Mid)* "What is chain-of-thought prompting and when does it hurt more than it helps?"
4. *(Senior)* "A user found they can make your AI assistant ignore its safety instructions by embedding a command in a document it processes. How do you fix this?"
5. *(Senior)* "You need your LLM to always output valid JSON with a specific schema. How do you guarantee this?"
6. *(Staff)* "Design a prompt testing infrastructure for a team of 5 AI engineers shipping 10 prompt changes per week."

### Strong Signals
- Treats prompt testing like software testing — regression suite, golden examples, evaluation metrics
- Knows structured output tools (JSON mode, function calling, Pydantic with instructor) rather than just "ask it to return JSON"
- Understands indirect prompt injection (via tool results, not just user input)
- Can articulate the system/user/assistant turn structure and why role matters

### Weak Signals
- "I just try different things until it works"
- No mention of testing or version control for prompts
- Thinks prompt injection = SQL injection (misses the LLM-specific nature)

---

## 3. RAG Architecture

### Mental Model
RAG is a retrieval system wired to a generation system. The quality of the answer is bounded by the quality of the retrieval. If you retrieve the wrong chunks, no amount of LLM intelligence can fix it.

**SWE analogy:** RAG is like a smart database query + templated response generator. The "smart" part is semantic search. The hard parts are chunking (schema design) and retrieval quality (query optimization).

### Core pipeline
```
Documents → [Chunk] → [Embed] → [Store in Vector DB]
User query → [Embed query] → [Retrieve top-K chunks] → [Rerank] → [Prompt with context] → [LLM] → Answer
```

### Production Scenarios
- Users report the chatbot gives wrong answers → check retrieval first (retrieve the same query yourself — is the right chunk even coming back?)
- Retrieval is slow under load → pgvector with HNSW index; check approximate vs exact search trade-offs
- The system answers correctly for English queries but poorly for Vietnamese → embedding model is English-biased; switch to multilingual embeddings (e.g., multilingual-e5)
- Adding new documents doesn't improve answers → index refresh isn't running; stale index

### Interview Questions
1. *(Screening)* "What is RAG and why would you use it instead of just giving the LLM a huge context?"
2. *(Mid)* "What chunking strategy would you use for a technical documentation site vs. a collection of PDFs with tables?"
3. *(Mid)* "Your RAG system has low retrieval recall — the right chunks aren't being retrieved. Walk me through diagnosis."
4. *(Senior)* "Compare hybrid search (BM25 + vector) vs. pure vector search. When does hybrid win?"
5. *(Senior)* "What is HyDE (Hypothetical Document Embedding) and when would you use it?"
6. *(Senior)* "Design a RAG system for a legal firm with 500,000 contracts. Include chunking strategy, retrieval, reranking, and evaluation."
7. *(Staff)* "Your RAG pipeline works in dev but has 40% lower faithfulness in production. What are the possible causes?"

### Strong Signals
- Immediately asks about chunk size and overlap trade-offs rather than treating it as a default
- Knows that retrieval quality (recall@K) and answer faithfulness are separate metrics
- Has used or can describe RAGAS or a similar RAG evaluation framework
- Understands parent-child chunking: retrieve child chunks but send parent chunk to LLM for context

### Weak Signals
- Thinks RAG = "just embed everything and search"
- No mention of reranking
- Can't describe how to evaluate retrieval quality
- Doesn't distinguish between retrieval failures and generation failures when troubleshooting

---

## 4. AI Agents

### Mental Model
An agent is an LLM with a loop: observe → think → act → observe. The LLM decides what tool to call, calls it, reads the result, and decides what to do next. This continues until the agent decides it's done — or gets stuck.

**SWE analogy:** Agents are like microservices where the routing logic is an LLM. Instead of deterministic if/else routing, the LLM decides which service to call. This means the failure modes are completely different — and harder to predict.

### Agent Anatomy
- **Brain**: The LLM (decides what to do next)
- **Tools**: Functions the LLM can call (search, database query, API call, code execution)
- **Memory**: What the agent remembers (conversation history, retrieved facts, summaries)
- **Planning**: How it breaks down complex tasks (ReAct: reason + act, plan-and-execute)

### Production Scenarios
- Agent keeps calling the search tool in a loop without making progress → missing termination condition; add a max_steps guard
- Agent calls a database write tool with hallucinated parameters → all agent tool calls should be validated + confirmed before destructive actions
- Agent costs $20 per run in testing → it called 15 tools in a chain; each called an LLM; add cost logging and circuit breakers
- Agent works perfectly for 90% of queries but catastrophically fails on 10% → need evaluation + human-in-the-loop for low-confidence cases

### Interview Questions
1. *(Screening)* "What's the difference between a chain and an agent?"
2. *(Mid)* "What makes a good tool definition for an AI agent? What makes a bad one?"
3. *(Mid)* "How would you prevent an agent from running in an infinite loop?"
4. *(Senior)* "Your agent needs to write to a production database based on user instructions. What guardrails do you add?"
5. *(Senior)* "Compare LangGraph vs. CrewAI for a multi-agent customer support escalation system."
6. *(Senior)* "What is prompt injection via tool results and how do you mitigate it?"
7. *(Staff)* "Design a multi-agent system for automated code review. Include agent roles, orchestration pattern, failure modes, and evaluation."

### Strong Signals
- Knows the ReAct loop by name and can explain why it works
- Immediately raises cost and loop prevention as concerns
- Distinguishes between single-agent and multi-agent patterns and when each applies
- Has thought about human-in-the-loop checkpoints for high-stakes actions
- Mentions MCP (Model Context Protocol) as a standardized tool interface

### Weak Signals
- Thinks "agent" just means a chatbot with a system prompt
- No mention of failure modes or cost control
- Can't distinguish LangChain chains from LangGraph agents

---

## 5. Fine-Tuning

### Mental Model
Fine-tuning adjusts the model's weights to make certain behaviors more likely. Use it to change *how* the model responds (style, format, domain vocabulary, task patterns) — not to add new knowledge (that's RAG's job).

**SWE analogy:** Fine-tuning is like forking a library and patching it for your specific needs. It's powerful but now you own the maintenance. LoRA is like writing a lightweight plugin that patches behavior without touching the core library.

### Decision framework: when to fine-tune
Fine-tune when:
- The desired behavior is a pattern the model needs to internalize (format, style, structured output)
- Few-shot prompting is too expensive (large examples in every request)
- The model needs to "speak" a domain vocabulary it wasn't trained on

Do NOT fine-tune when:
- You want to add factual knowledge (use RAG — fine-tuned facts are hard to update and often hallucinated anyway)
- You just need the model to follow instructions (better prompt engineering usually fixes this)

### LoRA in plain terms
LoRA freezes the full model and adds small trainable matrices to specific layers. Instead of updating 7 billion parameters, you update ~2 million. This makes fine-tuning feasible on a single GPU and produces an "adapter" that can be merged back or swapped out.

### Interview Questions
1. *(Screening)* "When would you choose fine-tuning over RAG over prompt engineering?"
2. *(Mid)* "What is LoRA and why is it usually preferred over full fine-tuning?"
3. *(Mid)* "How do you prepare a dataset for fine-tuning? What makes a good training example?"
4. *(Senior)* "What is catastrophic forgetting and how does LoRA help prevent it?"
5. *(Senior)* "You fine-tuned a model for legal document summarization but it now performs worse on general tasks. What happened and how would you fix it?"
6. *(Staff)* "Design the infrastructure to fine-tune, evaluate, version, and deploy a custom LLM adapter for a legal tech product."

### Strong Signals
- Immediately distinguishes "knowledge" (RAG) from "behavior" (fine-tuning)
- Knows LoRA rank as a hyperparameter to tune
- Understands that data quality >> data quantity (2k great examples beat 200k noisy ones)
- Has thought about evaluation during and after fine-tuning (not just training loss)

### Weak Signals
- Thinks fine-tuning = giving the model new information
- Can't explain what LoRA does without just naming it
- No mention of dataset quality or catastrophic forgetting

---

## 6. Evaluation & Evals

### Mental Model
Evals are to AI engineers what tests are to software engineers — except harder. Code is deterministic; LLM outputs are probabilistic. Your eval suite is only as good as your golden set. Treat evals as infrastructure, not an afterthought.

**SWE analogy:** Evals = integration tests, but for model behavior. A prompt change without running evals is like a code change without running tests — you're guessing.

### Evaluation pyramid
```
Level 3: Human evaluation (gold standard, expensive, slow)
Level 2: LLM-as-judge (scalable, biased toward verbosity and agreement)
Level 1: Automated metrics (fast, cheap, but often miss the point)
```

### Key metrics
- **BLEU/ROUGE**: N-gram overlap with reference. Fast, cheap, and often wrong for open-ended generation.
- **BERTScore**: Semantic similarity via embeddings. Better than BLEU, still misses reasoning quality.
- **LLM-as-judge**: A stronger model scores the output. Best for nuanced quality; biased toward longer, more confident-sounding answers.
- **Task-specific**: F1 for QA, accuracy for classification, faithfulness for RAG, code execution for code generation.
- **RAG-specific (RAGAS)**: Faithfulness, answer relevance, context precision, context recall.

### Interview Questions
1. *(Screening)* "How would you test whether your AI feature is working correctly?"
2. *(Mid)* "What's wrong with using BLEU score to evaluate a customer support chatbot?"
3. *(Mid)* "What is LLM-as-judge and what are its failure modes?"
4. *(Senior)* "Design an evaluation pipeline for a RAG-powered document Q&A system."
5. *(Senior)* "How do you build and grow a golden evaluation set over time?"
6. *(Staff)* "You need to run evals on every prompt change before deploying. Design the eval infrastructure."

### Strong Signals
- Distinguishes retrieval quality metrics from generation quality metrics
- Knows LLM-as-judge verbosity bias and has mitigation strategies (swap order of options, use a rubric)
- Has a process for growing the golden set from production data (log → sample → annotate)
- Treats failing evals like failing CI — block deploy, investigate, fix

### Weak Signals
- "We'd just try it out and see how it performs"
- Thinks BLEU/ROUGE are good for chatbot evaluation
- No mention of golden sets or regression testing

---

## 7. LLM Observability

### Mental Model
If you can't see what your LLM is doing in production, you can't improve it. Observability for LLMs includes everything APM covers (latency, errors, throughput) plus LLM-specific signals: token counts, cost, prompt versions, and the full prompt/response pair for debugging.

**SWE analogy:** This is APM (Datadog, Grafana) but you also need to log the actual prompt and completion — because "the request succeeded" doesn't mean "the LLM said something useful."

### What to observe
- **Inputs**: Full prompt (system + user), model, temperature, max tokens
- **Outputs**: Completion, finish reason (stop vs. length vs. content_filter)
- **Performance**: TTFT (time to first token), total latency, token counts (input/output), cost per call
- **Quality signals**: Thumbs up/down from users, LLM-as-judge inline scoring, refusal rate
- **Agent-specific**: Step count, tool calls made, tools that errored, total chain cost

### Interview Questions
1. *(Mid)* "What would you log for every LLM call in production and why?"
2. *(Mid)* "How would you monitor for cost anomalies in an LLM-powered feature?"
3. *(Senior)* "A user reports the chatbot gave a wrong answer. How do you investigate?"
4. *(Senior)* "Compare LangSmith, Helicone, and Langfuse. When would you choose each?"
5. *(Staff)* "Design an observability stack for a multi-agent system with 10,000 daily active users."

### Strong Signals
- Knows the difference between TTFT and total latency — and why TTFT matters more for streaming UX
- Has thought about prompt versioning: you need to know which prompt version produced which output
- Understands semantic caching trade-offs (stale answers vs. cost reduction)

### Weak Signals
- Only mentions "logging errors"
- No mention of cost monitoring or token tracking
- Doesn't know what TTFT means

---

## 8. AI Safety & Guardrails

### Mental Model
LLM safety is defense in depth — no single control is sufficient. Combine input filtering, output filtering, trust boundaries, system prompt hardening, and human review for high-stakes actions.

**SWE analogy:** This is like API security — but instead of SQL injection, you have prompt injection. Instead of XSS, you have model jailbreaks. The attack surface is the entire natural language input space, which is much harder to validate than structured inputs.

### Threat model for LLM applications
- **Prompt injection (direct)**: User manipulates the system prompt via the user turn ("Ignore previous instructions and...")
- **Prompt injection (indirect)**: Malicious instructions embedded in documents or tool results the agent processes
- **Jailbreaking**: User finds creative ways to bypass content policies
- **Data exfiltration**: User tricks the model into revealing system prompt contents or other users' data
- **Excessive agency**: Agent takes destructive real-world actions (delete files, send emails, make purchases) without confirmation

### Interview Questions
1. *(Mid)* "A user discovers they can make your customer service bot reveal your system prompt. How do you prevent this?"
2. *(Mid)* "What's the difference between direct and indirect prompt injection? Give an example of each."
3. *(Senior)* "Your agent has access to a user's email account. What guardrails do you put in place before it can take actions?"
4. *(Senior)* "Design an output validation layer for an LLM that generates legal documents."
5. *(Staff)* "You're building an AI feature for a healthcare product. What's your safety architecture?"

### Strong Signals
- Immediately raises principle of least capability (agents should have minimum permissions needed)
- Knows indirect prompt injection (via tool results, not just user input)
- Proposes defense in depth — not a single silver bullet
- Thinks about PII handling and data residency proactively

### Weak Signals
- "We'd use OpenAI's content moderation"
- No mention of indirect injection
- Treats safety as an afterthought ("we'd add guardrails later")

---

## 9. Production LLM Systems

### Mental Model
Building on LLMs in production is software engineering with a probabilistic, expensive, latency-variable dependency. The reliability patterns SWEs already know (retries, circuit breakers, caching, graceful degradation) all apply — with LLM-specific additions.

### Key additions over standard SWE
- **Model deprecation**: OpenAI deprecates model versions; you need versioning and migration strategy
- **Semantic caching**: Cache by meaning, not exact string — reduces costs but introduces staleness risk
- **Token budget management**: Unlike a DB query, an LLM response cost is variable and hard to cap exactly
- **Streaming UX**: Streaming tokens to the user changes the UX and error handling significantly
- **Fallback hierarchy**: If GPT-4o fails → try Claude Sonnet → try a smaller model → return graceful error

### Interview Questions
1. *(Mid)* "How would you implement a fallback if your primary LLM API is unavailable?"
2. *(Mid)* "What is semantic caching and when would you use it? What are the risks?"
3. *(Senior)* "A new model version was released with breaking changes. How do you handle the migration?"
4. *(Senior)* "Design an LLM gateway that routes requests across multiple providers based on cost, latency, and availability."
5. *(Staff)* "You're deploying an open-source LLM (Llama 3) for a privacy-sensitive product. Walk me through the serving infrastructure."

### Strong Signals
- Immediately applies retry/circuit breaker patterns from existing SWE knowledge
- Has a clear model versioning and migration strategy
- Understands the difference between managed inference (OpenAI/Anthropic) and self-hosted (vLLM, Ollama)

### Weak Signals
- No mention of fallback or graceful degradation
- Hasn't thought about model versioning or deprecation risk

---

## 10. LLM System Design

### Mental Model
LLM system design interviews combine traditional system design (data flow, API design, scalability) with AI-specific decisions (RAG vs. fine-tune, model selection, evaluation strategy, cost architecture). The best candidates make all AI decisions within a software engineering framework.

### The AI design decision framework
Before designing anything, answer:
1. **What does "correct" look like?** → Defines the evaluation strategy
2. **What knowledge does the model need?** → RAG vs. fine-tune vs. prompting
3. **What are the latency and cost constraints?** → Model size, caching, streaming
4. **What are the failure modes and mitigations?** → Hallucination, retrieval miss, agent loop, cost blowup
5. **How will you know it's working in production?** → Observability, user feedback loops

### Common design questions
- "Design an AI-powered customer support chatbot for a SaaS company"
- "Design an AI search system for a document repository with 1 million PDFs"
- "Design a code review assistant that integrates with GitHub PRs"
- "Design an AI writing assistant for a content platform"
- "Design an AI copilot for a legal document review workflow"

### Rubric for design answers
| Dimension | What to look for |
|---|---|
| Problem framing | Do they ask clarifying questions before designing? |
| Data flow | Can they trace the full request lifecycle? |
| AI decision | Do they justify RAG vs. fine-tune vs. prompt? |
| Evaluation | Do they define what "correct" means and how to measure it? |
| Failure modes | Do they name at least 3 failure modes and mitigations? |
| Observability | Do they design for debugging and monitoring from the start? |
| Cost/latency | Do they make cost-aware design choices? |
| Iteration | Do they describe a plan to improve the system post-launch? |

### Strong Signals
- Asks about latency budget, accuracy requirements, and cost constraints before starting
- Distinguishes between retrieval failures and generation failures in their failure mode analysis
- Has a concrete evaluation strategy (not just "we'll see how it performs")
- Proposes a feedback loop from production data back to eval set improvement

### Weak Signals
- Jumps straight to "we'd use RAG" without discussing trade-offs
- No evaluation strategy in the design
- Doesn't mention observability
- Only one or zero failure modes mentioned
