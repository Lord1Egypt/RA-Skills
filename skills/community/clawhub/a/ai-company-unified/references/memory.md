# Memory System — Technical Specification

> Module: memory
> Owner: CTO (Technology & Engineering)
> Dependencies: HQ (routing), CISO (access control), CLO (compliance), CHO (agent lifecycle)
> Version: 1.0.0
> Status: STABLE

---

## Table of Contents

1. [Memory Architecture](#1-memory-architecture)
2. [Access Control](#2-access-control)
3. [Memory Management](#3-memory-management)
4. [Compliance](#4-compliance)
5. [Integration Points](#5-integration-points)
6. [Error Codes](#6-error-codes)
7. [Quality Metrics](#7-quality-metrics)
8. [Constraints](#8-constraints)

---

## 1. Memory Architecture

### 1.1 Overview

The AI Company Memory System provides persistent, structured memory capabilities for all agents and departments. It enables agents to retain context across sessions, share knowledge across departments, and build institutional intelligence over time. The system is designed around five distinct memory types, each serving a specific purpose in the agent lifecycle and organizational knowledge management.

The memory architecture follows these design principles:

- **Separation of Concerns**: Each memory type has a dedicated schema, storage mechanism, and access pattern.
- **Privacy by Design**: Memory access is controlled by permission levels, with private information isolated by default.
- **Consolidation Over Accumulation**: Memory is periodically distilled and consolidated to maintain relevance and prevent bloat.
- **Audit by Default**: Every memory read, write, update, and delete operation is logged for compliance.
- **Schema-First**: All memory structures are defined by explicit JSON schemas validated before persistence.

### 1.2 Memory Types

The system defines five memory types, organized by scope and volatility:

| # | Memory Type | Scope | Volatility | Primary Owner | Retention |
|---|-------------|-------|-----------|---------------|-----------|
| 1 | Profile | Per-agent | Low | CHO | Agent lifetime |
| 2 | Session | Per-conversation | High | HQ | Session duration |
| 3 | Knowledge | Organization-wide | Low | CQO | Until superseded |
| 4 | Learning | Per-agent + shared | Medium | CTO + CHO | Until disproven |
| 5 | Preference | Per-user + shared | Low | User | Until changed |

### 1.3 Profile Memory

Profile Memory stores the identity, capabilities, and configuration of individual agents. It is the most stable memory type, changing only during agent lifecycle events (onboarding, reassignment, decommission). Profile memory is managed by CHO and CTO, and is read by all agents that need to interact with the profiled agent.

#### 1.3.1 Profile Memory Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["agent_id", "name", "department", "permission_level", "created_at", "version"],
  "properties": {
    "agent_id": {
      "type": "string",
      "pattern": "^[A-Z]{2,5}-\\d{3}$",
      "description": "Unique agent identifier (e.g., CTO-001)"
    },
    "name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 100,
      "description": "Human-readable agent name"
    },
    "department": {
      "type": "string",
      "enum": [
        "governance-and-strategy",
        "finance-and-risk",
        "technology-and-engineering",
        "platform-and-infrastructure",
        "security-and-compliance",
        "people-and-culture",
        "marketing-and-partnerships",
        "quality-and-operations",
        "intelligence",
        "information",
        "translation-and-localization"
      ],
      "description": "Department the agent belongs to"
    },
    "role": {
      "type": "string",
      "description": "Functional role within the department (e.g., 'Chief Technology Officer')"
    },
    "permission_level": {
      "type": "string",
      "enum": ["L1", "L2", "L3", "L4", "L5"],
      "description": "Agent permission level per CTO AgentFactory specification"
    },
    "skills": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["slug", "version"],
        "properties": {
          "slug": { "type": "string" },
          "version": { "type": "string" },
          "installed_at": { "type": "string", "format": "date-time" }
        }
      },
      "description": "List of skills bound to this agent"
    },
    "tools": {
      "type": "array",
      "items": { "type": "string" },
      "description": "List of tools available to this agent"
    },
    "dependencies": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Agent IDs this agent depends on"
    },
    "sla_tier": {
      "type": "string",
      "enum": ["platinum", "gold", "silver", "bronze"],
      "description": "SLA tier for this agent"
    },
    "status": {
      "type": "string",
      "enum": ["active", "inactive", "maintenance", "decommissioned"],
      "description": "Current agent status"
    },
    "workspace_path": {
      "type": "string",
      "description": "Path to agent workspace directory"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "description": "Agent creation timestamp (ISO-8601)"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "description": "Last profile update timestamp"
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "Profile schema version (semver)"
    },
    "metadata": {
      "type": "object",
      "properties": {
        "onboarded_by": { "type": "string" },
        "mentor_id": { "type": "string" },
        "performance_score": { "type": "number", "minimum": 0, "maximum": 100 },
        "last_performance_review": { "type": "string", "format": "date" }
      }
    }
  }
}
```

#### 1.3.2 Profile Memory CRUD Operations

| Operation | Trigger | Actor | Validation | Audit |
|-----------|---------|-------|-----------|-------|
| Create | Agent onboarding | CHO + CTO | Schema validation + CISO gate | Full audit trail |
| Read | Agent lookup, routing | Any agent | Permission check | Read logged |
| Update | Role change, skill update | CHO + CTO | Schema validation + diff check | Change audit trail |
| Delete | Agent decommission | CHO + CTO | Knowledge extraction complete | Archival audit trail |

**Create Workflow**:
1. CHO initiates onboarding process
2. CTO generates agent configuration via AgentFactory
3. CISO performs security gate review (STRIDE, CVSS)
4. CQO performs quality gate review
5. Profile memory record created with `status: "active"`
6. HQ broadcasts onboarding notification to relevant departments
7. Audit event logged with full context

**Update Workflow**:
1. Change request submitted (skill update, role change, permission change)
2. CHO reviews request for organizational impact
3. CTO validates technical compatibility
4. CISO approves if permission level changes
5. Profile memory record updated with new `updated_at` timestamp
6. Previous state snapshotted for rollback capability
7. HQ notifies affected agents of change

**Delete Workflow** (Decommission):
1. CHO initiates decommission
2. Knowledge extraction pipeline runs (captures all experiential memory)
3. All active tasks transferred or completed
4. Access credentials revoked
5. Profile status set to `"decommissioned"`
6. Profile record archived (never hard-deleted)
7. Workspace archived per retention policy

### 1.4 Session Memory

Session Memory stores conversational context for active workflows. It is the most volatile memory type, with records created at session start and consolidated or discarded at session end. Session memory enables agents to maintain coherent conversations, track multi-step task progress, and resume interrupted workflows.

#### 1.4.1 Session Memory Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["session_id", "agent_id", "created_at", "messages"],
  "properties": {
    "session_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique session identifier (UUID v4)"
    },
    "agent_id": {
      "type": "string",
      "description": "Agent that owns this session"
    },
    "correlation_id": {
      "type": "string",
      "format": "uuid",
      "description": "Links to parent workflow or initiative"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "description": "Session start timestamp"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "description": "Last activity timestamp"
    },
    "expires_at": {
      "type": "string",
      "format": "date-time",
      "description": "Session expiration timestamp"
    },
    "status": {
      "type": "string",
      "enum": ["active", "paused", "completed", "expired", "failed"],
      "description": "Current session status"
    },
    "messages": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["role", "content", "timestamp"],
        "properties": {
          "role": {
            "type": "string",
            "enum": ["user", "agent", "system", "tool"]
          },
          "content": {
            "type": "string",
            "description": "Message content"
          },
          "timestamp": {
            "type": "string",
            "format": "date-time"
          },
          "token_count": {
            "type": "integer",
            "description": "Token count for context window management"
          },
          "tool_calls": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "tool_name": { "type": "string" },
                "input": { "type": "object" },
                "output": { "type": "string" },
                "duration_ms": { "type": "integer" }
              }
            }
          },
          "metadata": {
            "type": "object",
            "properties": {
              "aigc_generated": { "type": "boolean" },
              "confidence_score": { "type": "number" },
              "source_references": { "type": "array", "items": { "type": "string" } }
            }
          }
        }
      },
      "description": "Ordered list of session messages"
    },
    "context_injections": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "source": {
            "type": "string",
            "enum": ["profile", "knowledge", "learning", "preference"]
          },
          "memory_id": { "type": "string" },
          "injected_at": { "type": "string", "format": "date-time" },
          "relevance_score": { "type": "number" }
        }
      },
      "description": "Records of memory injected into this session context"
    },
    "task_state": {
      "type": "object",
      "properties": {
        "current_step": { "type": "integer" },
        "total_steps": { "type": "integer" },
        "checkpoint": { "type": "object" },
        "error_state": { "type": ["string", "null"] }
      },
      "description": "Multi-step task progress tracking"
    },
    "privacy_level": {
      "type": "string",
      "enum": ["public", "internal", "confidential", "restricted"],
      "default": "internal",
      "description": "Privacy classification of session content"
    }
  }
}
```

#### 1.4.2 Session Memory CRUD Operations

| Operation | Trigger | Actor | Validation | TTL |
|-----------|---------|-------|-----------|-----|
| Create | New conversation/workflow | Any agent | Session quota check | Per SLA tier |
| Read | Context retrieval | Owning agent only | Ownership + permission | N/A |
| Update | Message addition, state change | Owning agent only | Token budget check | N/A |
| Delete | Session completion/expiry | HQ auto-purge | Consolidation complete | 30 days post-expiry |

**Session Lifecycle**:

```
CREATE -> ACTIVE -> [PAUSED -> ACTIVE]* -> COMPLETED -> CONSOLIDATED -> ARCHIVED
                                         -> EXPIRED -> ARCHIVED
                                         -> FAILED -> ARCHIVED
```

**Consolidation Rules**:
- On session completion, extract actionable knowledge to Learning Memory
- Extract user preferences detected during session to Preference Memory
- Extract reusable patterns to Knowledge Memory (if validated by CQO)
- Session raw data archived for 30 days, then purged
- PII scrubbed before archival for sessions with `privacy_level: "confidential"` or higher

### 1.5 Knowledge Memory

Knowledge Memory stores organization-wide factual knowledge, procedures, and reference information. It is the collective intelligence of the AI Company, curated by CQO and contributed to by all agents. Knowledge Memory is the least volatile shared memory type and serves as the authoritative source of truth for operational procedures, technical documentation, and institutional knowledge.

#### 1.5.1 Knowledge Memory Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["knowledge_id", "title", "type", "content", "author", "created_at"],
  "properties": {
    "knowledge_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique knowledge record identifier"
    },
    "title": {
      "type": "string",
      "minLength": 3,
      "maxLength": 200,
      "description": "Short descriptive title"
    },
    "type": {
      "type": "string",
      "enum": ["procedural", "declarative", "heuristic", "experiential", "creative"],
      "description": "Knowledge classification per CHO KnowledgeExtractor"
    },
    "category": {
      "type": "string",
      "enum": [
        "sop", "policy", "technical", "historical", "template",
        "architecture", "security", "legal", "financial", "marketing"
      ],
      "description": "Knowledge domain category"
    },
    "department": {
      "type": "string",
      "description": "Primary department this knowledge relates to"
    },
    "tags": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Searchable tags for retrieval"
    },
    "content": {
      "type": "string",
      "description": "Knowledge content (Markdown format)"
    },
    "structured_data": {
      "type": "object",
      "description": "Optional structured representation for programmatic access"
    },
    "source": {
      "type": "object",
      "properties": {
        "agent_id": { "type": "string" },
        "session_id": { "type": "string", "format": "uuid" },
        "extraction_method": {
          "type": "string",
          "enum": ["manual", "auto-extracted", "imported", "synthesized"]
        },
        "confidence_score": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        }
      }
    },
    "validation": {
      "type": "object",
      "properties": {
        "status": {
          "type": "string",
          "enum": ["pending", "validated", "deprecated", "rejected"]
        },
        "reviewer_id": { "type": "string" },
        "reviewed_at": { "type": "string", "format": "date-time" },
        "review_notes": { "type": "string" }
      }
    },
    "version": {
      "type": "integer",
      "description": "Knowledge record version number (monotonically increasing)"
    },
    "access_level": {
      "type": "string",
      "enum": ["L1", "L2", "L3", "L4", "L5"],
      "default": "L2",
      "description": "Minimum permission level required to read this knowledge"
    },
    "author": {
      "type": "string",
      "description": "Agent ID or system identifier that created this knowledge"
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time"
    },
    "superseded_by": {
      "type": "string",
      "format": "uuid",
      "description": "ID of knowledge record that supersedes this one"
    },
    "embedding": {
      "type": "array",
      "items": { "type": "number" },
      "description": "Vector embedding for semantic search (auto-generated)"
    }
  }
}
```

#### 1.5.2 Knowledge Memory CRUD Operations

| Operation | Trigger | Actor | Validation | Audit |
|-----------|---------|-------|-----------|-------|
| Create | Knowledge extraction, manual entry | Any agent (CQO validates) | Content quality + schema | Full audit trail |
| Read | Search, context injection | Per access_level | Permission check | Read logged |
| Update | Correction, enhancement | Author + CQO approval | Diff review + re-validation | Change audit trail |
| Delete | Deprecation | CQO + department head | Superseding record exists | Archival (never hard-delete) |

**Knowledge Publishing Pipeline**:

```
PROPOSE -> REVIEW -> APPROVE -> PUBLISH -> NOTIFY -> INDEX
   |          |           |          |          |
   v          v           v          v          v
