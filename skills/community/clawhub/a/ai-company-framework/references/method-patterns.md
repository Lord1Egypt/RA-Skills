# Method Patterns & Detailed Specifications

> Full specifications for AI Company Framework. Merged: Standardization + Modularization + Generalization + Ecosystem + Registry + SkillLearner + Starter.

---

# AI Company Framework Skill v3.0

> Framework & Infrastructure for All-AI-Employee Technology Companies.
> Standards, modularity, generalization, ecosystem, registry, skill learning, starter templates.

---

## 1. Trigger Scenarios

| Category | Trigger Keywords |
|----------|-----------------|
| Standards | "Standard", "Convention", "Naming", "Schema" |
| Modular | "Module", "Component", "Decompose", "Interface" |
| General | "Generalize", "Reuse", "Template", "Pattern" |
| Ecosystem | "Ecosystem", "Integration", "Compatibility", "Interoperability" |
| Registry | "Register", "Agent registry", "Skill registry", "Discovery" |
| Learning | "Skill learning", "Learn skill", "Skill acquisition" |
| Starter | "Starter template", "New project", "Bootstrap", "Quick start" |

---

## 2. Core Identity

- **Position**: AI Company Framework | **Permission Level**: L5 | **ID**: FW-000 | **Reports to**: CTO-001

---

## 3. Core Responsibilities

### 3.1 Standardization

```
Naming Conventions:
  Skills: ai-company-{function} (lowercase, hyphenated)
  Agents: {PREFIX}-{NNN} (uppercase prefix, numeric ID)
  Departments: {function} (lowercase, hyphenated)
  Versions: semver (MAJOR.MINOR.PATCH)
  Files: kebab-case.md, kebab-case.py

Schema Standards (ClawHub v1.0):
  Required Frontmatter:
    name, slug, version, description, license, tags,
    triggers (keywords, patterns),
    interface (inputs, outputs, errors),
    permissions (levels, constraints),
    quality (idempotent, robustness),
    metadata (author, created, updated, department)

  Optional Frontmatter:
    dependencies, conflicts, examples, documentation, changelog

Code Style:
  - English-only for all compiled content
  - Chinese allowed only in trigger keywords for market matching
  - Markdown for documentation (GFM extended)
  - JSON for schemas and configurations
  - YAML for frontmatter only
```

### 3.2 Modularization

```
Modularity Principles:
  - Single Responsibility: Each skill does one thing well
  - Interface Segregation: Minimal interface per consumer
  - Dependency Inversion: Depend on abstractions, not implementations
  - Maximum Dependencies: 5 per skill
  - No Circular Dependencies: DAG dependency graph only

Module Structure:
  Each skill is a self-contained module:
    SKILL.md          - Index and quick reference
    references/       - Detailed specifications
    prompts/          - User-facing prompts
    (No code execution within skill files)

Integration Patterns:
  | Pattern | Description | Use Case |
  |---------|-------------|----------|
  | Request-Response | Synchronous query | Single skill invocation |
  | Event-Driven | Async notification | Cross-skill triggers |
  | Pipeline | Sequential processing | Multi-step workflows |
  | Fan-out | Parallel distribution | Broadcast to multiple skills |
  | Aggregator | Collect and merge | Multi-source data collection |
```

### 3.3 Generalization

```
Generalization Levels:
  | Level | Description | Reuse Potential |
  |-------|-------------|----------------|
  | L1-Company-Specific | Hardcoded for one company | Low (single use) |
  | L2-Domain-Specific | Configurable for domain | Medium (domain reuse) |
  | L3-Industry-Standard | Follows industry patterns | High (industry reuse) |
  | L4-Universal | Applicable across industries | Very High (global reuse) |

  Target: All skills at L3+

Generalization Checklist:
  [ ] No company-specific names or identifiers
  [ ] No hardcoded URLs, paths, or credentials
  [ ] Configurable parameters (not inline values)
  [ ] Template-based generation (not one-off)
  [ ] Documentation uses generic examples
  [ ] Reusable in 3+ contexts without modification

Template System:
  Skill Template: Defines structure for new skills
  Agent Template: Defines structure for new agents
  Prompt Template: Defines structure for new prompts
  All templates version-controlled and ClawHub-published
```

### 3.4 Ecosystem

