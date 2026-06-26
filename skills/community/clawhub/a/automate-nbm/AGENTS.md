# Agent Registry

Complete reference for all 61 agents across 8 departments. Agents with dedicated persona files (✅) have full profiles; others operate from the catalog definition.

## Quick Reference

| Department | Agents | With Profiles |
|------------|--------|---------------|
| 💻 Engineering | 7 | 2 |
| 🎨 Design | 7 | 0 |
| 📢 Marketing | 8 | 1 |
| 📊 Product | 3 | 0 |
| 🎬 Project Management | 5 | 1 |
| 🧪 Testing | 7 | 1 |
| 🛟 Support | 6 | 0 |
| 🎯 Specialized | 6 | 1 |
| **Total** | **49 + orchestrator** | **6 + orchestrator** |

---

## How to Invoke an Agent

### Via GitHub Issue

0. Create an issue using the [Agent Task template](.github/ISSUE_TEMPLATE/agent-task.md)
1. Add a label: `agent:frontend-developer` or `department:engineering`
2. The workflow dispatches the task and posts results as a comment

### Via CLI Scripts

```bash
# Direct task execution
./scripts/run-task.sh backend-architect "Design a REST API for user management"

# Auto-dispatch (keyword detection picks the agent)
TASK_BODY="Build a React dashboard with charts" ./scripts/agent-dispatch.sh

# Explicit agent dispatch
AGENT=growth-hacker TASK_BODY="Create a 90-day growth plan" ./scripts/agent-dispatch.sh

# Department routing
DEPARTMENT=engineering TASK_BODY="Set up CI/CD pipeline" ./scripts/agent-dispatch.sh

# Orchestration mode
ORCHESTRATE=true TASK_BODY="Build a complete e-commerce site" ./scripts/agent-dispatch.sh
```

### Via Workflow Dispatch

Go to **Actions → Agent Task Runner → Run workflow**, enter the agent name and task description.

---

## 💻 Engineering (7 agents)

| Agent | Profile | Specialty |
|-------|---------|-----------|
| `frontend-developer` | ✅ [Profile](agents/engineering/frontend-developer.md) | React/Vue/Angular, TypeScript, responsive UI, performance, a11y |
| `backend-architect` | ✅ [Profile](agents/engineering/backend-architect.md) | API design, databases, microservices, cloud infrastructure |
| `mobile-app-builder` | 📋 Catalog | iOS/Android, React Native, Flutter, cross-platform mobile |
| `ai-engineer` | 📋 Catalog | Machine learning, deep learning, model training, AI integration |
| `devops-automator` | 📋 Catalog | CI/CD, Docker, Kubernetes, Terraform, infrastructure as code |
| `rapid-prototyper` | 📋 Catalog | MVP/POC rapid development, quick validation |
| `senior-developer` | 📋 Catalog | Complex implementations, architecture decisions, code review |

**Dispatch keywords:** react, vue, angular, frontend, api, database, backend, docker, kubernetes, cicd, mobile, ios, android, machine learning, mvp, prototype

---

## 🎨 Design (7 agents)

| Agent | Profile | Specialty |
|-------|---------|-----------|
| `ui-designer` | 📋 Catalog | Visual design, component libraries, design systems |
| `ux-researcher` | 📋 Catalog | User research, usability testing, interviews |
| `ux-architect` | 📋 Catalog | Information architecture, UX flows, CSS systems |
| `brand-guardian` | 📋 Catalog | Brand strategy, identity, style guides |
| `visual-storyteller` | 📋 Catalog | Visual narratives, presentations, multimedia |
| `whimsy-injector` | 📋 Catalog | Micro-interactions, animations, delight moments |
| `image-prompt-engineer` | 📋 Catalog | AI image generation prompts (Midjourney, DALL-E, Stable Diffusion) |

**Dispatch keywords:** ui design, design system, user research, usability, ux, brand, logo, animation, midjourney, dall-e

---

## 📢 Marketing (8 agents)

| Agent | Profile | Specialty |
|-------|---------|-----------|
| `growth-hacker` | ✅ [Profile](agents/marketing/growth-hacker.md) | User acquisition, conversion optimization, viral loops, experiments |
| `content-creator` | 📋 Catalog | Multi-platform content, blog posts, editorial calendars |
| `twitter-engager` | 📋 Catalog | Twitter/X engagement, thought leadership, real-time response |
| `tiktok-strategist` | 📋 Catalog | Short-form video strategy, algorithm optimization |
| `instagram-curator` | 📋 Catalog | Visual storytelling, community building, aesthetic curation |
| `reddit-community-builder` | 📋 Catalog | Subreddit engagement, organic community growth |
| `app-store-optimizer` | 📋 Catalog | ASO, app store listing optimization, conversion |
| `social-media-strategist` | 📋 Catalog | Cross-platform social strategy, content calendar |