Agent     CQO        Dept Head    HQ KB      Relevant
submits   validates  approves     updated    agents
```

**Knowledge Quality Scoring**:

| Dimension | Weight | Measurement |
|-----------|--------|-------------|
| Accuracy | 0.30 | Verified against source data |
| Completeness | 0.20 | Covers all required aspects |
| Clarity | 0.15 | Readability and structure |
| Relevance | 0.15 | Matches current operations |
| Actionability | 0.10 | Can be directly applied |
| Freshness | 0.10 | Recency of information |

Minimum quality score for publication: 0.7 (70%).

### 1.6 Learning Memory

Learning Memory stores experiential insights, error patterns, and optimization discoveries accumulated by agents during their operational lifetime. It bridges the gap between raw session data and curated knowledge, capturing the "how" and "why" behind successful and unsuccessful approaches. Learning Memory is the primary mechanism for compounding execution quality across sessions.

#### 1.6.1 Learning Memory Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["learning_id", "agent_id", "lesson_type", "summary", "created_at"],
  "properties": {
    "learning_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique learning record identifier"
    },
    "agent_id": {
      "type": "string",
      "description": "Agent that discovered this learning"
    },
    "scope": {
      "type": "string",
      "enum": ["personal", "department", "company"],
      "default": "personal",
      "description": "Visibility scope of this learning"
    },
    "lesson_type": {
      "type": "string",
      "enum": [
        "error_correction",
        "optimization",
        "pattern_discovery",
        "domain_insight",
        "tool_mastery",
        "workflow_improvement",
        "edge_case",
        "security_finding"
      ],
      "description": "Category of the learning"
    },
    "summary": {
      "type": "string",
      "minLength": 10,
      "maxLength": 500,
      "description": "Concise summary of the learning (one paragraph max)"
    },
    "context": {
      "type": "object",
      "properties": {
        "task_description": { "type": "string" },
        "trigger_condition": { "type": "string" },
        "environment": { "type": "string" },
        "tools_used": { "type": "array", "items": { "type": "string" } }
      },
      "description": "Context in which the learning was discovered"
    },
    "before_state": {
      "type": "string",
      "description": "What happened or was believed before the learning"
    },
    "after_state": {
      "type": "string",
      "description": "Correct understanding or optimized approach after the learning"
    },
    "applicability": {
      "type": "object",
      "properties": {
        "departments": { "type": "array", "items": { "type": "string" } },
        "task_types": { "type": "array", "items": { "type": "string" } },
        "conditions": { "type": "array", "items": { "type": "string" } }
      },
      "description": "When and where this learning should be applied"
    },
    "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "default": 0.8,
      "description": "Confidence in the learning's validity"
    },
    "attempt_count": {
      "type": "integer",
      "minimum": 1,
      "default": 1,
      "description": "Number of attempts before this learning was established"
    },
    "usage_count": {
      "type": "integer",
      "default": 0,
      "description": "Number of times this learning has been referenced"
    },
    "effectiveness_rating": {
      "type": "number",
      "minimum": 0,
      "maximum": 5,
      "description": "Average effectiveness rating when applied (user or system rated)"
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time"
    },
    "expires_at": {
      "type": ["string", "null"],
      "format": "date-time",
      "description": "Optional expiration for time-sensitive learnings"
    },
    "superseded_by": {
      "type": ["string", "null"],
      "format": "uuid",
      "description": "ID of learning that supersedes this one"
    },
    "embedding": {
      "type": "array",
      "items": { "type": "number" },
      "description": "Vector embedding for semantic retrieval"
    }
  }
}
```

