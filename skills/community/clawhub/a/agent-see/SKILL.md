---
name: agent-see
description: >
  Convert any website, SaaS product, or API into a live, discoverable, agent-executable
  integration. Use when the user asks to "convert a website", "turn this SaaS into a plugin",
  "create an agent bundle", "make my business agent-ready", "go live", "deploy the server",
  "publish discovery files", "connect to my database", "wire up real data", "set up maintenance",
  "re-sync the bundle", "package as a plugin", "verify the bundle", "generate launch artifacts",
  or provides a URL or OpenAPI spec to process. Also triggers proactively after any pipeline
  step completes to guide the user toward full go-live.
metadata:
  version: "0.2.0"
  repository: "https://github.com/Danielfoojunwei/Convert-any-SaaS-application-into-an-Agentic-interface"
  author: "Danielfoojunwei"
  license: "MIT"
---

# Agent-See: Full Pipeline Plugin

Convert any website, SaaS product, or API into a live, discoverable, agent-executable integration. This skill encodes the complete Agent-See workflow — from conversion through deployment, publication, backend connection, and ongoing maintenance.

**Operating principle**: Never stop at artifact generation. After every step, present the go-live status dashboard and proactively ask what's needed next. The conversion is the starting point, not the finish line.

## Pre-flight (All Commands)

Before running any agent-see command:

1. Check if `agent-see` is installed:
   ```bash
   agent-see --version 2>/dev/null
   ```
2. If not installed, auto-install from the repository:
   ```bash
   pip install git+https://github.com/Danielfoojunwei/Convert-any-SaaS-application-into-an-Agentic-interface.git --break-system-packages
   ```
3. If Python 3.11+ is not available, install via `uv`:
   ```bash
   uv python install 3.11
   uv venv --python 3.11 .venv
   source .venv/bin/activate
   uv pip install git+https://github.com/Danielfoojunwei/Convert-any-SaaS-application-into-an-Agentic-interface.git
   ```
4. For website/SaaS URL conversion, Playwright is required:
   ```bash
   playwright install chromium
   ```

---

# Part 1: Pipeline Skills

---

## Skill 1: Convert Source

Transform a website URL, SaaS product URL, or OpenAPI specification into a grounded agent bundle.

### Determine Source Type

| User provides | Source type | Example |
|---------------|------------|---------|
| A website URL | Website | `https://example.com` |
| A SaaS product URL | SaaS | `https://app.example.com` |
| A local file path ending in `.json`, `.yaml`, or `.yml` | OpenAPI spec | `./openapi.json` |

If the source type is ambiguous, ask the user to clarify.

### Run Conversion

Set the output directory. Default to `./agent-output` unless the user specifies otherwise.

```bash
agent-see convert <source> --output <output-dir> --verbose
```

### Post-Conversion Review

Read and summarize the key outputs:

1. **Read `agent_card.json`** — confirm identity and discovery metadata
2. **Read `AGENTS.md`** — verify the agent/operator guidance is accurate
3. **Read `openapi.yaml`** — check the API contract was captured correctly
4. **List `skills/`** — enumerate the business action wrappers generated
5. **Read `OPERATIONAL_READINESS.md`** — review execution boundaries

Present a structured summary:

- Number of skills/actions extracted
- Key workflows captured
- Any warnings about login, approval, or state-change boundaries
- Whether the bundle looks complete or needs re-running with adjusted scope

### Handling Failures

If conversion fails:

1. Read the error output carefully
2. Common issues:
   - **Network errors**: Check URL accessibility
   - **Missing Playwright**: Run `playwright install chromium`
   - **OpenAPI parse errors**: Validate the spec file format
3. Report the specific error and suggest remediation

### Proactive Next Steps — DO NOT SKIP

After conversion succeeds, immediately:

1. Run verification: `agent-see verify <output-dir>/proof/proof.json`
2. Present the go-live status dashboard showing what's done and what remains:

   | Step | Status | What's needed |
   |------|--------|--------------|
   | Conversion | ✅ Done | — |
   | Verification | ⏳ Running | — |
   | Launch layer | ❌ Not started | Business name, domain, contact info |
   | Runtime deployment | ❌ Not started | Hosting platform choice |
   | Discovery publishing | ❌ Not started | Website access |
   | Backend connection | ❌ Not started | Real API/database details |
   | Maintenance | ❌ Not started | Schedule preferences |

