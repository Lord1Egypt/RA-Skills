# Self-Memory System for DeepAllSpeak

Complete guide to DeepAllSpeak's self-learning capability through skill creation, storage, and retrieval using Supabase + Pinecone.

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Database Schemas](#database-schemas)
4. [Skill Structure](#skill-structure)
5. [API Reference](#api-reference)
6. [Usage Patterns](#usage-patterns)
7. [Learning Loop](#learning-loop)
8. [Implementation Guide](#implementation-guide)
9. [Best Practices](#best-practices)

---

## Overview

### What is the Self-Memory System?

The Self-Memory System enables DeepAllSpeak to:
- **Learn from usage** - Automatically identify repeatable tasks
- **Create skills** - Generate reusable skill definitions
- **Store knowledge** - Persist skills in Supabase (PostgreSQL)
- **Semantic search** - Find relevant skills using Pinecone (vector DB)
- **Execute skills** - Load and run stored skills on-demand
- **Improve continuously** - Refine skills based on execution feedback

### Why Self-Memory?

**Problem:** Users often perform similar tasks repeatedly, but the AI forgets previous patterns and starts from scratch each time.

**Solution:** Auto-create and store "skills" for recurring patterns. Next time the user has a similar task, retrieve the appropriate skill and execute it faster and more consistently.

### Key Benefits

1. **Faster Execution** - Pre-defined skills run faster than ad-hoc tasks
2. **Consistency** - Same task produces consistent results
3. **Learning** - AI improves over time from usage patterns
4. **Personalization** - Skills adapt to individual user preferences
5. **Knowledge Retention** - Skills persist across sessions

---

## Architecture

```
┌───────────────────────────────────────────────────────────────────┐
│                    Self-Memory System                              │
├───────────────────────────────────────────────────────────────────┤
│                                                                    │
│  1. User performs task via voice/text                             │
│     ↓                                                              │
│  2. DeepAllSpeak detects pattern (e.g., 3rd time doing similar)   │
│     ↓                                                              │
│  3. AI suggests: "Create a skill for this?"                       │
│     ↓                                                              │
│  4. Skill Creator generates skill definition                      │
│     ├─ Name: "analyze_sales_report"                               │
│     ├─ Description: "Analyze quarterly sales reports..."          │
│     ├─ Category: "business_intelligence"                          │
│     ├─ Prompt Template: "Analyze {{data}} for trends..."          │
│     ├─ Input Schema: { data: string, quarter: string }            │
│     └─ Output Schema: { trends: [], insights: [] }                │
│     ↓                                                              │
│  5. Storage Layer                                                 │
│     ├─ Supabase: Store skill JSON + metadata                      │
│     └─ Pinecone: Store embedding for semantic search              │
│        (uses OpenAI text-embedding-3-small)                       │
│     ↓                                                              │
│  6. Future Execution                                               │
│     ├─ User: "Analyze this sales report"                          │
│     ├─ Semantic Search: query Pinecone → find "analyze_sales..."  │
│     ├─ Load Skill: fetch from Supabase by ID                      │
│     ├─ Execute: run skill logic with user's data                  │
│     └─ Track: update usage stats in Supabase                      │
│     ↓                                                              │
│  7. Learning Loop                                                 │
│     ├─ After 100 uses: analyze execution patterns                 │
│     ├─ Suggest improvements: better prompt, new parameters        │
│     ├─ Update skill: increment version, store old version         │
│     └─ User feedback: collect ratings, comments                   │
│                                                                    │
└───────────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Databases:**
- **Supabase** (PostgreSQL) - Relational storage for skills, executions, feedback
- **Pinecone** (Vector DB) - Semantic search via embeddings

**Embeddings:**
- **OpenAI** `text-embedding-3-small` - 1536 dimensions, fast, cheap

**MCP Server:**
- **Node.js** - Skill-memory MCP server
- **TypeScript** - Type-safe skill definitions

---

## Database Schemas

### Supabase (PostgreSQL)

#### Skills Table

```sql
CREATE TABLE skills (
  -- Identity
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL UNIQUE,

  -- Description
  description TEXT,
  category VARCHAR(100),
  tags TEXT[] DEFAULT '{}',

  -- Skill Definition
  prompt_template TEXT NOT NULL,
  input_schema JSONB NOT NULL,
  output_schema JSONB,

  -- Execution Config
  agent VARCHAR(100),  -- Which agent to use (fatoni, deepsynaptica, etc.)
  tools TEXT[],        -- Which MCP tools to use
  temperature FLOAT DEFAULT 0.7,
  max_tokens INTEGER DEFAULT 2048,

  -- Metadata
  author VARCHAR(255),
  version INTEGER DEFAULT 1,
  parent_skill_id UUID REFERENCES skills(id),  -- For version history

  -- Statistics
  usage_count INTEGER DEFAULT 0,
  success_count INTEGER DEFAULT 0,
  failure_count INTEGER DEFAULT 0,
  success_rate FLOAT GENERATED ALWAYS AS (
    CASE
      WHEN usage_count > 0 THEN success_count::FLOAT / usage_count
      ELSE 0
    END
  ) STORED,
  avg_execution_time_ms INTEGER,

  -- Timestamps
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  deleted_at TIMESTAMP,

  -- Constraints
  CONSTRAINT valid_success_rate CHECK (success_rate >= 0 AND success_rate <= 1)
);

-- Indexes
CREATE INDEX idx_skills_category ON skills(category);
CREATE INDEX idx_skills_tags ON skills USING GIN(tags);
CREATE INDEX idx_skills_usage_count ON skills(usage_count DESC);
CREATE INDEX idx_skills_success_rate ON skills(success_rate DESC);
CREATE INDEX idx_skills_created_at ON skills(created_at DESC);

-- Update timestamp trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER skills_updated_at
BEFORE UPDATE ON skills
FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

#### Skill Executions Table

```sql
CREATE TABLE skill_executions (
  -- Identity
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,

  -- Execution Data
  inputs JSONB NOT NULL,
  outputs JSONB,

  -- Status
  status VARCHAR(50) NOT NULL CHECK (status IN ('pending', 'running', 'success', 'failed')),
  error_message TEXT,

  -- Performance
  execution_time_ms INTEGER,
  tokens_used INTEGER,
  cost_usd DECIMAL(10, 6),

  -- Context
  user_id UUID,  -- If multi-user
  session_id UUID,  -- Group related executions

  -- Timestamps
  started_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP,

  -- Indexes
  CONSTRAINT valid_execution_time CHECK (execution_time_ms >= 0)
);

CREATE INDEX idx_executions_skill_id ON skill_executions(skill_id);
CREATE INDEX idx_executions_status ON skill_executions(status);
CREATE INDEX idx_executions_started_at ON skill_executions(started_at DESC);

-- Update skill statistics trigger
CREATE OR REPLACE FUNCTION update_skill_stats()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.status = 'success' THEN
    UPDATE skills
    SET
      usage_count = usage_count + 1,
      success_count = success_count + 1,
      avg_execution_time_ms = (
        COALESCE(avg_execution_time_ms * usage_count, 0) + NEW.execution_time_ms
      ) / (usage_count + 1)
    WHERE id = NEW.skill_id;
  ELSIF NEW.status = 'failed' THEN
    UPDATE skills
    SET
      usage_count = usage_count + 1,
      failure_count = failure_count + 1
    WHERE id = NEW.skill_id;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER skill_execution_stats
AFTER INSERT OR UPDATE OF status ON skill_executions
FOR EACH ROW EXECUTE FUNCTION update_skill_stats();
```

#### Skill Feedback Table

```sql
CREATE TABLE skill_feedback (
  -- Identity
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
  execution_id UUID REFERENCES skill_executions(id),

  -- Feedback
  rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
  comment TEXT,

  -- Suggestions
  suggested_improvements JSONB,

  -- Context
  user_id UUID,

  -- Timestamp
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_feedback_skill_id ON skill_feedback(skill_id);
CREATE INDEX idx_feedback_rating ON skill_feedback(rating);

-- Update skill stats with feedback
CREATE OR REPLACE FUNCTION update_skill_feedback_stats()
RETURNS TRIGGER AS $$
BEGIN
  -- Could add avg_rating column to skills table
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER skill_feedback_stats
AFTER INSERT ON skill_feedback
FOR EACH ROW EXECUTE FUNCTION update_skill_feedback_stats();
```

### Pinecone (Vector Index)

**Index Configuration:**

```typescript
const pineconeConfig = {
  indexName: "deepallspeak-skills",
  dimension: 1536,  // OpenAI text-embedding-3-small
  metric: "cosine",
  pods: 1,
  replicas: 1,
  podType: "p1.x1"  // Starter tier
};
```

**Vector Metadata:**

```typescript
interface PineconeMetadata {
  skill_id: string;      // UUID from Supabase
  name: string;          // Skill name
  description: string;   // Skill description
  category: string;      // Category
  tags: string[];        // Tags array
  created_at: string;    // ISO timestamp
  usage_count: number;   // For ranking
  success_rate: number;  // For filtering
}
```

**Embedding Strategy:**

Combine multiple fields for rich semantic search:
```
embedding_text = `${name}\n${description}\n${category}\n${tags.join(', ')}`
```

Example:
```
"analyze_sales_report
Analyze quarterly sales reports and extract key metrics, trends, and insights
business_intelligence
sales, analytics, reports, business, quarterly"
```

---

## Skill Structure

### Skill Definition (TypeScript)

```typescript
interface Skill {
  // Identity
  id: string;  // UUID
  name: string;  // Unique, kebab-case (e.g., "analyze-sales-report")

  // Description
  description: string;
  category: SkillCategory;
  tags: string[];

  // Execution Definition
  promptTemplate: string;  // Template with {{variables}}
  inputSchema: JSONSchema;  // JSON Schema for inputs
  outputSchema?: JSONSchema;  // Optional output schema

  // Execution Config
  agent?: string;  // "fatoni", "deepsynaptica", "auto"
  tools?: string[];  // MCP tool names to use
  temperature?: number;  // 0.0 - 1.0
  maxTokens?: number;

  // Metadata
  author?: string;
  version: number;
  parentSkillId?: string;  // For versioning

  // Statistics (read-only)
  usageCount: number;
  successRate: number;
  avgExecutionTimeMs?: number;

  // Timestamps
  createdAt: Date;
  updatedAt: Date;
  deletedAt?: Date;
}

enum SkillCategory {
  BUSINESS_INTELLIGENCE = "business_intelligence",
  CODE_GENERATION = "code_generation",
  CODE_REVIEW = "code_review",
  DOCUMENT_ANALYSIS = "document_analysis",
  DATA_ANALYSIS = "data_analysis",
  SECURITY_AUDIT = "security_audit",
  STRATEGY_PLANNING = "strategy_planning",
  WORKFLOW_AUTOMATION = "workflow_automation",
  RESEARCH = "research",
  COMMUNICATION = "communication",
  GENERAL = "general"
}
```

### Prompt Template

Templates use Handlebars-style syntax:

```handlebars
Analyze the following {{document_type}} for {{analysis_focus}}.

Data:
{{data}}

Instructions:
{{#if include_charts}}
- Generate visualizations for key metrics
{{/if}}
{{#if compare_previous}}
- Compare with previous {{period}}
{{/if}}

Output the results in JSON format with:
- key_metrics: Array of important metrics
- trends: Array of identified trends
- insights: Array of actionable insights
{{#if include_recommendations}}
- recommendations: Array of recommended actions
{{/if}}
```

### Input Schema (JSON Schema)

```json
{
  "type": "object",
  "properties": {
    "data": {
      "type": "string",
      "description": "The data to analyze"
    },
    "document_type": {
      "type": "string",
      "enum": ["sales_report", "financial_statement", "user_survey"],
      "default": "sales_report"
    },
    "analysis_focus": {
      "type": "string",
      "description": "What aspect to focus on",
      "default": "revenue trends"
    },
    "period": {
      "type": "string",
      "enum": ["weekly", "monthly", "quarterly", "annually"],
      "default": "quarterly"
    },
    "include_charts": {
      "type": "boolean",
      "default": false
    },
    "compare_previous": {
      "type": "boolean",
      "default": true
    },
    "include_recommendations": {
      "type": "boolean",
      "default": true
    }
  },
  "required": ["data"]
}
```

### Output Schema

```json
{
  "type": "object",
  "properties": {
    "key_metrics": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "value": {"type": "number"},
          "unit": {"type": "string"},
          "change_percentage": {"type": "number"}
        }
      }
    },
    "trends": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "description": {"type": "string"},
          "direction": {"type": "string", "enum": ["up", "down", "stable"]},
          "confidence": {"type": "number", "minimum": 0, "maximum": 1}
        }
      }
    },
    "insights": {
      "type": "array",
      "items": {"type": "string"}
    },
    "recommendations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "action": {"type": "string"},
          "priority": {"type": "string", "enum": ["high", "medium", "low"]},
          "impact": {"type": "string"}
        }
      }
    }
  }
}
```

---

## API Reference

### MCP Tools

#### 1. skill_create

Create a new skill and store in database.

```typescript
{
  name: "skill_create",
  description: "Create a new reusable skill definition and store in the skill library",
  inputSchema: {
    type: "object",
    properties: {
      name: {
        type: "string",
        description: "Unique skill name (kebab-case)",
        pattern: "^[a-z0-9-]+$"
      },
      description: {
        type: "string",
        description: "Clear description of what the skill does"
      },
      category: {
        type: "string",
        enum: ["business_intelligence", "code_generation", "..."]
      },
      promptTemplate: {
        type: "string",
        description: "Prompt template with {{variables}}"
      },
      inputSchema: {
        type: "object",
        description: "JSON Schema for input validation"
      },
      outputSchema: {
        type: "object",
        description: "Optional JSON Schema for output"
      },
      tags: {
        type: "array",
        items: {"type": "string"}
      },
      agent: {
        type: "string",
        description: "Which agent to use (optional)"
      },
      tools: {
        type: "array",
        items: {"type": "string"},
        description: "MCP tools to use (optional)"
      }
    },
    required: ["name", "description", "category", "promptTemplate", "inputSchema"]
  }
}
```

**Example:**

```typescript
await callTool("skill_create", {
  name: "analyze-sales-report",
  description: "Analyze quarterly sales reports and extract key metrics",
  category: "business_intelligence",
  promptTemplate: "Analyze this {{period}} sales report:\n{{data}}\n\nFocus on: {{focus}}",
  inputSchema: {
    type: "object",
    properties: {
      data: {type: "string"},
      period: {type: "string", enum: ["Q1", "Q2", "Q3", "Q4"]},
      focus: {type: "string", default: "revenue trends"}
    },
    required: ["data", "period"]
  },
  tags: ["sales", "analytics", "business"]
});
```

#### 2. skill_search

Search for skills using semantic search.

```typescript
{
  name: "skill_search",
  description: "Search for skills using semantic similarity",
  inputSchema: {
    type: "object",
    properties: {
      query: {
        type: "string",
        description: "Search query (can be natural language)"
      },
      category: {
        type: "string",
        description: "Filter by category (optional)"
      },
      tags: {
        type: "array",
        items: {"type": "string"},
        description: "Filter by tags (optional)"
      },
      minSuccessRate: {
        type: "number",
        minimum: 0,
        maximum: 1,
        description: "Minimum success rate filter"
      },
      limit: {
        type: "number",
        default: 5,
        description: "Maximum results to return"
      }
    },
    required: ["query"]
  }
}
```

**Example:**

```typescript
await callTool("skill_search", {
  query: "analyze documents with citations",
  category: "document_analysis",
  minSuccessRate: 0.8,
  limit: 5
});

// Returns:
{
  results: [
    {
      skill_id: "uuid-123",
      name: "document-qa-with-citations",
      description: "Query documents and return answers with citations",
      score: 0.95,  // Similarity score
      success_rate: 0.92,
      usage_count: 47
    },
    // ...
  ]
}
```

#### 3. skill_execute

Execute a skill by ID.

```typescript
{
  name: "skill_execute",
  description: "Execute a skill with provided inputs",
  inputSchema: {
    type: "object",
    properties: {
      skillId: {
        type: "string",
        description: "UUID of the skill to execute"
      },
      inputs: {
        type: "object",
        description: "Input data (must match skill's inputSchema)"
      },
      sessionId: {
        type: "string",
        description: "Optional session ID for grouping executions"
      }
    },
    required: ["skillId", "inputs"]
  }
}
```

**Example:**

```typescript
await callTool("skill_execute", {
  skillId: "uuid-123",
  inputs: {
    data: "Q3 Sales: $1.2M, Q2: $980K...",
    period: "Q3",
    focus: "year-over-year growth"
  }
});

// Returns:
{
  success: true,
  executionId: "exec-uuid-456",
  outputs: {
    key_metrics: [...],
    trends: [...],
    insights: [...]
  },
  executionTimeMs: 2340,
  tokensUsed: 1250
}
```

#### 4. skill_list

List all skills with filtering and sorting.

```typescript
{
  name: "skill_list",
  description: "List skills with filtering and sorting options",
  inputSchema: {
    type: "object",
    properties: {
      category: {type: "string"},
      tags: {type: "array", items: {"type": "string"}},
      sortBy: {
        type: "string",
        enum: ["usage_count", "success_rate", "created_at", "name"],
        default: "usage_count"
      },
      sortOrder: {
        type: "string",
        enum: ["asc", "desc"],
        default: "desc"
      },
      limit: {type: "number", default: 10},
      offset: {type: "number", default: 0}
    }
  }
}
```

#### 5. skill_update

Update an existing skill.

```typescript
{
  name: "skill_update",
  description: "Update a skill definition. Creates new version if major changes.",
  inputSchema: {
    type: "object",
    properties: {
      skillId: {type: "string"},
      updates: {
        type: "object",
        properties: {
          description: {type: "string"},
          promptTemplate: {type: "string"},
          inputSchema: {type: "object"},
          outputSchema: {type: "object"},
          tags: {type: "array"},
          temperature: {type: "number"},
          maxTokens: {type: "number"}
        }
      },
      incrementVersion: {
        type: "boolean",
        default: false,
        description: "Create new version instead of updating"
      }
    },
    required: ["skillId", "updates"]
  }
}
```

#### 6. skill_delete

Soft delete a skill.

```typescript
{
  name: "skill_delete",
  description: "Soft delete a skill (marks as deleted but keeps in database)",
  inputSchema: {
    type: "object",
    properties: {
      skillId: {type: "string"}
    },
    required: ["skillId"]
  }
}
```

#### 7. skill_stats

Get detailed statistics for a skill.

```typescript
{
  name: "skill_stats",
  description: "Get usage statistics and performance metrics for a skill",
  inputSchema: {
    type: "object",
    properties: {
      skillId: {type: "string"},
      timeframe: {
        type: "string",
        enum: ["day", "week", "month", "all"],
        default: "all"
      }
    },
    required: ["skillId"]
  }
}
```

**Returns:**

```typescript
{
  skillId: "uuid-123",
  name: "analyze-sales-report",
  usageCount: 47,
  successCount: 45,
  failureCount: 2,
  successRate: 0.957,
  avgExecutionTimeMs: 2340,
  totalTokensUsed: 58750,
  totalCostUsd: 1.75,
  executionsByDay: [...],  // Time series data
  avgRating: 4.8,
  feedbackCount: 12
}
```

#### 8. skill_suggest_improvements

AI-powered skill improvement suggestions.

```typescript
{
  name: "skill_suggest_improvements",
  description: "Analyze skill executions and suggest improvements",
  inputSchema: {
    type: "object",
    properties: {
      skillId: {type: "string"},
      recentExecutions: {
        type: "number",
        default: 10,
        description: "Number of recent executions to analyze"
      }
    },
    required: ["skillId"]
  }
}
```

**Returns:**

```typescript
{
  skill_id: "uuid-123",
  suggestions: [
    {
      type: "prompt_improvement",
      current: "Analyze this {{period}} sales report",
      suggested: "Analyze this {{period}} sales report with focus on {{key_metrics}}",
      reason: "Users frequently specify which metrics to focus on",
      confidence: 0.85
    },
    {
      type: "new_parameter",
      parameter: "compare_to_previous",
      schema: {type: "boolean", default: true},
      reason: "70% of executions include previous period comparison",
      confidence: 0.92
    },
    {
      type: "temperature_adjustment",
      current: 0.7,
      suggested: 0.3,
      reason: "More deterministic outputs reduce variance",
      confidence: 0.78
    }
  ],
  analysis: {
    total_executions_analyzed: 45,
    success_rate: 0.957,
    common_patterns: [...],
    failure_causes: [...]
  }
}
```

---

## Usage Patterns

### Pattern 1: Auto-Skill Creation

**Trigger:** User performs similar task 3+ times

```typescript
// DeepAllSpeak detects pattern
const taskHistory = [
  "Analyze Q1 sales report",
  "Analyze Q2 sales report",
  "Analyze Q3 sales report"
];

// AI suggests skill creation
if (taskHistory.length >= 3) {
  suggestSkillCreation({
    tasks: taskHistory,
    suggestedName: "analyze-quarterly-sales-report",
    suggestedDescription: "Analyze quarterly sales reports for trends and insights",
    confidence: 0.92
  });
}

// User confirms
const skill = await createSkillFromPattern(taskHistory);
```

### Pattern 2: Skill Discovery & Execution

```typescript
// User voice command
"Analyze this sales report"

// 1. Semantic search for matching skill
const results = await callTool("skill_search", {
  query: "analyze sales report",
  category: "business_intelligence",
  limit: 3
});

// 2. Select best match (highest score + success rate)
const bestSkill = results[0];

// 3. Execute skill
const result = await callTool("skill_execute", {
  skillId: bestSkill.skill_id,
  inputs: {
    data: salesReportData,
    period: "Q3"
  }
});

// 4. Return result to user
```

### Pattern 3: Skill Versioning

```typescript
// When making significant changes
await callTool("skill_update", {
  skillId: "uuid-123",
  updates: {
    promptTemplate: "Improved prompt template...",
    inputSchema: {
      // New schema with additional fields
    }
  },
  incrementVersion: true  // Creates version 2
});

// Old version still accessible
const v1 = await getSkillVersion("uuid-123", version: 1);
const v2 = await getSkillVersion("uuid-123", version: 2);

// Users can roll back if needed
```

### Pattern 4: Skill Composition

**Combine multiple skills:**

```typescript
const compositeSkill = await callTool("skill_create", {
  name: "comprehensive-sales-analysis",
  description: "Complete sales analysis pipeline using multiple sub-skills",
  promptTemplate: "Execute sales analysis pipeline",
  inputSchema: {...},
  tools: [
    "skill_execute",  // Can execute other skills
    "fatoni_analytics_analyze"
  ],
  executionPlan: [
    {
      step: 1,
      skill: "extract-sales-data",
      inputs: {data: "{{raw_data}}"}
    },
    {
      step: 2,
      skill: "analyze-sales-trends",
      inputs: {data: "{{step1.output}}"}
    },
    {
      step: 3,
      skill: "generate-sales-report",
      inputs: {analysis: "{{step2.output}}"}
    }
  ]
});
```

---

## Learning Loop

### Automatic Improvement Cycle

```
1. Execution (100+ uses)
   ↓
2. Analysis
   - Common input patterns
   - Output quality metrics
   - User feedback sentiment
   - Failure causes
   ↓
3. Suggestion Generation
   - Prompt improvements
   - New parameters
   - Better defaults
   - Temperature adjustments
   ↓
4. User Review
   - Accept/reject suggestions
   - Provide feedback
   ↓
5. Skill Update
   - Increment version
   - Update prompt/schema
   - Re-generate embeddings
   ↓
6. A/B Testing
   - Run old vs new version
   - Compare success rates
   - Measure improvement
   ↓
7. Rollout or Rollback
   - If improved: make default
   - If worse: revert to previous
```

### Feedback Collection

**Explicit Feedback:**
```typescript
// After skill execution
await callTool("skill_feedback_create", {
  skillId: "uuid-123",
  executionId: "exec-456",
  rating: 5,
  comment: "Perfect analysis, very helpful!",
  suggestedImprovements: {
    additionalOutputs: ["add comparison charts"]
  }
});
```

**Implicit Feedback:**
```typescript
// Track user behavior
- Did user edit the output? → Skill could be improved
- Did user re-run with different params? → Defaults might be wrong
- Did user create manual refinement? → Add to skill
- Success vs failure rate → Overall quality metric
```

### Continuous Learning Metrics

```sql
-- Weekly improvement report
SELECT
  s.id,
  s.name,
  s.version,
  s.success_rate,
  LAG(s.success_rate) OVER (PARTITION BY s.name ORDER BY s.version) as prev_success_rate,
  s.success_rate - LAG(s.success_rate) OVER (PARTITION BY s.name ORDER BY s.version) as improvement,
  s.usage_count,
  AVG(f.rating) as avg_rating
FROM skills s
LEFT JOIN skill_feedback f ON s.id = f.skill_id
WHERE s.created_at > NOW() - INTERVAL '7 days'
GROUP BY s.id, s.name, s.version, s.success_rate, s.usage_count
ORDER BY improvement DESC;
```

---

## Implementation Guide

### Setup Supabase

**1. Create Supabase Project:**
```bash
# Via Supabase Dashboard
1. Go to https://supabase.com
2. Create new project
3. Copy URL and API key
```

**2. Run Migrations:**
```bash
# Create tables
supabase db push

# Or use SQL directly
psql $SUPABASE_DATABASE_URL < schema.sql
```

**3. Configure RLS (Row Level Security):**
```sql
-- Enable RLS on tables
ALTER TABLE skills ENABLE ROW LEVEL SECURITY;
ALTER TABLE skill_executions ENABLE ROW LEVEL SECURITY;
ALTER TABLE skill_feedback ENABLE ROW LEVEL SECURITY;

-- Policies (adjust based on auth strategy)
CREATE POLICY "Users can read all skills"
  ON skills FOR SELECT
  USING (true);

CREATE POLICY "Users can create their own skills"
  ON skills FOR INSERT
  WITH CHECK (auth.uid() = author);

CREATE POLICY "Users can update their own skills"
  ON skills FOR UPDATE
  USING (auth.uid() = author);

-- Similar for other tables...
```

### Setup Pinecone

**1. Create Pinecone Index:**
```bash
# Via Pinecone Dashboard
1. Go to https://www.pinecone.io
2. Create index:
   - Name: deepallspeak-skills
   - Dimensions: 1536
   - Metric: cosine
   - Pod type: p1.x1
```

**2. Initialize via API:**
```typescript
import { PineconeClient } from '@pinecone-database/pinecone';

const pinecone = new PineconeClient();
await pinecone.init({
  apiKey: process.env.PINECONE_API_KEY!,
  environment: process.env.PINECONE_ENVIRONMENT!
});

// Check if index exists
const indexList = await pinecone.listIndexes();
if (!indexList.includes('deepallspeak-skills')) {
  await pinecone.createIndex({
    createRequest: {
      name: 'deepallspeak-skills',
      dimension: 1536,
      metric: 'cosine'
    }
  });
}

const index = pinecone.Index('deepallspeak-skills');
```

### MCP Server Implementation

See `scripts/skill-memory-server.js` for complete implementation.

**Key Components:**

```typescript
// 1. Embedding Generator
async function generateEmbedding(text: string): Promise<number[]> {
  const response = await openai.createEmbedding({
    model: "text-embedding-3-small",
    input: text
  });
  return response.data[0].embedding;
}

// 2. Skill Creator
async function createSkill(skill: SkillInput): Promise<Skill> {
  // 1. Validate schema
  validateSkill(skill);

  // 2. Store in Supabase
  const {data, error} = await supabase
    .from('skills')
    .insert({
      name: skill.name,
      description: skill.description,
      category: skill.category,
      prompt_template: skill.promptTemplate,
      input_schema: skill.inputSchema,
      output_schema: skill.outputSchema,
      tags: skill.tags
    })
    .select()
    .single();

  if (error) throw error;

  // 3. Generate embedding
  const embeddingText = `${skill.name}\n${skill.description}\n${skill.category}\n${skill.tags.join(', ')}`;
  const embedding = await generateEmbedding(embeddingText);

  // 4. Store in Pinecone
  await pineconeIndex.upsert([{
    id: data.id,
    values: embedding,
    metadata: {
      skill_id: data.id,
      name: skill.name,
      description: skill.description,
      category: skill.category,
      tags: skill.tags,
      created_at: data.created_at
    }
  }]);

  return data;
}

// 3. Semantic Search
async function searchSkills(
  query: string,
  filters?: {category?: string; tags?: string[]},
  limit = 5
): Promise<SkillSearchResult[]> {
  // 1. Generate query embedding
  const queryEmbedding = await generateEmbedding(query);

  // 2. Search Pinecone
  const pineconeFilter: any = {};
  if (filters?.category) {
    pineconeFilter.category = filters.category;
  }
  if (filters?.tags && filters.tags.length > 0) {
    pineconeFilter.tags = {$in: filters.tags};
  }

  const searchResults = await pineconeIndex.query({
    vector: queryEmbedding,
    topK: limit,
    includeMetadata: true,
    filter: pineconeFilter
  });

  // 3. Fetch full skill data from Supabase
  const skillIds = searchResults.matches.map(m => m.id);
  const {data: skills} = await supabase
    .from('skills')
    .select('*')
    .in('id', skillIds);

  // 4. Combine results
  return searchResults.matches.map(match => {
    const skill = skills.find(s => s.id === match.id);
    return {
      ...skill,
      score: match.score
    };
  });
}

// 4. Skill Executor
async function executeSkill(
  skillId: string,
  inputs: Record<string, any>
): Promise<SkillExecutionResult> {
  // 1. Load skill from Supabase
  const {data: skill, error} = await supabase
    .from('skills')
    .select('*')
    .eq('id', skillId)
    .single();

  if (error) throw error;

  // 2. Validate inputs against schema
  const valid = validateInputs(inputs, skill.input_schema);
  if (!valid) throw new Error('Invalid inputs');

  // 3. Render prompt template
  const prompt = renderTemplate(skill.prompt_template, inputs);

  // 4. Execute via appropriate agent/tool
  const startTime = Date.now();
  const outputs = await executePrompt(prompt, {
    agent: skill.agent,
    tools: skill.tools,
    temperature: skill.temperature,
    maxTokens: skill.max_tokens
  });
  const executionTime = Date.now() - startTime;

  // 5. Record execution
  const {data: execution} = await supabase
    .from('skill_executions')
    .insert({
      skill_id: skillId,
      inputs,
      outputs,
      status: 'success',
      execution_time_ms: executionTime
    })
    .select()
    .single();

  return {
    success: true,
    executionId: execution.id,
    outputs,
    executionTimeMs: executionTime
  };
}
```

---

## Best Practices

### 1. Skill Naming

**Good:**
- `analyze-sales-report`
- `generate-api-documentation`
- `review-code-security`

**Bad:**
- `skill1`, `my_skill`, `test`
- `analyzeAndGenerateReportsWithCharts` (too long)
- `Sales Analysis` (use kebab-case, not spaces)

### 2. Prompt Templates

**Good:**
```
Analyze the following {{document_type}} for {{focus_area}}.

Data:
{{data}}

Provide:
1. Key metrics
2. Trends
3. Actionable insights
```

**Bad:**
```
Analyze this  // Too vague
Please analyze the data I provide and give me good insights  // No structure
```

### 3. Input Schemas

**Always:**
- Provide clear descriptions
- Set sensible defaults
- Use enums for constrained values
- Mark required fields
- Add validation (min/max, patterns, etc.)

**Example:**
```json
{
  "type": "object",
  "properties": {
    "data": {
      "type": "string",
      "description": "Sales data in CSV or JSON format",
      "minLength": 10
    },
    "period": {
      "type": "string",
      "enum": ["Q1", "Q2", "Q3", "Q4"],
      "description": "Which quarter to analyze"
    },
    "currency": {
      "type": "string",
      "default": "USD",
      "pattern": "^[A-Z]{3}$",
      "description": "Currency code (ISO 4217)"
    }
  },
  "required": ["data", "period"]
}
```

### 4. Categorization & Tagging

**Categories:** Broad, stable classifications
- business_intelligence
- code_generation
- document_analysis

**Tags:** Specific, flexible keywords
- sales, analytics, quarterly
- python, api, rest
- pdf, citations, rag

**Use both for effective filtering:**
```typescript
// Find all code generation skills related to APIs
searchSkills("generate API code", {
  category: "code_generation",
  tags: ["api", "rest"]
});
```

### 5. Version Management

**When to increment version:**
- ✅ Major prompt changes
- ✅ Input schema changes (breaking)
- ✅ Different agent/tool requirements

**When to update in-place:**
- ✅ Minor prompt refinements
- ✅ Description updates
- ✅ Adding optional parameters
- ✅ Tag updates

**Always keep old versions:**
```sql
-- Parent-child relationship
skill_v2.parent_skill_id = skill_v1.id
```

### 6. Security

**Never store in skills:**
- ❌ API keys
- ❌ Passwords
- ❌ Personal information
- ❌ Sensitive business data

**Use environment variables and secrets management:**
```typescript
// Good
const apiKey = process.env.API_KEY;

// Bad (hardcoded in skill)
const apiKey = "sk-12345...";
```

**Validate all inputs:**
```typescript
// Prevent injection attacks
function validateInput(input: string): boolean {
  // Check for suspicious patterns
  if (input.includes('{{')) return false;
  if (input.includes('}}')) return false;
  // More validation...
  return true;
}
```

### 7. Performance

**Optimize embedding generation:**
```typescript
// Batch embeddings when creating multiple skills
const embeddings = await openai.createEmbedding({
  model: "text-embedding-3-small",
  input: skills.map(s => `${s.name}\n${s.description}...`)
});
```

**Cache frequently used skills:**
```typescript
const skillCache = new Map();

async function getSkill(id: string): Promise<Skill> {
  if (skillCache.has(id)) {
    return skillCache.get(id);
  }
  const skill = await fetchSkillFromDatabase(id);
  skillCache.set(id, skill);
  return skill;
}
```

**Index optimization:**
```sql
-- Ensure proper indexes exist
CREATE INDEX CONCURRENTLY idx_skills_category_tags
  ON skills(category, tags);
```

---

## Summary

The Self-Memory System transforms DeepAllSpeak from a stateless AI assistant into a **self-improving, learning system** that:

1. **Remembers** - Stores skills in Supabase for persistence
2. **Learns** - Improves skills based on usage patterns
3. **Retrieves** - Finds relevant skills via semantic search (Pinecone)
4. **Executes** - Runs stored skills faster and more consistently
5. **Evolves** - Continuously refines skills based on feedback

**Key Benefits:**
- ⚡ Faster execution of repeated tasks
- 🎯 More consistent results
- 📈 Continuous improvement over time
- 🧠 Personalized to individual usage patterns
- 💾 Knowledge retention across sessions

**Next Steps:**
1. Set up Supabase and Pinecone
2. Implement MCP server (see `scripts/skill-memory-server.js`)
3. Start creating skills manually
4. Enable auto-suggestion for repeated tasks
5. Monitor improvement metrics
6. Iterate and refine based on feedback

---

**The AI that learns from you, for you.** 🚀
