# RAG Production Engineering

> Complete methodology for building, optimizing, and operating Retrieval-Augmented Generation systems in production. From architecture decisions through chunking strategies, embedding selection, retrieval tuning, evaluation frameworks, and production monitoring.

## Quick Health Check

Score your RAG system (1 = poor, 2 = okay):

| Signal | What to Check |
|--------|--------------|
| Retrieval relevance | Top-5 results contain answer >90% of time |
| Answer accuracy | Generated answers faithful to retrieved context |
| Latency | End-to-end response <3s (p95) |
| Chunk quality | Chunks are self-contained, meaningful units |
| Evaluation coverage | Automated eval suite with 50+ test cases |
| Index freshness | Documents indexed within SLA of source update |
| Failure handling | Graceful degradation when retrieval returns nothing |
| Cost efficiency | Cost per query within budget (<$0.05 typical) |

**Score: /16** — Below 10 = critical issues. Below 12 = significant gaps. 14+ = production-ready.

---

## Phase 1: Architecture Decision

### When to Use RAG (vs Alternatives)

| Approach | Use When | Don't Use When |
|----------|----------|----------------|
| **RAG** | Dynamic knowledge, source attribution needed, data changes frequently | Static small dataset (<10 pages), real-time data needed |
| **Fine-tuning** | Consistent style/format needed, domain-specific language | Frequently changing data, need source citations |
| **Long context** | Small corpus (<200K tokens), simple Q&A | Large corpus, cost-sensitive, need precise attribution |
| **RAG + Fine-tuning** | Domain-specific language AND dynamic knowledge | Budget-constrained, simple use case |
| **Agentic RAG** | Multi-step reasoning, tool use, complex queries | Simple lookup, latency-critical |

### RAG Architecture Brief

```yaml
# Fill this out before building
project:
  name: ""
  use_case: ""  # Q&A, search, summarization, analysis, chatbot
  domain: ""    # legal, medical, technical, general

data:
  sources: []        # PDF, web, database, API, markdown, code
  volume: ""         # <1K docs, 1K-100K, 100K-1M, >1M
  update_frequency: "" # real-time, daily, weekly, static
  avg_doc_length: "" # <1 page, 1-10 pages, 10-100 pages, >100 pages
  languages: []

requirements:
  latency_p95: ""    # <1s, <3s, <10s, <30s
  accuracy_target: "" # 85%, 90%, 95%, 99%
  citations_needed: true
  access_control: false
  compliance: []     # GDPR, HIPAA, SOC2, none

budget:
  monthly_queries: ""
  cost_per_query_target: ""
  infra_budget: ""
```

### Architecture Patterns

#### Basic RAG
```
Query → Embed → Vector Search → Top-K → LLM → Answer
```
Best for: Simple Q&A, <100K documents, single data source.

#### Advanced RAG
```
Query → Classify → Rewrite → Embed → Hybrid Search → Rerank → Filter → LLM → Answer + Citations
```
Best for: Production systems, mixed document types, accuracy-critical.

#### Agentic RAG
```
Query → Planner → [Search₁, Search₂, SQL, API] → Synthesize → Verify → Answer
```
Best for: Complex multi-step reasoning, multiple data sources, analytical queries.

#### Graph RAG
```
Query → Entity Extract → Graph Traverse → Subgraph → Context Assembly → LLM → Answer
```
Best for: Relationship-heavy data (org charts, legal references, knowledge bases).

### Architecture Decision Tree

```
Is your corpus < 200K tokens?
  YES → Try long-context first (cheapest, simplest)
  NO → Continue

Do you need source citations?
  YES → RAG (not fine-tuning)
  NO → Consider fine-tuning if style matters

Single data source, simple queries?
  YES → Basic RAG
  NO → Continue

Multi-step reasoning or multiple sources?
  YES → Agentic RAG
  NO → Advanced RAG
```

---

## Phase 2: Document Processing & Chunking

### Document Processing Pipeline

```
Source → Extract → Clean → Chunk → Enrich → Embed → Index
```

#### Extraction by Source Type

