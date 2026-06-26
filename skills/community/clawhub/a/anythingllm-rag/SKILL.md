---
name: anythingllm-rag
description: |
  Query local documents via AnythingLLM RAG (Retrieval-Augmented Generation). 
  Use when the user asks about their private/local documents, PDFs, uploaded files, 
  or wants to search their knowledge base. Also handles uploading new documents 
  to AnythingLLM. Triggers on phrases like "查询文档", "搜索本地", "PDF里说了什么", 
  "我的文档", "上传文档", "RAG", "知识库查询", "document search", "find in my files".
  For general questions not about local documents, use the default model instead.
---

# AnythingLLM RAG Skill

Query local/private documents through AnythingLLM's RAG API.

## Configuration

Environment variables (set in TOOLS.md or shell):
- `ANYTHINGLLM_URL` — default `http://localhost:3001`
- `ANYTHINGLLM_API_KEY` — API token
- `ANYTHINGLLM_WORKSPACE` — default workspace slug

Script location: `scripts/anythingllm.sh`

## When to Use

**Use AnythingLLM RAG when:**
- User asks about their local/private documents
- User wants to search uploaded PDFs, DOCX, TXT files
- User asks "what does X document say about Y"
- User wants to upload documents to the knowledge base

**Use default model when:**
- General knowledge questions
- Questions not related to local documents
- Coding, writing, analysis without document context

## Commands

### Query documents (RAG)
```bash
bash scripts/anythingllm.sh query "你的问题"
```

### Upload a file
```bash
bash scripts/anythingllm.sh upload /path/to/file.pdf
```

### Upload raw text
```bash
bash scripts/anythingllm.sh upload-text "文本内容" "文档标题"
```

### List documents
```bash
bash scripts/anythingllm.sh list-docs
```

### Check API health
```bash
bash scripts/anythingllm.sh health
```

## Response Format

Query returns JSON with:
- `textResponse` — the RAG-generated answer
- `sources` — array of source documents used for context

Present the answer to the user, citing relevant sources when available.

## Notes

- Scripts are in the skill's `scripts/` directory — use paths relative to skill location
- API key and workspace are pre-configured
- For PDF/DOCX queries, documents must be uploaded first
