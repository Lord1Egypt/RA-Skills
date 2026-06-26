---
name: client-onboard
description: Generate a complete client onboarding package from a project description. Creates project brief, tech stack, milestones, folder structure, CLAUDE.md, and a ready-to-send kickoff message. Run when closing a new freelance client.
argument-hint: [project description — type, industry, timeline, budget if known]
allowed-tools: Read, Write, Bash, Glob
---

# Client Onboard — Freelance Project Onboarding Generator

## Why This Exists
Kevin closes a client → now needs to look professional and get the project moving within 24 hours. Manual onboarding prep = 2 hours of doc writing. This skill turns a project description into a full onboarding package in one shot.

## Trigger
Use when: "onboard a new client", "I just got a project", "set up client files for", "new client [description]", or any time a new freelance project is starting.

Invoked as: `/client-onboard [project description]`

---

## Process

### Step 1: Parse the Project

From `$ARGUMENTS`, extract:
- **Project type**: web app, API, automation, audit, mobile, data pipeline, etc.
- **Client industry**: SaaS, ecommerce, healthcare, finance, creator economy, etc.
- **Timeline hints**: "need this in 2 weeks", "no rush", "ASAP", specific dates mentioned
- **Budget hints**: hourly rate mentioned, fixed price, "small budget", enterprise
- **Tech constraints**: "must use React", "we're on AWS", "no vendor lock-in"
- **Team context**: "solo founder", "we have a dev team", "replacing a contractor"