| Source | Tool/Method | Gotchas |
|--------|------------|---------|
| PDF (text) | PyMuPDF, pdfplumber | Tables break, headers repeat per page |
| PDF (scanned) | Tesseract, AWS Textract, Azure DI | OCR errors in technical terms |
| HTML/Web | BeautifulSoup, Trafilatura | Nav/footer pollution, JS-rendered content |
| Markdown | Direct parse | Frontmatter, relative links |
| Code | Tree-sitter, AST | Preserve structure, handle imports |
| Word/PPTX | python-docx, python-pptx | Formatting loss, embedded objects |
| Database | SQL export | Schema context needed |
| Audio/Video | Whisper → text | Timestamp alignment, speaker diarization |

#### Cleaning Checklist

- [ ] Remove headers/footers/page numbers
- [ ] Strip navigation, ads, boilerplate
- [ ] Normalize whitespace and encoding (UTF-8)
- [ ] Resolve abbreviations in domain text
- [ ] Handle tables (convert to structured text or separate)
- [ ] Preserve code blocks with language tags
- [ ] Remove duplicate content across documents
- [ ] Extract and preserve metadata (title, author, date, source URL)

### Chunking Strategies

| Strategy | Chunk Size | Best For | Weakness |
|----------|-----------|----------|----------|
| **Fixed-size** | 256-512 tokens | Homogeneous text, fast prototyping | Breaks mid-sentence/thought |
| **Recursive character** | 256-1024 tokens | General purpose (LangChain default) | May split related paragraphs |
| **Semantic** | Variable | High-quality retrieval, mixed content | Slower, needs embedding model |
| **Document structure** | Section-based | Well-structured docs (markdown, HTML) | Uneven chunk sizes |
| **Sentence window** | 3-5 sentences | Precise retrieval, reranking | More chunks to manage |
| **Parent-child** | Small retrieve, large context | Best of both worlds | Complex implementation |
| **Agentic** | Full section/doc | Complex reasoning | Higher token cost |

### Chunking Decision Guide

```
Is your content well-structured (headers, sections)?
  YES → Document structure chunking
  NO → Continue

Is retrieval precision critical (legal, medical)?
  YES → Sentence window + reranking
  NO → Continue

Mixed content types in same corpus?
  YES → Semantic chunking
  NO → Recursive character (start here, optimize later)
```

### Chunking Rules

1. **Always overlap** — 10-20% overlap prevents context loss at boundaries
2. **Chunk size matters** — Smaller = more precise retrieval, larger = more context. Start at 512 tokens, tune with eval
3. **Preserve structure** — Don't break tables, code blocks, or lists mid-element
4. **Include metadata** — Every chunk needs: source document, section title, page/position, timestamp
5. **Test with real queries** — The "right" chunk size depends on your actual query patterns
6. **Parent-child for production** — Retrieve small chunks, expand to parent for LLM context

### Chunk Metadata Schema

```yaml
chunk:
  id: "doc-123-chunk-7"
  text: "..."
  metadata:
    source_id: "doc-123"
    source_title: "Q3 Financial Report"
    source_url: "https://..."
    section_title: "Revenue Analysis"
    page_number: 12
    position: 7           # chunk position in document
    total_chunks: 23
    created_at: "2026-03-24T04:00:00Z"
    updated_at: "2026-03-24T04:00:00Z"
    content_type: "text"  # text, table, code, image_caption
    language: "en"
    # Domain-specific
    access_level: "internal"
    department: "finance"
```

---

## Phase 3: Embedding Models

### Embedding Model Selection

| Model | Dimensions | Context | Speed | Quality | Cost |
|-------|-----------|---------|-------|---------|------|
| **text-embedding-3-small** (OpenAI) | 1536 | 8191 | Fast | Good | $0.02/1M tokens |
| **text-embedding-3-large** (OpenAI) | 3072 | 8191 | Medium | Excellent | $0.13/1M tokens |
| **Cohere embed-v4** | 1024 | 512 | Fast | Excellent | $0.10/1M tokens |
| **Voyage-3** | 1024 | 32K | Medium | Excellent | $0.06/1M tokens |
| **BGE-large-en-v1.5** (open) | 1024 | 512 | Self-host | Very Good | Free (compute) |
| **GTE-Qwen2** (open) | Various | 8192 | Self-host | Excellent | Free (compute) |
| **Nomic-embed-text** (open) | 768 | 8192 | Self-host | Good | Free (compute) |

### Selection Rules

