---
name: coware
description: >
  Coware Living Specs — shared API spec sync for multi-agent coding teams.
  TRIGGER when: project has .coware/ directory, user mentions shared specs,
  API alignment, merge conflicts, interface sync, team coordination,
  vibe coding collaboration, or multi-dev AI coding workflow.
  DO NOT TRIGGER when: single-dev project with no .coware/ directory and
  user has not mentioned team collaboration.
---

# Coware — Shared Living Specs

Coware keeps AI agents aligned by syncing shared interface specs across your team.
Every agent reads the same spec before writing code — no more merge conflicts
from mismatched APIs, field names, or return types.

## FIRST: Check initialization status

Check if `.coware/config.json` exists in the project root.

---

## IF `.coware/config.json` EXISTS → Project is initialized

This project already uses Coware. Follow this workflow:

### Before coding

1. Run: `node .coware/pull.mjs`
   - This fetches the latest specs from the Coware server.
   - If the command fails (network error, server down), proceed with whatever
     local `.coware/specs/*.md` files exist.
2. Read ALL `.md` files in `.coware/specs/`.
   - These specs are the **source of truth** for all interfaces, types,
     API contracts, and data shapes in this project.
3. You are ready to code. Follow the specs exactly.

### While coding

- **Follow specs exactly.** Match field names, types, return formats, status codes.
- **If a spec needs to change** (new endpoint, renamed field, etc.):
  1. Update the relevant `.coware/specs/<slug>.md` file FIRST.
  2. THEN update the code to match.
  3. Never let code drift from specs.

### After coding

1. If you created or modified any spec files, run: `node .coware/sync.mjs`
   - This pushes updated specs to the server so teammates get them.
   - If sync fails, the local spec files are still the source of truth.
2. If you did NOT change any specs, no action needed.

---

## IF `.coware/config.json` DOES NOT EXIST → New project setup

This project has not been initialized with Coware yet.

### Setup instructions

1. Fetch the setup guide: `https://coware.team/llms.txt`
2. Read the response carefully.
3. Follow ALL instructions in the guide from start to finish, in order.
   - The guide will walk you through: login, project creation/joining,
     file setup, and spec generation.
   - Execute ALL steps in ONE go. Do NOT stop to ask the user questions mid-flow.
   - The ONLY acceptable way to ask the user something is via a tool-based
     selection dialog. NEVER stop your turn to ask via text.
4. After setup completes, follow the "Project is initialized" workflow above.

---

## Spec file format

Each spec file in `.coware/specs/` is a Markdown file:

```markdown
# Module Name

## Endpoints

### GET /api/resource
- Response: `{ data: Resource[], total: number }`
- Auth: Bearer token required

## Types

### Resource
- id: string (UUID)
- name: string
- createdAt: string (ISO 8601)
```

When generating or updating specs, follow this structure:
- One file per module/domain (e.g., `auth.md`, `users.md`, `orders.md`)
- Include endpoints with method, path, request/response shapes
- Include shared types and enums
- Include auth requirements and error formats
- Use consistent naming conventions throughout all specs

## Inviting teammates

After setup, share the invite code (found in `.coware/config.json` → `invite` field)
with teammates. They install this skill and run `/coware` — their agent will
automatically join the project and pull shared specs.

## Troubleshooting

- **pull.mjs fails**: Proceed with local `.coware/specs/*.md` files.
- **sync.mjs fails**: Local specs are still source of truth. Retry later.
- **No specs exist**: Scan the codebase and generate specs, then sync.
- **Specs conflict with code**: Specs win. Update code to match specs,
  or update specs first if the change is intentional.
