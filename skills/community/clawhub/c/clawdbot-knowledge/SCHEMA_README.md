# 📊 Complete Supabase Schema Documentation

## Overview
This directory contains the complete database schema for the **DeepAllSpeak Self-Memory System** integrated with the existing **Docling RAG** and **Agent Management** systems.

**Project:** vufkhfuphdsezilzclwv (Docling ui DB)  
**Total Tables:** 25  
**Total Views:** 5  
**Total Functions:** 2  
**Total Triggers:** 3

---

## 📁 Files

### `complete-schema-export.sql`
Complete SQL schema export containing:
- All 25 tables
- All indexes (40+)
- All functions & triggers
- All views
- Complete constraints & foreign keys

### `schema.sql`
Original skill-memory system schema (skills, skill_executions, skill_feedback)

---

## 🗂️ Schema Sections

### 1. Workspace & User Management
- `workspaces` - Multi-tenant workspace management
- `workspace_members` - User-workspace relationships

### 2. Document Management (Docling RAG)
- `namespaces` - Document organization
- `documents` - Uploaded documents (PDF, DOCX, etc.)
- `document_chunks` - Chunked content for RAG
- `query_history` - Search query logs
- `summaries` - Generated summaries

### 3. Agent System (Tool Management & Execution)
- `agent_tools` - Available MCP tools
- `agent_tool_policies` - Workspace-specific tool policies
- `agent_runs` - Agent execution runs
- `run_events` - Event logs per run
- `run_tool_calls` - Tool invocations
- `run_tool_results` - Tool execution results
- `run_artifacts` - Generated artifacts

### 4. Skill Memory System (NEW - DeepAllSpeak)
- `skills` - Reusable AI skills
- `skill_executions` - Skill execution history
- `skill_feedback` - User feedback on skills

### 5. Webhooks & System Config
- `webhooks` - Webhook endpoints
- `webhook_delivery_logs` - Webhook delivery logs
- `system_config` - System-wide configuration

---

## 🔗 Key Relationships

```
workspaces
  ├── workspace_members
  ├── agent_runs
  │   ├── run_events
  │   ├── run_tool_calls
  │   │   └── run_tool_results
  │   └── run_artifacts
  └── namespaces
      └── documents
          └── document_chunks

skills
  ├── skill_executions
  │   └── skill_feedback
  └── skills (parent_skill_id - version history)
```

---

## 📈 Statistics & Monitoring

### Auto-Updated Fields
- `skills.usage_count` - Incremented on each execution
- `skills.success_count` - Incremented on successful execution
- `skills.failure_count` - Incremented on failed execution
- `skills.success_rate` - Computed column (success_count / usage_count)
- `skills.avg_execution_time_ms` - Rolling average

### Triggers
1. `update_skills_updated_at` - Auto-update `updated_at` on skill changes
2. `update_agent_runs_updated_at` - Auto-update `updated_at` on run changes
3. `update_skill_stats_on_execution` - Auto-update skill statistics on execution

---

## 🔍 Useful Queries

### Get all skills with statistics
```sql
SELECT
  name,
  category,
  usage_count,
  success_rate,
  avg_execution_time_ms
FROM skills
WHERE deleted_at IS NULL
ORDER BY usage_count DESC;
```

### Get recent skill executions
```sql
SELECT
  s.name,
  se.status,
  se.execution_time_ms,
  se.created_at
FROM skill_executions se
JOIN skills s ON se.skill_id = s.id
ORDER BY se.created_at DESC
LIMIT 10;
```

### Get documents with chunk counts
```sql
SELECT * FROM documents_with_stats
WHERE status = 'completed'
ORDER BY uploaded_at DESC;
```

### Get agent runs with tool usage
```sql
SELECT
  ar.id,
  ar.query,
  ar.status,
  COUNT(rtc.id) AS tool_calls
FROM agent_runs ar
LEFT JOIN run_tool_calls rtc ON ar.id = rtc.run_id
GROUP BY ar.id
ORDER BY ar.created_at DESC;
```

---

## 🚀 Deployment

### Option 1: Supabase Dashboard (Recommended)
1. Go to: https://supabase.com/dashboard/project/vufkhfuphdsezilzclwv/sql/new
2. Copy content from `complete-schema-export.sql`
3. Paste into SQL Editor
4. Click "Run" (or Ctrl+Enter)

### Option 2: Supabase CLI
```bash
supabase db push
```

### Option 3: Direct PostgreSQL Connection
```bash
psql $SUPABASE_DB_URL < complete-schema-export.sql
```

---

## 🔒 Security

### Row Level Security (RLS)
- Currently: **Not enabled** (service role key used)
- Future: Enable RLS for multi-tenant isolation

### Sensitive Data
- `system_config.is_secret` - Marks sensitive config values
- `webhooks.secret` - Webhook signing secrets
- All API keys stored in environment variables (not in DB)

---

## 📊 Current Status

### Tables Created ✅
- ✅ 25 tables
- ✅ 40+ indexes
- ✅ 2 functions
- ✅ 3 triggers
- ✅ 5 views

### Data Status
- ✅ 1 skill created (summarize-text)
- ✅ Pinecone integration active
- ✅ OpenAI embeddings working
- ✅ Semantic search functional

---

## 🎯 Next Steps

1. ✅ Schema deployed
2. ✅ First skill created
3. ⏳ Enable RLS (optional)
4. ⏳ Add more skills
5. ⏳ Implement skill versioning
6. ⏳ Add skill analytics dashboard

---

**Last Updated:** 2025-01-01  
**Maintained By:** DeepAllSpeak Team

