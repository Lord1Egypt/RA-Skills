---
name: caremax-records
description: "Query and search medical records from CareMax Health API. Supports structured query, AI-powered semantic search with RAG (natural language answers with citations). Use when a user asks about medical reports, check-up history, hospital visits, test results, gene reports, or wants to find specific records. Trigger terms: medical record, check-up, hospital report, test result, health report, find report, search records, medical history, gene report, 体检, 报告, 检查, 基因, 搜索."
license: MIT
---

# CareMax Medical Records

> **Requires `caremax-auth` as a sibling directory** (`../caremax-auth/`). If missing, tell the user to install caremax-auth first (e.g. `npx skills add KittenYang/caremax-skills`).

## Prerequisites — Auto-Auth (MANDATORY)

```bash
APICALL="bash ../caremax-auth/scripts/api-call.sh"
```

If `api-call.sh` returns `{"error":"no_credentials",...}` → **immediately run `bash ../caremax-auth/scripts/auth-flow.sh [base_url]`** (from this skill’s root).

## Smart Search (Recommended)

Use `searchText` for natural language queries. Backend runs 4-layer search:
1. LLM keyword extraction (maps "喝酒" → "ALDH2 酒精代谢")
2. LIKE search on report titles, summaries, sections, indicators
3. Semantic vector search (BGE-M3 → Zilliz)
4. RAG: DeepSeek-V3.2 generates natural language answer with citations

```bash
$APICALL POST /api/skill/records/query '{"searchText":"我有哪个基因不能喝酒"}'
$APICALL POST /api/skill/records/query '{"searchText":"我猝死的概率大吗"}'
$APICALL POST /api/skill/records/query '{"searchText":"降压药建议"}'
$APICALL POST /api/skill/records/query '{"searchText":"MTHFR"}'
```

Response:
```json
{
  "type": "search",
  "query": "...",
  "data": [...],              // matched records (enriched)
  "totalCount": 1,
  "semanticHits": [           // vector similarity top-10
    {"text": "...", "score": 0.61, "recordId": "xxx"}
  ],
  "rag": {                    // AI natural language answer
    "answer": "根据您的基因检测报告...[来源1][来源2]",
    "citations": [
      {"index": 1, "source": "脑梗塞风险评估", "relevance": "高"}
    ]
  }
}
```

**Display the `rag.answer` to the user.** It contains the direct answer with citation references.

## Structured Query

```bash
# By date range
$APICALL POST /api/skill/records/query '{"dateRange":["2025-01-01","2025-12-31"]}'

# By indicator name
$APICALL POST /api/skill/records/query '{"indicatorName":"血红蛋白"}'

# By report title
$APICALL POST /api/skill/records/query '{"reportTitle":"血常规"}'

# By record ID (single record detail)
$APICALL POST /api/skill/records/query '{"recordId":"uuid"}'

# By member + pagination
$APICALL POST /api/skill/records/query '{"memberId":"member-uuid","page":1,"limit":20}'
```

## Report Types

The system handles multiple report types:
- **lab**: Standard lab reports (indicators with name/value/unit/reference_range)
- **genetic**: Gene testing reports (sections with gene/SNP/genotype/risk_level)
- **imaging**: Radiology reports (sections with location/finding/impression)
- **pathology**: Pathology reports (sections with tissue/grade/staging)
- **other**: Any other medical document

Non-lab reports have `report_type`, `summary`, and `sections[]` fields instead of `indicators[]`.

## AI 对话（推荐）

使用 `/api/skill/chat` 进行 AI 对话。所有对话自动保存到历史记录。

```bash
# 提问（自动搜索 + RAG + 保存历史）
$APICALL POST /api/skill/chat '{"question":"我有哪个基因不能喝酒"}'
$APICALL POST /api/skill/chat '{"question":"我的降压药应该怎么吃"}'

# 针对某份报告提问
$APICALL POST /api/skill/chat '{"question":"这份报告有什么建议","recordId":"uuid"}'
```

Response:
```json
{
  "id": "chat-uuid",
  "question": "...",
  "answer": "根据您的报告...[来源1]",
  "citations": [{"index":1,"source":"...","relevance":"高","quote":"原文..."}],
  "recordId": null,
  "created_at": "..."
}
```

**Display the `answer` to the user.** Citations contain original report text.

```bash
# 获取历史记录
$APICALL GET /api/skill/chat/history

# 删除单条
$APICALL DELETE /api/skill/chat/<chat_id>

# 清空所有
$APICALL DELETE /api/skill/chat
```

## Recommended Workflow

User: "我的基因检测报告说了什么"
```bash
$APICALL POST /api/skill/chat '{"question":"我的基因检测报告说了什么"}'
```

User: "show my recent check-up results"
```bash
$APICALL POST /api/skill/records/query '{"dateRange":["2025-01-01","2025-06-30"]}'
```

User: "我的降压药应该怎么吃"
```bash
$APICALL POST /api/skill/chat '{"question":"我的降压药应该怎么吃"}'
```
