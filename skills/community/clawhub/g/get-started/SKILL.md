---
name: get-started
description: Connect to Flow Relay, inspect accessible workspaces and projects, set the active project and choose the first workflow. Use right after installing the plugin or when no active project is selected.
---

# Get started with Flow Relay

Explicit user instructions always take priority over these defaults.

## Input
- Optional project name, key or ID if the user already named one.

## Workflow
1. Call `get_workspace_context` and `list_projects` to inspect the user's accessible personal and organization projects and see whether an active project is already set.
2. If Flow Relay tools are unavailable or authentication fails, stop and tell the user to connect Flow Relay via OAuth in the plugin settings and retry.
3. If no active project is set:
   - If the user named a project and it matches uniquely, call `set_active_project`.
   - If there is only one accessible project, suggest setting it active and ask before mutating session state if the user did not ask to switch.
   - Otherwise list the accessible projects (name, scope, role and key) and ask which one to activate.
4. Once an active project is selected, briefly offer three concrete next steps:
   - Read the latest handoff (`list_handoffs`) or ask a cited question (`ask_project`).
   - Review open work items (`list_work_items`) and top RAID risks (`list_raid`).
   - Check the simulated finish forecast (`get_forecast`).

## Guardrails
- Never invent project IDs, names, dates or roles.
- Note that OAuth consent scopes (`mcp:read`, `mcp:ai`, `mcp:write`) govern which actions are permitted; if a tool returns an insufficient-scope error, tell the user which permission is needed without retrying blindly.
