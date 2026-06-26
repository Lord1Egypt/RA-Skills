---
name: eric-app-builder
description: "Full-stack application builder that creates web apps, APIs, mobile apps, and more from natural language requests. Use when the user wants to build a new application, add features to existing projects, scaffold a project structure, or plan an implementation."
---

# App Builder Skill

This skill provides structured knowledge for building full-stack applications from scratch or enhancing existing projects. It covers project detection, tech stack selection, scaffolding patterns, implementation planning, and feature building.

## Contents

1. **Project Detection** - Keyword matrix for identifying project types
2. **Tech Stack** - 2025 default technologies and alternatives
3. **Scaffolding** - Directory structures and core files
4. **Implementation Planning** - Requirement analysis, task breakdown, and plan format
5. **Feature Building** - Analysis and implementation patterns
6. **Coordination** - Multi-phase development workflow

---

## 1. Project Detection

### Keyword Matrix

| Keywords | Project Type | Recommended Stack |
|----------|--------------|-------------------|
| blog, post, article | Blog | Next.js Static |
| e-commerce, product, cart, payment | E-commerce | Next.js + Stripe |
| dashboard, panel, management | Admin Dashboard | Next.js + Supabase |
| api, backend, service, rest | API Service | Express or FastAPI |
| python, fastapi, django | Python API | FastAPI |
| mobile, android, ios, react native | Mobile App | React Native (Expo) |
| portfolio, personal, cv | Portfolio | Next.js Static |
| crm, customer, sales | CRM | Next.js + Supabase |
| saas, subscription, stripe | SaaS | Next.js + Stripe + Auth |
| landing, promotional, marketing | Landing Page | Next.js Static |
| extension, plugin, chrome | Browser Extension | Chrome MV3 |
| cli, command line, terminal | CLI Tool | Node.js |

### Detection Process

```
1. Tokenize user request
2. Extract keywords and match to project type
3. Identify missing information → ask clarifying questions
4. Suggest appropriate tech stack
5. Confirm with user before proceeding
```

---

## 2. Tech Stack Selection (2025)

### Default Web App Stack

```yaml
Frontend:
  framework: Next.js 16 (Stable)
  language: TypeScript 5.7+
  styling: Tailwind CSS v4
  state: React 19 Actions / Server Components
  bundler: Turbopack (Dev Mode)

Backend:
  runtime: Node.js 23
  framework: Next.js API Routes
  validation: Zod

Database:
  primary: PostgreSQL
  provider: Supabase
  orm: Prisma

Auth:
  provider: Supabase Auth or Clerk

Deployment:
  tool: Built-in deploy command
```

### Alternative Options

| Need | Default | Alternative |
|------|---------|-------------|
| Real-time | Supabase Realtime | Socket.io |
| File storage | Supabase Storage | Cloudinary, S3 |
| Payment | Stripe | LemonSqueezy, Paddle |
| Email | Resend | SendGrid |
| Search | - | Algolia, Typesense |

---

## 3. Project Scaffolding

### Next.js Full-Stack Structure

```
project-name/
├── src/
│   ├── app/                        # Routes only (thin layer)
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── globals.css
│   │   ├── (auth)/                 # Route group - auth pages
│   │   │   ├── login/page.tsx
│   │   │   └── register/page.tsx
│   │   ├── (dashboard)/            # Route group - dashboard
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   └── api/
│   │       └── [resource]/route.ts
│   │
│   ├── features/                   # Feature-based modules
│   │   ├── auth/
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   ├── actions.ts          # Server Actions
│   │   │   ├── queries.ts          # Data fetching
│   │   │   └── types.ts
│   │   └── [other-features]/
│   │
│   ├── shared/                     # Shared utilities
│   │   ├── components/ui/          # Reusable UI components
│   │   ├── lib/                    # Utils, helpers
│   │   └── hooks/                  # Global hooks
│   │
│   └── server/                     # Server-only code
│       ├── db/                     # Database client
│       ├── auth/                   # Auth config
│       └── services/               # External API integrations
│
├── prisma/
│   ├── schema.prisma
│   └── seed.ts
│
├── public/
├── .env.example
├── package.json
├── tailwind.config.ts
└── tsconfig.json
```

### Structure Principles

| Principle | Implementation |
|-----------|----------------|
| **Feature isolation** | Each feature in `features/` with its own components, hooks, actions |
| **Server/Client separation** | Server-only code in `server/`, prevents accidental client imports |
| **Thin routes** | `app/` only for routing, logic lives in `features/` |
| **Route groups** | `(groupName)/` for layout sharing without URL impact |
| **Shared code** | `shared/` for truly reusable UI and utilities |