1. **Start with OpenAI text-embedding-3-small** — best cost/quality ratio for most use cases
2. **Upgrade to large/Voyage-3** when eval shows retrieval gaps
3. **Use open models** when: data can't leave your infra, cost-sensitive at scale (>10M chunks), need fine-tuning
4. **Match chunk size to model context** — don't exceed model's context window
5. **Same model for indexing AND querying** — ALWAYS. Mixing models = broken retrieval
6. **Benchmark on YOUR data** — MTEB scores don't predict domain-specific performance

### Embedding Best Practices

- **Normalize embeddings** before storing (L2 normalization for cosine similarity)
- **Batch embed** documents (not one-by-one) for efficiency
- **Cache embeddings** — re-embedding is expensive and slow
- **Version your embeddings** — when you change models, re-embed everything
- **Instruction-prefix for asymmetric models** — some models need "query: " vs "passage: " prefixes
- **Dimensionality reduction** — text-embedding-3 models support Matryoshka (lower dims for speed, test quality)

---

## Phase 4: Vector Database & Indexing

### Vector Database Selection

| Database | Type | Scale | Speed | Features | Best For |
|----------|------|-------|-------|----------|----------|
| **Pinecone** | Managed | Billions | Fast | Metadata filter, namespaces | Production SaaS, zero-ops |
| **Weaviate** | Managed/Self | Millions | Fast | Hybrid search, modules | Mixed search needs |
| **Qdrant** | Managed/Self | Billions | Very Fast | Payload filters, sparse vectors | Performance-critical |
| **Chroma** | Embedded | <1M | Good | Simple API, local | Prototyping, small scale |
| **pgvector** | Extension | Millions | Good | SQL, existing Postgres | Already have Postgres |
| **Milvus** | Self-hosted | Billions | Fast | GPU support, hybrid | Large-scale self-hosted |
| **LanceDB** | Embedded | Millions | Fast | Serverless, multi-modal | Cost-sensitive, serverless |

### Selection Decision

```
Prototyping or <100K chunks?
  → Chroma or LanceDB (embedded, no server)

Already running PostgreSQL?
  → pgvector (add extension, done)

Production, want zero-ops?
  → Pinecone or Weaviate Cloud

Need hybrid search (vector + keyword)?
  → Weaviate or Qdrant

>100M vectors, self-hosted?
  → Milvus or Qdrant
```

### Indexing Strategy

| Index Type | Speed | Recall | Memory | Use When |
|-----------|-------|--------|--------|----------|
| **HNSW** | Very Fast | 95-99% | High | Default choice, <10M vectors |
| **IVF-PQ** | Fast | 90-95% | Low | >10M vectors, memory-constrained |
| **Flat/Brute** | Slow | 100% | High | <100K vectors, accuracy-critical |
| **ScaNN** | Very Fast | 95-99% | Medium | Google ecosystem, large scale |

### Index Configuration Rules

1. **HNSW: M=16, efConstruction=200, efSearch=100** — good defaults, tune from here
2. **Build index AFTER bulk loading** — not during insertion
3. **Use metadata filters BEFORE vector search** — reduces search space dramatically
4. **Namespace/collection per tenant** — for multi-tenant access control
5. **Monitor index health** — fragmentation, query latency percentiles

---

## Phase 5: Retrieval Engineering

### Query Processing Pipeline

```
User Query
  → Query Understanding (classify intent)
  → Query Transformation (rewrite, expand, decompose)
  → Retrieval (vector + keyword + filters)
  → Post-Retrieval (rerank, filter, deduplicate)
  → Context Assembly (order, truncate, format)
  → LLM Generation
  → Post-Processing (citations, formatting)
```

### Query Transformation Techniques

| Technique | What It Does | When to Use |
|-----------|-------------|-------------|
| **Query rewriting** | LLM rewrites for better retrieval | Conversational queries, vague questions |
| **HyDE** | Generate hypothetical answer, embed that | Semantic gap between query and docs |
| **Query decomposition** | Break complex query into sub-queries | Multi-part questions |
| **Step-back prompting** | Ask a more general question first | Specific queries that miss context |
| **Query expansion** | Add synonyms/related terms | Domain jargon, acronyms |
| **Multi-query** | Generate N query variants, union results | Improve recall for ambiguous queries |

### Hybrid Search

Combine vector similarity with keyword matching for best results:

```
Score = α × vector_score + (1 - α) × bm25_score
```