3. Ask: "Should we continue with generating the launch layer, or do you want to deploy the server first?"

### Conversion Output Artifacts Reference

**Core bundle files:**

| Artifact | Description |
|----------|-------------|
| `mcp_server/` | Callable tool surface for agents. Contains `server.py`, deployment configs (Dockerfile, docker-compose.yml, fly.toml, railway.json, render.yaml), and runtime metadata (route_map.json, tool_metadata.json, runtime_state.json). |
| `openapi.yaml` | Machine-readable API contract. All discovered endpoints, request/response schemas, auth requirements, rate limits. |
| `agent_card.json` | Identity and discovery metadata. Agent name, description, capabilities, supported protocols, trust signals. |
| `AGENTS.md` | Human and agent-readable guidance. What the integration does, how to use it, operational boundaries, caveats. |
| `OPERATIONAL_READINESS.md` | Execution boundaries. Auth requirements, state-changing operations, rate limits, known limitations. |
| `skills/*.md` | Individual business action wrappers (e.g., `list_products.md`, `add_to_cart.md`). |
| `skills/workflows/*.md` | Composite workflow files chaining multiple skills (e.g., `purchase_flow.md`). |
| `proof/` | Grounding evidence: screenshots, DOM snapshots, API response samples, cross-validation reports. |
| `capability_graph.json` | Structured graph of capabilities and their relationships. |

---

## Skill 2: Verify Bundle

Assess conversion quality across coverage, fidelity, and hallucination metrics.

### Run Verification

```bash
agent-see verify <output-dir>/proof/proof.json
```

### Interpret Results

| Metric | High | Medium | Low |
|--------|------|--------|-----|
| Coverage | >80% — most actions captured | 50-80% — significant gaps | <50% — re-run required |
| Fidelity | Faithfully represents source | Simplified/approximated | Significant deviations |
| Hallucination | None detected | Weak grounding evidence | Fabricated capabilities — must remove |

### Report to User

Present a structured summary:

1. Overall quality score
2. Coverage gaps — workflows not captured
3. Fidelity issues — imprecise extractions
4. Hallucination flags — fabricated capabilities (critical)
5. Recommendation — proceed or re-run

### Remediation

| Issue type | Action |
|-----------|--------|
| Low coverage | Re-run conversion with adjusted scope or better access |
| Low fidelity | Re-run with verbose mode |
| Hallucinations | Remove fabricated entries from skills/ and update agent_card.json |
| Missing proof | Re-run conversion to regenerate grounding evidence |

---

## Skill 3: Launch Artifacts

Generate the public discovery and trust layer from an existing grounded agent bundle.

### Pre-flight

Confirm a grounded agent bundle exists:
```bash
ls <output-dir>/agent_card.json
```

### Launch Intake

Check for or generate a launch intake file:

```bash
agent-see launch init ./launch-intake.json \
  --name "<business name>" \
  --domain "https://<domain>" \
  --business-type <type> \
  --summary "<description>" \
  --contact-email "<email>" \
  --support-url "https://<domain>/support" \
  --agent-see-output-dir <output-dir> \
  --verbose
```

Key fields to confirm with the user: business name and URL, public page locations, trust signals, contact information.

### Generate Launch Layer

```bash
agent-see launch sync ./launch-intake.json --verbose
```

### Run Truthfulness Check

```bash
agent-see launch check <launch-output> --bundle <output-dir>
```

### Post-Generation Review

Read and summarize:

| Artifact | What to check |
|----------|--------------|
| `launch/llms.txt` | Accurately describes public pages |
| `launch/agents.md` | Truthful agent access instructions |
| `launch/reference_layer/` | Supporting usage, limitation, trust, policy pages |
| `launch/launch_report.md` | Readiness warnings |
| `launch/surface_alignment.json` | Public claims match runtime capabilities |
| `launch/update_register.md` | Maintenance plan |

### Launch Artifacts Reference

| Artifact | Purpose |
|----------|---------|
| **llms.txt** | Model-facing guide at website root. Tells LLMs which pages are most important. Follows the `llms.txt` convention. |
| **agents.md** | Canonical "how to use this integration" document. Actions, connection details, boundaries, contacts. |
| **Reference layer** | Usage guide, limitations, trust signals, policy page. |
| **Launch report** | Internal readiness assessment. Checks artifacts generated, claims supported. |
| **Surface alignment JSON** | Machine-readable comparison: each claim tagged `aligned`, `partial`, or `misaligned`. |
| **Update register** | Maintenance plan: trigger conditions, commands, expected outputs. |

