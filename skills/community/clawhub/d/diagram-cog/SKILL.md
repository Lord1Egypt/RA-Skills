---
name: diagram-cog
description: "AI diagram generation powered by CellCog. Flowcharts, system architecture, mind maps, org charts, ER diagrams, sequence diagrams, Gantt charts, network diagrams. Describe your system in plain English, get interactive diagrams or print-ready PDFs."
metadata:
  openclaw:
    emoji: "🔀"
    os: [darwin, linux, windows]
    requires:
      bins: [python3]
      env: [CELLCOG_API_KEY]
author: CellCog
homepage: https://cellcog.ai
dependencies: [cellcog]
---
# Diagram Cog - Describe It in Words, Get It as a Diagram

Describe your system, process, or idea in plain English — CellCog produces professional, interactive diagrams you can share with a URL.

No Visio. No Lucidchart. No dragging boxes around for hours. Just describe what you need, and CellCog renders it as an interactive web page you can zoom, pan, and click — or a print-ready PDF for documentation.

## How to Use

For your first CellCog task in a session, read the **cellcog** skill for the full SDK reference — file handling, chat modes, timeouts, and more.

**OpenClaw (fire-and-forget):**
```python
result = client.create_chat(
    prompt="[your task prompt]",
    notify_session_key="agent:main:main",
    task_label="my-task",
    chat_mode="agent",
)
```

**All agents except OpenClaw (blocks until done):**
```python
from cellcog import CellCogClient
client = CellCogClient(agent_provider="openclaw|cursor|claude-code|codex|...")
result = client.create_chat(
    prompt="[your task prompt]",
    task_label="my-task",
    chat_mode="agent",
)
print(result["message"])
```


---

## Why Diagrams Are Hard

Creating good diagrams manually is surprisingly painful:

- **Layout is tedious**: Arranging boxes, arrows, and labels takes longer than the thinking itself
- **Tools are complex**: Visio, Lucidchart, Draw.io all have learning curves
- **Iteration is slow**: Changing one element cascades into repositioning everything
- **Sharing is friction**: Export → attach → hope it renders on their device

CellCog eliminates all of this. Describe your diagram in words, get a shareable interactive URL. Need to change something? Just ask.

---

## What Makes This Different

Other AI diagram tools output a static image. CellCog does something fundamentally different.

CellCog **reasons about your system, picks the right rendering approach, and deploys an interactive web application** you can share with a URL. Zoom into your microservices architecture. Click a node to see details. Pan across a sprawling org chart. Or export to a print-ready PDF for your board deck.

| What You Ask For | What CellCog Actually Does |
|-----------------|---------------------------|
| "Diagram my microservices" | Reasons about the architecture → generates Mermaid/D3 code → deploys interactive web app → delivers shareable URL |
| "Flowchart for our hiring process" | Analyzes the process → renders with proper decision logic → color-codes paths → interactive HTML with click states |
| "ER diagram for my database" | Understands entity relationships → generates diagram with cardinality → exports as both interactive HTML and PDF |
| "Mind map for brainstorming" | Explores the topic → creates hierarchical structure → deploys zoomable, expandable mind map |

The power comes from having a world-class coding agent, multiple rendering libraries (Mermaid.js, D3.js, custom SVG, Highcharts), and built-in app deployment — all orchestrated together. When standard tools fall short, the agent writes custom code.

---

## What Diagrams You Can Create

### Flowcharts & Process Flows

Visualize any process or decision tree:

- **Business Processes**: "Create a flowchart for our customer onboarding process — from signup to first value"
- **Decision Trees**: "Build a decision tree for our support team to triage incoming tickets"
- **User Flows**: "Create a user flow diagram for the checkout process in our e-commerce app"
- **Approval Workflows**: "Diagram our expense approval workflow — who approves what at each dollar threshold"
- **Troubleshooting Guides**: "Create a troubleshooting flowchart for common API integration errors"

**Example prompt:**
> "Create an interactive flowchart for our hiring process:
> 
> Steps:
> 1. Job posted → Applications received
> 2. Resume screening (HR) → Pass/Fail
> 3. Phone screen (Recruiter) → Pass/Fail
> 4. Technical interview (Engineering) → Pass/Fail
> 5. Culture interview (Team) → Pass/Fail
> 6. Offer → Accept/Decline
> 7. If decline → Back to step 2 with next candidate
> 
> Color-code: Green for forward progress, red for rejection paths, yellow for decision points.
> Include average time at each stage."