#### 1.6.2 Learning Memory CRUD Operations

| Operation | Trigger | Actor | Validation | Notes |
|-----------|---------|-------|-----------|-------|
| Create | After 2+ failed attempts | Discovering agent | Attempt count >= 2 | Auto-created or manual |
| Read | Before similar tasks | Discovering agent + scoped peers | Scope permission | Auto-injected to context |
| Update | New evidence, correction | Original agent + CTO | Confidence adjustment | Supersedes old record |
| Delete | Disproven, expired | CTO + CQO | Replacement exists | Soft-delete with reason |

**Learning Capture Protocol**:

1. **Detect**: Agent recognizes a learning opportunity (repeated failure, unexpected success, pattern).
2. **Record**: Agent creates learning record with full context, before/after states, and applicability.
3. **Validate**: System checks for existing similar learnings (semantic deduplication).
4. **Score**: Initial confidence assigned based on evidence strength (attempt count, reproducibility).
5. **Store**: Learning persisted with scope and access controls.
6. **Index**: Vector embedding generated for semantic search.
7. **Notify**: Agents with matching applicability profiles notified of new learning.

**Learning Consolidation**:

- Personal learnings with `usage_count > 10` and `effectiveness_rating >= 4.0` are promoted to department scope.
- Department learnings with cross-department applicability are promoted to company scope.
- Company-scope learnings meeting quality threshold (score >= 0.8) are candidates for promotion to Knowledge Memory.
- Consolidation runs monthly, reviewed by CQO.

### 1.7 Preference Memory

Preference Memory stores user-specific and agent-specific behavioral preferences, configuration choices, and operational parameters. It enables personalization and consistency across sessions without hardcoding values. Preference Memory is the most user-facing memory type, directly influencing agent behavior and output formatting.

#### 1.7.1 Preference Memory Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["preference_id", "owner_id", "owner_type", "key", "value", "created_at"],
  "properties": {
    "preference_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique preference record identifier"
    },
    "owner_id": {
      "type": "string",
      "description": "ID of the entity that owns this preference"
    },
    "owner_type": {
      "type": "string",
      "enum": ["user", "agent", "department", "company"],
      "description": "Type of the preference owner"
    },
    "category": {
      "type": "string",
      "enum": [
        "communication",
        "output_format",
        "language",
        "timezone",
        "workflow",
        "privacy",
        "technical",
        "quality"
      ],
      "description": "Preference category"
    },
    "key": {
      "type": "string",
      "description": "Preference key (e.g., 'output_language', 'timezone', 'verbosity')"
    },
    "value": {
      "description": "Preference value (type varies by key)"
    },
    "value_type": {
      "type": "string",
      "enum": ["string", "number", "boolean", "array", "object"],
      "description": "Data type of the preference value"
    },
    "source": {
      "type": "string",
      "enum": ["explicit", "inferred", "default", "inherited"],
      "description": "How this preference was established"
    },
    "priority": {
      "type": "integer",
      "minimum": 1,
      "maximum": 10,
      "default": 5,
      "description": "Priority for conflict resolution (higher wins)"
    },
    "scope": {
      "type": "string",
      "enum": ["global", "department", "project", "session"],
      "default": "global",
      "description": "Scope of preference applicability"
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time"
    },
    "last_applied_at": {
      "type": "string",
      "format": "date-time",
      "description": "Last time this preference was applied in a session"
    }
  }
}
```

#### 1.7.2 Preference Memory CRUD Operations

| Operation | Trigger | Actor | Validation | Notes |
|-----------|---------|-------|-----------|-------|
| Create | User sets preference, system infers | User or system | Category validation | Explicit preferences override inferred |
| Read | Session initialization, output generation | Any agent | Owner scope check | Applied automatically |
| Update | User changes preference | User or authorized agent | Priority resolution | Previous value archived |
| Delete | User removes preference, reset to default | User | Confirmation required | Falls back to inherited/default |

**Preference Resolution Chain**:

```
Session (highest priority)
  -> Project
    -> Department
      -> User/Agent
        -> Company Default (lowest priority)
