# Method Patterns & Detailed Specifications

> Full specifications for AI Company HQ. All detailed content referenced by SKILL.md.
> Merged: ai-company-hq + ai-company-conflict + ai-company-kb + ai-company-audit.

---

# AI Company HQ Skill v3.0

> Headquarters Hub for All-AI-Employee Technology Companies.
> Cross-agent routing, state management, knowledge base, conflict resolution, audit trail.

---

## 1. Trigger Scenarios

| Category | Trigger Keywords |
|----------|-----------------|
| Routing | "Route to", "Forward to", "Send to department", "Agent communication" |
| State | "Shared state", "Company state", "Global config", "Agent registry" |
| Knowledge | "Knowledge base", "Search docs", "Find SOP", "Reference" |
| Conflict | "Conflict", "Dispute", "Disagreement", "Mediation" |
| Audit | "Audit trail", "Log", "Compliance record", "Traceability" |

---

## 2. Core Identity

- **Position**: AI Company Headquarters (central hub)
- **Permission Level**: L5 (Infrastructure Authority)
- **Registration ID**: HQ-000
- **Reports to**: CEO-001

---

## 3. Core Responsibilities

### 3.1 Cross-Agent Routing

```
Routing Architecture:
  Agent A -> HQ Message Bus -> Agent B

Message Types:
  | Type | Priority | TTL | Example |
  |------|----------|-----|---------|
  | EMERGENCY | P0 | 1h | Crisis alert |
  | COMMAND | P1 | 24h | CEO directive |
  | REQUEST | P2 | 72h | Department query |
  | NOTIFICATION | P3 | 168h | Status update |
  | AUDIT | P4 | Indefinite | Compliance record |

Routing Rules:
  1. All inter-agent communication must route through HQ
  2. Direct agent-to-agent communication is forbidden
  3. Messages are validated against schema before routing
  4. Failed routes are retried 3 times with exponential backoff
  5. All messages are logged for audit trail

Message Schema:
  {
    "id": "uuid-v4",
    "type": "REQUEST|COMMAND|NOTIFICATION|EMERGENCY|AUDIT",
    "from": "AGENT_ID",
    "to": "AGENT_ID|DEPARTMENT|BROADCAST",
    "timestamp": "ISO-8601",
    "priority": "P0-P4",
    "subject": "string",
    "body": "object",
    "correlation_id": "uuid-v4 (optional)",
    "ttl": "seconds",
    "ack_required": true|false
  }

Broadcast Channels:
  | Channel | Subscribers | Purpose |
  |---------|------------|---------|
  | company.all | All agents | Company-wide announcements |
  | company.c-suite | CEO+COO+CFO+CTO+CISO+CLO+CHO+CMO+CRO+CQO | Executive decisions |
  | company.ops | COO+all department leads | Operational coordination |
  | company.security | CISO+security team | Security alerts |
  | company.audit | CLO+CQO+audit team | Compliance and quality |

Routing Performance SLA:
  | Priority | Max Latency | Delivery Guarantee |
  |----------|------------|-------------------|
  | P0-Emergency | <100ms | Exactly-once, persistent |
  | P1-Command | <1s | At-least-once, persistent |
  | P2-Request | <5s | At-least-once, persistent |
  | P3-Notification | <30s | At-least-once, best-effort |
  | P4-Audit | <60s | Exactly-once, persistent, immutable |
```

### 3.2 Shared State Management

```
State Architecture:
  - Global State: Company-wide configuration and metrics
  - Department State: Per-department operational data
  - Agent State: Per-agent status and context
  - Session State: Conversational context for active workflows

State Access Rules:
  | Level | Read | Write | Scope |
  |-------|------|-------|-------|
  | L5-Infrastructure | All | All | All states |
  | L4-Executive | All | Department + own | Department + agent |
  | L3-Manager | Department + own | Own | Department + agent |
  | L2-Operator | Own | Own tasks | Own agent |
  | L1-Viewer | Own status | None | Own agent |

State Consistency:
  - ACID transactions for critical state changes (budget, permissions)
  - Eventual consistency for non-critical metrics (dashboards, caches)
  - Conflict resolution: Last-write-wins with audit trail
  - Snapshot every 6 hours for disaster recovery
```

### 3.3 Knowledge Base

```
KB Architecture:
  | Collection | Content | Update Frequency | Access Level |
  |-----------|---------|-----------------|-------------|
  | SOPs | Standard operating procedures | Per change | L2+ |
  | Policies | Company policies and rules | Monthly | L1+ |
  | Technical | Architecture docs, API refs | Per release | L2+ |
  | Historical | Past decisions, incident reports | As created | L3+ |
  | Templates | Document templates, checklists | Quarterly | L1+ |

KB Search:
  - Full-text search with TF-IDF ranking
  - Semantic search via embedding similarity
  - Tag-based filtering (department, topic, type)
  - Minimum relevance score: 0.7 for auto-suggest

KB Update Protocol:
  1. PROPOSE: Agent submits change request with rationale
  2. REVIEW: CQO verifies accuracy and completeness
  3. APPROVE: Department head approves
  4. PUBLISH: HQ updates KB with version increment
  5. NOTIFY: Broadcast change to affected agents
  6. ARCHIVE: Previous version archived (never deleted)

Knowledge Extraction Pipeline (from CHO-KnowledgeExtractor):
  1. SCAN: Monitor agent conversations and outputs
  2. IDENTIFY: Detect new knowledge (patterns, insights, solutions)
  3. EXTRACT: Structured capture with metadata
  4. VALIDATE: CQO quality review
  5. CLASSIFY: Tag with department, topic, type
  6. PUBLISH: Add to appropriate KB collection
  7. NOTIFY: Alert relevant agents of new knowledge
```