```
Ecosystem Architecture:
  Core Layer: CEO, COO, HQ, CTO, CISO, CLO, CHO, CFO, CRO, CQO, CMO
  Executive Layer: WRTR, PMGR, ANLT, CSSM, ENGR, QENG, LEGAL, HR
  Translation Layer: TR-COORD, TR-EN, TR-ZH, TR-RU, TR-FR
  Infrastructure Layer: Framework, Harness, Registry, Starter

Interoperability Rules:
  - All inter-skill communication via HQ
  - All skills must declare dependencies explicitly
  - All skills must handle missing dependencies gracefully
  - Version compatibility: semver, MAJOR = breaking change
  - Deprecation: 90-day notice before removal

Ecosystem Health:
  | Metric | Target |
  |--------|--------|
  | Dependency resolution rate | 100% |
  | Circular dependency count | 0 |
  | Deprecated skill usage | 0 |
  | Version compatibility | 100% |
```

### 3.5 Registry

```
Agent Registry:
  | Field | Type | Required |
  |-------|------|----------|
  | agent_id | string | Yes |
  | name | string | Yes |
  | department | string | Yes |
  | permission_level | L1-L5 | Yes |
  | skills | list | Yes |
  | dependencies | list | Yes |
  | status | enum | Yes |
  | created_at | timestamp | Yes |
  | updated_at | timestamp | Yes |

Skill Registry:
  | Field | Type | Required |
  |-------|------|----------|
  | slug | string | Yes |
  | name | string | Yes |
  | version | semver | Yes |
  | department | string | Yes |
  | dependencies | list | Yes |
  | clawhub_id | string | Yes |
  | quality_score | number | No |
  | last_reviewed | timestamp | No |

Discovery:
  - Skills discoverable by: keyword, department, capability
  - Agents discoverable by: department, capability, availability
  - Auto-suggest based on task description
```

### 3.6 Skill Learning (from SkillLearner)

```
Skill Acquisition Pipeline:
  1. IDENTIFY: Determine skill gap from CHO assessment or task failure
  2. SEARCH: Search ClawHub for matching skills
  3. EVALUATE: Assess skill quality (CQO gates G0-G7)
  4. INSTALL: Download and integrate skill
  5. CONFIGURE: Map skill to agent, set permissions
  6. TEST: Validate skill in sandbox
  7. ACTIVATE: Enable skill for production use
  8. MONITOR: Track skill effectiveness

Learning Priorities:
  | Priority | Source | Example |
  |----------|--------|---------|
  | P0 | Task failure | Agent cannot complete assigned task |
  | P1 | CHO assessment | Skills gap identified in review |
  | P2 | Strategic plan | New capability needed for OKR |
  | P3 | Market opportunity | CMO discovers new demand signal |
```

### 3.7 Starter Templates

```
Quick Start:
  1. Install: clawhub install ai-company-starter
  2. Initialize: Configure company name, departments, agents
  3. Deploy: Activate core C-Suite agents
  4. Customize: Add domain-specific skills
  5. Launch: Begin operations

Starter Includes:
  - Core C-Suite skills (CEO, COO, CFO, CTO, CISO, CLO, CHO, CMO, CRO, CQO)
  - HQ routing and state management
  - Default permission levels
  - Standard SOPs and templates
  - Sample OKRs and dashboards

Customization Points:
  - Department structure
  - Agent configurations
  - Permission policies
  - SLA tiers and targets
  - Brand voice and style guide
```

---

## 4. Error Codes

| Code | Meaning | Resolution |
|------|---------|------------|
| FW_E001 | Schema validation failed | Fix frontmatter, re-validate |
| FW_E002 | Circular dependency detected | Break cycle, restructure |
| FW_E003 | Generalization level too low | Refactor for reusability |
| FW_E004 | Registry entry missing | Register agent/skill |
| FW_E005 | Skill installation failed | Check compatibility, retry |
| FW_E006 | Template rendering failed | Fix template variables |
| FW_E007 | Ecosystem compatibility issue | Version check, update |
| FW_E008 | Starter initialization failed | Check prerequisites, retry |

---

## 5. Constraints & Metrics

Constraints: All skills L3+ generalization; No circular dependencies; All agents registered; ClawHub Schema v1.0 mandatory; 90-day deprecation notice required.

| Metric | Target |
|--------|--------|
| Schema compliance | 100% |
| Generalization level | L3+ for all |
| Circular dependencies | 0 |
| Registry completeness | 100% |
| Skill learning success rate | >90% |
| Starter setup time | <30min |

*Enhanced by AI-Company Skills Rebuilder v3.0*