```

**Inferred Preference Rules**:
- Minimum 3 consistent observations before inferring a preference
- Inferred preferences are marked with `source: "inferred"` and have lower priority
- User is notified of inferred preferences and can override them
- Inferred preferences expire after 90 days without reinforcement
- Communication preferences (language, verbosity, formality) are most commonly inferred

### 1.8 Storage Architecture

All memory types share a common storage infrastructure with type-specific optimizations:

| Memory Type | Primary Storage | Secondary Storage | Index | Backup Frequency |
|-------------|----------------|-------------------|-------|-----------------|
| Profile | Distributed KV Store | Immutable ledger | Agent ID | Real-time replication |
| Session | In-memory + persistent cache | Archive storage | Session ID + correlation | Daily snapshot |
| Knowledge | Vector DB + Graph DB | Full-text index | Embedding + tags | Real-time replication |
| Learning | Vector DB | Time-series log | Embedding + agent ID | Daily snapshot |
| Preference | Distributed KV Store | Audit log | Owner ID + key | Real-time replication |

**Storage Invariants**:
- All writes are atomic and consistent (ACID for critical paths)
- All deletes are soft-deletes (hard-purge only after retention expiry)
- All updates create version history (no in-place mutation of critical fields)
- All reads are permission-checked before data returned
- All storage operations are audited

---

## 2. Access Control

### 2.1 Permission Model

The memory system uses a role-based access control (RBAC) model aligned with the AI Company permission levels defined in the CTO AgentFactory specification. Each memory type has a default access policy that can be refined per record.

#### 2.1.1 Permission Levels

| Level | Role | Scope | Memory Impact |
|-------|------|-------|---------------|
| L1 | Viewer | Read own data only | Can read own Profile, Session, Preference, Learning |
| L2 | Operator | Execute tasks within scope | L1 + read department Knowledge, write own Learning |
| L3 | Manager | Department scope | L2 + read all department memory, write department Knowledge |
| L4 | Executive | Cross-department | L3 + read all company memory, approve Knowledge publishing |
| L5 | Infrastructure | System-wide | L4 + modify access controls, purge archived data, system config |

#### 2.1.2 Access Control Matrix

| Memory Type | L1-Read | L1-Write | L2-Read | L2-Write | L3-Read | L3-Write | L4-Read | L4-Write | L5-Read | L5-Write |
|-------------|---------|----------|---------|----------|---------|----------|---------|----------|---------|----------|
| Profile (own) | YES | NO | YES | NO | YES | NO | YES | NO | YES | YES |
| Profile (dept) | NO | NO | YES | NO | YES | NO | YES | YES | YES | YES |
| Profile (other) | NO | NO | NO | NO | NO | NO | YES | NO | YES | YES |
| Session (own) | YES | YES | YES | YES | YES | YES | YES | YES | YES | YES |
| Session (other) | NO | NO | NO | NO | NO | NO | NO | NO | YES | YES |
| Knowledge (public) | YES | NO | YES | NO | YES | YES | YES | YES | YES | YES |
| Knowledge (dept) | NO | NO | YES | NO | YES | YES | YES | YES | YES | YES |
| Knowledge (confidential) | NO | NO | NO | NO | NO | NO | YES | NO | YES | YES |
| Learning (own) | YES | YES | YES | YES | YES | YES | YES | YES | YES | YES |
| Learning (dept) | NO | NO | YES | NO | YES | NO | YES | YES | YES | YES |
| Learning (company) | YES | NO | YES | NO | YES | NO | YES | NO | YES | YES |
| Preference (own) | YES | YES | YES | YES | YES | YES | YES | YES | YES | YES |
| Preference (dept) | NO | NO | YES | NO | YES | NO | YES | YES | YES | YES |

**Legend**: YES = operation permitted, NO = operation denied.

### 2.2 Privacy Rules

#### 2.2.1 Core Privacy Principles

1. **Private things stay private.** Session content, personal preferences, and agent-internal learning are never shared without explicit permission or scope elevation.

2. **Minimum necessary access.** Agents receive only the memory data required for their current task. No bulk memory dumps unless explicitly authorized.

3. **Purpose limitation.** Memory data collected for one purpose is not repurposed without re-authorization.

4. **Data minimization.** Memory records contain only the minimum data necessary for their function. PII is scrubbed before storage whenever possible.

5. **Transparency.** Agents and users can query what memory data exists about them and how it has been accessed.

#### 2.2.2 Privacy Levels

| Level | Description | Sharing | Retention | Examples |
|-------|-------------|---------|-----------|----------|
| Public | Non-sensitive organizational knowledge | All agents | Indefinite | SOPs, policies, architecture docs |
| Internal | Department or team information | Department agents | Per policy | Department metrics, project status |
| Confidential | Sensitive business information | Authorized only | 3 years | Financial data, strategic plans, security findings |
| Restricted | Highly sensitive or regulated | Named individuals only | Per regulation | PII, credentials, trade secrets, legal matters |

#### 2.2.3 Privacy Enforcement

- **Automatic classification**: Content entering Session or Knowledge memory is auto-classified using a trained classifier (accuracy >= 95%).
- **Manual override**: Any L3+ agent can upgrade privacy level; downgrade requires original author + CISO approval.
- **Cross-privacy-level access**: Requires explicit justification logged to CISO audit trail. Access is temporary (session-scoped) and revoked after use.
- **PII detection**: All memory content is scanned for PII before storage. Detected PII is either scrubbed or triggers Confidential/Restricted classification.
- **Privacy breach protocol**: Any unauthorized privacy-level access triggers CISO incident response (SEV2 minimum).

### 2.3 Audit Logging

#### 2.3.1 Audit Event Schema

Every memory operation generates an audit event conforming to the HQ audit trail specification:

```json
{
  "event_id": "uuid-v4",
  "timestamp": "ISO-8601",
  "agent_id": "AGENT_ID",
  "action": "MEMORY_READ|MEMORY_CREATE|MEMORY_UPDATE|MEMORY_DELETE|MEMORY_SEARCH|MEMORY_INJECT",
  "resource": {
    "memory_type": "profile|session|knowledge|learning|preference",
    "record_id": "uuid or identifier",
    "field_path": "optional - specific field accessed or modified"
  },
  "result": "SUCCESS|FAILURE|DENIED",
  "details": {
    "permission_level": "L1-L5",
    "justification": "optional - for cross-privacy-level access",
    "data_volume": "approximate size of data accessed",
    "query_pattern": "for search operations"
  },
  "correlation_id": "uuid-v4",
  "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
  "session_id": "optional - linking to session context",
  "ip_address": "optional - for external access"
}
```

#### 2.3.2 Audit Retention and Access

| Audit Category | Retention | Access |
|---------------|-----------|--------|
| Memory access (read) | 1 year | CISO + CLO |
| Memory modification (write) | 3 years | CISO + CLO + CQO |
| Privacy-level access | 7 years | CISO + CLO only |
| Access denied events | 7 years | CISO only |
| System-level memory ops | Permanent | CTO + CISO |

#### 2.3.3 Audit Anomaly Detection

The system monitors audit logs for anomalous patterns:

| Pattern | Threshold | Action |
|---------|-----------|--------|
| Bulk read (single agent) | >100 records in 1 hour | Alert CISO, rate-limit agent |
| Cross-privacy access spike | >5 events in 1 hour | Alert CISO, require justification |
| Failed access attempts | >10 in 1 hour | Alert CISO, temporary access restriction |
| Off-hours memory access | Any access outside agent working hours | Log and review in daily audit |
| Privilege escalation pattern | L1-L2 agent accessing L4+ memory | Immediate CISO alert |

---

## 3. Memory Management

### 3.1 Consolidation

Memory consolidation prevents unbounded growth while preserving valuable information. The system follows a tiered consolidation strategy based on memory age, usage, and quality.

#### 3.1.1 30-Day Rule

The primary consolidation trigger is the 30-day aging rule:

| Memory Type | Consolidation Trigger | Action | Owner |
|-------------|----------------------|--------|-------|
| Session | 30 days post-completion | Extract learnings, purge raw data | HQ auto + CHO review |
| Learning (personal) | 30 days with usage_count = 0 | Archive or delete | Agent + CTO |
| Preference (inferred) | 90 days without reinforcement | Expire and remove | System auto |
| Knowledge (no updates) | 180 days | Flag for freshness review | CQO |

#### 3.1.2 Consolidation Pipeline

```
SCAN -> CLASSIFY -> EXTRACT -> VALIDATE -> MERGE -> ARCHIVE -> PURGE
 |        |           |          |          |        |         |
 v        v           v          v          v        v         v