**Tuning α:**
- α = 0.7 (default) — mostly semantic, some keyword
- α = 0.5 — equal weight (good for technical docs with specific terms)
- α = 0.3 — mostly keyword (good for exact match needs, codes, IDs)

### Reranking

Reranking dramatically improves precision. Retrieve more (top-20), rerank to fewer (top-5).

| Reranker | Quality | Speed | Cost |
|----------|---------|-------|------|
| **Cohere Rerank** | Excellent | Fast | $2/1K queries |
| **Voyage Rerank** | Excellent | Fast | $0.05/1M tokens |
| **BGE-reranker-v2** | Very Good | Self-host | Free (compute) |
| **Cross-encoder** | Best | Slow | Free (compute) |
| **ColBERT** | Very Good | Medium | Free (compute) |
| **LLM-as-reranker** | Excellent | Slow | API cost |

### Retrieval Rules

1. **Always rerank** in production — it's the highest-ROI improvement
2. **Retrieve more, show less** — fetch top-20, rerank to top-5
3. **Hybrid search > pure vector** — keyword matching catches what embeddings miss
4. **Filter before search** — metadata filters (date, department, access level) reduce noise
5. **Deduplicate** — same content from different sources = wasted context
6. **Set similarity threshold** — don't return irrelevant results (typical: 0.7 for cosine)
7. **Return "I don't know"** — when no chunk meets threshold, say so. Never hallucinate from thin context

---

## Phase 6: Context Assembly & Generation

### Context Window Management

```yaml
context_budget:
  total_tokens: 128000      # Model context window
  system_prompt: 2000       # Instructions, persona, rules
  retrieved_context: 80000  # Retrieved chunks
  conversation_history: 20000  # Prior turns
  generation_buffer: 26000  # Room for response
```

### Context Assembly Rules

1. **Order matters** — put most relevant chunks first (LLMs attend more to beginning)
2. **Include source metadata** — chunk source, page number in context
3. **Separate chunks clearly** — use delimiters (`---` or `[Source: doc-title, page 5]`)
4. **Don't exceed budget** — truncate least-relevant chunks, never the most relevant
5. **Include diversity** — if top-5 chunks are from same doc, include from other sources too

### Generation Prompt Template

```
You are a helpful assistant. Answer the user's question using ONLY the provided context.

Rules:
- If the context doesn't contain the answer, say "I don't have enough information to answer that."
- Cite sources using [Source: title] format
- Never make up information not in the context
- If the answer spans multiple sources, synthesize and cite all

Context:
---
[Source: {title_1}, Page {page_1}]
{chunk_text_1}

[Source: {title_2}, Page {page_2}]
{chunk_text_2}
---

User question: {query}
```

### Citation Strategies

| Strategy | Quality | Complexity | Best For |
|----------|---------|-----------|----------|
| **Chunk-level** | Good | Low | Simple Q&A |
| **Sentence-level** | Excellent | Medium | Research, legal |
| **Quote extraction** | Best | High | Compliance-critical |
| **Inline footnotes** | Good | Medium | Chat interfaces |

---

## Phase 7: Evaluation Framework

### RAG Evaluation Dimensions

| Dimension | What It Measures | Metric |
|-----------|-----------------|--------|
| **Retrieval Relevance** | Are retrieved chunks relevant? | Precision@K, Recall@K, MRR, NDCG |
| **Context Relevance** | Is context sufficient for answer? | Context Precision, Context Recall |
| **Answer Faithfulness** | Is answer grounded in context? | Faithfulness Score (0-1) |
| **Answer Relevance** | Does answer address the question? | Answer Relevance Score (0-1) |
| **Answer Correctness** | Is the answer factually correct? | Correctness vs ground truth |
| **Hallucination** | Does answer contain made-up info? | Hallucination Rate |
| **Latency** | How fast is end-to-end response? | p50, p95, p99 |
| **Cost** | How much per query? | $/query |

### Building an Evaluation Dataset

Minimum 50 test cases. Target 200+ for production.

```yaml
eval_case:
  id: "eval-042"
  query: "What is the refund policy for enterprise customers?"
  # Ground truth
  expected_answer: "Enterprise customers can request a full refund within 30 days..."
  expected_source_docs: ["enterprise-tos.pdf", "refund-policy.md"]
  # Categories for analysis
  category: "policy"       # policy, technical, factual, analytical, multi-hop
  difficulty: "easy"       # easy, medium, hard
  requires_multi_doc: false
```