### System Architecture

Technical diagrams for engineering teams:

- **Microservices**: "Diagram our microservices architecture showing all services, their communication patterns, and data stores"
- **Cloud Infrastructure**: "Create an AWS architecture diagram for our production environment — VPC, ECS, RDS, ElastiCache, CloudFront"
- **Data Pipelines**: "Diagram our data pipeline from raw ingestion through transformation to the analytics warehouse"
- **API Architecture**: "Create an API gateway architecture showing routing, authentication, and rate limiting"
- **CI/CD Pipelines**: "Diagram our deployment pipeline from git push to production"

**Example prompt:**
> "Create a system architecture diagram for a SaaS application:
> 
> Frontend: React app on CloudFront/S3
> API: FastAPI on ECS Fargate behind ALB
> Auth: Firebase Authentication
> Database: PostgreSQL on RDS (primary + read replica)
> Cache: Redis on ElastiCache
> Queue: SQS for async jobs
> Workers: Celery on ECS
> Storage: S3 for user uploads
> Monitoring: CloudWatch + Datadog
> 
> Show the data flow between components with arrows.
> Group by VPC / public / external.
> Interactive — I want to be able to zoom into each component."

### Mind Maps & Concept Maps

Brainstorm and organize ideas:

- **Brainstorming**: "Create a mind map exploring all possible revenue streams for our SaaS product"
- **Topic Exploration**: "Build a concept map of machine learning — main branches, sub-topics, and relationships"
- **Content Planning**: "Create a mind map for our Q2 content strategy — blog, social, video, email"
- **Strategy Mapping**: "Map our go-to-market strategy showing channels, messaging, and target segments"

**Example prompt:**
> "Create an interactive mind map for 'AI in Healthcare':
> 
> Central node: AI in Healthcare
> 
> Main branches:
> - Diagnostics (imaging, pathology, genomics)
> - Drug Discovery (target identification, clinical trials, molecule design)
> - Patient Care (chatbots, monitoring, personalized medicine)
> - Operations (scheduling, billing, supply chain)
> - Research (literature mining, clinical data analysis)
> 
> Each branch should have 3-5 sub-topics with brief descriptions.
> Color-code by maturity: green = in production, yellow = clinical trials, red = research stage."

### Org Charts

Visualize organizational structure:

- **Company Hierarchy**: "Create an org chart for a 50-person startup showing all departments and reporting lines"
- **Team Structure**: "Diagram our engineering team structure — squads, tech leads, and cross-functional relationships"
- **Matrix Organization**: "Create an org chart showing both functional reporting and project reporting lines"

### UML Diagrams

Software engineering diagrams:

- **Sequence Diagrams**: "Create a sequence diagram showing the OAuth 2.0 authorization code flow"
- **Class Diagrams**: "Diagram the class hierarchy for our e-commerce domain model — Product, Order, Customer, Payment"
- **State Diagrams**: "Create a state diagram for an order lifecycle — placed, paid, shipped, delivered, returned"
- **Activity Diagrams**: "Diagram the activity flow for our data processing pipeline"

**Example prompt:**
> "Create a sequence diagram for a payment processing flow:
> 
> Actors: User, Frontend, API Server, Payment Service, Stripe, Database
> 
> Flow:
> 1. User clicks 'Pay' → Frontend sends payment request to API
> 2. API creates payment intent with Stripe
> 3. Stripe returns client secret
> 4. API sends client secret to Frontend
> 5. Frontend confirms payment with Stripe.js
> 6. Stripe sends webhook to API
> 7. API updates order status in Database
> 8. API sends confirmation email to User
> 
> Include error paths: payment declined, webhook timeout."

### ER Diagrams

Database design and data modeling:

- **Database Schema**: "Create an ER diagram for a social media platform — users, posts, comments, likes, follows"
- **Data Models**: "Diagram the data model for our inventory management system"
- **Entity Relationships**: "Create an ER diagram showing the relationships between customers, orders, products, and suppliers"

### Network Diagrams

IT infrastructure visualization:

- **Network Topology**: "Create a network diagram showing our office network — firewalls, switches, VLANs, wireless APs"
- **Security Zones**: "Diagram our network security zones — DMZ, internal, management, guest"
- **Cloud Networking**: "Create a network diagram for our multi-VPC AWS setup with peering and transit gateway"

