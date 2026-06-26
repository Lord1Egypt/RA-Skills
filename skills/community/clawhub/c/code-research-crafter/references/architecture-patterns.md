# Architecture Patterns

Proven design patterns for structuring solutions in Phase 3 of the Code Research Crafter workflow.

## Layered Architecture

The default architecture pattern for Code Research Crafter proposals. Organize the system into layers with clear dependencies flowing downward.

```
┌─────────────────────────────────────────┐
│           Layer 4: Governance           │
│  Policy · Audit · Monitoring · Admin     │
├─────────────────────────────────────────┤
│          Layer 3: Intelligence           │
│  ML Models · Pattern Detection · Insights│
├─────────────────────────────────────────┤
│          Layer 2: Enhancement            │
│  Core Features · APIs · Integrations     │
├─────────────────────────────────────────┤
│           Layer 1: Foundation            │
│  Data Models · Storage · Collection      │
└─────────────────────────────────────────┘
```

**Rules:**
- Each layer only depends on layers below it (never upward)
- Layers communicate through well-defined interfaces
- Higher layers can be removed without breaking lower layers

### Layer 1: Foundation

Purpose: Data collection, storage, and basic retrieval.

**Components:**
- Data models and schemas
- Storage backends (database, file system, cache)
- Collection pipelines (APIs, scrapers, event listeners)
- Basic CRUD operations

**Key decisions:**
- Choose storage format based on query patterns (SQL vs NoSQL vs file-based)
- Design schemas for forward compatibility (versioning, optional fields)
- Plan data retention and cleanup policies

### Layer 2: Enhancement

Purpose: Core features that add value on top of Foundation data.

**Components:**
- Business logic and processing pipelines
- API endpoints and client libraries
- Integration adapters (third-party services)
- Configuration and customization hooks

**Key decisions:**
- API design: RESTful vs GraphQL vs gRPC
- Extensibility: plugin system vs configuration-driven
- Error handling strategy: fail-fast vs graceful degradation

### Layer 3: Intelligence

Purpose: AI/ML capabilities that derive insights from accumulated data.

**Components:**
- Model training and inference pipelines
- Feature extraction and engineering
- Recommendation and ranking systems
- Anomaly detection and alerting

**Key decisions:**
- Model serving: batch vs real-time inference
- Training data: what to collect, how to label, how to validate
- Fallback behavior: what happens when the model is uncertain

### Layer 4: Governance

Purpose: Control, monitoring, and policy enforcement across all layers.

**Components:**
- Access control and permissions
- Audit logging and compliance
- Performance monitoring and alerting
- Configuration management and feature flags

**Key decisions:**
- RBAC vs ABAC for access control
- What to audit and how long to retain logs
- SLA definitions and escalation procedures

## Dual-Track Data Pattern

When a system needs both explicit user configuration and implicit learned behavior, use the dual-track pattern.

```
User-Defined Track (Static)     System-Learned Track (Dynamic)
┌──────────────────────┐       ┌──────────────────────┐
│ Configuration files  │       │ Usage metrics         │
│ User preferences     │       │ Behavioral patterns   │
│ Explicit rules       │       │ Inferred preferences  │
│ Manual overrides     │       │ Statistical models    │
└──────────┬───────────┘       └──────────┬───────────┘
           │                              │
           └──────────┬───────────────────┘
                      ▼
              ┌──────────────┐
              │  Merge Layer  │
              │ (user > system)│
              └──────────────┘
```

**Rule**: User-defined values always override system-learned values when they conflict.

## Visibility Tiers Pattern

For systems with multi-tenant or collaborative features, define clear visibility boundaries.

| Tier | Scope | Example |
|------|-------|---------|
| `private` | Owner only | Personal API keys, private notes |
| `team` | Collaborators | Shared dashboards, team workflows |
| `global` | All users | Public templates, community insights |

**Implementation:**
- Every data object has a `visibility` field
- Access control checks filter by visibility + user membership
- Default visibility is `private` (most restrictive)
- Users can promote visibility but never demote below their tier

## Phased Rollout Pattern

For introducing changes to existing systems without disruption.

```
Phase 1: Shadow Mode      → Deploy alongside existing, no user impact
Phase 2: Opt-in Beta      → Users can enable new behavior explicitly
Phase 3: Default-On       → New behavior is default, old available via flag
Phase 4: Legacy Removal   → Old behavior fully deprecated and removed
```

**Key principles:**
- Each phase should be independently deployable and reversible
- Provide migration scripts/tools between phases
- Monitor metrics at each phase transition
- Set clear timelines with communication at each step

## Choosing the Right Pattern

| Situation | Recommended Pattern |
|-----------|-------------------|
| New feature on existing system | Layered + Phased Rollout |
| Data-rich system needing intelligence | Layered + Dual-Track |
| Multi-user collaborative system | Layered + Visibility Tiers |
| Breaking change to existing API | Phased Rollout |
| Research prototype → production | Layered (start with L1-L2, add L3-L4 later) |