### Proactive Next Steps — DO NOT SKIP

After launch artifacts are generated, immediately:

1. Present the updated go-live status dashboard
2. Ask: "Launch layer is ready. These files need to be published on your website. Should we:"
   - "Deploy the MCP server first?" → trigger deploy-runtime
   - "Publish the discovery files now?" → trigger publish-discovery
   - "Connect to your real data first?" → trigger connect-backend

3. Recommend this order: deploy runtime → publish discovery (with real endpoint URL) → connect real data

---

## Skill 4: Package Plugin

Wrap a grounded agent bundle as a distributable plugin for a target harness.

### Pre-flight

Confirm bundle exists:
```bash
ls <output-dir>/agent_card.json
```

### Target Harness Selection

Default to **Claude workspace** format. Supported targets:

| Harness | Description | Artifact mix |
|---------|-------------|-------------|
| **Claude** | Claude workspaces / Cowork plugins | MCP runtime or OpenAPI, AGENTS guidance, plugin guide |
| **Manus** | Manus-style agents | MCP runtime, AGENTS guidance, skills, readiness outputs |
| **OpenClaw** | OpenClaw-like orchestrators | Runtime metadata, agent card, route map, connector guide |
| **Generic** | Any other agent system | OpenAPI, AGENTS guidance, plugin manifest, starter kit |

### Run Plugin Packaging

```bash
agent-see plugin sync <output-dir> --launch-output <launch-output> --verbose
```

### Post-Packaging Review

| Artifact | Purpose |
|----------|---------|
| `plugins/plugin_manifest.json` | Machine-readable inventory of the grounded bundle |
| `plugins/PLUGIN_GUIDE.md` | Step-by-step usage for target harness |
| `plugins/connectors/` | Harness-specific connection guides (claude_workspace.md, manus.md, openclaw.md, generic.md) |
| `plugins/starter_kit/` | Templates: plugin_template.md, skill_template.md, connector_template.md |

### Harness-Specific Packaging Reference

**Claude Workspaces / Cowork:**
```
plugin-name/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── skill-name/
│       └── SKILL.md
├── .mcp.json          (if runtime endpoint exists)
└── README.md
```

MCP integration in `.mcp.json`:
```json
{
  "mcpServers": {
    "agent-see-runtime": {
      "command": "python",
      "args": ["${CLAUDE_PLUGIN_ROOT}/mcp_server/server.py"],
      "env": { "API_BASE_URL": "${API_BASE_URL}" }
    }
  }
}
```

**Manus-style agents:** MCP endpoint URL + tool_metadata.json + skills + AGENTS.md

**OpenClaw-like orchestrators:** agent_card.json registered with discovery service + route_map.json + capability_graph.json + thin protocol connector

**Generic harnesses:** OpenAPI spec + AGENTS.md guidance + plugin manifest + starter kit templates

---

# Part 2: Go-Live Skills

---

## Skill 5: Go Live (Master Orchestrator)

Proactive end-to-end orchestrator that guides a business owner from a completed conversion all the way to a live, discoverable, agent-executable integration.

### Operating Principle

The conversion is the starting point, not the finish line. A converted business needs to become easy for agents and LLMs to **retrieve**, **understand**, **trust**, and **act on**. This means operating two layers simultaneously: the human-facing website and the machine-facing agent integration surface.

### Step 0: Assess Current State

Read the bundle directory and present a status dashboard:

| Step | Status | What's needed |
|------|--------|--------------|
| Conversion | ✅/❌ | Source URL or OpenAPI spec |
| Verification | ✅/❌ | Run agent-see verify |
| Launch layer | ✅/❌ | Business name, domain, contact info |
| Runtime deployment | ✅/❌ | Hosting platform choice |
| Discovery publishing | ✅/❌ | Website access or hosting details |
| Backend connection | ✅/❌ | Real database/API credentials |
| Structured data | ✅/❌ | Website template access |
| Maintenance loop | ✅/❌ | Schedule preferences |

Ask: "Which of these do you want to tackle next, or should we go through them in order?"

### Step 1: Confirm Canonical Task URLs

For each extracted capability, suggest a corresponding URL:

| Capability | Suggested URL | User intent it answers |
|-----------|--------------|----------------------|
| list_products | `/products` or `/menu` | "What do you sell?" |
| get_product_details | `/products/{slug}` | "Tell me about this item" |
| add_to_cart | `/cart` | "I want to buy this" |
| submit_checkout | `/checkout` | "I'm ready to pay" |
| get_order_status | `/orders/{id}` | "Where's my order?" |

Ask: "Do these URLs exist on your site? Which ones need to be created or updated?"

### Step 2: Page Rewriting Guidance

For each canonical URL, the top of the page must immediately answer: who the offer is for, what action can be completed, what inputs are required, what constraints exist, and what the next step is.

Ask: "Do you want help rewriting any of these pages? I can generate answer-first content based on your converted capabilities."

### Step 3: Deploy the Runtime

Trigger **Skill 6: Deploy Runtime**. Ask:

- "Where do you want to host the MCP server? Docker, Fly.io, Railway, or Render?"
- "Do you have an account on any of these platforms?"
- "What's the base URL of your actual API?"

### Step 4: Publish Discovery Files

Trigger **Skill 8: Publish Discovery**. Ask:

- "Do you have access to upload files to your website root?"
- "What's your website's domain?"
- "Do you use a CMS (WordPress, Shopify, etc.) or static hosting?"

### Step 5: Create the Agent Integration Page

Help the user create a public `/agents` page from `launch-output/agents.md`. Ask:

- "Do you want this as a standalone page or part of your existing docs?"
- "Should it link to the live MCP endpoint or the OpenAPI spec?"

### Step 6: Add Structured Data

Generate JSON-LD snippets based on business type:
- `Organization` for the homepage
- `Product` for product pages
- `FAQPage` for FAQ
- `BreadcrumbList` for navigation

### Step 7: Establish Identity and Trust

Ask about Search Console verification, Google Business Profile, and contact detail consistency across web properties.

### Step 8: Connect to Real Data

Trigger **Skill 7: Connect Backend**. Ask:

- "What database or API serves your real product/order data?"
- "What authentication does your backend use?"
- "Do you have a staging environment?"

### Step 9: Set Up Maintenance

Trigger **Skill 9: Maintain**. Ask:

- "How often does your menu/catalog change?"
- "Do you want automatic re-sync reminders?"

### Step 10: Final Verification

1. Verify MCP server health endpoint responds
2. Confirm llms.txt is publicly accessible
3. Confirm /agents page is live
4. Run `agent-see launch check` for surface alignment
5. Test each capability end-to-end if possible

Present a final go-live report.

### Proactive Chaining Rule

After ANY skill completes (convert, verify, launch, package), immediately present this status dashboard and offer to continue with the next incomplete step. Do not stop at artifact generation.

---

## Skill 6: Deploy Runtime

Deploy the generated MCP server so agents can call it over the network.

### Pre-flight

Confirm `mcp_server/server.py` exists in the bundle output.

### Gather Required Configuration

Ask the user for every required setting before deploying.

**Mandatory:**

| Setting | Environment variable | What to ask |
|---------|---------------------|-------------|
| Target API URL | `TARGET_URL` | "What's the base URL of your real API that this server should proxy to?" |
| Port | `PORT` | Default 8000 unless specified |

**Authentication (ask which applies):**

| Method | Variables | What to ask |
|--------|-----------|-------------|
| Bearer token | `AUTH_TOKEN` | "Does your API use a bearer token?" |
| Custom header | `AUTH_HEADER_NAME`, `AUTH_HEADER_VALUE` | "Custom auth header name and value?" |
| None | — | "Is the API publicly accessible?" |

**Operational limits:**

| Setting | Variable | Default |
|---------|----------|---------|
| Request timeout | `REQUEST_TIMEOUT_MS` | 30000 |
| Max retries | `MAX_RETRIES` | 3 |
| Session TTL | `SESSION_TTL_SECONDS` | 3600 |
| Max sessions | `MAX_SESSIONS` | 100 |

### Platform Deployment

**Docker (Local or VPS):**
```bash
cd <output-dir>/mcp_server
cp .env.example .env
# User fills in .env values
docker-compose up -d
```

**Fly.io:**
```bash
cd <output-dir>/mcp_server
fly launch --no-deploy
fly secrets set TARGET_URL=<value> AUTH_TOKEN=<value>
fly deploy
```