### Gantt Charts & Timelines

Project planning and scheduling:

- **Project Timelines**: "Create a Gantt chart for our 6-month product launch — design, development, testing, marketing, launch"
- **Sprint Planning**: "Diagram our next 3 sprints with epics, stories, and dependencies"
- **Roadmaps**: "Create a product roadmap timeline for 2026 showing quarterly milestones"

### Swimlane Diagrams

Cross-functional process visualization:

- **Cross-Team Workflows**: "Create a swimlane diagram showing how a customer support ticket flows between Support, Engineering, and Product teams"
- **RACI Charts**: "Diagram our incident response process with swimlanes for each role"

### User Journey Maps

Customer experience visualization:

- **End-to-End Journeys**: "Create a user journey map for a customer discovering, evaluating, purchasing, and onboarding to our product"
- **Touchpoint Mapping**: "Map all customer touchpoints across email, web, app, and support"

---

## Output Formats

| Format | Features | Best For |
|--------|----------|----------|
| **Interactive HTML** | Zoom, pan, click, hover, responsive, shareable via URL | Presentations, team sharing, exploration |
| **PDF** | Print-ready, static, professional | Documentation, email attachments, printing |

CellCog defaults to interactive HTML — the whole point is diagrams you can explore, not static images. Request PDF explicitly when you need print-ready output.

---

## Chat Mode for Diagrams

| Scenario | Recommended Mode |
|----------|------------------|
| Individual diagrams — flowcharts, org charts, ER diagrams, mind maps | `"agent"` |
| Complex multi-diagram documentation, full system design docs with multiple views | `"agent team"` |

**Use `"agent"` for most diagrams.** Individual flowcharts, architecture diagrams, and org charts execute well in agent mode.

**Use `"agent team"` for comprehensive documentation** — when you need multiple interconnected diagrams that form a complete system design document.

---

## Example Prompts

**Quick flowchart:**
> "Create a flowchart for returning a product on our e-commerce site. Include: initiate return → reason selection → approval check → shipping label → refund processing → confirmation. Show the happy path and the rejection path."

**Architecture diagram:**
> "Diagram our production infrastructure:
> 
> Load Balancer → 3 API servers → PostgreSQL (primary + replica)
> API servers also talk to Redis cache and S3 for file storage
> Background workers pull from SQS queue
> Everything monitored by Datadog
> 
> Show it as a clean architecture diagram with arrows showing data flow direction."

**Mind map:**
> "Create a mind map for planning a product launch:
> 
> Center: Product Launch
> Branches: Marketing, Engineering, Sales, Support, Legal
> Each branch should have 4-6 specific tasks
> Color-code by priority: red = critical path, yellow = important, green = nice to have"

**Database ER diagram:**
> "Create an ER diagram for a project management tool:
> 
> Entities: User, Organization, Project, Task, Comment, Attachment, Label
> 
> Key relationships:
> - Users belong to Organizations (many-to-many)
> - Projects belong to Organizations
> - Tasks belong to Projects, assigned to Users
> - Comments belong to Tasks, created by Users
> - Tasks can have multiple Labels (many-to-many)
> 
> Show primary keys, foreign keys, and cardinality."

---

## Tips for Better Diagrams

1. **Describe the components and relationships**: "A connects to B which talks to C" is all CellCog needs. Don't worry about layout.

2. **Specify the diagram type**: "Flowchart", "sequence diagram", "ER diagram" — naming the type helps CellCog choose the right rendering approach.

3. **Include data flow direction**: For architecture diagrams, mention which way data flows. "Frontend → API → Database" is clearer than just listing components.

4. **Request interactivity**: "I want to zoom in" or "clickable components" tells CellCog to build an interactive experience.

5. **Color-coding helps**: "Color-code by team" or "green for success paths, red for error paths" makes diagrams immediately useful.

6. **Think about audience**: "For the engineering team" vs. "for the board presentation" changes the level of technical detail.

---

## If CellCog is not installed

Run `/cellcog-setup` (or `/cellcog:cellcog-setup` depending on your tool) to install and authenticate.
**OpenClaw users:** Run `clawhub install cellcog` instead.
**Manual setup:** `pip install -U cellcog` and set `CELLCOG_API_KEY`. See the **cellcog** skill for SDK reference.