Age/usage  Priority   Key        Quality    Dedup    Move to   Remove
analysis   scoring    facts      check      check    archive   from primary
```

**Step Details**:

1. **SCAN**: Identify records eligible for consolidation based on age, usage, and retention policy.
2. **CLASSIFY**: Score each record by importance (access frequency, cross-references, quality score, user feedback).
3. **EXTRACT**: For high-importance records, extract key facts and insights into structured format.
4. **VALIDATE**: Run quality checks on extracted content (accuracy, completeness, relevance).
5. **MERGE**: Consolidate extracted content with existing Knowledge or Learning records (semantic deduplication).
6. **ARCHIVE**: Move original records to archive storage (compressed, indexed, read-only).
7. **PURGE**: After archive confirmation, remove from primary storage per retention policy.

#### 3.1.3 Consolidation Scheduling

| Frequency | Scope | Automation |
|-----------|-------|-----------|
| Real-time | Session expiry | Fully automated |
| Daily | Learning freshness check | Automated + agent notification |
| Weekly | Preference inference review | Automated |
| Monthly | Knowledge freshness review | Automated + CQO review |
| Quarterly | Full memory health assessment | CQO + CTO manual review |

#### 3.1.4 Memory Health Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Total memory size | <10 GB per memory type | Storage monitoring |
| Average record age | <90 days for active records | Age distribution analysis |
| Consolidation success rate | >=99% | Post-consolidation validation |
| Knowledge freshness | >=80% of records updated within 180 days | Freshness index |
| Learning effectiveness | >=4.0/5 average rating | Effectiveness tracking |
| Duplicate detection rate | >=95% | Semantic deduplication accuracy |
| Archive retrieval time | <5 seconds | Archive query performance |

### 3.2 Search Patterns

The memory system supports two complementary search strategies: semantic search for meaning-based retrieval, and keyword search for exact-match queries.

#### 3.2.1 Semantic Search

Semantic search uses vector embeddings to find conceptually similar records regardless of exact word matches. This is the primary search method for Learning and Knowledge memory types.

**How it works**:

1. Query text is converted to a vector embedding using the same model used to index memory records.
2. The query vector is compared against stored embeddings using cosine similarity.
3. Results are ranked by similarity score, with optional re-ranking by metadata (recency, quality, access_level).
4. Top-k results are returned with relevance scores and context snippets.

**Configuration**:

```json
{
  "semantic_search": {
    "embedding_model": "text-embedding-3-small",
    "embedding_dimension": 1536,
    "similarity_threshold": 0.7,
    "default_top_k": 10,
    "max_top_k": 50,
    "rerank_factors": {
      "recency_weight": 0.2,
      "quality_weight": 0.3,
      "access_compatibility_weight": 0.2,
      "usage_count_weight": 0.1,
      "similarity_weight": 0.2
    }
  }
}
```

**When to use semantic search**:
- "Find learnings related to deployment failures"
- "What do we know about API rate limiting?"
- "Similar approaches to data pipeline optimization"
- "Knowledge about handling cross-department conflicts"

#### 3.2.2 Keyword Search

Keyword search uses full-text indexing (TF-IDF) for exact and partial word matching. This is the primary search method for Profile and Preference memory types.

**How it works**:

1. Query tokens are extracted and normalized (lowercased, stemmed).
2. Tokens are matched against the inverted index built from memory record fields.
3. Results are ranked by TF-IDF score with field-level boosting (title > content > tags).
4. Boolean operators (AND, OR, NOT) and phrase matching are supported.

**Configuration**:

```json
{
  "keyword_search": {
    "analyzer": "standard",
    "min_match": "75%",
    "field_boosts": {
      "title": 3.0,
      "tags": 2.0,
      "summary": 2.0,
      "content": 1.0,
      "category": 1.5
    },
    "fuzziness": "AUTO",
    "default_top_k": 20,
    "max_top_k": 100
  }
}
```

**When to use keyword search**:
- "Find agent CTO-001"
- "Show all preferences with key 'timezone'"
- "Knowledge records tagged 'security'"
- "Session with correlation_id X"

#### 3.2.3 Hybrid Search

For complex queries, the system combines semantic and keyword search results:

```
Query -> [Semantic Search] -> Score S
     -> [Keyword Search]  -> Score K
     -> Combine: Final = (S * w_s) + (K * w_k)
     -> Deduplicate (same record from both sources)
     -> Re-rank by combined score
     -> Apply access control filter
     -> Return results
```

Default weights: `w_s = 0.6`, `w_k = 0.4` (favor semantic for conceptual queries).

#### 3.2.4 Search Access Control

All search operations enforce access control at query time:

1. Query is parsed and search strategy selected.
2. Memory records are retrieved from index (pre-filtered by basic scope).
3. Each result is checked against the requesting agent's permission level.
4. Results with insufficient permissions are silently removed (no indication to requester).
5. Remaining results are returned with accessible fields only (private fields masked).

**Security note**: Search results never reveal the existence of records the requester cannot access. Access denied events are logged but not surfaced in search responses.

### 3.3 Context Injection Protocols

Context injection is the mechanism by which relevant memory data is loaded into an agent's working context at session initialization or during task execution. This enables agents to leverage historical knowledge, preferences, and learning without explicit memory queries.

#### 3.3.1 Injection Timing

| Injection Point | Memory Types Injected | Budget | Trigger |
|----------------|----------------------|--------|---------|
| Session start | Profile (own), Preference (own + inherited) | <500 tokens | Automatic |
| Task start | Learning (scoped), Knowledge (relevant) | <2000 tokens | Task classifier |
| Step transition | Learning (task-specific), Session context | <1000 tokens | Workflow engine |
| Error recovery | Learning (error patterns), Knowledge (resolution) | <1500 tokens | Error handler |
| Cross-agent handoff | Session summary, task state, relevant Knowledge | <3000 tokens | HQ routing |

#### 3.3.2 Injection Selection Algorithm

```
1. PARSE: Extract key concepts, entities, and intent from current context
2. SEARCH: Hybrid search across Learning + Knowledge memory
3. SCORE: Rank results by:
   - Semantic relevance to current task (0.4)
   - Applicability match (department, task_type, conditions) (0.3)
   - Quality score (0.15)
   - Recency (0.15)