**Railway:**
```bash
cd <output-dir>/mcp_server
railway init
railway up
```

**Render:** Push `mcp_server/` to a Git repo and connect via Render dashboard.

### Post-Deployment Verification

1. **Health**: `curl <deployed-url>/health`
2. **Tools**: `curl <deployed-url>/tools`
3. **Test read-only tool**: Call `list_products` and verify real data
4. **Check logs**: Confirm no errors

### Security Checklist

- [ ] TARGET_URL points to correct backend
- [ ] Auth credentials set as secrets, not in code
- [ ] HTTPS enabled
- [ ] Health endpoint responds
- [ ] Rate limits configured
- [ ] Session TTL prevents unbounded memory growth

### Record the Endpoint

After deployment, record the live URL. Ask: "Deployment is live at `<url>`. Should we continue with publishing discovery files?"

### Production Readiness Checklist

**Configuration:**
- [ ] `TARGET_URL` set and correct
- [ ] Auth credentials as environment secrets
- [ ] Request timeout configured (`REQUEST_TIMEOUT_MS`)
- [ ] Max retries with backoff (`MAX_RETRIES`)
- [ ] Session TTL (`SESSION_TTL_SECONDS`)
- [ ] Max concurrent sessions bounded (`MAX_SESSIONS`)

**Runtime Safety:**
- [ ] Health endpoint at `/health`
- [ ] Readiness endpoint confirms backend connectivity
- [ ] HTTPS enabled
- [ ] No hardcoded credentials
- [ ] Docker runs as non-root user (if Docker)

**Execution Resilience:**
- [ ] Retry policies with exponential backoff
- [ ] Request timeouts prevent hanging
- [ ] Error responses follow typed format (NOT_FOUND, AUTH_FAILED, RATE_LIMITED, etc.)

**Session Management:**
- [ ] TTL expires inactive sessions
- [ ] Max count prevents memory exhaustion
- [ ] Cleanup runs on schedule or LRU eviction

**Approval Governance:**
- [ ] State-changing operations require confirmation
- [ ] Payment operations require human approval
- [ ] Destructive operations blocked by default

**Known Limitations:**
- Browser automation is fragile — scope conservatively
- Best against SaaS with stable APIs
- In-memory session state lost on restart — use external storage for production
- Generated servers are "validated operational prototypes" — review before production hardening

---

## Skill 7: Connect Backend

Wire the generated MCP server to real data sources.

### Pre-flight

Read `route_map.json` and `tool_metadata.json` to understand what endpoints exist.

### Identify the Data Source

Ask the user:

1. "Where does your real product/service data live?"
   - Existing REST API (most common for SaaS)
   - Database (PostgreSQL, MySQL, MongoDB, etc.)
   - E-commerce platform (Shopify, WooCommerce, Stripe, Square)
   - Spreadsheet or static file
   - Multiple sources

2. "Is there API documentation or an OpenAPI spec for your backend?"

3. "What authentication does your backend require?"
   - API key / OAuth2 / Basic auth / Session / None

4. "Do you have a staging/test environment, or should we work against production?"

### Connection Strategy by Data Source

**Existing REST API:**

1. Update `TARGET_URL` to point to the real API
2. Map each MCP tool to corresponding real endpoint:

   | MCP Tool | Generated route | Real API endpoint |
   |----------|----------------|------------------|
   | list_products | POST /tools/list_products | GET /api/products |
   | add_to_cart | POST /tools/add_to_cart | POST /api/cart/items |

3. Adjust request/response transformations if schemas differ
4. Set authentication headers

**Database Direct:**

1. Add database connection layer to `server.py`
2. Get connection details (host, port, db name, credentials as env vars)
3. Write query functions per tool
4. Add connection pooling and error handling

**E-commerce Platform (Shopify, WooCommerce, Square):**

1. Get platform API credentials
2. Update MCP server to use platform API
3. Map generated tool schema to platform endpoints
4. Handle platform-specific pagination, rate limits, auth

**Spreadsheet or Static File:**

1. Load data into MCP server as in-memory store
2. Implement read operations against loaded data
3. For writes, set up SQLite or notification system

### Tool-by-Tool Wiring

For each capability:

1. Read the generated skill file — understand expected inputs/outputs
2. Identify the real data source
3. Map the schema — align generated parameter names with real field names
4. Handle authentication
5. Test the connection
6. Update server.py

### Testing Protocol