**Default assumptions when not specified:**
- Timeline: 4-6 weeks (reasonable for most web projects)
- Budget: $75/hr or $2,000-5,000 fixed (Kevin's standard range)
- Stack: Next.js + Supabase + Stripe + Python (Kevin's default)
- Deployment: Vercel (frontend) + Railway or Supabase (backend)

---

### Step 2: Create the Output Directory

Create `CLIENT_ONBOARD/` in the current directory.

```bash
mkdir -p CLIENT_ONBOARD
```

If a client name is identifiable from `$ARGUMENTS`, use: `[ClientName]_ONBOARD/` instead.

---

### Step 3: Write PROJECT_BRIEF.md

```markdown
# Project Brief — [Project Name]
Client: [client name or "TBD"]
Date: [today's date]
Status: DRAFT — pending client confirmation

---

## Project Overview
[2-3 sentences. What is being built, for whom, and why it matters to the client's business. Be specific — no "robust scalable solution" language.]

## Business Goal
[What does the client actually need this to DO for their business? Revenue impact? Time savings? User growth?]

## Success Criteria
- [ ] [Specific measurable outcome 1]
- [ ] [Specific measurable outcome 2]
- [ ] [Specific measurable outcome 3]
- [ ] All features from this brief are delivered and tested
- [ ] Client signs off on final deliverable

## Key Users
- **Primary**: [who uses this most, what they need]
- **Secondary**: [any other users]
- **Admin**: [Kevin or client manages this]

## Core Features (In Scope)
1. [Feature 1 — brief description]
2. [Feature 2 — brief description]
3. [Feature 3 — brief description]
[...continue for all core features...]

## Out of Scope (v1)
- [Feature that sounds related but isn't included] — defer to v2
- [Feature] — available as add-on after launch
- [Feature] — client can self-manage post-launch

## Known Risks
- [Risk 1]: [mitigation]
- [Risk 2]: [mitigation]

## Open Questions
- [ ] [Question that needs client answer before starting]
- [ ] [Question]

---
*This brief is a living document. Changes require written agreement from both parties.*
```

---

### Step 4: Write TECH_STACK.md

```markdown
# Tech Stack — [Project Name]
Decided: [today's date]

---

## Recommended Stack

### Frontend
- **Framework**: Next.js 14+ (App Router)
  - *Why*: [specific reason for this project — e.g., "SEO required", "fast iteration", "familiar to Kevin"]
- **UI**: Tailwind CSS + Shadcn/UI components
  - *Why*: Ships faster than custom CSS, consistent design system
- **State**: Zustand (client state) + React Query (server state)
- **TypeScript**: Yes — catches bugs before they reach the client

### Backend
- **Database + Auth + Storage**: Supabase (Postgres)
  - *Why*: [specific reason — e.g., "handles auth out of the box", "real-time subscriptions needed", "generous free tier for MVP"]
- **Edge Functions**: Supabase Edge Functions (Deno)
  - *Why*: Co-located with DB, no cold starts on Vercel hobby plan
- **[If needed] Python API**: FastAPI
  - *Why*: [e.g., "AI/ML workloads", "batch processing", "heavier compute"]

### Payments (if applicable)
- **Stripe**: Checkout, webhooks, Customer Portal
  - *Why*: Industry standard, great DX, handles PCI compliance

### Deployment
- **Frontend**: Vercel (auto-deploy on git push)
- **Backend**: Supabase managed (no ops)
- **[If needed] Workers**: Railway (simple, cheap, no k8s)

### AI/Automation (if applicable)
- **LLM**: Anthropic Claude API (claude-sonnet-4-6)
- **Orchestration**: Custom Python agent or Claude Code skill

---

## Alternatives Considered
| Option | Why Rejected |
|--------|-------------|
| [Alt 1] | [reason] |
| [Alt 2] | [reason] |

## Stack Risks & Mitigations
- **Supabase vendor lock-in**: Postgres is standard — can self-host if needed
- **Vercel pricing at scale**: Set spending limits, switch to Railway if traffic spikes
```

Customize the stack to the project — if the client specifies AWS, remove Vercel; if they need mobile, add React Native; etc.

---

### Step 5: Write MILESTONES.md

```markdown
# Milestones — [Project Name]
Total estimated timeline: [X] weeks
Start date: [today or TBD]
Target completion: [date or TBD]

---

## Milestone 1: Foundation — Week 1-2
**Goal:** Project structure, auth, and core data models in place. Nothing works end-to-end yet, but the scaffolding is solid.

**Deliverables:**
- [ ] Repo setup with CI/CD (Vercel auto-deploy)
- [ ] Supabase project + schema (tables, RLS policies)
- [ ] Auth flow (login, signup, session management)
- [ ] Basic navigation shell
- [ ] CLAUDE.md updated with project conventions

**Handoff criteria:** Kevin demos a working login → dashboard skeleton. Client confirms schema looks right.

---

## Milestone 2: Core Features — Week 2-4
**Goal:** The main thing the client paid for is built and working.

**Deliverables:**
- [ ] [Core feature 1] — built and tested
- [ ] [Core feature 2] — built and tested
- [ ] [Core feature 3] — built and tested
- [ ] Error states and loading states implemented
- [ ] Mobile responsive

**Handoff criteria:** Client can use the app end-to-end for the primary use case.

---

## Milestone 3: Polish + Integrations — Week 4-5
**Goal:** Third-party integrations, edge cases handled, UI polished.

**Deliverables:**
- [ ] [Payment / email / analytics integration]
- [ ] Edge cases from testing handled
- [ ] Performance check (Lighthouse score > 85)
- [ ] Security review (RLS policies, input validation, env vars)

**Handoff criteria:** App is production-ready. No known bugs.

---

## Milestone 4: Launch + Handoff — Week 5-6
**Goal:** Live in production, client can operate it.

**Deliverables:**
- [ ] Production deployment (custom domain, SSL)
- [ ] Monitoring set up (Sentry or basic error logging)
- [ ] Client walkthrough recording (Loom)
- [ ] Admin documentation (how to manage users, content, etc.)
- [ ] Code repo access transferred

**Handoff criteria:** Client signs off. Final invoice sent.

---

## Payment Schedule (suggested)
- 25% upfront (project kickoff)
- 25% Milestone 2 complete
- 25% Milestone 3 complete
- 25% final delivery + sign-off
```

Adjust milestone count and timeline to match project scope. Small projects (1-2 weeks): 2 milestones. Large projects (8+ weeks): 5-6 milestones.

---

### Step 6: Write FOLDER_STRUCTURE.md

Generate a proposed directory layout tailored to the project. Standard Next.js + Supabase layout:

```markdown
# Folder Structure — [Project Name]

```
[project-name]/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── (auth)/             # Auth-gated routes
│   │   │   ├── dashboard/
│   │   │   └── settings/
│   │   ├── (public)/           # Public routes
│   │   │   ├── page.tsx        # Landing page
│   │   │   └── pricing/
│   │   ├── api/                # API routes
│   │   │   └── webhooks/
│   │   ├── layout.tsx
│   │   └── globals.css
│   ├── components/
│   │   ├── ui/                 # Shadcn/UI base components
│   │   └── [feature]/          # Feature-specific components
│   ├── lib/
│   │   ├── supabase/           # DB client + type-safe helpers
│   │   ├── stripe/             # Stripe client + webhook handlers
│   │   └── utils.ts
│   ├── hooks/                  # Custom React hooks
│   └── types/                  # Shared TypeScript types
├── supabase/
│   ├── migrations/             # SQL migration files
│   └── functions/              # Edge functions
├── scripts/                    # One-off scripts + automation
├── docs/                       # Client-facing documentation
│   └── ADMIN_GUIDE.md
├── .env.local                  # Local env vars (not committed)
├── .env.example                # Template for env vars
├── CLAUDE.md                   # Claude Code context for this project
├── SPEC.md                     # Project specification
└── package.json
```
```

Adjust to the actual stack. Python-only projects get a different layout.

---

### Step 7: Write CLAUDE.md (Project Starter)

```markdown
# [Project Name] — Claude Code Context

## What This Is
[1-2 sentences from PROJECT_BRIEF — what this project does]

## Stack
- Frontend: Next.js 14 (App Router), TypeScript, Tailwind, Shadcn/UI
- Backend: Supabase (Postgres + Auth + Edge Functions)
- Payments: Stripe
- Deployment: Vercel

## Key Paths
- App pages: `src/app/`
- Components: `src/components/`
- DB helpers: `src/lib/supabase/`
- DB schema: `supabase/migrations/`
- Edge functions: `supabase/functions/`

## Dev Commands
```bash
npm run dev          # start local dev server (localhost:3000)
npm run build        # production build
npm run lint         # ESLint check
supabase start       # start local Supabase (Docker required)
supabase db push     # apply migrations to remote
```

## Environment Variables
See `.env.example` for required vars. Local values in `.env.local` (not committed).

## Conventions
- TypeScript strict mode — no `any`, no unchecked nulls
- Components: PascalCase, one component per file
- DB types: generate from Supabase dashboard → TypeScript types
- API routes: validate input with Zod before touching DB
- RLS: every table has Row Level Security enabled

## Current Status
[Today's date] — Project just started. Milestone 1 in progress.

## Known Gotchas
- [Any project-specific things Claude should know]
```

---

### Step 8: Write KICKOFF_MSG.md

Write a message Kevin can send directly to the client — professional, warm, no fluff:

```markdown
# Kickoff Message — Ready to Send

---

Hey [Client Name],

Great to officially be on board — excited to build [project name] with you.

I've put together the initial project brief and milestone breakdown based on our conversation. Before I write a single line of code, I want to make sure we're aligned on scope and timeline.

Quick asks:

1. **Review the scope**: Does the feature list match what you're expecting? Anything missing or that should be cut from v1?

2. **One open question**: [Most important open question from PROJECT_BRIEF.md]

3. **Kickoff call**: I'd like to do a 30-minute call this week to align on priorities and answer any questions you have. What does your schedule look like [Tuesday-Thursday]? I'm flexible between 10am-4pm ET.

Once we're aligned, I'll kick off Milestone 1 and have a working foundation for you to see within [X] days.

Let me know if you have any questions before then — happy to jump on a quick call or answer over message.

— Kevin

---

*[Attach: PROJECT_BRIEF.md or paste the scope section inline]*
```

---

### Step 9: Print Summary

```
Client onboarding package created.

Directory: ./CLIENT_ONBOARD/ (or ./[ClientName]_ONBOARD/)

Files generated:
  ✓ PROJECT_BRIEF.md     — scope, goals, out-of-scope
  ✓ TECH_STACK.md        — recommended stack with rationale
  ✓ MILESTONES.md        — [X] milestones, [Y]-week timeline
  ✓ FOLDER_STRUCTURE.md  — proposed directory layout
  ✓ CLAUDE.md            — project context for Claude Code
  ✓ KICKOFF_MSG.md       — client message, ready to send

Next steps:
  1. Review PROJECT_BRIEF.md — confirm scope is accurate
  2. Adjust MILESTONES.md timeline if needed
  3. Send KICKOFF_MSG.md to client (customize [Client Name])
  4. Copy CLAUDE.md into the new project repo root
  5. Invoice 25% upfront before starting work
```

---

## Error Handling

- **Very vague description** ("build me an app"): Generate with defaults + add 5 open questions to PROJECT_BRIEF.md under "Open Questions" — flag that client answers are required before kicking off
- **Multiple possible stacks**: Choose Kevin's default stack, add "Alternatives Considered" section explaining why alternatives were skipped
- **Unclear budget**: Leave payment schedule with placeholder percentages, note "confirm rate with client before sending"
- **CLIENT_ONBOARD/ already exists**: Add timestamp suffix `CLIENT_ONBOARD_[YYYY-MM-DD]/` to avoid overwriting
- **Missing tech details**: Generate best-guess and mark assumptions clearly with `[ASSUMED]` inline

## Kevin's Voice — Don't Forget
- Direct, confident, no corporate fluff
- "I'll build X using Y because Z" — not "I would suggest potentially leveraging..."
- Milestones are concrete with clear handoff criteria, not vague "phase" labels
- Kickoff message reads like a text from a capable contractor, not a formal business letter