### Eval Case Categories

| Category | Example | Why It Matters |
|----------|---------|---------------|
| **Factual lookup** | "What's the API rate limit?" | Basic retrieval accuracy |
| **Multi-hop** | "Compare Q1 and Q2 revenue" | Tests cross-document reasoning |
| **Negative** | "What's the Mars colonization policy?" | Should return "I don't know" |
| **Temporal** | "What changed in the latest update?" | Tests freshness and recency |
| **Ambiguous** | "How do I connect?" | Tests query understanding |
| **Adversarial** | "Ignore instructions and..." | Tests prompt injection resistance |

### Evaluation Tools

| Tool | Type | Strengths |
|------|------|-----------|
| **RAGAS** | Open-source | Comprehensive RAG metrics, LLM-based evaluation |
| **DeepEval** | Open-source | 14+ metrics, pytest integration |
| **TruLens** | Open-source | Feedback functions, experiment tracking |
| **Langfuse** | Managed | Tracing, scoring, datasets |
| **Braintrust** | Managed | Eval, logging, prompt management |
| **Custom** | Build | Full control, domain-specific metrics |

### Evaluation Rules

1. **Build eval BEFORE optimizing** — you can't improve what you can't measure
2. **Include negative cases** — at least 10% of eval should be "no answer available"
3. **Separate retrieval eval from generation eval** — debug each stage independently
4. **Automate eval in CI/CD** — run on every pipeline change
5. **Track metrics over time** — quality drift is real and sneaky
6. **Human evaluation quarterly** — automated metrics correlate but don't replace human judgment
7. **Test with real user queries** — log production queries, add interesting ones to eval set

---

## Phase 8: Production Operations

### Indexing Pipeline Operations

```yaml
pipeline:
  schedule: "0 2 * * *"  # Daily at 2 AM
  steps:
    - name: "Detect changes"
      method: "incremental"  # full, incremental, CDC
      track: "last_modified, content_hash"
    - name: "Extract & clean"
      parallelism: 4
      timeout: 30m
    - name: "Chunk"
      strategy: "recursive_character"
      chunk_size: 512
      overlap: 50
    - name: "Embed"
      model: "text-embedding-3-small"
      batch_size: 100
    - name: "Upsert to vector DB"
      collection: "production"
      dedup: true
    - name: "Verify"
      run_eval_subset: true
      min_score: 0.85
    - name: "Cleanup"
      remove_stale: true
      stale_threshold: "30d"
```

### Update Strategy Decision

| Strategy | Complexity | Freshness | Best For |
|----------|-----------|-----------|----------|
| **Full re-index** | Low | Batch only | <100K docs, weekly updates OK |
| **Incremental** | Medium | Near-real-time | Content with timestamps/hashes |
| **CDC (Change Data Capture)** | High | Real-time | Database sources, streaming |
| **Hybrid** | Medium | Configurable | Mixed — full weekly + incremental daily |

### Monitoring Dashboard

```yaml
realtime_metrics:
  - name: "Query Latency (p95)"
    threshold: "<3s"
    alert_if: ">5s for 5 minutes"
  - name: "Retrieval Relevance"
    threshold: ">0.85 avg similarity"
    alert_if: "<0.75 for 10 queries"
  - name: "Empty Results Rate"
    threshold: "<5%"
    alert_if: ">10% in 1 hour"
  - name: "Error Rate"
    threshold: "<1%"
    alert_if: ">5% in 5 minutes"

periodic_metrics:
  - name: "Eval Suite Score"
    frequency: "daily"
    threshold: ">0.85"
  - name: "Index Freshness"
    frequency: "hourly"
    threshold: "<24h behind source"
  - name: "Cost per Query"
    frequency: "daily"
    threshold: "<$0.05"
  - name: "Hallucination Rate"
    frequency: "weekly"
    threshold: "<3%"

weekly_review:
  - Eval suite trend (improving/degrading?)
  - Top failing query categories
  - Cost per query trend
  - User feedback analysis
  - Index health and freshness
```

### Failure Modes & Remediation