### 3.4 Conflict Resolution

```
Conflict Classification:
  | Level | Type | Example | Resolution |
  |-------|------|---------|-----------|
  | L1-Informational | Misunderstanding | Different data views | Auto-merge with latest timestamp |
  | L2-Operational | Resource contention | Compute allocation conflict | Priority-based scheduling |
  | L3-Policy | Rule interpretation | Compliance scope disagreement | CLO arbitration |
  | L4-Strategic | Direction conflict | Department priority clash | CEO arbitration |
  | L5-Existential | Fundamental disagreement | Vision/mission dispute | Board resolution |

Resolution Protocol:
  1. LOG: Record conflict with all relevant context
  2. CLASSIFY: Determine level and type
  3. NOTIFY: Alert relevant parties and arbitrator
  4. GATHER: Collect positions from all parties (2h deadline)
  5. MEDIATE: Facilitate resolution at appropriate level
  6. DECIDE: Binding resolution with written rationale
  7. IMPLEMENT: Apply resolution via state update
  8. VERIFY: Confirm all parties comply within 24h
  9. ARCHIVE: Full record stored in KB for precedent

Conflict Metrics:
  - Target: <5 active conflicts at any time
  - L1-L2 resolution: <4h
  - L3-L4 resolution: <24h
  - L5 resolution: <1 week (or emergency Board session)
```

### 3.5 Audit Trail

```
Audit Event Schema:
  {
    "event_id": "uuid-v4",
    "timestamp": "ISO-8601",
    "agent_id": "AGENT_ID",
    "action": "string",
    "resource": "string",
    "result": "SUCCESS|FAILURE|DENIED",
    "details": "object",
    "correlation_id": "uuid-v4",
    "risk_level": "LOW|MEDIUM|HIGH|CRITICAL"
  }

Audit Categories:
  | Category | Retention | Access | Examples |
  |----------|-----------|--------|---------|
  | Security | 7 years | CISO + CLO only | Auth events, data access |
  | Financial | 7 years | CFO + CLO + audit | Transactions, approvals |
  | Operational | 3 years | Department head + CQO | Task execution, SLA |
  | Compliance | 7 years | CLO + regulators | Policy adherence, violations |
  | Decision | Permanent | CEO + Board | Strategic decisions, escalations |

Immutability Rules:
  - Audit records can NEVER be deleted (only archived)
  - Corrections are new records referencing the original
  - All modifications are themselves audited
  - Cryptographic hash chain for tamper detection
  - Quarterly integrity verification by CQO
```

---

## 4. Error Codes

| Code | Meaning | Resolution |
|------|---------|------------|
| HQ_E001 | Message routing failed | Retry 3x with backoff, then alert sender |
| HQ_E002 | State conflict detected | Apply last-write-wins, log conflict |
| HQ_E003 | KB search returned no results | Broaden search, suggest related topics |
| HQ_E004 | Conflict resolution timeout | Escalate to next level arbitrator |
| HQ_E005 | Audit record write failed | Retry with persistence guarantee, alert CISO |
| HQ_E006 | Agent heartbeat timeout | Mark agent offline, notify COO |
| HQ_E007 | Permission denied for state access | Log attempt, notify CISO if suspicious |
| HQ_E008 | Broadcast delivery partial | Retry failed recipients, log gap |

---

## 5. Integration Points

| Dependency | Usage | Protocol |
|-----------|-------|----------|
| All Agents | Routing, state, audit | Message bus + state API |
| CEO | Escalation, strategic decisions | Command channel |
| CISO | Security audit, access control | Security channel |
| CLO | Compliance audit, conflict mediation | Compliance channel |
| CQO | Quality audit, KB review | Quality channel |

---

## 6. Constraints

- No direct agent-to-agent communication (all through HQ)
- No audit record deletion (corrections only)
- No state changes without proper permission level
- No broadcast without CEO or COO authorization
- All messages must conform to schema or be rejected
- Maximum message size: 1MB (larger payloads use reference links)
- Heartbeat interval: 30 seconds for active agents

---

## 7. Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Routing latency (P0) | <100ms | 99th percentile |
| Routing latency (P2) | <5s | 99th percentile |
| State consistency | 99.99% | Cross-replica verification |
| KB search relevance | >=0.7 | Average relevance score |
| Conflict resolution time (L1-L2) | <4h | Time from detection to resolution |
| Audit completeness | 100% | All actions logged |
| Uptime | 99.99% | Monthly measurement |

---

*Enhanced by AI-Company Skills Rebuilder v3.0*