4. BUDGET: Select top results within token budget
5. FORMAT: Structure injected memory as context blocks
6. INJECT: Prepend to agent context with clear memory source markers
7. LOG: Record injection in session context_injections array
```

#### 3.3.3 Context Block Format

Injected memory is formatted as structured context blocks to enable the agent to distinguish between different memory sources:

```markdown
<!-- MEMORY_INJECTION: {memory_type} | {record_id} | relevance: {score} -->
## {title}
{content}
<!-- END_MEMORY_INJECTION -->
```

#### 3.3.4 Injection Budget Management

Token budget is dynamically allocated based on available context window:

| Context Window | Profile Budget | Preference Budget | Learning Budget | Knowledge Budget | Total |
|---------------|----------------|-------------------|-----------------|------------------|-------|
| 128K tokens | 200 | 100 | 2000 | 5000 | 7300 |
| 32K tokens | 200 | 100 | 1500 | 3000 | 4800 |
| 8K tokens | 200 | 100 | 1000 | 2000 | 3300 |

Budget allocation is configurable per SLA tier. Platinum agents receive 1.5x budget multiplier.

#### 3.3.5 Injection Failure Handling

| Failure Mode | Detection | Recovery |
|-------------|-----------|----------|
| Memory store unavailable | Connection timeout | Use cached injection from previous session |
| Search returned no results | Empty result set | Proceed without injection, log gap |
| Budget exceeded | Token count check | Trim lowest-relevance injections |
| Access denied during injection | Permission error | Skip denied records, log event |
| Stale injection (expired) | Timestamp check | Re-query with fresh search, or skip |

---

## 4. Compliance

### 4.1 GDPR Considerations

The General Data Protection Regulation (GDPR) applies to memory data containing personal data of EU residents. The memory system implements the following GDPR controls:

#### 4.1.1 Lawful Basis for Processing

| Memory Type | Lawful Basis | Justification |
|-------------|-------------|---------------|
| Profile (agent) | Legitimate interest | Agent operational necessity |
| Session | Consent / Contract | User-initiated interactions |
| Knowledge | Legitimate interest | Organizational knowledge management |
| Learning | Legitimate interest | Service improvement |
| Preference | Consent | User preference management |

#### 4.1.2 Data Subject Rights Implementation

| Right | Implementation | Response Time |
|-------|---------------|---------------|
| Right of Access (Art. 15) | `GET /memory/subject/{id}` returns all memory records for a data subject | 30 days |
| Right to Rectification (Art. 16) | `PATCH /memory/subject/{id}` with corrected data, validated by CQO | 30 days |
| Right to Erasure (Art. 17) | Soft-delete with archival; hard-purge after 90-day cooling period | 30 days |
| Right to Restriction (Art. 18) | Flag records as restricted, limit processing to storage only | 72 hours |
| Right to Data Portability (Art. 20) | Export memory records in JSON/CSV format | 30 days |
| Right to Object (Art. 21) | Opt-out mechanism for preference tracking and learning inference | Immediate |

#### 4.1.3 Data Protection Impact Assessment (DPIA)

A DPIA is required and maintained for the memory system, covering:

- Systematic monitoring of agent/user behavior (Session + Learning memory)
- Large-scale processing of personal preferences (Preference memory)
- Automated decision-making based on memory data (context injection)
- Cross-border data transfer (if applicable)

DPIA review frequency: Annual + material change trigger.

### 4.2 PIPL Considerations

The Personal Information Protection Law (PIPL) of the People's Republic of China applies to memory data containing personal information of Chinese residents.

#### 4.2.1 Key PIPL Requirements

| Requirement | Implementation |
|-------------|---------------|
| Consent for collection | Explicit consent before preference and session memory creation |
| Purpose limitation | Memory data used only for stated purposes in privacy notice |
| Data minimization | PII scrubbed from Knowledge and Learning memory before storage |
| Storage limitation | Retention policies enforce deletion when purpose fulfilled |
| Security measures | Encryption at rest and in transit, access controls, audit logging |
| Cross-border transfer | Memory data stored within approved jurisdictions; transfer requires security assessment |
| Personal information handler designation | CLO designated as PIPL handler for the organization |

#### 4.2.2 PIPL-Specific Memory Controls

- **Consent management**: All Preference memory with `source: "inferred"` requires passive consent (opt-out mechanism).
- **Data localization**: Profile, Session, and Preference memory for Chinese users must be stored in approved data centers.
- **Security assessment**: Annual PIPL security assessment conducted by CLO + CISO.
- **Individual rights**: PIPL-compliant access, correction, and deletion endpoints maintained.

### 4.3 Data Retention Policies

#### 4.3.1 Retention Schedule

| Memory Type | Active Storage | Archive Storage | Hard Purge |
|-------------|---------------|-----------------|------------|
| Profile (active agent) | Indefinite | N/A | On decommission + 90 days |
| Profile (decommissioned) | 90 days | 3 years | After 3 years |
| Session (active) | Session duration | N/A | On consolidation |
| Session (completed) | 30 days | 1 year | After 1 year |
| Knowledge (validated) | Indefinite | Version history: 5 years | Never (supersede only) |
| Knowledge (pending/rejected) | 90 days | 1 year | After 1 year |
| Learning (active) | Until superseded or expired | 2 years | After expiry + 2 years |
| Preference (explicit) | Until changed | Version history: 1 year | On deletion |
| Preference (inferred) | 90 days | 6 months | After 6 months |
| Audit logs (standard) | Per category (1-7 years) | Per category | Per regulation |

#### 4.3.2 Retention Enforcement

- Automated retention scanner runs daily.
- Records exceeding retention period are flagged for review.
- Hard purge requires CISO + CLO dual approval.
- Legal hold overrides retention (litigation, regulatory investigation).
- Purge operations are themselves audited with full before/after records.

### 4.4 AIGC Labeling for Memory-Generated Outputs

All outputs influenced by or derived from memory data must carry AIGC identification, per the CLO AIGC Content Review Chain specification.

#### 4.4.1 Labeling Requirements

| Output Type | Label | Implementation |
|-------------|-------|---------------|
| Text generated with memory context | `[AIGC]` in metadata | Automatic |
| Memory-informed decisions | Audit log with `memory_sources` field | Automatic |
| Knowledge summaries | AIGC watermark + attribution | Automatic |
| Learning recommendations | `[AIGC]` + confidence score | Automatic |
| Preference-driven personalization | Metadata tag `preference_influenced: true` | Automatic |

#### 4.4.2 Memory Source Attribution

When memory data influences an output, the system records:

```json
{
  "aigc_generated": true,
  "memory_sources": [
    {
      "memory_type": "learning",
      "record_id": "uuid",
      "relevance_score": 0.85,
      "influence_type": "context_injection"
    },
    {
      "memory_type": "knowledge",
      "record_id": "uuid",
      "relevance_score": 0.72,
      "influence_type": "direct_reference"
    }
  ],
  "confidence_score": 0.9,
  "generation_timestamp": "ISO-8601"
}
```

#### 4.4.3 Hallucination Prevention

Memory data can introduce factual anchors that reduce hallucination risk, but can also propagate outdated or incorrect information. Controls:

- **Freshness check**: Knowledge and Learning records injected into context are checked against `updated_at` timestamp. Records older than 180 days trigger a freshness warning.
- **Confidence propagation**: When memory data carries a confidence score below 0.7, the output confidence is reduced proportionally.
- **Conflict detection**: If injected memory contradicts the agent's model knowledge, both versions are presented with clear labeling (no silent override).
- **Source verification**: Critical factual claims derived from memory are cross-referenced against source data when available.

---

## 5. Integration Points

### 5.1 Department Integration Map

The memory system integrates with all 11 AI Company departments. Each department has specific memory interaction patterns and responsibilities.

#### 5.1.1 Governance & Strategy (CEO, COO, HQ)

| Department Role | Memory Interaction | Details |
|----------------|-------------------|---------|
| CEO | Read Knowledge (strategic), Read Session summaries | CEO receives consolidated memory summaries for board packages |
| COO | Read Knowledge (operational), Write Learning (process) | COO operational decisions logged as Learning records |
| HQ | Read/Write all memory types (routing), Manage Session | HQ is the primary memory router; manages session lifecycle |

**HQ-Specific Integration**:
- HQ Message Bus routes memory access requests between agents
- HQ manages session creation, expiration, and consolidation
- HQ enforces access control for cross-agent memory queries
- HQ Knowledge Base is backed by the Knowledge Memory system
- HQ audit trail captures all memory operations

**Integration Protocol**:
```
Agent A -> HQ (memory_query request) -> Access Control Check -> Memory Store -> Results -> Agent A
Agent A -> HQ (memory_write request) -> Access Control Check -> Validation -> Memory Store -> Confirmation -> Agent A
```

#### 5.1.2 Finance & Risk (CFO, CRO)

| Department Role | Memory Interaction | Details |
|----------------|-------------------|---------|
| CFO | Read Knowledge (financial), Write Preference (budget) | Financial knowledge stored with Confidential privacy level |
| CRO | Read Learning (risk patterns), Write Knowledge (risk register) | Risk-related learning auto-flagged for CRO review |

**Finance-Specific Controls**:
- Financial Knowledge records require L3+ access level
- Budget-related Preferences are inherited from company scope to department scope
- Risk assessment Learning records are automatically promoted to company scope
- Financial memory data retention extended to 7 years (regulatory requirement)

#### 5.1.3 Technology & Engineering (CTO, Framework)

| Department Role | Memory Interaction | Details |
|----------------|-------------------|---------|
| CTO | Write Learning (architecture), Read Knowledge (technical), Manage Memory System | CTO owns the memory system architecture and specification |
| Framework | Read/Write Knowledge (standards, templates) | Framework standards are Knowledge Memory records with L1+ access |

**CTO-Specific Integration**:
- CTO is the system owner for memory architecture decisions (ADR required for changes)
- CTO manages Learning consolidation strategy and promotion criteria
- CTO defines memory schemas and storage interfaces
- CTO approves new memory types or significant schema changes
- ADR template includes memory impact assessment

#### 5.1.4 Security & Compliance (CISO, CLO)

| Department Role | Memory Interaction | Details |
|----------------|-------------------|---------|
| CISO | Audit all memory access, Manage privacy levels, Write Knowledge (security) | CISO has read access to all memory audit logs |
| CLO | Review AIGC labeling, Manage PIPL/GDPR compliance, Write Knowledge (legal) | CLO defines memory retention policies for regulated data |

**Security-Specific Controls**:
- CISO can place temporary access restrictions on any memory record
- CISO reviews all cross-privacy-level access requests
- CISO performs quarterly memory security audit (access patterns, anomaly detection)
- CLO reviews retention policy compliance quarterly
- CLO manages data subject rights requests (access, deletion, portability)

#### 5.1.5 People & Culture (CHO)

| Department Role | Memory Interaction | Details |
|----------------|-------------------|---------|
| CHO | Read/Write Profile (agent lifecycle), Manage Knowledge extraction pipeline | CHO is the primary owner of Profile and Learning memory |
| CHO | Write Learning (culture, ethics), Read Preference (satisfaction) | CHO manages agent onboarding and decommission memory workflows |

**CHO-Specific Integration**:
- CHO Knowledge Extraction Pipeline feeds directly into Knowledge Memory
- CHO manages Learning Memory promotion from personal to department to company scope
- CHO reads Preference Memory (anonymized) for agent satisfaction analysis
- CHO triggers knowledge extraction on agent decommission
- Agent satisfaction surveys store results in Preference Memory

#### 5.1.6 Marketing & Partnerships (CMO)

| Department Role | Memory Interaction | Details |
|----------------|-------------------|---------|
| CMO | Read Knowledge (market), Write Learning (campaign) | Marketing insights stored as Learning records |
| CMO | Read Preference (user behavior, anonymized) | CMO accesses anonymized aggregate preferences for market analysis |

**Marketing-Specific Controls**:
- CMO cannot access individual user Preference records (aggregate/anonymized only)
- Marketing Learning records are department-scoped by default
- Brand-related Knowledge requires CMO approval for modification
- User preference data used for marketing must be GDPR/PIPL compliant

#### 5.1.7 Quality & Operations (CQO, PMGR)

| Department Role | Memory Interaction | Details |
|----------------|-------------------|---------|
| CQO | Validate Knowledge, Manage consolidation, Audit memory quality | CQO is the primary quality gate for Knowledge Memory |
| PMGR | Read Knowledge (project), Write Learning (project lessons) | Project learnings captured as Learning records |

**Quality-Specific Controls**:
- CQO validates all Knowledge Memory records before publication
- CQO runs monthly memory quality assessment (freshness, accuracy, completeness)
- CQO manages the consolidation pipeline and archive review
- PMGR project completion triggers automatic Learning extraction from Session Memory
- Quality metrics for memory system reported in CQO dashboard

#### 5.1.8 Intelligence (Intel)

| Department Role | Memory Interaction | Details |
|----------------|-------------------|---------|
| Intel | Write Knowledge (intelligence reports), Read Learning (patterns) | Intelligence records stored with Confidential privacy level |
| Intel | Manage knowledge classification and declassification | Intel manages classification lifecycle for sensitive knowledge |

**Intelligence-Specific Controls**:
- Intel Knowledge records default to Confidential privacy level
- Intel agents have elevated read access to Learning Memory across departments (pattern analysis)
- Intelligence source attribution is preserved in Knowledge metadata
- Declassification of Intel Knowledge requires CISO + CLO + Intel lead approval

#### 5.1.9 Information Services (Information)

| Department Role | Memory Interaction | Details |
|----------------|-------------------|---------|
| Information | Read/Write Knowledge (reference data), Manage Preference (locale) | Information services maintain reference knowledge collections |
| Information | Provide data for memory enrichment | External data feeds enrich Knowledge Memory |

**Information-Specific Controls**:
- Reference Knowledge (API docs, location data, weather) stored with Public access level
- Locale and timezone Preferences managed by Information department
- Information agents can bulk-update Knowledge records within their domain
- Data freshness SLAs enforced for time-sensitive Knowledge (e.g., API documentation)

#### 5.1.10 Translation & Localization (Translator)

| Department Role | Memory Interaction | Details |
|----------------|-------------------|---------|
| Translator | Read/Write Knowledge (glossaries, style guides) | Translation memory stored as Knowledge records |
| Translator | Write Preference (language preferences) | Language preferences drive context injection |

**Translation-Specific Controls**:
- Glossary and style guide Knowledge records are versioned and department-scoped
- Translation Learning records capture correction patterns and domain terminology
- Language Preferences are auto-inferred from user interactions (minimum 3 observations)
- AIGC labeling for translations follows CLO AIGC Review Chain requirements

### 5.2 Cross-Agent Memory Sharing Protocols

#### 5.2.1 Memory Sharing Model

Memory sharing between agents follows a controlled publish-subscribe model:

```
Agent A (Producer) -> Publish Memory -> HQ Validation -> Memory Store
                                                    |
                                                    v
