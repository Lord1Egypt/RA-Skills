# RAG Architecture Design Document Template

## Document Information

| Field | Content |
|------|------|
| System Name | [RAG System Name] |
| Version | V1.0 |
| Date | YYYY-MM-DD |
| Author | [Name] |

---

## 1. RAG System Overview

### 1.1 System Objective
[What problem does this RAG system solve? One sentence description]

### 1.2 Use Cases

| Scenario | Typical Query | Expected Output | Frequency |
|------|----------|---------|------|
| | | | |

---

## 2. Knowledge Base Design

### 2.1 Data Sources

| Data Source | Type | Document Count | Update Frequency | Priority |
|--------|------|---------|---------|--------|
| | | | | |

### 2.2 Document Ingestion Pipeline

```
Raw Documents → Parsing → Cleaning → Chunking → Vectorization → Storage → Metadata Indexing
```

### 2.3 Chunking Strategy

| Decision | Choice | Rationale |
|------|------|------|
| Chunking Method | Fixed-size / Semantic / Hierarchical | |
| Chunk Size | 512 / 1024 / 2048 tokens | |
| Overlap Rate | 10% / 20% | |
| Metadata | [Document Name / Date / Author / Permissions / Tags] | |

### 2.4 Embedding Model

| Decision | Choice | Rationale |
|------|------|------|
| Model | | |
| Dimensions | | |
| Max Input Length | | |
| Chinese Evaluation | | |

---

## 3. Retrieval Design

### 3.1 Retrieval Architecture

```
User Query
    │
BM25 (Keyword) + Dense (Vector) → Parallel Retrieval
    │
Merge Candidates (top-50)
    │
Cross-encoder Reranker → top-5
    │
LLM Generation (with citations)
```

### 3.2 Retrieval Parameters

| Parameter | Value | Rationale |
|------|-----|------|
| Initial Recall Count | top-50 | |
| Post-Rerank Count | top-5 | |
| Similarity Threshold | 0.7 | |
| BM25 Weight | 0.3 | |
| Dense Weight | 0.7 | |

### 3.3 Vector Database

| Decision | Choice | Rationale |
|------|------|------|
| Database | Pinecone / Milvus / Weaviate / Qdrant / pgvector | |
| Index Type | HNSW / IVF | |
| Sharding Strategy | | |

### 3.4 Retrieval Filtering

| Filter Dimension | Rule | Implementation |
|---------|------|------|
| Permissions | Users can only retrieve authorized documents | metadata filter |
| Timeliness | Prioritize documents from the last 1 year | metadata + boost |
| Document Type | Filter by type | metadata filter |

---

## 4. Generation Design

### 4.1 System Prompt

```
[Fill in the RAG System Prompt here]

You are [Role]. Your task is to answer user questions based on the provided reference documents.

Constraints:
- Answer only based on the provided document content
- If the documents contain no relevant information, say "Cannot be determined based on available materials"
- Every answer must cite sources (document name + paragraph)
- Do not fabricate any information
```

### 4.2 Context Assembly Template

```
[System Prompt]

Reference Documents:
---
[Document 1] (Source: XXX, Date: YYYY-MM-DD)
{Retrieved document content}
---
[Document 2] ...
---

User Question: [User Query]

Please answer based on the above reference documents and cite information sources.
```

---

## 5. Evaluation Plan

### 5.1 RAGAS Metrics

| Metric | Target | Measurement Method |
|------|--------|---------|
| Faithfulness | >0.90 | Automated evaluation |
| Answer Relevancy | >0.85 | Automated evaluation |
| Context Precision | >0.85 | Automated evaluation |
| Context Recall | >0.90 | Automated evaluation |

### 5.2 Evaluation Dataset

| Type | Sample Count | Source |
|------|--------|------|
| Common Queries | | Real users |
| Edge Queries | | PM + Domain experts |
| Adversarial Queries | | Purpose-built |

### 5.3 Bad Case Analysis Process

```
Discover Bad Case → Root Cause Analysis (Retrieval? Generation? Chunking?) → Fix → Regression Test → Close
```

---

## 6. Optimization & Iteration

### 6.1 Continuous Optimization Points

| Optimization Item | Method | Expected Improvement |
|--------|------|---------|
| Chunking Strategy Tuning | | |
| Retrieval Parameter Tuning | | |
| Prompt Optimization | | |
| Reranker Calibration | | |

### 6.2 Knowledge Base Maintenance

| Maintenance Item | Frequency | Owner |
|--------|------|--------|
| New Document Ingestion | | |
| Expired Document Cleanup | | |
| Evaluation Set Update | Monthly | |
| Retrieval Quality Review | Weekly | |

---

## 7. Monitoring & Alerting

### 7.1 Monitoring Metrics

| Metric | Alert Threshold |
|------|---------|
| Retrieval Latency P95 | >500ms |
| Generation Latency P95 | >3s |
| Empty Retrieval Rate | >10% |
| RAGAS Faithfulness | <0.85 |

### 7.2 Degradation Strategy

| Scenario | Degradation Plan |
|------|---------|
| Vector database unavailable | Degrade to BM25-only retrieval |
| Empty retrieval results | Inform user + suggest rephrasing |
| Generation timeout | Return simplified answer |

---

## v1.1.0 New: RAG Evaluation Framework

### RAG Quality Evaluation Dimensions
| Dimension | Metric | Target | Measurement Method |
|------|------|------|---------|
| Retrieval Accuracy | Recall@K | >90% | Manual annotation + automated evaluation |
| Retrieval Relevance | Precision@K | >80% | Relevance scoring |
| Generation Quality | Answer Accuracy | >95% | Manual evaluation + LLM-as-Judge |
| Hallucination Rate | Hallucination Ratio | <5% | Fact-checking |
| Latency | P95 Response Time | <2s | Performance testing |
| Citation Accuracy | Citation Match Rate | >90% | Source verification |

### RAG Evaluation Test Set Design
| Test Type | Sample Size | Coverage |
|---------|--------|--------|
| Simple Fact Queries | 50 | Single-document direct answers |
| Multi-hop Reasoning | 30 | Cross-document information integration |
| Comparative Analysis | 20 | Multi-document comparison |
| Ambiguous Queries | 20 | Semantic understanding + disambiguation |
| Adversarial Tests | 10 | Confusing/contradictory information |

### RAG vs Fine-tuning Decision Matrix
| Scenario | Recommended Approach | Rationale |
|------|---------|------|
| Frequently updated knowledge | RAG | Real-time retrieval, no retraining needed |
| Fixed domain knowledge | Fine-tuning | Deep understanding, low latency |
| Requires precise citations | RAG | Traceable sources |
| Requires style imitation | Fine-tuning | Learns specific expression patterns |
| Hybrid needs | RAG + Fine-tuning | Best of both worlds |