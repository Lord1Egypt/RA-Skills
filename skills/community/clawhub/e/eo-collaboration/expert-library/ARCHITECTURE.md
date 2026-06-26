# Expert Library Architecture

## Overview

EO's expert library has a **two-layer architecture** that balances breadth and usability:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Expert Library Architecture                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ LAYER 1: Expert Source (13 Categories)                     │ │
│  │ ────────────────────────────────────────────────────────   │ │
│  │ 141 real-world experts organized by domain                 │ │
│  │ Located in: expert-library/{category}/                    │ │
│  │                                                            │ │
│  │ Categories:                                                 │ │
│  │ ├── engineering (23)     - Dev, SRE, Security, etc.        │ │
│  │ ├── design (8)          - UI/UX, Visual, Brand            │ │
│  │ ├── marketing (27)      - Social, SEO, Content, etc.      │ │
│  │ ├── sales (8)           - Strategy, Coaching, Analysis    │ │
│  │ ├── product (5)         - PM, Research, Strategy          │ │
│  │ ├── testing (8)         - QA, Performance, Accessibility │ │
│  │ ├── specialized (27)    - Blockchain, Legal, Healthcare   │ │
│  │ └── ... (6 more categories)                               │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ LAYER 2: Role Mapping (8 Roles)                           │ │
│  ──────────────────────────────────────────────────────────── │
│  │ 35 optimized role-based experts mapped from Layer 1        │ │
│  │ Located in: expert-library/{role}/                        │ │
│  │                                                            │ │
│  │ Each role IS a MAPPING to relevant category experts:       │ │
│  │                                                            │ │
│  │ Role      │ Maps From Categories                        │ │
│  │ ──────────┼─────────────────────────────────────────────  │ │
│  │ Architect │ engineering, specialized, product, spatial    │ │
│  │ Planner   │ marketing, sales, product, project-mgmt      │ │
│  │ Frontend  │ engineering, design, game-dev                │ │
│  │ Backend   │ engineering, specialized                      │ │
│  │ QA        │ testing, engineering                         │ │
│  │ Security  │ engineering, specialized                      │ │
│  │ DevOps    │ engineering, specialized                     │ │
│  │ CodeReview│ engineering, specialized                      │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ LAYER 3: Command Interface (9 Commands)                    │ │
│  │ ────────────────────────────────────────────────────────   │ │
│  │ User-facing commands that invoke role-based experts        │ │
│  │                                                            │ │
│  │ /plan        → Planner Expert                             │ │
│  │ /architect   → Architect Expert                            │ │
│  │ /code-review → CodeReviewer Expert                        │ │
│  │ /verify      → QA Expert                                   │ │
│  │ /security-scan → Security Expert                          │ │
│  │ /deploy      → DevOps Expert                               │ │
│  │ /e2e         → QA Expert                                  │ │
│  │ /tdd         → QA Expert                                   │ │
│  │ /build-fix   → DevOps Expert                              │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Why Two-Layer Architecture?

### The Problem

**Option A: Direct 141 Expert Access**
- Pros: Maximum flexibility, all specialists available
- Cons: Choice paralysis, slow to find right expert

**Option B: Fixed 8 Role Access**
- Pros: Simple, fast, clear responsibilities
- Cons: Missing domain depth, generic solutions

### The Solution: Two-Layer

```
Fast Path (8 Roles)          Deep Path (141 Experts)
─────────────────            ──────────────────────
/plan "blog system"    →     marketing-content-strategist
                            marketing-seo-specialist
                            sales-sales-strategist
                            product-product-manager
                            ...

/architect "scalable" →     engineering-backend-architect
                            specialized-cloud-architect
                            specialized-mlops-engineer
                            ...
```

**Fast Path**: When you need standard tasks, use 8 roles for quick expert matching.

**Deep Path**: When you need specialized domain knowledge, access 141 experts directly.

## How to Call Experts

### Quick Call (Recommended)

```
/plan "开发博客系统"              → 直接调用 Planner 角色
/architect "设计架构"            → 直接调用 Architect 角色
/code-review "./src"             → 直接调用 CodeReviewer 角色
```

### Specific Expert Call

```
"我需要一个区块链安全审计专家"  → specialized/blockchain-security-auditor.md
"我需要小红书运营专家"          → marketing/xiaohongshu-specialist.md
```

### Multi-Expert Collaboration

```
/plan "开发博客系统" + /architect "设计架构"
    ↓
EO 自动调度:
    ├── Planner (from marketing, sales, product)
    └── Architect (from engineering, specialized)
```

## Expert Source: 13 Categories (Layer 1)