### Path Aliases (tsconfig.json)

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"],
      "@/features/*": ["./src/features/*"],
      "@/shared/*": ["./src/shared/*"],
      "@/server/*": ["./src/server/*"]
    }
  }
}
```

---

## 4. Implementation Planning

When planning a new project or feature, follow this structured approach before writing any code.

### Requirement Analysis

1. **Break down user requests** into concrete features
2. **Identify data models** and their relationships
3. **Determine API endpoints** or server actions needed
4. **List UI components** required
5. **Identify potential blockers** early

### Task Breakdown

- Create an ordered task list with dependencies
- Estimate complexity for each task (simple / medium / complex)
- Flag tasks that require user decisions or external services

### Plan Output Format

When presenting a plan to the user, use this structure:

```markdown
# Implementation Plan: [Project Name]

## Overview
[Brief description of what will be built]

## Data Models
- Model1: [fields and relationships]
- Model2: [fields and relationships]

## API Routes / Server Actions
- POST /api/resource - [description]
- GET /api/resource - [description]

## Pages & Components
- /page-name
  - ComponentA
  - ComponentB

## Implementation Order
1. [ ] Database schema
2. [ ] API routes / server actions
3. [ ] UI components
4. [ ] Integration & wiring
5. [ ] Testing & error fixing

## Dependencies
- [package1]
- [package2]
```

### Planning Guidelines

- Be specific and actionable in each task
- Consider edge cases and error states
- Plan for input validation and error handling
- Keep security in mind (auth, authorization, input sanitization)
- Present the plan to the user and get approval before proceeding

---

## 5. Feature Building

### Feature Analysis Template

```
Request: "[user feature request]"

Analysis:
├── Required Changes:
│   ├── Database: [tables/columns needed]
│   ├── Backend: [API routes/actions needed]
│   ├── Frontend: [components/pages needed]
│   └── Config: [environment variables needed]
│
├── Dependencies:
│   ├── [npm packages]
│   └── [existing features required]
│
└── Implementation Steps:
    1. [Step 1]
    2. [Step 2]
    ...
```

### Iterative Enhancement Process

```
1. Analyze existing project structure
2. Create detailed change plan
3. Present plan to user for approval
4. Get confirmation
5. Apply changes incrementally
6. Test after each change
7. Deploy and show preview
```

### Error Handling

| Error Type | Solution Strategy |
|------------|-------------------|
| TypeScript Error | Fix type, add missing import |
| Missing Dependency | Install with npm/pnpm |
| Build Error | Check syntax, verify imports |
| Database Error | Check schema, validate migrations |
| Runtime Error | Debug logic, check API responses |

### Recovery Strategy

```
1. Detect error from build/runtime output
2. Attempt automatic fix
3. If failed, report to user with context
4. Suggest alternative approach
5. Rollback if necessary (git)
```

---

## 6. Development Coordination

### Core Workflow

```
1. ANALYZE → Understand user request, detect project type
2. PLAN → Create detailed implementation plan, get user approval
3. BUILD → Scaffold structure, implement features (database → backend → frontend)
4. TEST → Run build, verify functionality, fix errors
5. DEPLOY → Deploy application and provide URL
```

### Execution Phases

| Phase | Focus | Checkpoint |
|-------|-------|------------|
| 1. Analysis | Understand requirements | Clear spec confirmed |
| 2. Planning | Create implementation plan | Plan approved by user |
| 3. Database | Schema design, migrations | Schema created |
| 4. Backend | API routes, server actions | Endpoints working |
| 5. Frontend | Components, pages, styling | UI complete |
| 6. Testing | Build check, error fixing | Build passes |
| 7. Deployment | Deploy to production | Live URL provided |

### Quality Gates

- **Before Phase 3**: User must approve the plan
- **Before Phase 7**: Build must pass without errors
- **After Deployment**: Verify the live site works

---

## Usage Guidelines

1. **Always start with project type detection** - Match keywords to determine the best approach
2. **Present plans before implementing** - Get user confirmation on significant decisions
3. **Build incrementally** - Test after each major change
4. **Deploy early** - Get a working version deployed quickly, then iterate
5. **Handle errors gracefully** - Fix issues and continue, don't give up
6. **Type safety throughout** - Full TypeScript coverage with Zod validation for inputs
7. **Progressive enhancement** - Start simple, add complexity as needed