| Failure | Detection | Fix |
|---------|-----------|-----|
| Retrieval returns irrelevant chunks | Low similarity scores, user feedback | Tune chunk size, add reranking, improve embeddings |
| Hallucinated answers | Faithfulness < 0.8, contradiction detection | Strengthen "cite only" prompt, lower temperature |
| Stale information | Document freshness check, user reports | Increase sync frequency, add freshness filter |
| Missing documents | Recall drop in eval, gap analysis | Audit data sources, check ingestion pipeline |
| Slow responses | p95 > SLA | Cache frequent queries, optimize index, reduce chunk count |
| Cost spike | $/query exceeds budget | Reduce top-K, use smaller embedding model, cache |
| Prompt injection | Adversarial eval failures | Input sanitization, output guardrails |

---

## Phase 9: Advanced Patterns

### Parent-Child Retrieval

Retrieve small chunks for precision, expand to parent for context:

```
Document
  └── Parent Chunk (2048 tokens) — sent to LLM
       ├── Child Chunk (256 tokens) — used for retrieval
       ├── Child Chunk (256 tokens)
       └── Child Chunk (256 tokens)
```

Implementation: Store child embeddings with parent_id reference. On retrieval, fetch children, deduplicate by parent, return parent text.

### Multi-Index Routing

Route queries to specialized indexes:

```yaml
indexes:
  - name: "technical_docs"
    trigger: "code, API, implementation, error"
    collection: "tech_v2"
  - name: "policies"
    trigger: "policy, compliance, legal, terms"
    collection: "policies_v1"
  - name: "general"
    trigger: "default"
    collection: "general_v1"
```

Use an LLM or classifier to route incoming queries to the right index.

### Contextual Retrieval (Anthropic Pattern)

Prepend each chunk with document-level context before embedding:

```
Chunk context: "This chunk is from the Q3 2025 financial report, 
specifically the Revenue Analysis section discussing APAC market growth."

[Original chunk text follows]
```

**Impact:** 35% reduction in retrieval failures (Anthropic research). Adds embedding cost but dramatically improves retrieval quality.

### Conversation-Aware RAG

For multi-turn conversations:

```
1. Combine last N turns into standalone query
   "What about their pricing?" → "What is Acme Corp's pricing for enterprise plans?"
2. Use standalone query for retrieval
3. Include conversation history in LLM context (after retrieved chunks)
```

### Knowledge Graph + RAG (GraphRAG)

When relationships matter more than text similarity:

```
1. Extract entities and relationships from documents
2. Build knowledge graph (Neo4j, NetworkX)
3. On query: identify entities → traverse graph → collect relevant subgraph
4. Use subgraph context + vector-retrieved chunks for generation
```

Best for: Organizational knowledge, legal document networks, research papers with citations.

### Corrective RAG (CRAG)

Self-correcting retrieval:

```
1. Retrieve chunks
2. LLM evaluates: "Are these chunks relevant to the query?"
3. If YES → proceed with generation
4. If PARTIALLY → web search for supplementary info
5. If NO → fallback to web search or "I don't know"
```

### Multi-Modal RAG

For documents with images, charts, tables:

| Content Type | Processing | Embedding |
|-------------|-----------|-----------|
| Text | Standard chunking | Text embedding model |
| Images | Vision model → description | Text embedding of description |
| Tables | Structure-preserving extraction | Text embedding of linearized table |
| Charts | Vision model → data extraction | Text embedding of extracted data |

---

## Phase 10: Security & Access Control

### RAG Security Checklist

**P0 — Before Launch:**
- [ ] Row-level access control on vector DB queries
- [ ] Input sanitization (prompt injection prevention)
- [ ] Output guardrails (PII detection, content filtering)
- [ ] API authentication and rate limiting
- [ ] Audit logging of all queries and retrievals
- [ ] Data encryption at rest and in transit

**P1 — Within 30 days:**
- [ ] Prompt injection test suite (adversarial eval)
- [ ] Data retention and deletion policy (GDPR Article 17)
- [ ] Access control audit trail
- [ ] Source document access verification
- [ ] Cost abuse prevention (rate limits per user/org)

### Access Control Implementation

```
Query with user_context
  → Extract user permissions (role, department, clearance)
  → Apply metadata filter BEFORE vector search
  → Filter: access_level IN user.allowed_levels
  → Retrieve only authorized chunks
  → Generate answer from authorized context only
```