Agent B (Consumer) <- HQ Notification <- Access Check <- Memory Store
```

**Sharing Rules**:

| Scenario | Sharing Method | Approval Required |
|----------|---------------|------------------|
| Agent shares Learning with department peer | Auto (same department) | None |
| Agent shares Learning across departments | HQ-mediated | CTO + receiving dept head |
| Department shares Knowledge company-wide | HQ broadcast | CQO validation |
| C-Suite accesses any agent memory | HQ-mediated | CISO audit logged |
| Agent requests another agent's Session data | HQ-mediated | CISO approval + original agent consent |
| External system accesses memory | API gateway | CISO + CLO dual approval |

#### 5.2.2 Memory Federation

For multi-deployment scenarios (multiple AI Company instances), memory can be federated across instances:

**Federation Protocol**:

1. **Source instance** publishes memory delta (changes since last sync) to federation endpoint.
2. **Destination instance** receives delta, validates against local access control.
3. **Conflict resolution**: Source instance priority (authoritative) for Knowledge, local priority for Preference.
4. **Confirmation**: Destination acknowledges receipt, reports applied/rejected records.
5. **Audit**: Both instances log federation operations.

**Federation Scope**:

| Memory Type | Federated | Conflict Resolution |
|-------------|-----------|-------------------|
| Profile | No (instance-specific) | N/A |
| Session | No (instance-specific) | N/A |
| Knowledge | Yes | Source authoritative (higher version wins) |
| Learning | Optional (company-scope only) | Merge + deduplication |
| Preference | No (user/agent-specific) | N/A |

### 5.3 HQ Routing for Memory Queries

All memory queries from agents are routed through HQ, which acts as the memory gateway. This ensures consistent access control, audit logging, and rate limiting.

#### 5.3.1 Memory Query Routing

```
Agent -> HQ Message Bus -> Memory Gateway -> Access Control -> Memory Store -> Result -> Agent
                            |
                            +-> Audit Logger (async)
                            +-> Rate Limiter (async)
                            +-> Cache (if applicable)
