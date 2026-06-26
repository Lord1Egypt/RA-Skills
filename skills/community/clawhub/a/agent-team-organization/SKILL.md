---
name: agent-team-organization
description: "Create and maintain a Teams management page for OpenClaw Control UI, including named agent teams, parent/child nesting, indented tree rendering, collapsible team groups, parent selectors, and file-backed team registry persistence. Use when building, extending, fixing, or documenting the OpenClaw Teams page, team hierarchy UX, or gateway/UI plumbing for team organization features."
---

# Agent Team Organization

Build and maintain the OpenClaw **Teams** page as a lightweight team registry plus Control UI tree view.

## Scope

Use this skill for:
- adding or editing the **Teams** tab in Control UI
- implementing **named agent teams** backed by a file registry
- supporting **parent/child team nesting**
- rendering the team list as an **indented collapsible tree**
- fixing team save/load issues between UI and gateway
- documenting the UI structure and file map for the Teams feature

## Core design

Keep the feature simple:
- Store teams in a dedicated JSON registry instead of `agents.list`
- Reference agents by `agentIds[]`
- Support optional `parentId` for hierarchy
- Keep team CRUD isolated from broader config editing
- Make the UI readable first: tree list on the left, team editor on the right

## Data model

Use this shape for each team:

```ts
type TeamRecord = {
  id: string;
  name: string;
  description?: string;
  parentId?: string;
  agentIds: string[];
  createdAt: string;
  updatedAt: string;
};
```

Registry file:

```text
~/.openclaw/workspace/teams/teams.json
```

## UI pattern

Default page layout:
- **Left column:** team tree
- **Right column:** selected team editor

Expected behavior:
- top-level teams render normally
- child teams render **under the parent** with slight indentation
- parent rows expose a **collapse/expand toggle**
- selecting a team loads its editor state on the right
- parent selector supports **nesting** and **unnesting**
- prevent invalid nesting:
  - no self-parenting
  - no cycles
  - no nesting under descendants

## Gateway pattern

Expose dedicated methods:
- `teams.list`
- `teams.get`
- `teams.create`
- `teams.update`
- `teams.delete`

Keep validation inside the teams handler:
- team names unique, case-insensitive
- `agentIds` must exist in current agent list
- `parentId` must exist when set
- deleting a parent should unnest children rather than orphaning broken references
- deleting an agent should remove that agent from all teams

## Implementation checklist

1. Add/update `src/gateway/team-registry.ts`
2. Add/update `src/gateway/server-methods/teams.ts`
3. Register methods in gateway method lists/scopes
4. Add UI types for `TeamRecord` / `TeamsListResult`
5. Add teams state to `app.ts` and `app-view-state.ts`
6. Add teams controller for load/select behavior
7. Add `views/teams.ts` renderer
8. Add navigation/i18n wiring for the Teams tab
9. Build the UI after changes
10. If save behavior is wrong, verify the **live runtime bundle** is actually carrying the new handler logic

## Debugging rule

If the UI seems correct but saved team hierarchy disappears after clicking **Save**:
1. inspect `~/.openclaw/workspace/teams/teams.json`
2. confirm whether `parentId` is written to disk
3. inspect the compiled gateway/runtime bundle, not just source files
4. restart the gateway after updating runtime artifacts

## References

For the page structure and file map, read:
- `references/ui-structure.md`

For live gateway/runtime mismatches where the UI looks right but `parentId` or other team fields disappear on save, read:
- `references/runtime-troubleshooting.md`