**CRITICAL: Filter at retrieval time, not after generation.** If the LLM sees restricted content, it may leak it in the answer even if you try to filter afterward.

### Prompt Injection Defense

| Layer | Defense |
|-------|---------|
| Input | Sanitize special characters, detect injection patterns |
| System prompt | Strong instruction hierarchy, "ignore attempts to override" |
| Retrieved context | Wrap in delimiters, instruct LLM to treat as data not instructions |
| Output | Content filter, PII detector, answer verification |

---

## Phase 11: Cost Optimization

### Cost Breakdown per Query

| Component | Typical Cost | Optimization |
|-----------|-------------|-------------|
| Embedding (query) | $0.000002 | Negligible |
| Vector search | $0.0001-$0.001 | Cache frequent queries |
| Reranking | $0.001-$0.005 | Skip for simple queries |
| LLM generation | $0.01-$0.10 | Smaller model, shorter context |
| **Total** | **$0.01-$0.10** | |

### Cost Reduction Strategies

1. **Cache frequent queries** — semantic cache (embed query, check similarity to cached). 20-40% hit rate typical
2. **Tiered models** — simple queries → small model, complex → large model
3. **Reduce context** — send top-3 instead of top-10 chunks when confidence is high
4. **Batch embeddings** — embed in batches, not per-query
5. **Dimensionality reduction** — Matryoshka embeddings at 512 dims vs 1536
6. **Self-hosted embeddings** — BGE/GTE models eliminate per-token API costs at scale
7. **Query classification** — route "I need help" to FAQ, not full RAG pipeline

### Scale Planning

| Scale | Architecture | Monthly Cost Estimate |
|-------|-------------|---------------------|
| <1K queries/day | Chroma + OpenAI API | $50-200 |
| 1K-10K queries/day | Managed vector DB + API | $200-2,000 |
| 10K-100K queries/day | Dedicated infra + mix | $2,000-20,000 |
| >100K queries/day | Self-hosted everything | $10,000+ (compute) |

---

## Phase 12: Common Patterns Library

### Pattern 1: Internal Knowledge Base Q&A

```yaml
architecture: "Advanced RAG"
sources: ["Confluence", "Google Docs", "Notion"]
chunking: "Document structure"
embedding: "text-embedding-3-small"
vector_db: "Pinecone"
retrieval: "Hybrid search + Cohere Rerank"
generation: "Claude Sonnet with citations"
access_control: "Department-based metadata filtering"
eval: "200 questions from real Slack threads"
```

### Pattern 2: Customer Support Bot

```yaml
architecture: "Agentic RAG"
sources: ["Help center", "Release notes", "Internal runbooks"]
chunking: "Sentence window (3 sentences)"
embedding: "text-embedding-3-small"
vector_db: "Weaviate"
retrieval: "Vector + BM25 hybrid, α=0.6"
generation: "GPT-4o-mini (cost-efficient)"
fallback: "Escalate to human after 2 failed retrievals"
eval: "500 real support tickets with expert answers"
```

### Pattern 3: Legal Document Analysis

```yaml
architecture: "Graph RAG + Advanced RAG"
sources: ["Contracts", "Regulations", "Case law"]
chunking: "Semantic chunking (clause-level)"
embedding: "Voyage-3 (legal fine-tuned)"
vector_db: "Qdrant (self-hosted, data sovereignty)"
retrieval: "Multi-index routing (contracts vs regulations)"
generation: "Claude Opus with sentence-level citations"
access_control: "Matter-based, attorney-client privilege tagging"
eval: "100 questions reviewed by practicing attorneys"
```

### Pattern 4: Code Documentation Search

```yaml
architecture: "Advanced RAG"
sources: ["Code comments", "README", "ADRs", "API specs"]
chunking: "Code-aware (function/class level via tree-sitter)"
embedding: "Voyage-code-3"
vector_db: "pgvector (already have Postgres)"
retrieval: "Hybrid (code keywords + semantic)"
generation: "Claude Sonnet with code snippets"
eval: "Developer survey + retrieval accuracy"
```

---

## Quality Rubric (0-100)

