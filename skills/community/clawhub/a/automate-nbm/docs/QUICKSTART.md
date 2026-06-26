# Quick Start Guide

Get Automate running in 5 minutes. This guide covers the three main ways to use the platform.

---

## Prerequisites

- A GitHub repository (this one: `automate-nbm`)
- Git and Bash (for local scripts)
- Optional: `OPENCLAW_TOKEN` secret for AI-powered execution
- Optional: `AUTOMATE_SSH_KEY` secret for secure operations

## Setup

### 0. Clone the Repo

```bash
git clone git@github.com:ironiclawdoctor-design/automate-nbm.git
cd automate-nbm
```

### 1. Configure GitHub Secrets

Go to **Settings → Secrets and variables → Actions** and add:

| Secret | Purpose | Required |
|--------|---------|----------|
| `OPENCLAW_TOKEN` | AI-powered agent execution | Recommended |
| `AUTOMATE_SSH_KEY` | SSH back to host server | Optional |
| `ALLOWED_SENDERS` | Whitelist for `repository_dispatch` | Optional |

### 2. Verify Setup

```bash
# Validate configuration and agent files
make validate

# List all available agents
make list-agents

# Run the test suite
make test
```

---

## Method 1: GitHub Issues (Recommended)

The simplest way. Create an issue, the system does the rest.

### Submit an Agent Task

0. Go to **Issues → New Issue → Agent Task** template
1. Fill in the agent name and task description
2. Submit — the workflow auto-dispatches and posts results as comments

**Example issue:**

```
Title: [AGENT] Design a REST API for user management

Agent: backend-architect
Department: engineering

## Task Description
Design a REST API for a user management system. Requirements:
- User CRUD operations
- Authentication (JWT)
- Role-based access control (admin, user, viewer)
- Rate limiting
- PostgreSQL database schema

## Expected Deliverables
- OpenAPI spec
- Database schema (SQL)
- Authentication flow diagram
```

### What Happens

0. **Acknowledge** — Bot comments "Task received, assigned to backend-architect"
1. **Dispatch** — Task is routed to the agent via `scripts/agent-dispatch.sh`
2. **Execute** — Agent processes the task (AI-powered if `OPENCLAW_TOKEN` is set)
3. **Report** — Results are posted as an issue comment
4. **Label** — Issue gets labeled `completed`

### Trigger Orchestration

For complex multi-agent projects, add the `orchestrate` label:

```
Title: [ORCHESTRATE] Build an e-commerce MVP

## Task Description
Build a minimum viable e-commerce site:
- Product catalog with search and filtering
- Shopping cart and checkout flow
- User authentication
- Admin dashboard for inventory management
- Tech stack: React + Node.js + PostgreSQL

## Expected Deliverables
- Frontend components
- API design
- Database schema
- Deployment configuration
```

The orchestrator will decompose this into tasks, assign agents, run QA loops, and deliver integrated results.

---

## Method 2: CLI Scripts (Local)

Run agents directly from the command line.

### Run a Single Agent

```bash
# Syntax
./scripts/run-task.sh <agent-name> "<task-description>"

# Examples
./scripts/run-task.sh frontend-developer "Create a responsive navigation component using React and Tailwind CSS"
./scripts/run-task.sh backend-architect "Design a PostgreSQL schema for a multi-tenant SaaS application"
./scripts/run-task.sh growth-hacker "Create a 90-day growth plan targeting 10K MAU for a developer tool"
./scripts/run-task.sh reality-checker "Assess production readiness for the v2.0 release"
./scripts/run-task.sh senior-pm "Break down this project into sprint-sized tasks: build a mobile banking app"
```

### Auto-Dispatch (Keyword Detection)

Let the system pick the right agent based on task keywords:

```bash
# The dispatch script analyzes keywords and routes automatically
TASK_BODY="Build a React dashboard with real-time charts" ./scripts/agent-dispatch.sh
# → Auto-detects: frontend-developer

TASK_BODY="Set up a Kubernetes deployment with auto-scaling" ./scripts/agent-dispatch.sh
# → Auto-detects: devops-automator

TASK_BODY="Design a user onboarding flow that increases activation by 20%" ./scripts/agent-dispatch.sh
# → Auto-detects: growth-hacker
```

### Department Routing

```bash
# Route to best agent in a department
DEPARTMENT=engineering TASK_BODY="Optimize database queries" ./scripts/agent-dispatch.sh

# Orchestration mode
ORCHESTRATE=true TASK_BODY="Build a complete blog platform" ./scripts/agent-dispatch.sh
```

### Send Notifications

```bash
# Console
./scripts/notify.sh info "Task started" console

# GitHub issue comment
GITHUB_TOKEN=xxx GITHUB_REPOSITORY=owner/repo ISSUE_NUMBER=42 \
  ./scripts/notify.sh success "Task completed!" github

# Webhook
WEBHOOK_URL=https://hooks.example.com/notify \
  ./scripts/notify.sh error "Build failed" webhook
```

---

## Method 3: Workflow Dispatch (Manual Trigger)

Trigger workflows directly from the GitHub Actions UI.

0. Go to **Actions** tab
1. Select a workflow:
   - **Agent Task Runner** — single agent task
   - **Orchestrator Pipeline** — multi-agent project
   - **Scheduled Automation** — manual trigger of scheduled tasks
2. Click **Run workflow**
3. Fill in the inputs (agent name, task description, QA level)
4. Watch the run and check results

---

## Writing Good Task Descriptions

The quality of agent output depends heavily on task description quality.

### ❌ Too Vague
```
Build a website
```

### ✅ Good
```
Build a responsive landing page for a SaaS product:
- Hero section with headline, subheading, and CTA button
- Feature grid (3 features with icons)
- Pricing table (3 tiers)
- FAQ accordion
- Footer with links and newsletter signup

Tech: React + Tailwind CSS
Target: Desktop and mobile (320px+)
Constraints: Must score 90+ on Lighthouse performance
```

### Tips
- **Be specific** about tech stack, constraints, and deliverables
- **Provide context** — what's the product? who are the users?
- **Define "done"** — what does the output look like?
- **Include examples** or references when possible

---

## Configuration

All configuration lives in `config/automate.yml`. Key settings:

```yaml
# Agent selection strictness
orchestrator:
  qa_level: 2          # 0=quick, 4=production-grade

# Task limits
tasks:
  max_concurrent: 3
  timeout_minutes: 30

# Notification targets
notifications:
  targets: [console, github]
```

See the full config file for all options.

---

## Troubleshooting

### Issue created but no response
- Check that the issue has the `task` or `agent-task` label
- Verify workflows are enabled: **Settings → Actions → General**
- Check workflow run logs in the **Actions** tab

### Agent not found
- See [AGENTS.md](../AGENTS.md) for the full list of agent names
- Names are case-sensitive and use kebab-case: `frontend-developer`, not `Frontend Developer`

### "Basic mode" — no AI processing
- Set the `OPENCLAW_TOKEN` secret in **Settings → Secrets**
- Without it, tasks are recorded but not AI-processed

### Workflow syntax errors
- Run `make validate` to check all workflow files
- Use [actionlint](https://github.com/rhysd/actionlint) for detailed validation

---

## Next Steps

- Browse the [Agent Registry](../AGENTS.md) to see all 61 agents
- Read agent profiles in `agents/` for capability details
- Check the [Orchestrator docs](../orchestrator/SKILL.md) for multi-agent pipelines
- Review `config/automate.yml` to customize settings