**Dispatch keywords:** growth, acquisition, conversion, content, blog, twitter, tiktok, instagram, reddit, app store, social media

---

## 📊 Product (3 agents)

| Agent | Profile | Specialty |
|-------|---------|-----------|
| `sprint-prioritizer` | 📋 Catalog | Agile sprint planning, backlog grooming, prioritization |
| `trend-researcher` | 📋 Catalog | Market intelligence, competitive analysis, trend reports |
| `feedback-synthesizer` | 📋 Catalog | User feedback analysis, NPS/CSAT insights, feature requests |

**Dispatch keywords:** sprint, backlog, prioritization, trend, market research, feedback, nps

---

## 🎬 Project Management (5 agents)

| Agent | Profile | Specialty |
|-------|---------|-----------|
| `senior-pm` | ✅ [Profile](agents/project-management/project-manager-senior.md) | Requirements decomposition, estimation, scope management |
| `studio-producer` | 📋 Catalog | High-level coordination, portfolio management |
| `project-shepherd` | 📋 Catalog | Cross-functional coordination, handoff management |
| `studio-operations` | 📋 Catalog | Daily efficiency, process optimization, tooling |
| `experiment-tracker` | 📋 Catalog | A/B test management, experiment tracking, hypothesis validation |

**Dispatch keywords:** project plan, task breakdown, scope, timeline, roadmap, coordinate, a/b test, experiment

---

## 🧪 Testing (7 agents)

| Agent | Profile | Specialty |
|-------|---------|-----------|
| `reality-checker` | ✅ [Profile](agents/testing/testing-reality-checker.md) | Quality certification, production readiness, release decisions |
| `evidence-collector` | 📋 Catalog | Screenshot QA, visual verification, evidence gathering |
| `test-results-analyzer` | 📋 Catalog | Test result evaluation, coverage analysis, gap identification |
| `performance-benchmarker` | 📋 Catalog | Load testing, performance benchmarks, capacity planning |
| `api-tester` | 📋 Catalog | API validation, integration testing, contract testing |
| `tool-evaluator` | 📋 Catalog | Technology evaluation, tool comparison, recommendations |
| `workflow-optimizer` | 📋 Catalog | Process analysis, bottleneck identification, optimization |

**Dispatch keywords:** quality, release, qa, screenshot, test result, performance test, load test, api test, workflow

---

## 🛟 Support (6 agents)

| Agent | Profile | Specialty |
|-------|---------|-----------|
| `support-responder` | 📋 Catalog | Customer service, ticket resolution, FAQ management |
| `analytics-reporter` | 📋 Catalog | Data analysis, dashboard creation, metric reporting |
| `finance-tracker` | 📋 Catalog | Financial planning, budgets, cost tracking |
| `infrastructure-maintainer` | 📋 Catalog | System reliability, maintenance, uptime monitoring |
| `legal-compliance-checker` | 📋 Catalog | Regulatory compliance, GDPR, legal review |
| `executive-summary-generator` | 📋 Catalog | C-suite communications, board reports, exec briefs |

**Dispatch keywords:** customer, support, analytics, dashboard, finance, budget, maintenance, compliance, legal, executive summary

---

## 🎯 Specialized (6 agents)

| Agent | Profile | Specialty |
|-------|---------|-----------|
| `orchestrator` | ✅ [Profile](orchestrator/SKILL.md) | Multi-agent pipeline — dispatches and coordinates other agents |
| `data-analytics-reporter` | 📋 Catalog | Business intelligence, data pipelines, BI dashboards |
| `lsp-index-engineer` | 📋 Catalog | Language Server Protocol, code intelligence, IDE tooling |
| `sales-data-extraction-agent` | 📋 Catalog | Sales data extraction, CRM integration |
| `data-consolidation-agent` | 📋 Catalog | Data consolidation, deduplication, merge strategies |
| `report-distribution-agent` | 📋 Catalog | Report scheduling, delivery, multi-channel distribution |

**Dispatch keywords:** orchestrate, data extraction, lsp, code intelligence, consolidation, report distribution

---

## Auto-Dispatch

When no agent is explicitly specified, the dispatch script (`scripts/agent-dispatch.sh`) matches task keywords to agents automatically. If no match is found, the task defaults to `senior-pm` for triage and decomposition.

The full keyword → agent mapping is defined in `scripts/agent-dispatch.sh` and mirrored in `config/automate.yml`.