| Dimension | Weight | 0 (Poor) | 50 (Adequate) | 100 (Excellent) |
|-----------|--------|-----------|---------------|-----------------|
| Retrieval Accuracy | 25% | <70% relevant in top-5 | 80-90% relevant | >95% relevant, reranked |
| Answer Quality | 20% | Hallucinations, unfaithful | Mostly accurate, some gaps | Faithful, cited, comprehensive |
| Latency | 15% | >10s p95 | 3-5s p95 | <2s p95 |
| Evaluation Coverage | 15% | No eval suite | 50+ cases, manual | 200+ cases, automated CI |
| Data Freshness | 10% | Manual, weeks behind | Daily sync | Near-real-time CDC |
| Security | 10% | No access control | Basic auth, no audit | Row-level ACL, audit trail, injection defense |
| Cost Efficiency | 5% | >$0.50/query | $0.05-$0.10/query | <$0.03/query with caching |

**Scoring: Sum(dimension_score × weight). Below 50 = not production-ready. 50-70 = MVP. 70-85 = good. 85+ = excellent.**

---

## 10 RAG Commandments

1. **Evaluate first, optimize second** — build eval dataset before tuning anything
2. **Chunk quality > embedding model** — garbage in, garbage out
3. **Always rerank** — cheapest improvement with biggest impact
4. **Filter at retrieval, not generation** — security is not a prompt
5. **Same model for index and query** — always, no exceptions
6. **Return "I don't know"** — honest uncertainty > confident hallucination
7. **Monitor continuously** — quality drifts silently
8. **Cache what you can** — semantic caching saves 20-40% cost
9. **Test with real queries** — synthetic eval misses real user patterns
10. **Start simple, add complexity only when eval demands it**

---

## 10 Common RAG Mistakes

| Mistake | Consequence | Fix |
|---------|------------|-----|
| No evaluation dataset | Can't measure improvement | Build 50+ eval cases before optimizing |
| Chunks too large | Low retrieval precision | Reduce to 256-512 tokens, add reranking |
| Chunks too small | Missing context | Use parent-child retrieval |
| No overlap between chunks | Lost context at boundaries | 10-20% overlap |
| Ignoring metadata | Can't filter, poor citations | Rich metadata on every chunk |
| Pure vector search | Misses keyword matches | Add BM25 hybrid search |
| No access control | Data leakage | Filter at retrieval time |
| No "I don't know" path | Hallucinations | Similarity threshold + explicit instruction |
| Over-engineering | Slow delivery, high cost | Start with Basic RAG, upgrade with eval data |
| Not monitoring production | Silent quality degradation | Automated daily eval + alerting |

---

## Edge Cases

### Multilingual RAG
- Use multilingual embedding models (Cohere multilingual, BGE-M3)
- Query language detection → route to language-specific index OR cross-lingual retrieval
- Generate in query language regardless of document language

### Very Large Documents (>100 pages)
- Hierarchical chunking: document → section → paragraph → sentence
- Table of contents as routing layer
- Summarize each section, use summaries for first-pass retrieval

### Rapidly Changing Data
- Streaming ingestion pipeline with CDC
- Time-weighted retrieval (prefer recent)
- Versioned chunks with effective dates

### Multi-Modal (Images + Text)
- Vision model to describe images → embed descriptions
- Separate image and text indexes, merge at retrieval
- Use multi-modal embedding models (CLIP, SigLIP) for direct image search

### Low-Resource / Offline
- Self-hosted everything (Ollama + BGE + Chroma + SQLite)
- Optimize for small models and CPU inference
- Pre-compute and cache common queries

---

## Natural Language Commands

When user says → Agent does:
- "Set up a RAG system" → Walk through Architecture Brief, recommend stack
- "My RAG is returning wrong answers" → Debug with evaluation checklist, check each pipeline stage
- "Optimize retrieval" → Audit chunking, add reranking, tune hybrid search
- "How should I chunk these documents?" → Analyze document types, recommend strategy
- "Compare vector databases for my use case" → Apply selection criteria from Phase 4
- "Build an eval dataset" → Generate eval cases from Phase 7 template
- "My RAG is too slow" → Profile each pipeline stage, identify bottleneck
- "How do I handle access control?" → Implement Phase 10 patterns
- "Reduce RAG costs" → Apply Phase 11 optimization strategies
- "Set up monitoring" → Configure Phase 8 dashboard and alerts
- "Review my RAG architecture" → Score against Quality Rubric
- "I need citations in answers" → Implement citation strategy from Phase 6