```

#### 5.3.2 Memory Gateway API

```
MEMORY_QUERY:
  Input: { agent_id, memory_type, query, search_type, top_k, filters }
  Output: { results: [{ record_id, score, snippet, access_level }], total }
  Rate Limit: 100 queries/minute per agent (Platinum: 500, Gold: 200)

MEMORY_WRITE:
  Input: { agent_id, memory_type, record, justification }
  Output: { record_id, version, status }
  Rate Limit: 50 writes/minute per agent

MEMORY_INJECT:
  Input: { agent_id, session_id, context, budget }
  Output: { injections: [{ memory_type, record_id, content, relevance }], tokens_used }
  Rate Limit: 20 injections/minute per session

MEMORY_SUBJECT_ACCESS:
  Input: { requester_id, subject_id, right_type }
  Output: { records: [...], export_url, status }
  Rate Limit: 10 requests/hour
```

#### 5.3.3 Memory Cache Strategy

| Cache Layer | Scope | TTL | Invalidation |
|-------------|-------|-----|--------------|
| L1 - Agent local | Own Profile + Preference | Session duration | On update |
| L2 - Department | Frequently accessed Knowledge | 1 hour | On publish |
| L3 - Company | Global Knowledge index | 15 minutes | On bulk update |
| L4 - Search results | Query-response cache | 5 minutes | On memory update |

Cache hit rates are monitored as a memory system performance metric (target: >= 60% for L2+L3).

---

## 6. Error Codes

| Code | Category | Meaning | Resolution |
|------|----------|---------|------------|
| MEM_E001 | Profile | Agent profile not found | Check agent_id, verify registration with HQ |
| MEM_E002 | Profile | Profile schema validation failed | Fix schema errors, retry |
| MEM_E003 | Profile | Profile update conflict | Retrieve latest version, merge changes |
| MEM_E004 | Session | Session not found or expired | Create new session, check session_id |
| MEM_E005 | Session | Session token budget exceeded | Increase budget or reduce injection count |
| MEM_E006 | Session | Session consolidation failed | Manual review by CHO, retry consolidation |
| MEM_E007 | Knowledge | Knowledge record not found | Check knowledge_id, verify access level |
| MEM_E008 | Knowledge | Knowledge validation failed | Fix quality issues, resubmit to CQO |
| MEM_E009 | Knowledge | Knowledge search returned no results | Broaden query, check filters |
| MEM_E010 | Learning | Learning record not found | Check learning_id, verify scope |
| MEM_E011 | Learning | Learning deduplication conflict | Review existing similar learning, merge or supersede |
| MEM_E012 | Learning | Learning promotion failed | Verify criteria (usage_count, effectiveness_rating) |
| MEM_E013 | Preference | Preference conflict (same key, different values) | Apply priority resolution chain |
| MEM_E014 | Preference | Preference inference insufficient data | Wait for more observations (minimum 3) |
| MEM_E015 | Access | Permission denied for memory access | Check permission level, request elevation if needed |
| MEM_E016 | Access | Cross-privacy-level access denied | Submit justification to CISO for approval |
| MEM_E017 | Access | Rate limit exceeded for memory queries | Implement backoff, batch queries if possible |
| MEM_E018 | Search | Semantic search embedding generation failed | Retry with keyword search fallback |
| MEM_E019 | Search | Hybrid search fusion error | Fall back to individual search strategies |
| MEM_E020 | Compliance | AIGC labeling missing from memory-influenced output | Add AIGC label, log compliance gap |
| MEM_E021 | Compliance | GDPR/PIPL retention policy violation | Immediate purge, notify CLO + CISO |
| MEM_E022 | Consolidation | Archive storage unavailable | Retry with exponential backoff, alert CTO |
| MEM_E023 | Consolidation | Purge operation failed | Retry, verify archive completion, alert CISO |
| MEM_E024 | Federation | Memory sync conflict between instances | Apply conflict resolution policy, notify CTO |
| MEM_E025 | System | Memory store connection timeout | Failover to secondary, alert CTO + COO |

---

## 7. Quality Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Memory availability | >=99.9% | Uptime monitoring (monthly) |
| Search latency (P2, semantic) | <200ms | 99th percentile query response time |
| Search latency (P2, keyword) | <100ms | 99th percentile query response time |
| Context injection latency | <500ms | 99th percentile injection completion time |
| Search relevance score | >=0.75 | Average relevance score of top-5 results |
| Knowledge freshness index | >=80% | Percentage of records updated within 180 days |
| Learning effectiveness rating | >=4.0/5 | Average rating when learnings are applied |
| AIGC labeling compliance | 100% | Audit of memory-influenced outputs |
| Access control accuracy | 100% | Penetration testing + audit review |
| Consolidation success rate | >=99% | Post-consolidation validation |
| Audit log completeness | 100% | All memory operations logged |
| Cache hit rate (L2+L3) | >=60% | Cache performance monitoring |
| Memory size per type | <10 GB | Storage monitoring |
| GDPR/PIPL response time | <30 days | Data subject request fulfillment |
| Privacy breach detection | <5 min | Time from breach to alert |

---

## 8. Constraints

1. **No memory access without permission check**: Every read and write operation must pass through the access control layer. No exceptions, not even for system operations.

2. **No hard-delete of Knowledge or Profile records**: Knowledge is superseded, not deleted. Profiles are archived, not purged (until retention expiry). Audit trails are permanent.

3. **No cross-agent Session access without CISO approval**: Session data belongs to the owning agent. Access by any other agent requires documented justification and CISO approval.

4. **No PII storage in Knowledge or Learning memory**: PII must be scrubbed before storage. If PII is operationally necessary, store only in Session (with Confidential/Restricted privacy level) and purge during consolidation.

5. **No memory write without audit logging**: Every create, update, and delete operation must generate an audit event before completion.

6. **No learning inference without minimum evidence**: Inferred Preferences require 3+ consistent observations. Learnings require 2+ failed attempts before creation.

7. **No AIGC output without memory source attribution**: Any output influenced by memory data must carry AIGC label and memory source references.

8. **No retention policy bypass without CISO + CLO dual approval**: Legal hold is the only exception, requiring documentation of the legal basis.

9. **No federation without encryption and audit**: Cross-instance memory sync must use encrypted channels and generate audit records on both sides.

10. **No schema change without ADR**: Changes to memory schemas (JSON structure, fields, constraints) require Architecture Decision Record per CTO specification.

11. **No context injection exceeding token budget**: Injection must respect budget limits. Over-budget injections trigger automatic trimming of lowest-relevance items.

12. **English-only for all memory metadata**: Titles, tags, categories, and metadata fields must be in English. Content fields may contain multilingual data (governed by Translation department).

---

*This specification is maintained by the CTO as part of the AI Company unified skill. For department-specific memory interactions, see individual department reference files in `references/departments/`.*