1. **Read-only tools first**: list_products, get_product_details
2. **State-reading tools**: get_cart, get_order_status
3. **State-changing tools last**: add_to_cart — staging only
4. **Never test checkout against production** without explicit approval

After all tools connected, run the complete workflow end-to-end.

---

## Skill 8: Publish Discovery

Place generated discovery and trust files on the business's actual web surface.

### Gather Website Details

Ask before proceeding:

1. "What is your website's domain?"
2. "How do you manage your website?" (Static hosting / CMS / Custom server)
3. "Do you have access to upload files to the website root?"
4. "Do you already have a `robots.txt` and `sitemap.xml`?"

### File-by-File Publication Guide

**1. robots.txt**

Ask: "Do you want AI search crawlers to find your site?"

```text
User-agent: *
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Applebot
Allow: /

Sitemap: https://<domain>/sitemap.xml
```

Ask: "Allow AI training crawlers too, or only search/user-directed access?"

**2. sitemap.xml**

Generate XML sitemap with all canonical task URLs and accurate `lastmod` dates.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://<domain>/</loc>
    <lastmod>YYYY-MM-DD</lastmod>
    <changefreq>weekly</changefreq>
  </url>
</urlset>
```

**3. llms.txt**

Update the generated `llms.txt` with actual deployed runtime endpoint and real domain URLs. Place at `https://<domain>/llms.txt`.

**4. /agents Page**

Customize `launch-output/agents.md` with real endpoint URLs. Ask: "HTML page, markdown, or CMS-pasteable content?"

**5. Reference Layer Pages**

coverage.md, limitations.md, pricing_eligibility.md, support_escalation.md, change_policy.md

Ask: "Separate pages or combined into one reference page?"

**6. Structured Data (JSON-LD)**

Generate snippets based on business type:

**Homepage — Organization:**
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "<business name>",
  "url": "https://<domain>",
  "logo": "https://<domain>/logo.png",
  "contactPoint": {
    "@type": "ContactPoint",
    "email": "<support email>",
    "contactType": "customer service"
  }
}
```

**Product pages — Product:**
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "<name>",
  "description": "<description>",
  "offers": {
    "@type": "Offer",
    "price": "<price>",
    "priceCurrency": "<currency>",
    "availability": "https://schema.org/InStock"
  }
}
```

**7. IndexNow Setup**

Ask: "Want search engines notified automatically when content changes?" If yes, generate key file and provide submission URL format.

### Platform-Specific Instructions

| Platform | How to publish |
|----------|---------------|
| **Netlify/Vercel** | Add files to `public/` or `static/`, deploy normally |
| **WordPress** | File manager plugin or FTP for root files; WP admin for pages; structured data via plugin |
| **Shopify** | Theme editor for JSON-LD in theme.liquid; pages for /agents content |
| **Custom server** | Place in static/public directory; add routes for /agents and reference pages |

### Verification

```bash
curl -I https://<domain>/robots.txt
curl -I https://<domain>/sitemap.xml
curl -I https://<domain>/llms.txt
curl -I https://<domain>/agents
```

---

## Skill 9: Maintain

Keep the agent-facing surface aligned with the real business.

### Determine What Changed

Ask: "What changed in your business?"

| Change type | What needs refreshing |
|------------|----------------------|
| Products/menu added or removed | Re-run conversion, update sitemap, product pages, IndexNow |
| Prices changed | Update product pages, schema markup, sitemap lastmod, IndexNow |
| Policies changed | Update policy pages, reference layer, sitemap lastmod |
| Workflows changed | Re-run conversion, redeploy runtime, update /agents page |
| Auth or access changed | Re-run conversion, update MCP server config, update /agents page |
| Contact/support info changed | Update Organization markup, Business Profile, support pages |
| New capability added | Re-run conversion, refresh all downstream layers |
| Branding or domain change | Update all URLs in llms.txt, sitemap, agents page, structured data |

### Re-sync Protocol (Follow This Order)

**1. Re-run Conversion (if business logic changed):**
```bash
agent-see convert <source> --output <output-dir> --verbose
agent-see verify <output-dir>/proof/proof.json
```

**2. Refresh Launch Layer:**
```bash
agent-see launch sync <launch-intake.json> --bundle <output-dir> --output <launch-output>
agent-see launch check <launch-output> --bundle <output-dir>
```

