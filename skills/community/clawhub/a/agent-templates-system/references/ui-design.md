# Agent Templates UI Design

## Current UI location

**Primary view:** `/home/charl/openclaw/ui/src/ui/views/templates.ts`

**State/controller logic:** `/home/charl/openclaw/ui/src/ui/controllers/templates.ts`

## Purpose

The Control UI exposes Agent Templates as a reusable blueprint editor and launcher.

The UX is designed for power users who need to:
- browse templates quickly
- edit metadata fields directly
- edit the underlying definition JSON
- attach skills
- create a real agent from the selected template

## Layout

The UI is a two-column grid.

### Left column — template browser
Contains:
- section title: `Templates`
- short explanatory subtitle
- refresh button
- new template button
- list of template cards

Each card shows:
- name
- category
- version
- tags
- description

Behavior:
- selecting a card loads it into the editor
- active card gets highlighted

### Right column — template editor
Contains:
- title: `Edit Template` or `Create Template`
- subtitle explaining that templates may include skills and definition JSON
- metadata fields:
  - name
  - category
  - version
  - tags
  - description
- included skills multiline editor
- raw `Definition JSON` editor
- save button
- delete button for existing templates

### Bottom of right column — create agent section
Contains:
- title: `Create Agent from Template`
- helper copy explaining that it materializes a normal agent workspace/config entry
- optional overrides:
  - agent name
  - workspace path
- create button

## UX characteristics

### Strengths
- compact power-user workflow
- direct access to the full definition JSON
- no hidden magic around what gets stored
- skills are separated from raw definition editing for readability
- create-agent action is colocated with the selected template

### Constraints
- raw JSON editing is fragile for non-technical users
- there is no visual structured editor for `workspace.files` or `memorySeeds`
- there is no live preview of the resulting workspace files
- no template diff/history UI
- create-agent success feedback is minimal unless surrounding UI surfaces it

## Suggested future improvements

### 1. Structured definition editor
Replace or augment raw JSON with form-based sections for:
- identity
- included skills
- config
- workspace files
- memory seeds

### 2. Preview panel
Show what will be materialized:
- agent id
- workspace path
- identity markdown preview
- files to be written
- memory seed targets
- merged skill list

### 3. Safer editing affordances
Add:
- JSON validation hints inline
- field-level examples
- starter snippets/templates
- reset-to-default actions

### 4. Better launch feedback
After `Create Agent`:
- show created agent id
- show workspace path
- offer button to open/select created agent
- offer link to inspect created workspace

## UI design intent summary

The current design is best understood as:
- **admin-facing**
- **low abstraction**
- **fast for technical operators**
- **schema-driven**

That makes it good for internal power use, but a future broader audience would benefit from a more guided editor.
