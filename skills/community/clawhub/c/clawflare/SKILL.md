---
name: clawflare
version: 0.1.0
description: Publish web content to Cloudflare Pages. Supports account/project selection, new project creation, and deploying HTML or static asset directories. Primary auth via Cloudflare API Token.
tags: [cloudflare, pages, deploy, publish, hosting, static-site]
author: Relevant Ads / OpenClaw community
license: MIT
---

# ClawFlare Publisher Skill

**What this skill does:**
Turn natural language requests like "Publish a new landing page for the emergency plumbing promo" or "Deploy the generated site to my client project" into live Cloudflare Pages deployments — reliably and with good agent UX.

It handles the boring but important parts (auth, project selection/clarification, manifest creation, deployment, URL extraction) so you (the agent) can focus on the content and user intent.

**When to use this skill:**
- User wants to publish HTML, a landing page, marketing site, documentation, or any static web content to production.
- You have generated or received content that should go live on a `.pages.dev` (or custom) domain.
- You need to create a new project/subdomain or update an existing one.

**Do NOT use for:**
- Dynamic server-side logic (Workers / Functions) — use dedicated skills instead.
- Large/complex builds that require custom build steps (for MVP we keep it simple).

## Core Principles (Follow These Strictly)

1. **Always clarify before publishing** — Never guess the target project or account. Ask the user (or use context) about:
   - Which Cloudflare account (if they have multiple)
   - New project name or existing one?
   - Branch (main/production vs feature branch for preview)
   - Any custom subdomain notes?

2. **Be reliable and deterministic** — Use the provided Python tools. Do not try to construct raw API calls yourself unless the tools fail.

3. **Return clean, structured results** — Always surface the live URL prominently. Include deployment ID and status when available.

4. **Progress & transparency** — Tell the user what you're doing: "Listing your projects...", "Creating new project 'plumbing-promo-2026'...", "Uploading 12 files via Wrangler...", "Deployment live at https://..."

5. **Safety** — For production projects, consider a quick confirmation ("This will update the live site at example.pages.dev — proceed?") unless the user has previously said it's fine.

## Available Tools

You have access to these tools (call them via the normal function/tool mechanism):

### 1. `cf_auth_setup` / `cf_validate_token`
- Purpose: Set up or validate the Cloudflare API token.
- The user should provide a token with `Pages:Write` (or equivalent account Pages Edit) permission.
- The skill securely stores it for the workspace/session.

### 2. `cf_list_accounts`
- Lists Cloudflare accounts the current token can access.
- Returns structured list with IDs and names.
- Use this when the user has multiple accounts or you're unsure which one to target.

### 3. `cf_list_projects`
- Lists existing Pages projects for the selected account.
- Shows name, current subdomain, last deployment URL, etc.
- Great for helping the user choose an existing target.

### 4. `cf_create_project`
- Creates a new Pages project.
- Parameters: `name`, `production_branch` (default "main"), optional description.
- Returns the new project details + its auto-generated `.pages.dev` subdomain.

### 5. `cf_publish`
- **The main publishing tool.**
- Accepts either:
  - `html_content`: A string of HTML (will be deployed as `/index.html`)
  - `source_dir`: Path to a local directory containing pre-built static assets
- Other params: `project_name` (or "new:desired-name"), `branch`, `account_id` (optional if only one account)
- Behavior:
  - If Wrangler is available in the environment → uses `wrangler pages deploy` (most robust for directories).
  - Falls back to direct API upload for simple single-file HTML cases.
- Always returns a clean result object with `url`, `deployment_id`, `success`, etc.

### 6. `cf_get_deployment_status`
- Check status of a recent deployment by ID or project+branch.

## Example Agent Workflows

**Simple HTML publish (most common):**
User: "Publish this landing page for the new water heater promo"
You: 
1. Call `cf_list_projects` (or ask which project / new name)
2. Clarify if needed: "Publish to existing 'client-sites' project or create new 'water-heater-promo'?"
3. Once confirmed, call `cf_publish` with the HTML content + target project/branch
4. Present the live URL: "✅ Live at https://water-heater-promo.pages.dev"

**Directory / generated site:**
After a Content Factory sub-agent produces a folder of assets:
You: "I have a generated static site in /tmp/generated-site-123. Ready to publish?"
→ Call `cf_publish` with `source_dir=/tmp/generated-site-123` + chosen project.

**New project flow:**
"Create a new project called 'demo-landing' and publish this hero section..."
→ Use `cf_create_project` then `cf_publish`.

## Error Handling & Helpful Responses

- Project name taken → "That name is taken. Options: use 'water-heater-promo-2', deploy to existing 'marketing' project, or pick another name?"
- Token invalid / insufficient permissions → Clear message + guidance on creating a Pages-scoped token.
- Upload fails → Retry with exponential backoff in the tool; surface useful error to user.

## Security Notes

- Tokens are stored via OpenClaw's secure mechanisms (never in prompts or logs).
- Only request the minimum scopes needed (Pages Write/Edit).
- For sensitive/production publishes, the skill can surface a confirmation step.

## Future Enhancements (Not in MVP)

- OAuth / PKCE support for public or multi-user scenarios
- Custom domain attachment
- Pages Functions deployment
- Rich template / "vibe-based" site generation + publish in one flow
- MCP server exposure

**This skill makes publishing a reliable, first-class capability instead of an ad-hoc API dance.** Use it whenever content needs to go live on Cloudflare Pages.