| Category | Count | Description | Example Experts |
|----------|-------|-------------|----------------|
| `engineering` | 23 | Development & Architecture | Frontend Dev, Backend Architect, SRE |
| `design` | 8 | UI/UX & Visual Design | Brand Guardian, UI Designer |
| `marketing` | 27 | Digital Marketing | SEO Specialist, Social Media Strategist |
| `sales` | 8 | Sales & CRM | Account Strategist, Sales Coach |
| `product` | 5 | Product Management | Product Manager, Behavioral Engineer |
| `testing` | 8 | QA & Testing | Performance Benchmarker, Accessibility Auditor |
| `specialized` | 27 | Domain Specialists | Blockchain Auditor, Compliance Expert |
| `project-management` | 6 | Project Coordination | Project Shepherd, Scrum Master |
| `support` | 6 | Support & Operations | Finance Tracker, Legal Compliance |
| `paid-media` | 7 | Paid Advertising | PPC Strategist, Programmatic Buyer |
| `spatial-computing` | 6 | AR/VR/XR | VisionOS Engineer, XR Developer |
| `game-development` | 5 | Game Development | Game Designer, Technical Artist |
| `academic` | 5 | Research & Academia | Research Methodologist |

## Role Mapping: 8 Roles (Layer 2)

| Role | Count | Maps From | Primary Tasks |
|------|-------|----------|---------------|
| **Architect** | 5 | engineering, specialized, product, spatial | System architecture, tech selection |
| **Planner** | 4 | marketing, sales, product, project-mgmt | Project planning, task decomposition |
| **Frontend** | 4 | engineering, design, game-dev | UI development, component libraries |
| **Backend** | 5 | engineering, specialized | API design, database, services |
| **QA** | 4 | testing, engineering | Test design, automation, verification |
| **Security** | 4 | engineering, specialized | Security audit, vulnerability assessment |
| **DevOps** | 4 | engineering, specialized | CI/CD, deployment, monitoring |
| **CodeReviewer** | 5 | engineering, specialized | Code quality, refactoring, patterns |

## Architecture Decision: Why This Works

### 1. Separation of Concerns

| Layer | Purpose | When to Use |
|-------|---------|-------------|
| 13 Categories | Domain expertise source | Need specific specialist |
| 8 Roles | Fast access to common roles | Standard tasks, quick start |
| 9 Commands | User-friendly interface | Any task via standardized commands |

### 2. Mappings vs Duplication

The 8 roles do NOT duplicate the 141 experts. Instead:

```
Role Expert (e.g., "Backend Architect ar-002")
    │
    ├── Has generic backend architecture skills
    │
    └── MAPPED to relevant category experts:
            ├── engineering-backend-architect.md
            ├── specialized-cloud-architecture-specialist.md
            ├── specialized-data-architect.md
            └── ...
```

When you call `/architect`, EO can optionally involve multiple category experts for deeper analysis.

### 3. Command → Role → Category Expert Flow

```
User Input: /architect "设计微服务架构"
    │
    ▼
Command Handler (architect.md)
    │
    ▼
Role Expert (architect/ar-002)
    │
    ▼
Optional: Deep-dive into category experts
    │
    ├── engineering/backend-architect.md
    ├── specialized/microservices-expert.md
    └── specialized/distributed-systems-expert.md
```

## File Structure

```
expert-library/
├── index.json                    # Master index of all 141 experts
│
├── engineering/                  # 23 experts by category
│   ├── engineering-frontend-developer.md
│   ├── engineering-backend-architect.md
│   └── ...
│
├── design/                       # 8 experts
│   └── ...
│
├── ... (11 more categories)
│
├── architect/                   # Role: 5 mapped experts
│   ├── EXPERTS.md              # Role index
│   └── README.md               # Role documentation
│
├── planner/                     # Role: 4 mapped experts
│   └── ...
│
├── frontend/                     # Role: 4 mapped experts
│   └── ...
│
├── backend/                      # Role: 5 mapped experts
│   └── ...
│
├── qa/                          # Role: 4 mapped experts
│   └── ...
│
├── security/                    # Role: 4 mapped experts
│   └── ...
│
├── devops/                      # Role: 4 mapped experts
│   └── ...
│
└── code-reviewer/               # Role: 5 mapped experts
    └── ...
```

## Usage Examples

### Scenario 1: Quick Project Planning

```
User: /plan "开发一个博客系统"

→ Calls: Planner role (pl-001)
→ Fast response with WBS and milestones
→ No need to browse 141 experts
```

### Scenario 2: Deep Security Audit

```
User: "我需要智能合约安全审计专家"

→ Direct access: specialized/blockchain-security-auditor.md
→ Specific domain expertise
→ Not just generic "Security" role
```

### Scenario 3: Multi-Expert Architecture Review

```
User: /architect "设计电商系统架构"

→ Calls: Architect role (ar-001)
    │
    ├── Frontend expert (e-commerce UI patterns)
    ├── Backend expert (scalable API design)
    ├── QA expert (testing strategy)
    └── DevOps expert (deployment architecture)
```

## Benefits Summary

| Benefit | How It's Achieved |
|---------|-------------------|
| **Fast Access** | 8 roles cover 80% of common tasks |
| **Deep Expertise** | 141 experts cover specialized needs |
| **No Duplication** | Roles map to categories, not copy |
| **Flexible** | Call at role level OR category level |
| **Scalable** | Add new categories without restructuring |
| **Clear** | Users know exactly what they're getting |
