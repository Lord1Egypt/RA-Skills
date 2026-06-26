# Teams Page UI Structure

## Purpose

The Teams page organizes agents into named groups and optional parent/child hierarchies.

Primary goals:
- make agent teams easy to create and edit
- keep hierarchy readable at a glance
- avoid coupling team management to general config editing

## Layout

Use a two-column layout.

### Left column: Team tree

Show the team list as a hierarchy.

Recommended rendering:
- top-level teams first
- child teams directly under their parent
- indent children slightly
- show a collapse/expand toggle on teams with children
- keep card styling consistent with the rest of Control UI

### Right column: Team editor

Show editor fields for the selected team.

Recommended fields:
- **Name**
- **Description**
- **Parent Team** dropdown
- **Agents** checklist
- **Save** button
- **Delete Team** button when editing an existing team

## Behavior

### Tree behavior

- root teams render in alphabetical order
- children render under the parent in alphabetical order
- collapse state is UI-only and should not affect registry data
- collapsed parent rows still remain selectable

### Parent selection behavior

Parent dropdown should:
- allow `No parent team`
- exclude the team itself
- exclude descendants of the selected team
- visually hint hierarchy depth for candidate parent teams

### Save behavior

Saving must preserve:
- `name`
- `description`
- `parentId`
- `agentIds`

If `parentId` disappears after save, inspect both:
- the registry file on disk
- the compiled runtime bundle serving the teams RPCs

## Data flow

```text
Teams UI
  -> controller load/save/select
  -> gateway RPC (teams.*)
  -> team registry JSON
```

## File map

### Backend

- `src/gateway/team-registry.ts`
  - registry path
  - normalization
  - load/save helpers
  - cleanup helpers

- `src/gateway/server-methods/teams.ts`
  - CRUD handlers
  - parent validation
  - cycle prevention
  - child unnesting on delete

### UI

- `ui/src/ui/types.ts`
  - `TeamRecord`
  - `TeamsListResult`

- `ui/src/ui/app.ts`
  - state fields for teams UI

- `ui/src/ui/app-view-state.ts`
  - shared view state typing

- `ui/src/ui/controllers/teams.ts`
  - load/select editor sync

- `ui/src/ui/views/teams.ts`
  - tree renderer
  - editor layout
  - collapse toggle UX

- `ui/src/ui/navigation.ts`
  - Teams tab registration

- `ui/src/i18n/locales/en.ts`
  - tab label and subtitle

- `ui/src/ui/app-render.ts`
  - page render wiring and handlers

- `ui/src/ui/app-settings.ts`
  - initial load when Teams tab opens

## Styling notes

For dropdowns in dark UI:
- explicitly style `select`
- explicitly style `option`
- set dark-compatible foreground/background colors
- use `color-scheme: dark` when needed

## Quality bar

A good Teams page should feel:
- simple
- obvious
- fast to scan
- safe to edit
- hard to break with invalid nesting