**3. Refresh Plugin Layer:**
```bash
agent-see plugin sync <output-dir> --launch-output <launch-output>
```

**4. Redeploy Runtime** (if server code changed)

**5. Update Published Discovery Files:**
- sitemap.xml with new/changed URLs and accurate lastmod
- llms.txt if pages or capabilities changed
- /agents page if capabilities or connection details changed
- JSON-LD structured data if product/pricing data changed
- Submit changed URLs via IndexNow

**6. Verify Alignment:**
1. Check MCP server health
2. Confirm llms.txt is current
3. Confirm /agents page reflects actual capabilities
4. Run `agent-see launch check`

### Maintenance Cadences

| Cadence | What to review |
|---------|---------------|
| **Weekly** | Broken links, stale prices, runtime uptime, support details, primary CTAs |
| **Monthly** | Search Console signals, sitemap freshness, robots.txt, schema validity |
| **After every material change** | Re-run Agent-See, redeploy runtime, update discovery files, IndexNow |
| **Quarterly** | Reassess customer prompts, add task pages, review competitor gaps, expand reference pages |

### Drift Detection

Signs the agent surface has drifted:
- Agents returning products that no longer exist
- Prices in structured data don't match website
- /agents page lists removed capabilities
- Launch alignment check reports failures
- Customer complaints about incorrect agent behavior

If drift detected, run the full re-sync protocol immediately.

---

# Part 3: Reference Material

---

## Agentic Search Playbook

### The Four Decisions

A business becomes strong in the prompt economy when it wins four decisions inside a model pipeline: whether the business is **retrieved**, whether it is **selected**, whether it is **trusted**, and whether it can be **executed** immediately.

| Layer | Goal | Business owner must do | Agent-See provides |
|-------|------|----------------------|-------------------|
| Discovery | Get retrieved | Publish crawlable, text-rich, task-shaped pages and discovery files | Runtime artifacts and machine-usable operational surface |
| Selection | Get recommended | Make use cases, fit, constraints, pricing, policies explicit | Structured description of actions and workflows |
| Trust | Get cited as safe | Maintain entity data, support info, policy pages, visible consistency | Clear workflow boundaries, auth notes, approval-sensitive actions |
| Execution | Let agents act | Deploy the runtime and expose clear connection guidance | MCP/OpenAPI/runtime outputs and harness-facing artifacts |
| Maintenance | Stay fresh | Update pages, feeds, schema, sitemaps, re-run conversion | Regeneration path for the executable surface |

### 10-Step Operational Sequence

1. **Choose canonical task URLs** — Every core commercial action gets a dedicated URL
2. **Rewrite pages as answer-first** — Title states the task, opening paragraph states audience + action + next step
3. **Publish discovery files** — robots.txt, sitemap.xml (with accurate lastmod), llms.txt, markdown mirrors
4. **Add structured data** — JSON-LD for Organization, Product, FAQPage, BreadcrumbList
5. **Establish identity** — Search Console, Business Profile, consistent contact details
6. **Make offers comparable** — Visible pricing, variants, availability, shipping, returns, warranties
7. **Publish agent integration page** — /agents page connecting discovery to execution
8. **Push updates fast** — IndexNow, sitemap refresh, re-run Agent-See on business logic changes
9. **Build reference layer** — Coverage, limitations, pricing/eligibility, policies, examples, support
10. **Maintain continuously** — Weekly, monthly, quarterly, and on-change review cadences

### Answer-First Page Format

Every high-value page must immediately answer: who the offer is for, what action can be completed, what inputs are required, what constraints exist, and what the next step is.

### Discovery File Placement

| File | Location | Purpose |
|------|----------|---------|
| robots.txt | Website root | Control crawler access intentionally |
| sitemap.xml | Website root | Complete URL inventory with accurate lastmod |
| llms.txt | Website root | Curated guide for models to find highest-value pages |
| /agents page | Public docs or site | Connection instructions for agents |

### Structured Data Priority

| Page type | Schema type | Why |
|-----------|------------|-----|
| Homepage | Organization | Official identity, logo, contacts |
| Product pages | Product | Price, availability, ratings, shipping |
| FAQ | FAQPage | Direct answers to recurring objections |
| Navigation | BreadcrumbList | Page hierarchy and topical relationships |

### Key Principle

Do not invent capabilities in the launch or plugin layer. Extract the real business surface first, then wrap it with thin public guidance and thin harness-specific packaging.
